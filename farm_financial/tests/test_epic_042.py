# -*- coding: utf-8 -*-
from odoo.addons.farm_core.tests.bdd_base import BddTransactionCase
from odoo.exceptions import UserError, ValidationError

class TestEpic042(BddTransactionCase):
    """ BDD Test Suite for Epic 042: Epic 042 Multi-Entity Collaboration & Cooperative """

    def setUp(self):
        super(TestEpic042, self).setUp()

    def test_01_cooperative_joint_settlement_cost_split(self):
        """
        Scenario: Cooperative Joint Settlement Cost Split
        Given a joint cooperative harvest campaign involving 3 independent farm partners under model "res.partner"
        And the cooperative share profile is configured as Partner A with 50%, Partner B with 30%, and Partner C with 20%
        When a campaign cost of 12000.0 USD is logged in the cooperative ledger "agri.coop.share"
        Then the system must automatically create cost split journal lines for Partner A of 6000.0 USD, Partner B of 3600.0 USD, and Partner C of 2400.0 USD
        And post these allocated clearing lines to each partner's respective general ledger account
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a joint cooperative harvest campaign involving 3 independent farm partners under model "res.partner"',
            'And the cooperative share profile is configured as Partner A with 50%, Partner B with 30%, and Partner C with 20%',
            'When a campaign cost of 12000.0 USD is logged in the cooperative ledger "agri.coop.share"',
            'Then the system must automatically create cost split journal lines for Partner A of 6000.0 USD, Partner B of 3600.0 USD, and Partner C of 2400.0 USD',
            'And post these allocated clearing lines to each partner's respective general ledger account'
        ])

    def test_02_shared_agricultural_workstation_allocation(self):
        """
        Scenario: Shared Agricultural Workstation Allocation
        Given a shared sorting workstation "COOP-SORTING-WC" represented by model "mrp.workcenter"
        And Partner A has a validated booking reservation from "2026-08-09 08:00:00" to "2026-08-09 12:00:00"
        When the scheduler for Partner B attempts to save a new booking for the same workstation "COOP-SORTING-WC" from "2026-08-09 10:00:00" to "2026-08-09 14:00:00"
        Then the system must raise a ValidationError with code "WORKSTATION_RESOURCE_COLLISION" (工作站排程冲突，该时段已被合作社成员 A 占用)
        And refuse to save the overlapping booking
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a shared sorting workstation "COOP-SORTING-WC" represented by model "mrp.workcenter"',
            'And Partner A has a validated booking reservation from "2026-08-09 08:00:00" to "2026-08-09 12:00:00"',
            'When the scheduler for Partner B attempts to save a new booking for the same workstation "COOP-SORTING-WC" from "2026-08-09 10:00:00" to "2026-08-09 14:00:00"',
            'Then the system must raise a ValidationError with code "WORKSTATION_RESOURCE_COLLISION" (工作站排程冲突，该时段已被合作社成员 A 占用)',
            'And refuse to save the overlapping booking'
        ])

    def test_03_interpartner_stock_transfer_value_clearing(self):
        """
        Scenario: Inter-Partner Stock Transfer Value Clearing
        Given a stock picking transfer order of model "stock.picking" to move 5000.0 kg of raw organic seeds from Partner A's warehouse location to Partner B's warehouse location
        And the seed material standard valuation is set to 1.50 USD per kg
        When the warehouse manager validates the stock transfer picking
        Then the system must automatically create a cross-company clearing journal entry netting a total value of 7500.0 USD (双边对账清算金额 7500.0)
        And post inter-company due-to/due-from transactions to keep both partners' ledgers in balance
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a stock picking transfer order of model "stock.picking" to move 5000.0 kg of raw organic seeds from Partner A's warehouse location to Partner B's warehouse location',
            'And the seed material standard valuation is set to 1.50 USD per kg',
            'When the warehouse manager validates the stock transfer picking',
            'Then the system must automatically create a cross-company clearing journal entry netting a total value of 7500.0 USD (双边对账清算金额 7500.0)',
            'And post inter-company due-to/due-from transactions to keep both partners' ledgers in balance'
        ])

    def test_04_multientity_revenue_profit_sharing(self):
        """
        Scenario: Multi-Entity Revenue Profit Sharing
        Given a consolidated bulk sale of organic tomatoes yielding a total profit of 15000.0 USD in the cooperative settlement registry
        And the profit distribution ratio is configured as 40.0% for Partner A, 40.0% for Partner B, and 20.0% for Partner C
        When the Cooperative Leader executes the profit clearing run via "agri.coop.share"
        Then the system must automatically distribute and record 6000.0 USD profit for Partner A, 6000.0 USD profit for Partner B, and 3000.0 USD profit for Partner C (收益二次分配清算)
        And generate independent settlement statements for each farmer showing the exact distribution breakdown
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a consolidated bulk sale of organic tomatoes yielding a total profit of 15000.0 USD in the cooperative settlement registry',
            'And the profit distribution ratio is configured as 40.0% for Partner A, 40.0% for Partner B, and 20.0% for Partner C',
            'When the Cooperative Leader executes the profit clearing run via "agri.coop.share"',
            'Then the system must automatically distribute and record 6000.0 USD profit for Partner A, 6000.0 USD profit for Partner B, and 3000.0 USD profit for Partner C (收益二次分配清算)',
            'And generate independent settlement statements for each farmer showing the exact distribution breakdown'
        ])

    def test_05_cooperative_joint_equipment_maintenance_split(self):
        """
        Scenario: Cooperative Joint Equipment Maintenance Split
        Given a shared autonomous crop spraying drone "DRONE-SPRAY-01" undergoing scheduled maintenance
        And the drone's historical flight hour usages are logged as Partner A with 60 hours and Partner B with 40 hours
        When Partner A registers the total repair invoice of 2000.0 USD under model "maintenance.equipment"
        Then the system must automatically split the maintenance cost across partners based on their recorded flight hour usages
        And allocate a maintenance expense of 1200.0 USD to Partner A and 800.0 USD to Partner B
        And generate matching internal accounts payable records to clear the repair debt
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a shared autonomous crop spraying drone "DRONE-SPRAY-01" undergoing scheduled maintenance',
            'And the drone's historical flight hour usages are logged as Partner A with 60 hours and Partner B with 40 hours',
            'When Partner A registers the total repair invoice of 2000.0 USD under model "maintenance.equipment"',
            'Then the system must automatically split the maintenance cost across partners based on their recorded flight hour usages',
            'And allocate a maintenance expense of 1200.0 USD to Partner A and 800.0 USD to Partner B',
            'And generate matching internal accounts payable records to clear the repair debt'
        ])

    def test_06_multientity_intercompany_clearing_netting_boundary(self):
        """
        Scenario: Multi-Entity Intercompany Clearing Netting Boundary
        Given a list of reciprocal transactions between multiple cooperative partners under model "res.partner" (业务伙伴)
        And a netting clearance run is initiated under model "account.move" (日记账分录)
        When the accountant executes the multi-entity clearing and balance settlement (对账清算)
        Then the system must enforce a netting boundary validation checkpoint (轧差边界校验关卡)
        And verify that the sum of all debits and credits across intercompany accounts equals exactly 0
        And raise a ValidationError with code "NETTING_BALANCE_MISMATCH" (双边清算不平衡，自动回滚交易) to block posting if any discrepancy is detected
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a list of reciprocal transactions between multiple cooperative partners under model "res.partner" (业务伙伴)',
            'And a netting clearance run is initiated under model "account.move" (日记账分录)',
            'When the accountant executes the multi-entity clearing and balance settlement (对账清算)',
            'Then the system must enforce a netting boundary validation checkpoint (轧差边界校验关卡)',
            'And verify that the sum of all debits and credits across intercompany accounts equals exactly 0',
            'And raise a ValidationError with code "NETTING_BALANCE_MISMATCH" (双边清算不平衡，自动回滚交易) to block posting if any discrepancy is detected'
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
