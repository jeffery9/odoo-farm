# -*- coding: utf-8 -*-
from odoo.addons.farm_core.tests.bdd_base import BddTransactionCase
from odoo.exceptions import UserError, ValidationError

class TestEpic103(BddTransactionCase):
    """ BDD Test Suite for Epic 103: Epic 103 Brand Supply Chain Synergy (Epic 103 品牌与供应链协同) """

    def setUp(self):
        super(TestEpic103, self).setUp()

    def test_01_organic_source_integrity_chain_audit(self):
        """
        Scenario: Organic Source Integrity Chain Audit (有机来源完整性链条审计)
        Given an outbound stock.picking (库存拣货/调拨) record tracked by agri.brand.synergy (品牌协同)
        And the picking is linked to premium branded sale.order (销售订单) records
        When the quality auditor triggers verification action "action_verify_organic_components" (验证有机原料动作) on component lots linked via "component_lot_ids" (原料批次列表)
        And one of the ingredient lots has "organic_certified" (有机认证) set to False (假)
        Then the system blocks the picking validation
        And raises a ValidationError (验证错误) "ValidationError: Component lot lacks active organic certification (验证错误：原料批次缺少有效的有机认证)"
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an outbound stock.picking (库存拣货/调拨) record tracked by agri.brand.synergy (品牌协同)',
            'And the picking is linked to premium branded sale.order (销售订单) records',
            'When the quality auditor triggers verification action "action_verify_organic_components" (验证有机原料动作) on component lots linked via "component_lot_ids" (原料批次列表)',
            'And one of the ingredient lots has "organic_certified" (有机认证) set to False (假)',
            'Then the system blocks the picking validation',
            'And raises a ValidationError (验证错误) "ValidationError: Component lot lacks active organic certification (验证错误：原料批次缺少有效的有机认证)"'
        ])

    def test_02_multifarm_worked_hectare_cost_split_settlements(self):
        """
        Scenario: Multi-Farm Worked Hectare Cost Split Settlements (多农场工作公顷成本分摊结算)
        Given a cooperative harvesting campaign under agri.brand.synergy (品牌协同)
        And cooperative farms Farm-A and Farm-B worked 30 hectares and 20 hectares respectively
        When the finance administrator executes calculation action "action_calculate_cost_splits" (计算成本分摊动作)
        Then the system splits harvesting costs proportionally setting "cost_share_ratio" (成本分摊比例) as 60.0% and 40.0% respectively
        And automatically creates and posts balanced accounting entries under account.move (日记账分录) with status (状态) "posted" (已过账)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a cooperative harvesting campaign under agri.brand.synergy (品牌协同)',
            'And cooperative farms Farm-A and Farm-B worked 30 hectares and 20 hectares respectively',
            'When the finance administrator executes calculation action "action_calculate_cost_splits" (计算成本分摊动作)',
            'Then the system splits harvesting costs proportionally setting "cost_share_ratio" (成本分摊比例) as 60.0% and 40.0% respectively',
            'And automatically creates and posts balanced accounting entries under account.move (日记账分录) with status (状态) "posted" (已过账)'
        ])

    def test_03_multifarm_subscription_weekly_box_allotment(self):
        """
        Scenario: Multi-Farm Subscription Weekly Box Allotment (多农场订阅周度配额箱分配)
        Given cooperative farms supplying fresh produce to subscriber sale.order (销售订单) records
        And weekly crop yields are registered in agri.brand.synergy (品牌协同)
        When the automated scheduler triggers the allotment action "action_generate_box_allotments" (生成配箱分配动作)
        Then the system generates outbound stock.picking (库存拣货/调拨) records
        And sets "csa_weekly_box_allotment" (CSA周箱分配) quantities proportional to each cooperative farm's active yield
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given cooperative farms supplying fresh produce to subscriber sale.order (销售订单) records',
            'And weekly crop yields are registered in agri.brand.synergy (品牌协同)',
            'When the automated scheduler triggers the allotment action "action_generate_box_allotments" (生成配箱分配动作)',
            'Then the system generates outbound stock.picking (库存拣货/调拨) records',
            'And sets "csa_weekly_box_allotment" (CSA周箱分配) quantities proportional to each cooperative farm's active yield'
        ])

    def test_04_joint_credit_biological_collateral_valuation_ledger(self):
        """
        Scenario: Joint Credit Biological Collateral Valuation Ledger (联合信用生物资产质押估值账簿)
        Given cooperative farmers applying for micro-loans secured by active crops
        And the loans are tracked in agri.brand.synergy (品牌协同)
        When the appraiser executes recalculation action "action_update_biological_valuation" (更新生物资产估值动作)
        Then the system updates the credit evaluation ledger "joint_credit_valuation" (联合信用估值) based on drone biomass maps
        And sets the valuation status (状态) to "valued" (已估值)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given cooperative farmers applying for micro-loans secured by active crops',
            'And the loans are tracked in agri.brand.synergy (品牌协同)',
            'When the appraiser executes recalculation action "action_update_biological_valuation" (更新生物资产估值动作)',
            'Then the system updates the credit evaluation ledger "joint_credit_valuation" (联合信用估值) based on drone biomass maps',
            'And sets the valuation status (状态) to "valued" (已估值)'
        ])

    def test_05_cooperative_debt_netting_financial_settlement(self):
        """
        Scenario: Cooperative Debt Netting Financial Settlement (合作社债务轧差财务结算)
        Given outstanding crop loans under agri.brand.synergy (品牌协同)
        And the farmer delivers a harvest lot under a purchase order
        When the settlement clerk executes netting action "action_execute_debt_netting" (执行债务轧差动作)
        Then the system calculates "netting_payment_amount" (轧差支付金额) by subtracting the outstanding loan balance from the purchase total
        And registers the netted payment and updates the loan status (状态) to "settled" (已结清)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given outstanding crop loans under agri.brand.synergy (品牌协同)',
            'And the farmer delivers a harvest lot under a purchase order',
            'When the settlement clerk executes netting action "action_execute_debt_netting" (执行债务轧差动作)',
            'Then the system calculates "netting_payment_amount" (轧差支付金额) by subtracting the outstanding loan balance from the purchase total',
            'And registers the netted payment and updates the loan status (状态) to "settled" (已结清)'
        ])

    def test_06_circular_economy_biomass_gating_synergy(self):
        """
        Scenario: Circular Economy Biomass Gating Synergy (循环经济生物质门控协同)
        Given a cooperative crop waste transfer under stock.picking (库存拣货/调拨) tracked by agri.brand.synergy (品牌协同)
        And the target processing station requires circular economy verified biomass
        When the logistics operator attempts to validate the transfer via action "action_validate_biomass" (验证生物质动作)
        And the biomass verification state is found to be uncertified (未认证)
        Then the system blocks the transfer validation
        And raises a ValidationError (验证错误) "ValidationError: Biomass lacks circular economy certification (验证错误：生物质缺少循环经济认证)"
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a cooperative crop waste transfer under stock.picking (库存拣货/调拨) tracked by agri.brand.synergy (品牌协同)',
            'And the target processing station requires circular economy verified biomass',
            'When the logistics operator attempts to validate the transfer via action "action_validate_biomass" (验证生物质动作)',
            'And the biomass verification state is found to be uncertified (未认证)',
            'Then the system blocks the transfer validation',
            'And raises a ValidationError (验证错误) "ValidationError: Biomass lacks circular economy certification (验证错误：生物质缺少循环经济认证)"'
        ])

    def test_07_compliance_traceability_synthetics_prohibited_gating(self):
        """
        Scenario: Compliance Traceability Synthetics Prohibited Gating (合规营销标签及违禁化学添加物拦截机制)
        Given an organic crop lot registered in "product.template" (产品模板模型) with status "organic" (有机认证状态)
        When a dynamic laboratory chemical test logs a positive "prohibited_synthetics" (当实验检测到任何呈阳性的违禁化学添加物残留时)
        Then the brand compliance engine must automatically strip organic status on "agri.brand.marketing" (品牌合规引擎必须自动剥离该产品标签上的有机认证资格)
        And raise a ValidationError (并且系统抛出验证错误) with message "PROHIBITED_SYNTHETICS_DETECTED" (包含"检测到违禁化学物残留，降级销售"提示信息)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an organic crop lot registered in "product.template" (产品模板模型) with status "organic" (有机认证状态)',
            'When a dynamic laboratory chemical test logs a positive "prohibited_synthetics" (当实验检测到任何呈阳性的违禁化学添加物残留时)',
            'Then the brand compliance engine must automatically strip organic status on "agri.brand.marketing" (品牌合规引擎必须自动剥离该产品标签上的有机认证资格)',
            'And raise a ValidationError (并且系统抛出验证错误) with message "PROHIBITED_SYNTHETICS_DETECTED" (包含"检测到违禁化学物残留，降级销售"提示信息)'
        ])
