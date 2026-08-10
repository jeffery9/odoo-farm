# -*- coding: utf-8 -*-
from odoo.addons.farm_core.tests.bdd_base import BddTransactionCase
from odoo.exceptions import UserError, ValidationError

class TestEpic057(BddTransactionCase):
    """ BDD Test Suite for Epic 057: Epic 057 Circular Economy (循环经济) """

    def setUp(self):
        super(TestEpic057, self).setUp()

    def test_01_crop_biomass_waste_transfer_cost_offsets(self):
        """
        Scenario: Crop Biomass Waste Transfer Cost Offsets
        Given a completed crop harvest yields 1200.0 kg of green biomass waste
        When the worker logs a stock move under "stock.move" (库存移动) transferring this waste to the biogas reactor location
        Then the system automatically generates a cost offset entry in "agri.esg.ledger" (ESG台账)
        And credits the corresponding crop cultivation analytic account "account.analytic.account" (分析账户) with a waste value credit of 300.0 USD
        And transitions the waste stock move status to "done" (已完成)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a completed crop harvest yields 1200.0 kg of green biomass waste',
            'When the worker logs a stock move under "stock.move" (库存移动) transferring this waste to the biogas reactor location',
            'Then the system automatically generates a cost offset entry in "agri.esg.ledger" (ESG台账)',
            'And credits the corresponding crop cultivation analytic account "account.analytic.account" (分析账户) with a waste value credit of 300.0 USD',
            'And transitions the waste stock move status to "done" (已完成)'
        ])

    def test_02_biogas_reactor_methane_yield_contamination_and_feeding_halt(self):
        """
        Scenario: Biogas Reactor Methane Yield Contamination and Feeding Halt
        Given an active biogas anaerobic fermentation campaign under "mrp.production" (生产订单)
        And the target methane yield rate is set to 60.0% of biogas volume
        When real-time analyzer sensors log methane purity dropping below 45.0% due to organic contamination
        Then the system triggers an emergency quality alert in the supervisor dashboard
        And automatically pauses upstream raw feeding stock moves under "stock.move" (库存移动) (暂停上游投料移动)
        And updates the production order status to "paused" (已暂停) to prevent reactor acidification
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an active biogas anaerobic fermentation campaign under "mrp.production" (生产订单)',
            'And the target methane yield rate is set to 60.0% of biogas volume',
            'When real-time analyzer sensors log methane purity dropping below 45.0% due to organic contamination',
            'Then the system triggers an emergency quality alert in the supervisor dashboard',
            'And automatically pauses upstream raw feeding stock moves under "stock.move" (库存移动) (暂停上游投料移动)',
            'And updates the production order status to "paused" (已暂停) to prevent reactor acidification'
        ])

    def test_03_organic_spent_digestate_fertilizer_return_loop(self):
        """
        Scenario: Organic Spent Digestate Fertilizer Return Loop
        Given a fermentation campaign finishes and produces 5000.0 kg of spent digestate under "stock.lot" (库存批次)
        When a tractor loads and recycles the digestate back to Orchard Parcel 4 as organic fertilizer
        Then the system validates the bio-compost NPK nutrient mass profile
        And registers a nutrient return record in the parcel's ESG ledger "agri.esg.ledger" (ESG台账)
        And updates the soil health dashboard card with the returned organic matter mass
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a fermentation campaign finishes and produces 5000.0 kg of spent digestate under "stock.lot" (库存批次)',
            'When a tractor loads and recycles the digestate back to Orchard Parcel 4 as organic fertilizer',
            'Then the system validates the bio-compost NPK nutrient mass profile',
            'And registers a nutrient return record in the parcel\'s ESG ledger "agri.esg.ledger" (ESG台账)',
            'And updates the soil health dashboard card with the returned organic matter mass'
        ])

    def test_04_recycled_straw_animal_bedding_cost_netting(self):
        """
        Scenario: Recycled Straw Animal Bedding Cost Netting
        Given a crop harvesting operation outputs 800.0 kg of agricultural wheat straw
        When the logistics clerk transfers the straw to the swine breeding barn for animal bedding under "stock.move" (库存移动)
        Then the system automatically nets the material value of the straw at 1.5 USD per kg
        And reduces the crop waste disposal expense account and debits the swine livestock WIP account "account.analytic.account" (分析账户) by 1200.0 USD
        And marks the transfer as "internal netting complete" (内部结算完成)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a crop harvesting operation outputs 800.0 kg of agricultural wheat straw',
            'When the logistics clerk transfers the straw to the swine breeding barn for animal bedding under "stock.move" (库存移动)',
            'Then the system automatically nets the material value of the straw at 1.5 USD per kg',
            'And reduces the crop waste disposal expense account and debits the swine livestock WIP account "account.analytic.account" (分析账户) by 1200.0 USD',
            'And marks the transfer as "internal netting complete" (内部结算完成)'
        ])

    def test_05_esg_carbon_offset_credits_liquidation(self):
        """
        Scenario: ESG Carbon Offset Credits Liquidation
        Given a cooperative farm has accumulated 150.0 Tons of certified CO2-equivalent reduction credits under "agri.esg.ledger" (ESG台账)
        When the carbon liquidation automated schedule "ir.cron" (定时任务) is executed
        Then the system generates virtual financial credits valued at 30.0 USD per Ton
        And posts a credit netting journal entry to offset overall farm operating expenses (抵消农场整体运营开支) under "account.move" (日记账分录)
        And updates the carbon ledger status to "liquidated" (已清算) with blockchain transaction reference
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a cooperative farm has accumulated 150.0 Tons of certified CO2-equivalent reduction credits under "agri.esg.ledger" (ESG台账)',
            'When the carbon liquidation automated schedule "ir.cron" (定时任务) is executed',
            'Then the system generates virtual financial credits valued at 30.0 USD per Ton',
            'And posts a credit netting journal entry to offset overall farm operating expenses (抵消农场整体运营开支) under "account.move" (日记账分录)',
            'And updates the carbon ledger status to "liquidated" (已清算) with blockchain transaction reference'
        ])

    def test_06_multifarm_waste_bedding_netting_credit_boundary_check(self):
        """
        Scenario: Multi-Farm Waste Bedding Netting Credit Boundary Check
        Given a recycled straw bedding transfer from a crop farm to a swine breeding farm under model "stock.move" (库存移动)
        And an accumulated cost offset logged in "agri.esg.ledger" (ESG台账)
        When the financial manager executes the cooperative netting clearance run (执行循环清算结算)
        Then the system must verify that the net credit debit values do not exceed the pre-approved credit limits of either farm under model "res.partner" (业务伙伴)
        And raise a ValidationError with code "COOP_CREDIT_LIMIT_EXCEEDED" (超额信用额度限制，循环清算对账失败) to roll back the inter-farm account transactions if any boundary breach is detected
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a recycled straw bedding transfer from a crop farm to a swine breeding farm under model "stock.move" (库存移动)',
            'And an accumulated cost offset logged in "agri.esg.ledger" (ESG台账)',
            'When the financial manager executes the cooperative netting clearance run (执行循环清算结算)',
            'Then the system must verify that the net credit debit values do not exceed the pre-approved credit limits of either farm under model "res.partner" (业务伙伴)',
            'And raise a ValidationError with code "COOP_CREDIT_LIMIT_EXCEEDED" (超额信用额度限制，循环清算对账失败) to roll back the inter-farm account transactions if any boundary breach is detected'
        ])

    def test_07_esg_carbon_limit_excess_supply_chain_gating_block(self):
        """
        Scenario: ESG Carbon Limit Excess Supply Chain Gating Block (碳排放配方超限集成供应链硬性拦截机制)
        Given a supply chain transfer plan registered in "stock.picking" (库存拣货模型) with carbon footprint tracked in "agri.esg.ledger" (ESG碳排放账簿模型)
        When the calculated emission of the shipment exceeds the allotted carbon quota "carbon_quota" (当该笔运输计划计算出的总碳排放量超过分配的碳排放配额字段值时)
        Then the supply chain gateway must automatically freeze the shipping state and block validation (供应链网关必须自动冻结该拣货单状态并强行拦截校验操作)
        And raise a ValidationError (并且系统抛出验证错误) with message "CARBON_QUOTA_EXCEEDED_SHIPMENT_BLOCKED" (包含"碳排放指标超支，拣货单自动锁定阻断"提示信息)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a supply chain transfer plan registered in "stock.picking" (库存拣货模型) with carbon footprint tracked in "agri.esg.ledger" (ESG碳排放账簿模型)',
            'When the calculated emission of the shipment exceeds the allotted carbon quota "carbon_quota" (当该笔运输计划计算出的总碳排放量超过分配的碳排放配额字段值时)',
            'Then the supply chain gateway must automatically freeze the shipping state and block validation (供应链网关必须自动冻结该拣货单状态并强行拦截校验操作)',
            'And raise a ValidationError (并且系统抛出验证错误) with message "CARBON_QUOTA_EXCEEDED_SHIPMENT_BLOCKED" (包含"碳排放指标超支，拣货单自动锁定阻断"提示信息)'
        ])
