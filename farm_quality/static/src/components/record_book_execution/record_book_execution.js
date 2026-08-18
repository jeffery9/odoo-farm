import { registry } from "@web/core/registry";
import { Component, useState, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class RecordBookExecution extends Component {
    setup() {
        this.orm = useService("orm");
        this.notification = useService("notification");
        this.action = useService("action");
        this.state = useState({
            recordBook: {},
            checks: [],
            loading: true,
            currentIndex: 0,
            activeTab: "grid", // 'grid' | 'wizard'
        });

        onWillStart(async () => {
            await this.loadData();
        });
    }

    async loadData() {
        const context = this.props.action.context || {};
        const recordBookId = context.active_id || (this.props.action.params && this.props.action.params.active_id);
        if (!recordBookId) {
            this.state.loading = false;
            return;
        }
        try {
            const books = await this.orm.read("agri.quality.record.book", [recordBookId], ["name", "code", "book_type", "state", "cryptographic_signature"]);
            if (books.length) {
                this.state.recordBook = books[0];
                const checks = await this.orm.searchRead(
                    "agri.quality.check",
                    [["record_book_id", "=", recordBookId]],
                    ["name", "point_id", "instruction", "norm", "tolerance_min", "tolerance_max", "measure", "quality_state", "test_type", "lot_id"]
                );
                this.state.checks = checks.map(c => ({
                    ...c,
                    _dirty: false, // track local edits for saving
                }));
            }
        } catch (error) {
            this.notification.add("Error loading Record Book data", { type: "danger" });
        } finally {
            this.state.loading = false;
        }
    }

    onMeasureChange(check, val) {
        if (this.state.recordBook.state === "locked") return;
        const numVal = parseFloat(val) || 0.0;
        check.measure = numVal;
        check._dirty = true;
        
        // Auto-evaluation of pass/fail like a real spreadsheet
        if (check.test_type === "measure") {
            if (numVal >= check.tolerance_min && numVal <= check.tolerance_max) {
                check.quality_state = "pass";
            } else {
                check.quality_state = "fail";
            }
        }
    }

    setQuickState(check, state) {
        if (this.state.recordBook.state === "locked") return;
        check.quality_state = state;
        check._dirty = true;
    }

    async saveChanges() {
        if (this.state.recordBook.state === "locked") return;
        const dirtyChecks = this.state.checks.filter(c => c._dirty);
        if (!dirtyChecks.length) {
            this.notification.add("No changes to save.", { type: "info" });
            return;
        }
        try {
            for (const check of dirtyChecks) {
                await this.orm.write("agri.quality.check", [check.id], {
                    measure: check.measure,
                    quality_state: check.quality_state,
                });
                check._dirty = false;
            }
            this.notification.add("All quality checks saved successfully!", { type: "success" });
        } catch (error) {
            this.notification.add("Failed to save changes.", { type: "danger" });
        }
    }

    async sealRecordBook() {
        if (this.state.recordBook.state === "locked") return;
        
        // Save first if there are edits
        await this.saveChanges();
        
        try {
            await this.orm.call("agri.quality.record.book", "action_lock", [this.state.recordBook.id]);
            this.notification.add("Record Book sealed and locked cryptographically!", { type: "success" });
            await this.loadData(); // reload status
        } catch (error) {
            this.notification.add("Failed to seal Record Book.", { type: "danger" });
        }
    }

    goBack() {
        this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "agri.quality.record.book",
            res_id: this.state.recordBook.id,
            views: [[false, "form"]],
            target: "current",
        });
    }

    switchTab(tab) {
        this.state.activeTab = tab;
    }

    prevStep() {
        if (this.state.currentIndex > 0) {
            this.state.currentIndex--;
        }
    }

    nextStep() {
        if (this.state.currentIndex < this.state.checks.length - 1) {
            this.state.currentIndex++;
        }
    }

    selectStep(index) {
        this.state.currentIndex = index;
    }
}

RecordBookExecution.template = "farm_quality.RecordBookExecution";
registry.category("actions").add("record_book_execution_client_action", RecordBookExecution);
