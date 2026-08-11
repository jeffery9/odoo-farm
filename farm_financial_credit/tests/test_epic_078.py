# -*- coding: utf-8 -*-
from odoo.addons.farm_core.tests.bdd_base import BddTransactionCase
from odoo.exceptions import UserError, ValidationError

class TestEpic078(BddTransactionCase):
    """ BDD Test Suite for Epic 078: Epic 078 Agri Financial Credit & Insurance (农业金融信用与保险) """

    def setUp(self):
        super(TestEpic078, self).setUp()

    def test_01_biological_collateral_valuation_adjuster_for_borrowing_capacity(self):
        """
        Scenario: Biological collateral valuation adjuster for borrowing capacity
        Given a farmer partner applying for a loan under credit model "agri.credit.rating" (信用评级单)
        When the system calculates the dynamic biological valuation (动态生物资产估值) of their active biological crop lots under "stock.lot" (库存批次)
        Then the system automatically updates the collateral ledger under "agri.collateral.valuation" (动产抵押估值)
        And dynamically adjusts their overall borrowing capacity based on the updated collateral valuation
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a farmer partner applying for a loan under credit model "agri.credit.rating" (信用评级单)',
            'When the system calculates the dynamic biological valuation (动态生物资产估值) of their active biological crop lots under "stock.lot" (库存批次)',
            'Then the system automatically updates the collateral ledger under "agri.collateral.valuation" (动产抵押估值)',
            'And dynamically adjusts their overall borrowing capacity based on the updated collateral valuation'
        ])

    def test_02_loan_approval_financial_credit_score_gating(self):
        """
        Scenario: Loan approval financial credit score gating
        Given a cooperative agricultural credit loan application under "agri.credit.rating" (信用评级单) in status "draft" (草稿)
        When the credit evaluation engine evaluates the partner's credit score (信用评分) "credit_score" as 550 points (低于安全信用阈值)
        Then the system raises a ValidationError (验证错误) "Credit score 550 is below safety threshold" (信用评分550低于安全准入阈值)
        And blocks the loan application approval
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a cooperative agricultural credit loan application under "agri.credit.rating" (信用评级单) in status "draft" (草稿)',
            'When the credit evaluation engine evaluates the partner\'s credit score (信用评分) "credit_score" as 550 points (低于安全信用阈值)',
            'Then the system raises a ValidationError (验证错误) "Credit score 550 is below safety threshold" (信用评分550低于安全准入阈值)',
            'And blocks the loan application approval'
        ])

    def test_03_dynamic_biological_valuation_collateral_drop_risk_alert(self):
        """
        Scenario: Dynamic biological valuation collateral drop risk alert
        Given an active agricultural loan in status "approved" (已批准) secured by biological collateral under "agri.collateral.valuation" (动产抵押估值)
        When field disease alerts or extreme weather drops the estimated biological collateral valuation by more than 30.0%
        Then the system automatically flags a credit risk alert (信用风险警报) on the active partner record
        And prompts the risk officer for an immediate manual collateral review task
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an active agricultural loan in status "approved" (已批准) secured by biological collateral under "agri.collateral.valuation" (动产抵押估值)',
            'When field disease alerts or extreme weather drops the estimated biological collateral valuation by more than 30.0%',
            'Then the system automatically flags a credit risk alert (信用风险警报) on the active partner record',
            'And prompts the risk officer for an immediate manual collateral review task'
        ])

    def test_04_loan_repayment_crop_delivery_purchase_settlement_netting(self):
        """
        Scenario: Loan repayment crop delivery purchase settlement netting
        Given an outstanding crop loan payment balance on a farmer partner "res.partner" (业务伙伴)
        When the farmer delivers raw harvest lots under "stock.lot" (库存批次) to the cooperative and a purchase settlement is generated
        Then the system triggers the action "action_settlement_netting" (交收轧差结算)
        And automatically offsets the input debt and nets the outstanding loan balances against the purchase settlement credits with standard accounting entries
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an outstanding crop loan payment balance on a farmer partner "res.partner" (业务伙伴)',
            'When the farmer delivers raw harvest lots under "stock.lot" (库存批次) to the cooperative and a purchase settlement is generated',
            'Then the system triggers the action "action_settlement_netting" (交收轧差结算)',
            'And automatically offsets the input debt and nets the outstanding loan balances against the purchase settlement credits with standard accounting entries'
        ])

    def test_05_harvester_equipment_lease_gxp_asset_gate(self):
        """
        Scenario: Harvester equipment lease GxP asset gate
        Given a machinery lease loan application under "agri.credit.rating" (信用评级单) for a cooperative member
        When registering the leased harvester equipment serial number "equipment_serial"
        Then the system validates that the harvester holds an active GxP safety certification (GxP合规证书) "gxp_certificate"
        And blocks the lease loan approval with a ValidationError (验证错误) if the certification is expired or invalid
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a machinery lease loan application under "agri.credit.rating" (信用评级单) for a cooperative member',
            'When registering the leased harvester equipment serial number "equipment_serial"',
            'Then the system validates that the harvester holds an active GxP safety certification (GxP合规证书) "gxp_certificate"',
            'And blocks the lease loan approval with a ValidationError (验证错误) if the certification is expired or invalid'
        ])

    def test_06_remote_sensing_ndvi_index_drought_insurance_payout_ndvi(self):
        """
        Scenario: Remote Sensing NDVI Index Drought Insurance Payout (遥感NDVI指数干旱保险赔付触发)
        Given a crop insurance policy record "agri.credit.rating" (信用评级单) linked to an active crop lot "stock.lot" (库存批次)
        When remote sensing satellite NDVI sensors "iiot.device" (智能物联网设备) log an average canopy index below "0.20" (平均绿度指标低于0.20) for "14 consecutive days" indicating severe drought
        Then the insurance engine must automatically trigger the claim payout action "action_trigger_payout" (触发保险赔付)
        And create an automated credit note under "agri.collateral.valuation" (动产抵押估值) to settle cooperative premium debts
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a crop insurance policy record "agri.credit.rating" (信用评级单) linked to an active crop lot "stock.lot" (库存批次)',
            'When remote sensing satellite NDVI sensors "iiot.device" (智能物联网设备) log an average canopy index below "0.20" (平均绿度指标低于0.20) for "14 consecutive days" indicating severe drought',
            'Then the insurance engine must automatically trigger the claim payout action "action_trigger_payout" (触发保险赔付)',
            'And create an automated credit note under "agri.collateral.valuation" (动产抵押估值) to settle cooperative premium debts'
        ])
