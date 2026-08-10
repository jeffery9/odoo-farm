# -*- coding: utf-8 -*-
from odoo.addons.farm_core.tests.bdd_base import BddTransactionCase
from odoo.exceptions import UserError, ValidationError

class TestEpic011(BddTransactionCase):
    """ BDD Test Suite for Epic 011: Epic 011 Business Sustainability Framework """

    def setUp(self):
        super(TestEpic011, self).setUp()

    def test_01_triple_bottom_line_tracking_via_sustainabilitymixin(self):
        """
        Scenario: Triple Bottom Line tracking via SustainabilityMixin
        Given the "Sustainability Settings" are enabled in the ESG config of "res.company"
        When any business model inherits "SustainabilityMixin"
        Then the ORM must expose "carbon_footprint_score" and "resource_efficiency_index" fields
        And the Sustainability Dashboard should calculate and reflect the balanced score based on "BasePPOCritic" algorithm
        And persist these scores in the "agri.esg.ledger" record for the company
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given the "Sustainability Settings" are enabled in the ESG config of "res.company"',
            'When any business model inherits "SustainabilityMixin"',
            'Then the ORM must expose "carbon_footprint_score" and "resource_efficiency_index" fields',
            'And the Sustainability Dashboard should calculate and reflect the balanced score based on "BasePPOCritic" algorithm',
            'And persist these scores in the "agri.esg.ledger" record for the company'
        ])

    def test_02_scope_1_and_2_carbon_footprint_compilation_on_logistics_picking_and_manufacturing(self):
        """
        Scenario: Scope 1 and 2 Carbon Footprint Compilation on logistics picking and manufacturing
        Given a logistics picking of model "stock.picking" or manufacturing order of model "mrp.production" is active
        And the "res.company" emission factor for "Diesel Fuel" is configured as "0.00268" CO2 metric tons per liter
        When a user registers fuel consumption of "150" liters on the "agri.esg.ledger" line associated with this transaction
        Then the system must calculate the Scope 1 emissions as "0.402" CO2 metric tons
        And automatically add this value to the global carbon balance of "agri.esg.ledger"
        And write "co2_metric_tons = 0.402" and "emission_scope = 'scope_1'" to the ledger
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a logistics picking of model "stock.picking" or manufacturing order of model "mrp.production" is active',
            'And the "res.company" emission factor for "Diesel Fuel" is configured as "0.00268" CO2 metric tons per liter',
            'When a user registers fuel consumption of "150" liters on the "agri.esg.ledger" line associated with this transaction',
            'Then the system must calculate the Scope 1 emissions as "0.402" CO2 metric tons',
            'And automatically add this value to the global carbon balance of "agri.esg.ledger"',
            'And write "co2_metric_tons = 0.402" and "emission_scope = 'scope_1'" to the ledger'
        ])

    def test_03_scope_2_electricity_indirect_emission_computation(self):
        """
        Scenario: Scope 2 Electricity indirect emission computation
        Given a manufacturing workorder of model "mrp.workorder" completed at "Workcenter-Greenhouse"
        And the regional electricity grid emission factor is set to "0.00038" CO2 metric tons per kWh
        When the system records electricity usage of "5000" kWh for the production cycle on "agri.esg.ledger"
        Then the ESG ledger must calculate Scope 2 emissions as "1.9" CO2 metric tons
        And update the active company's cumulative indirect carbon footprint balance
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a manufacturing workorder of model "mrp.workorder" completed at "Workcenter-Greenhouse"',
            'And the regional electricity grid emission factor is set to "0.00038" CO2 metric tons per kWh',
            'When the system records electricity usage of "5000" kWh for the production cycle on "agri.esg.ledger"',
            'Then the ESG ledger must calculate Scope 2 emissions as "1.9" CO2 metric tons',
            'And update the active company's cumulative indirect carbon footprint balance'
        ])

    def test_04_sustainable_supply_chain_verification_via_agenttoagent_a2a_kyc(self):
        """
        Scenario: Sustainable supply chain verification via Agent-to-Agent (A2A) KYC
        Given a new supplier profile being registered on model "res.partner"
        When the system performs an autonomous Agent-to-Agent (A2A) KYC check using "agri.esg.ledger"
        Then it must verify the supplier agent's reputation score on the distributed registry
        And restrict procurement confirmation if the supplier's reputation score is below the "Sustainability Threshold" of "70"
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a new supplier profile being registered on model "res.partner"',
            'When the system performs an autonomous Agent-to-Agent (A2A) KYC check using "agri.esg.ledger"',
            'Then it must verify the supplier agent's reputation score on the distributed registry',
            'And restrict procurement confirmation if the supplier's reputation score is below the "Sustainability Threshold" of "70"'
        ])

    def test_05_carbon_tax_penalty_journal_voucher_allocation_esg(self):
        """
        Scenario: Carbon Tax Penalty Journal Voucher Allocation (碳税罚款日记账凭证分配与ESG负债拆分)
        Given the carbon emission in "agri.esg.ledger" (ESG分类账模型) exceeds the baseline limit of "100" CO2 metric tons (排放量超过100公吨二氧化碳基准限制)
        When the sustainability manager triggers the carbon tax penalty allocation action "action_allocate_carbon_tax" (触发碳税分配动作)
        Then the system must create a journal entry of model "account.move" (创建"account.move"日记账凭证模型记录)
        And split the carbon liability under "account.move.line" (在"account.move.line"日记账分录行模型中分摊碳排放负债金额)
        And when the transaction is confirmed, the status of the "account.move" must be set to "posted" (并且凭证状态必须更新为"已过账")
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given the carbon emission in "agri.esg.ledger" (ESG分类账模型) exceeds the baseline limit of "100" CO2 metric tons (排放量超过100公吨二氧化碳基准限制)',
            'When the sustainability manager triggers the carbon tax penalty allocation action "action_allocate_carbon_tax" (触发碳税分配动作)',
            'Then the system must create a journal entry of model "account.move" (创建"account.move"日记账凭证模型记录)',
            'And split the carbon liability under "account.move.line" (在"account.move.line"日记账分录行模型中分摊碳排放负债金额)',
            'And when the transaction is confirmed, the status of the "account.move" must be set to "posted" (并且凭证状态必须更新为"已过账")'
        ])

    def test_06_core_registration_concurrency_bypass_check(self):
        """
        Scenario: Core Registration Concurrency Bypass Check (核心主数据并发注册绕过防御机制)
        Given a system configuration in "res.partner" (核心注册配置模型) with status "active" (活跃状态)
        And a registration lock "concurrency_lock" is set to "locked" (并且并发锁状态字段值设置为已锁定状态)
        When another system administrator attempts to write (当另一位系统管理员尝试写入数据时)
        Then the ORM registry must block the write action and raise a UserError (注册表必须拦截写入动作并抛出用户错误) with message "REGISTRY_LOCK_ACTIVE" (包含"注册表已被并发锁定"提示信息)
        And execute rollback (并且系统必须执行事务回滚) to restore physical state integrity (以恢复物理状态完整性)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a system configuration in "res.partner" (核心注册配置模型) with status "active" (活跃状态)',
            'And a registration lock "concurrency_lock" is set to "locked" (并且并发锁状态字段值设置为已锁定状态)',
            'When another system administrator attempts to write (当另一位系统管理员尝试写入数据时)',
            'Then the ORM registry must block the write action and raise a UserError (注册表必须拦截写入动作并抛出用户错误) with message "REGISTRY_LOCK_ACTIVE" (包含"注册表已被并发锁定"提示信息)',
            'And execute rollback (并且系统必须执行事务回滚) to restore physical state integrity (以恢复物理状态完整性)'
        ])
