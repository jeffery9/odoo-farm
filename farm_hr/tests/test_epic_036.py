# -*- coding: utf-8 -*-
from odoo.addons.farm_core.tests.bdd_base import BddTransactionCase
from odoo.exceptions import UserError, ValidationError

class TestEpic036(BddTransactionCase):
    """ BDD Test Suite for Epic 036: Epic 036 HR & Labor Scheduling """

    def setUp(self):
        super(TestEpic036, self).setUp()

    def test_01_outdoor_wbgt_heat_stress_scheduling_and_automated_pause(self):
        """
        Scenario: Outdoor WBGT heat stress scheduling and automated pause
        Given a weather station sensor logs telemetry for farm parcel "North Field Orchards"
        And the Wet Bulb Globe Temperature (WBGT) registers a temperature of 32.5 °C
        When the cron "agri_hr.cron_monitor_heat_stress" runs to evaluate outdoor worker conditions
        Then the system must automatically pause all active harvest "mrp.workorder" records in that parcel
        And update the "agri.hr.heat.stress" state to "Dangerous" (热指数危险 / Dangerous)
        And auto-schedule remaining labor hours to the cooler evening block starting at "18:00:00"
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a weather station sensor logs telemetry for farm parcel "North Field Orchards"',
            'And the Wet Bulb Globe Temperature (WBGT) registers a temperature of 32.5 °C',
            'When the cron "agri_hr.cron_monitor_heat_stress" runs to evaluate outdoor worker conditions',
            'Then the system must automatically pause all active harvest "mrp.workorder" records in that parcel',
            'And update the "agri.hr.heat.stress" state to "Dangerous" (热指数危险 / Dangerous)',
            'And auto-schedule remaining labor hours to the cooler evening block starting at "18:00:00"'
        ])

    def test_02_worker_spray_gxp_certificate_validation_and_assignment_lock(self):
        """
        Scenario: Worker spray GxP certificate validation and assignment lock
        Given a plant protection chemical spraying "mrp.workorder" is created for "agri.chemical.spray"
        And the required certificate type is "Chemical Application Certification" (化学施用安全证书)
        When I attempt to assign employee "Li Ming" to this workorder
        And employee "Li Ming" does not have an active, non-expired certification in "agri.hr.certificate"
        Then the system must raise a ValidationError with message "BIOSECURITY_GXP_CERT_REQUIRED" (缺失有效的化学作业GxP安全证书)
        And block the saving of the "mrp.workorder" assignment
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a plant protection chemical spraying "mrp.workorder" is created for "agri.chemical.spray"',
            'And the required certificate type is "Chemical Application Certification" (化学施用安全证书)',
            'When I attempt to assign employee "Li Ming" to this workorder',
            'And employee "Li Ming" does not have an active, non-expired certification in "agri.hr.certificate"',
            'Then the system must raise a ValidationError with message "BIOSECURITY_GXP_CERT_REQUIRED" (缺失有效的化学作业GxP安全证书)',
            'And block the saving of the "mrp.workorder" assignment'
        ])

    def test_03_labor_capacity_wip_backpressure_control_delaying_picking_validation(self):
        """
        Scenario: Labor capacity WIP backpressure control delaying picking validation
        Given a manufacturing sorting workstation "Sorting Line Alpha" under workcenter "mrp.workcenter"
        And the active worker queue backlog is recorded as 4.5 hours which exceeds the max capacity limit of 3.0 hours
        When a supplier delivery "stock.picking" is processed to receive raw spinach lot "SPIN-2026-001"
        Then the system must intercept the validation of the "stock.picking"
        And put the picking state to "Backpressure Hold" (待检流控中 / Backpressure Hold) to prevent workstation overflow
        And notify the on-duty logistics coordinator via an automated dashboard alert
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a manufacturing sorting workstation "Sorting Line Alpha" under workcenter "mrp.workcenter"',
            'And the active worker queue backlog is recorded as 4.5 hours which exceeds the max capacity limit of 3.0 hours',
            'When a supplier delivery "stock.picking" is processed to receive raw spinach lot "SPIN-2026-001"',
            'Then the system must intercept the validation of the "stock.picking"',
            'And put the picking state to "Backpressure Hold" (待检流控中 / Backpressure Hold) to prevent workstation overflow',
            'And notify the on-duty logistics coordinator via an automated dashboard alert'
        ])

    def test_04_harvester_operator_maximum_consecutive_overtime_blocking(self):
        """
        Scenario: Harvester operator maximum consecutive overtime blocking
        Given a heavy machinery "maintenance.equipment" harvester operator "Zhang Wei"
        And the current daily hours logged for operator "Zhang Wei" in "hr.timesheet" is 12.5 hours
        When the scheduler attempts to assign "Zhang Wei" to a new harvesting campaign "mrp.workorder" within a 10-hour rest window
        Then the system must block the assignment
        And raise a UserError with message "LABOR_SAFETY_MAX_OVERTIME_BREACH" (操作员连续作业时长超限，强制休息不足10小时)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a heavy machinery "maintenance.equipment" harvester operator "Zhang Wei"',
            'And the current daily hours logged for operator "Zhang Wei" in "hr.timesheet" is 12.5 hours',
            'When the scheduler attempts to assign "Zhang Wei" to a new harvesting campaign "mrp.workorder" within a 10-hour rest window',
            'Then the system must block the assignment',
            'And raise a UserError with message "LABOR_SAFETY_MAX_OVERTIME_BREACH" (操作员连续作业时长超限，强制休息不足10小时)'
        ])

    def test_05_swine_barn_entry_biosecurity_mandatory_downtime_check(self):
        """
        Scenario: Swine barn entry biosecurity mandatory downtime check
        Given a swine barn entry terminal connected to workcenter "Swine Breeding Barn B"
        And a worker "Wang Chao" has a biosecurity contact log in "agri.hr.biosecurity.log" with foreign animals within 48 hours
        When the worker attempts a barn entry check-in via the mobile PDA device "agri_ux.pda_entry"
        Then the system must refuse the entry check-in with a red status warning
        And log a biosecurity violation alert with message "BIOSECURITY_DOWNTIME_VIOLATION" (生物安全隔离期不足48小时，拒绝进入生猪舍)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a swine barn entry terminal connected to workcenter "Swine Breeding Barn B"',
            'And a worker "Wang Chao" has a biosecurity contact log in "agri.hr.biosecurity.log" with foreign animals within 48 hours',
            'When the worker attempts a barn entry check-in via the mobile PDA device "agri_ux.pda_entry"',
            'Then the system must refuse the entry check-in with a red status warning',
            'And log a biosecurity violation alert with message "BIOSECURITY_DOWNTIME_VIOLATION" (生物安全隔离期不足48小时，拒绝进入生猪舍)'
        ])

    def test_06_wet_bulb_globe_temperature_wbgt_sensor_telemetry_failure_and_saferest_manual_dispatch_fallback(self):
        """
        Scenario: Wet Bulb Globe Temperature (WBGT) Sensor Telemetry Failure and Safe-Rest Manual Dispatch Fallback
        Given an outdoor crop field parcel monitored by an IoT weather station
        And the heat monitoring state in "agri.hr.heat.stress" (热应激日志) is "Normal" (正常)
        When the Wet Bulb Globe Temperature (WBGT) sensor fails and reports null telemetry values for over 30 minutes
        Then the system must transition the heat stress status to "SENSORY_FAILED" (传感器异常)
        And automatically pause active "hr.timesheet" (工时单) entries for outdoor field workers
        And apply a mandatory protective work-rest schedule of 15 minutes of rest per hour
        And raise a "ValidationError" (验证错误) blocking the validation of new field harvesting missions "mrp.workorder" [mrp.workorder] (作业任务) unless manual wet-bulb checks are logged
        And generate an emergency repair mission "mrp.workorder" [mrp.workorder] (作业任务) for the technician
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an outdoor crop field parcel monitored by an IoT weather station',
            'And the heat monitoring state in "agri.hr.heat.stress" (热应激日志) is "Normal" (正常)',
            'When the Wet Bulb Globe Temperature (WBGT) sensor fails and reports null telemetry values for over 30 minutes',
            'Then the system must transition the heat stress status to "SENSORY_FAILED" (传感器异常)',
            'And automatically pause active "hr.timesheet" (工时单) entries for outdoor field workers',
            'And apply a mandatory protective work-rest schedule of 15 minutes of rest per hour',
            'And raise a "ValidationError" (验证错误) blocking the validation of new field harvesting missions "mrp.workorder" [mrp.workorder] (作业任务) unless manual wet-bulb checks are logged',
            'And generate an emergency repair mission "mrp.workorder" [mrp.workorder] (作业任务) for the technician'
        ])

    def test_07_dynamic_credit_overdraft_transaction_savepoint_rollback(self):
        """
        Scenario: Dynamic Credit Overdraft Transaction Savepoint Rollback (合作社信用额度穿透事务保存点回滚防呆机制)
        Given a joint clearing balance account inside "account.move" (会计分录模型) with cooperative member status "active" (且合作社成员信用状态为活跃)
        And a dynamic credit limit registered in the virtual ledger (并且在虚拟账簿中登记了固定的动态额度上限)
        When a clearing transaction fails due to concurrent credit overdraft (当清算交易由于信用额度并发穿透导致处理失败时)
        Then the transaction engine must execute rollback to "cr.savepoint" (交易引擎必须强制执行事务回滚到指定的事务保存点)
        And raise a UserError (并且抛出用户错误) with message "CREDIT_OVERDRAFT_TRANSACTION_FAILED" (包含"信用额度超支交易回滚，防范资金坏账"提示信息)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a joint clearing balance account inside "account.move" (会计分录模型) with cooperative member status "active" (且合作社成员信用状态为活跃)',
            'And a dynamic credit limit registered in the virtual ledger (并且在虚拟账簿中登记了固定的动态额度上限)',
            'When a clearing transaction fails due to concurrent credit overdraft (当清算交易由于信用额度并发穿透导致处理失败时)',
            'Then the transaction engine must execute rollback to "cr.savepoint" (交易引擎必须强制执行事务回滚到指定的事务保存点)',
            'And raise a UserError (并且抛出用户错误) with message "CREDIT_OVERDRAFT_TRANSACTION_FAILED" (包含"信用额度超支交易回滚，防范资金坏账"提示信息)'
        ])
