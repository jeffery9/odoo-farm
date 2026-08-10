# -*- coding: utf-8 -*-
from odoo.addons.farm_core.tests.bdd_base import BddTransactionCase
from odoo.exceptions import UserError, ValidationError

class TestEpic054(BddTransactionCase):
    """ BDD Test Suite for Epic 054: Epic 054 Mobile Site Check-in """

    def setUp(self):
        super(TestEpic054, self).setUp()

    def test_01_gps_boundary_attendance_verification(self):
        """
        Scenario: GPS Boundary Attendance Verification
        Given a field worker scheduled to perform operations on a designated agricultural parcel
        When the worker logs a check-in transaction on their mobile PDA device under "agri.pda.attendance" (移动端考勤记录)
        And the logged GPS coordinates are more than 50.0 meters away from the scheduled parcel's boundary polygon
        Then the system blocks the check-in transaction, logged in the database as "unverified" (未核实)
        And requires a manager's override PIN or note to complete the labor attendance record
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a field worker scheduled to perform operations on a designated agricultural parcel',
            'When the worker logs a check-in transaction on their mobile PDA device under "agri.pda.attendance" (移动端考勤记录)',
            'And the logged GPS coordinates are more than 50.0 meters away from the scheduled parcel's boundary polygon',
            'Then the system blocks the check-in transaction, logged in the database as "unverified" (未核实)',
            'And requires a manager's override PIN or note to complete the labor attendance record'
        ])

    def test_02_hr_mobile_checkin_labor_activity_mapping(self):
        """
        Scenario: HR Mobile Check-In Labor Activity Mapping
        Given a validated mobile check-in recorded for a field worker
        When the worker selects and logs active work hours against a specific harvesting workorder
        Then the system automatically creates a corresponding "account.analytic.line" (分析账户明细) timesheet record in Odoo
        And links the labor hours directly to the analytic distribution account assigned to the harvesting lot
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a validated mobile check-in recorded for a field worker',
            'When the worker selects and logs active work hours against a specific harvesting workorder',
            'Then the system automatically creates a corresponding "account.analytic.line" (分析账户明细) timesheet record in Odoo',
            'And links the labor hours directly to the analytic distribution account assigned to the harvesting lot'
        ])

    def test_03_attending_worker_gxp_certification_verification(self):
        """
        Scenario: Attending Worker GxP Certification Verification
        Given an advanced GxP chemical sterilization or harvesting workorder
        When an operator attempts to check in and register labor hours for this specific workorder on their mobile PWA
        And the operator's Odoo employee profile does not possess an active, valid "GxP Sterilization Certificate" (GxP 灭菌操作证书认证)
        Then the system blocks the PWA task-start check-in with a strict security validation warning (强力拦截签到并进行安全校验提示)
        And prevents any labor hours from being credited or tasks started under their name
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an advanced GxP chemical sterilization or harvesting workorder',
            'When an operator attempts to check in and register labor hours for this specific workorder on their mobile PWA',
            'And the operator's Odoo employee profile does not possess an active, valid "GxP Sterilization Certificate" (GxP 灭菌操作证书认证)',
            'Then the system blocks the PWA task-start check-in with a strict security validation warning (强力拦截签到并进行安全校验提示)',
            'And prevents any labor hours from being credited or tasks started under their name'
        ])

    def test_04_mobile_checkin_offline_caching_sync(self):
        """
        Scenario: Mobile Check-In Offline Caching Sync
        Given a mobile field worker operating in a deep mountain parcel with no cellular network signal
        When the worker records a task check-in on the mobile app
        Then the app caches the check-in payload containing exact GPS, timestamp, and photo locally inside the PWA's IndexedDB queue
        And upon detecting restored network connectivity, the app synchronizes all queued offline records with the main Odoo server in strict FIFO order
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a mobile field worker operating in a deep mountain parcel with no cellular network signal',
            'When the worker records a task check-in on the mobile app',
            'Then the app caches the check-in payload containing exact GPS, timestamp, and photo locally inside the PWA's IndexedDB queue',
            'And upon detecting restored network connectivity, the app synchronizes all queued offline records with the main Odoo server in strict FIFO order'
        ])

    def test_05_labor_overtime_safety_limit_block(self):
        """
        Scenario: Labor Overtime Safety Limit Block
        Given a heavy machinery operator actively logging tasks on their mobile PDA
        And the operator's cumulative work hours for the current 24-hour cycle exceed 12.0 hours
        When the operator attempts to perform a new check-in or start a new high-risk machinery workorder
        Then the mobile system hard-blocks the start transaction, raising a safety warning (强制拦截启动事务并触发安全警报)
        And enforces a mandatory 8-hour rest block period before the operator can re-authorize any active machine intervention
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a heavy machinery operator actively logging tasks on their mobile PDA',
            'And the operator's cumulative work hours for the current 24-hour cycle exceed 12.0 hours',
            'When the operator attempts to perform a new check-in or start a new high-risk machinery workorder',
            'Then the mobile system hard-blocks the start transaction, raising a safety warning (强制拦截启动事务并触发安全警报)',
            'And enforces a mandatory 8-hour rest block period before the operator can re-authorize any active machine intervention'
        ])

    def test_06_mobile_checkin_transaction_database_lock_to_prevent_double_checkin(self):
        """
        Scenario: Mobile Check-In Transaction Database Lock to Prevent Double Check-In
        Given a field worker logging a check-in transaction on their mobile PDA device under "agri.pda.attendance" (移动端考勤记录)
        When the server receives the check-in API request from the client
        Then the system must acquire a database row-level lock FOR UPDATE on the worker's active attendance log for today
        And verify that no other active check-in or timesheet record under model "account.analytic.line" (分析账户明细) has been created within the last 5 minutes
        And raise a ValidationError with code "DUPLICATE_CHECKIN_ATTEMPT" (签到请求并发冲突，请勿重复提交) if a lock collision is detected, discarding the duplicate request
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a field worker logging a check-in transaction on their mobile PDA device under "agri.pda.attendance" (移动端考勤记录)',
            'When the server receives the check-in API request from the client',
            'Then the system must acquire a database row-level lock FOR UPDATE on the worker's active attendance log for today',
            'And verify that no other active check-in or timesheet record under model "account.analytic.line" (分析账户明细) has been created within the last 5 minutes',
            'And raise a ValidationError with code "DUPLICATE_CHECKIN_ATTEMPT" (签到请求并发冲突，请勿重复提交) if a lock collision is detected, discarding the duplicate request'
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
