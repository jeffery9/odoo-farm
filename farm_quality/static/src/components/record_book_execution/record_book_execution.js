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
                    ["name", "point_id", "replicate_count", "instruction", "norm", "tolerance_min", "tolerance_max", "measure", "quality_state", "test_type", "lot_id", "measure_line_ids"]
                );
                
                // Batch-query all sub-measurement replicate lines in a single query
                const checkIds = checks.map(c => c.id);
                const subLines = await this.orm.searchRead(
                    "agri.quality.check.measure.line",
                    [["check_id", "in", checkIds]],
                    ["check_id", "sequence", "value"]
                );

                // Group sub-measurements by check_id
                const subMeasuresByCheck = {};
                for (const line of subLines) {
                    const checkId = line.check_id[0];
                    if (!subMeasuresByCheck[checkId]) {
                        subMeasuresByCheck[checkId] = [];
                    }
                    subMeasuresByCheck[checkId].push(line);
                }

                this.state.checks = checks.map(c => {
                    const checkLines = subMeasuresByCheck[c.id] || [];
                    checkLines.sort((a, b) => a.sequence - b.sequence);
                    return {
                        ...c,
                        _dirty: false,
                        sub_measures: checkLines.map(l => ({ ...l, _dirty: false })),
                    };
                });
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
        
        // Auto-evaluation of pass/fail
        if (check.test_type === "measure") {
            if (numVal >= check.tolerance_min && numVal <= check.tolerance_max) {
                check.quality_state = "pass";
            } else {
                check.quality_state = "fail";
            }
        }
    }

    onSubMeasureChange(check, subMeasure, val) {
        if (this.state.recordBook.state === "locked") return;
        const numVal = parseFloat(val) || 0.0;
        subMeasure.value = numVal;
        subMeasure._dirty = true;
        check._dirty = true;

        // Dynamic recalculation of overall average
        const vals = check.sub_measures.map(m => m.value);
        check.measure = vals.reduce((sum, v) => sum + v, 0.0) / vals.length;

        // Auto-evaluation based on new average
        if (check.test_type === "measure") {
            if (check.measure >= check.tolerance_min && check.measure <= check.tolerance_max) {
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
                // Save dirty sub-measurements first
                if (check.sub_measures && check.sub_measures.length > 0) {
                    const dirtySubs = check.sub_measures.filter(sm => sm._dirty);
                    for (const sm of dirtySubs) {
                        await this.orm.write("agri.quality.check.measure.line", [sm.id], {
                            value: sm.value,
                        });
                        sm._dirty = false;
                    }
                }

                // Save main quality check status
                await this.orm.write("agri.quality.check", [check.id], {
                    measure: check.measure,
                    quality_state: check.quality_state,
                });
                check._dirty = false;
            }
            this.notification.add("All quality checks and replicates saved successfully!", { type: "success" });
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
