# -*- coding: utf-8 -*-
from odoo.addons.farm_core.tests.bdd_base import BddTransactionCase
from odoo.exceptions import UserError, ValidationError

class TestEpic009(BddTransactionCase):
    """ BDD Test Suite for Epic 009: Epic 009 Integrated Supply Chain """

    def setUp(self):
        super(TestEpic009, self).setUp()

    def test_01_demanddriven_production_mto_with_growth_duration_check(self):
        """
        Scenario: Demand-driven production (MTO) with growth duration check
        Given a sales order is created for a crop with "growth_duration" set to 90 days
        When the sales order confirmation is attempted with a scheduled delivery date only 45 days in the future
        Then the system must block confirmation and raise a "ValidationError" explaining that the growth duration requirement of 90 days is not met
        And the user must be prompted to adjust the delivery date or select an existing inventory stock lot
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a sales order is created for a crop with "growth_duration" set to 90 days',
            'When the sales order confirmation is attempted with a scheduled delivery date only 45 days in the future',
            'Then the system must block confirmation and raise a "ValidationError" explaining that the growth duration requirement of 90 days is not met',
            'And the user must be prompted to adjust the delivery date or select an existing inventory stock lot'
        ])

    def test_02_logistic_temperature_route_degradation_and_automatic_taint_flagging(self):
        """
        Scenario: Logistic Temperature Route Degradation and Automatic Taint Flagging
        Given a cold-chain logistics picking order "WH-OUT-00123" is registered on "stock.picking"
        And the shipment is assigned to a logistic route "agri.logistic.route" with active IoT temperature sensor devices
        And the associated product lot is "LOT-2026-APPLE-05" in "stock.lot"
        When the IoT temperature sensor registers a reading of 15.5C which is a deviation > 10.0C from the target temperature (4.0C)
        And this temperature deviation persists for a continuous duration of 2.5 hours
        Then the "agri.logistic.route" status must automatically transition to "degraded"
        And the stock lot "LOT-2026-APPLE-05" quality state must be auto-flagged as "tainted"
        And the system must block the automatic inventory reception/delivery confirmation of "WH-OUT-00123"
        And a critical Activity "Tainted Cold Chain Alert: Quarantine and Inspection Required" must be created and assigned to the Warehouse Compliance Admin
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a cold-chain logistics picking order "WH-OUT-00123" is registered on "stock.picking"',
            'And the shipment is assigned to a logistic route "agri.logistic.route" with active IoT temperature sensor devices',
            'And the associated product lot is "LOT-2026-APPLE-05" in "stock.lot"',
            'When the IoT temperature sensor registers a reading of 15.5C which is a deviation > 10.0C from the target temperature (4.0C)',
            'And this temperature deviation persists for a continuous duration of 2.5 hours',
            'Then the "agri.logistic.route" status must automatically transition to "degraded"',
            'And the stock lot "LOT-2026-APPLE-05" quality state must be auto-flagged as "tainted"',
            'And the system must block the automatic inventory reception/delivery confirmation of "WH-OUT-00123"',
            'And a critical Activity "Tainted Cold Chain Alert: Quarantine and Inspection Required" must be created and assigned to the Warehouse Compliance Admin'
        ])

    def test_03_supplier_compliance_verification_and_po_locking(self):
        """
        Scenario: Supplier compliance verification and PO locking
        Given a purchase order is created for a supplier
        When the system checks the supplier's certificate validity
        Then if the certificate is expired, the "Confirm" button must be hard-locked
        And an Activity must be created for the "Compliance Officer" to update the credentials
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a purchase order is created for a supplier',
            'When the system checks the supplier's certificate validity',
            'Then if the certificate is expired, the "Confirm" button must be hard-locked',
            'And an Activity must be created for the "Compliance Officer" to update the credentials'
        ])

    def test_04_dynamic_shelflife_prediction_based_on_iot_temperature_logs(self):
        """
        Scenario: Dynamic shelf-life prediction based on IoT temperature logs
        Given a batch of produce in transit with IoT temperature sensors
        When the system detects a cumulative temperature deviation (Arrhenius Equation)
        Then the "Expiry Date" of the lot must be updated automatically
        And if the remaining shelf-life drops to 20%, a "Priority Sale" Activity must be triggered
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a batch of produce in transit with IoT temperature sensors',
            'When the system detects a cumulative temperature deviation (Arrhenius Equation)',
            'Then the "Expiry Date" of the lot must be updated automatically',
            'And if the remaining shelf-life drops to 20%, a "Priority Sale" Activity must be triggered'
        ])

    def test_05_fefo_first_expired_first_out_pick_strategy(self):
        """
        Scenario: FEFO (First Expired First Out) pick strategy
        Given multiple lots of the same product with different expiry dates
        When the system generates a picking order
        Then it must automatically suggest the lot with the earliest expiry date
        And if a worker scans a later lot on a PDA, a red hard warning must be displayed
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given multiple lots of the same product with different expiry dates',
            'When the system generates a picking order',
            'Then it must automatically suggest the lot with the earliest expiry date',
            'And if a worker scans a later lot on a PDA, a red hard warning must be displayed'
        ])

    def test_06_dna_contamination_lineage_chain_transit_block_dna(self):
        """
        Scenario: DNA Contamination Lineage Chain Transit Block (DNA污染溯源链条运输拦截机制)
        Given a stock lot "LOT-2026-GRAIN-01" registered in "stock.lot" (库存批次模型) has an active non-GMO certification (激活了非转基因认证)
        And the DNA lineage analysis detects genetic contamination exceeding the authorized threshold (且DNA溯源分析检测到基因污染超过授权阈值)
        When the logistics manager attempts to confirm a transit stock move on "stock.move" (库存移动模型) for this lot
        Then the system must block the confirmation of the stock move, hard-locking its status to "quarantine" (强制锁定至隔离检疫状态)
        And raise a "ValidationError" (验证错误) with message "DNA_CONTAMINATION_DETECTED" (包含"检测到基因修饰污染"提示信息)
        And the system must propagate the certification quarantine block to all child stock moves in the downstream lineage chain (并将此证书锁定状态自动传递至下游溯源链中的所有子级库存移动)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a stock lot "LOT-2026-GRAIN-01" registered in "stock.lot" (库存批次模型) has an active non-GMO certification (激活了非转基因认证)',
            'And the DNA lineage analysis detects genetic contamination exceeding the authorized threshold (且DNA溯源分析检测到基因污染超过授权阈值)',
            'When the logistics manager attempts to confirm a transit stock move on "stock.move" (库存移动模型) for this lot',
            'Then the system must block the confirmation of the stock move, hard-locking its status to "quarantine" (强制锁定至隔离检疫状态)',
            'And raise a "ValidationError" (验证错误) with message "DNA_CONTAMINATION_DETECTED" (包含"检测到基因修饰污染"提示信息)',
            'And the system must propagate the certification quarantine block to all child stock moves in the downstream lineage chain (并将此证书锁定状态自动传递至下游溯源链中的所有子级库存移动)'
        ])
