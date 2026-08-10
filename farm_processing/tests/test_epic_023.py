# -*- coding: utf-8 -*-
from odoo.addons.farm_core.tests.bdd_base import BddTransactionCase
from odoo.exceptions import UserError, ValidationError

class TestEpic023(BddTransactionCase):
    """ BDD Test Suite for Epic 023: Epic 023 Essential Oil Management """

    def setUp(self):
        super(TestEpic023, self).setUp()

    def test_01_gcms_purity_grade_valuation(self):
        """
        Scenario: GC-MS Purity Grade Valuation
        Given a steam-extracted essential oil lot registered in "agri.isl.essential.oil"
        And the lot's initial target grade is set to "Premium"
        When the Gas Chromatography (GC-MS) laboratory analysis registers a Linalool content below 35.0%
        Then the system must automatically downgrade the lot's quality grade classification to "Standard"
        And the system must decrease the lot's default selling unit price by 20% in the price list
        And the system must log the grade correction in the lot chatter
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a steam-extracted essential oil lot registered in "agri.isl.essential.oil"',
            'And the lot's initial target grade is set to "Premium"',
            'When the Gas Chromatography (GC-MS) laboratory analysis registers a Linalool content below 35.0%',
            'Then the system must automatically downgrade the lot's quality grade classification to "Standard"',
            'And the system must decrease the lot's default selling unit price by 20% in the price list',
            'And the system must log the grade correction in the lot chatter'
        ])

    def test_02_highpressure_steam_extraction_interlock(self):
        """
        Scenario: High-Pressure Steam Extraction Interlock
        Given a running essential oil steam extractor in a production workcenter
        And an extraction workorder active in "mrp.workorder"
        When the pressure sensors in the extractor log a reading greater than 6.0 Bar
        Then the system must trigger a high-visibility emergency pressure relief alarm
        And the system must atomically transition the active extraction workorder state to "paused"
        And the system must shut off the steam inlet valve actuator automatically
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a running essential oil steam extractor in a production workcenter',
            'And an extraction workorder active in "mrp.workorder"',
            'When the pressure sensors in the extractor log a reading greater than 6.0 Bar',
            'Then the system must trigger a high-visibility emergency pressure relief alarm',
            'And the system must atomically transition the active extraction workorder state to "paused"',
            'And the system must shut off the steam inlet valve actuator automatically'
        ])

    def test_03_extraction_spent_biomass_recycled_cost_credits(self):
        """
        Scenario: Extraction Spent Biomass Recycled Cost Credits
        Given a completed essential oil extraction workorder yielding spent lavender straw biomass
        And a transfer order "stock.picking" created to move the spent straw
        When the operator moves the spent lavender straw to the farm compost location
        Then the system must calculate and allocate composting resource value credits
        And the system must automatically apply these credits to reduce the overall raw agricultural material costs of the original production order
        And the system must log the circular economy credit in the accounting ledger
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a completed essential oil extraction workorder yielding spent lavender straw biomass',
            'And a transfer order "stock.picking" created to move the spent straw',
            'When the operator moves the spent lavender straw to the farm compost location',
            'Then the system must calculate and allocate composting resource value credits',
            'And the system must automatically apply these credits to reduce the overall raw agricultural material costs of the original production order',
            'And the system must log the circular economy credit in the accounting ledger'
        ])

    def test_04_multilot_material_batch_blending_traceability(self):
        """
        Scenario: Multi-Lot Material Batch Blending Traceability
        Given multiple raw harvest lots consumed in a blending operation
        And the target mixed oil batch registered as a new lot in "stock.lot"
        When the blending operation is finalized and confirmed via the inventory interface
        Then the system must construct a precise lot lineage tree mapping each percentage input of raw harvest lots
        And the system must embed this lineage tree directly into the final product lot's digital passport
        And the system must allow inspectors to trace any final bottle back to all original fields
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given multiple raw harvest lots consumed in a blending operation',
            'And the target mixed oil batch registered as a new lot in "stock.lot"',
            'When the blending operation is finalized and confirmed via the inventory interface',
            'Then the system must construct a precise lot lineage tree mapping each percentage input of raw harvest lots',
            'And the system must embed this lineage tree directly into the final product lot's digital passport',
            'And the system must allow inspectors to trace any final bottle back to all original fields'
        ])

    def test_05_oil_moisture_density_lab_gating(self):
        """
        Scenario: Oil Moisture & Density Lab Gating
        Given a refined essential oil lot awaiting inventory confirmation
        And laboratory sample inputs for moisture and density parameters
        When the lab moisture content exceeds 0.05%
        And the lab density is measured outside the range of 0.875 to 0.895 g/cm³
        Then the system must raise a quality alert error
        And the system must automatically lock the lot from inventory valuation and picking confirmations
        And the lot state must transition to "Hold for Re-refinement"
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a refined essential oil lot awaiting inventory confirmation',
            'And laboratory sample inputs for moisture and density parameters',
            'When the lab moisture content exceeds 0.05%',
            'And the lab density is measured outside the range of 0.875 to 0.895 g/cm³',
            'Then the system must raise a quality alert error',
            'And the system must automatically lock the lot from inventory valuation and picking confirmations',
            'And the lot state must transition to "Hold for Re-refinement"'
        ])

    def test_06_extraction_vessel_pressure_telemetry_disconnect_and_emergency_vent_valve_open(self):
        """
        Scenario: Extraction Vessel Pressure Telemetry Disconnect and Emergency Vent Valve Open
        Given an active extraction run recorded in "mrp.production" (制造订单)
        And the pressure monitoring stream in "agri.isl.essential.oil" (精油物联网记录) status is "Normal" (正常)
        When the primary pressure sensor suddenly goes offline and reports null values during high-pressure steam extraction
        Then the system must transition the workstation status to "SENSORY_FAILED" (传感器异常)
        And trigger an automated backup physical vent valve actuator to "Fully Open" (全开) to prevent explosion risks
        And transition the active extraction mission "mrp.workorder" [mrp.workorder] (作业任务) state to "Paused" (已暂停)
        And raise a "UserError" (用户错误) and lock the associated essential oil lot in "stock.lot" (库存批次) from further processing
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an active extraction run recorded in "mrp.production" (制造订单)',
            'And the pressure monitoring stream in "agri.isl.essential.oil" (精油物联网记录) status is "Normal" (正常)',
            'When the primary pressure sensor suddenly goes offline and reports null values during high-pressure steam extraction',
            'Then the system must transition the workstation status to "SENSORY_FAILED" (传感器异常)',
            'And trigger an automated backup physical vent valve actuator to "Fully Open" (全开) to prevent explosion risks',
            'And transition the active extraction mission "mrp.workorder" [mrp.workorder] (作业任务) state to "Paused" (已暂停)',
            'And raise a "UserError" (用户错误) and lock the associated essential oil lot in "stock.lot" (库存批次) from further processing'
        ])

    def test_07_recipe_highmixing_entropy_quality_penalty_gating(self):
        """
        Scenario: Recipe High-Mixing Entropy Quality Penalty Gating (配方物料高混合熵防错拦截门禁机制)
        Given a multi-input biological compound formulation using "mrp.bom" (物料清单模型)
        And a processing batch in "mrp.production" (生产订单模型)
        When the operator attempts to confirm recipe "action_confirm" with a calculated mixing entropy score "mixing_entropy" above 0.85 (当操作员尝试执行确认配方系统动作且计算出的混合熵得分字段值超过0.85阈值时)
        Then the quality engine must apply a 10.0% mixing entropy score penalty on "mixing_entropy_penalty" (系统必须自动在该批次中应用10.0%的混合熵惩罚比例字段值)
        And raise a ValidationError (并且抛出验证错误) with message "MIXING_ENTROPY_LIMIT_EXCEEDED" (包含"混合熵超限，批次质量评级降级"提示信息)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a multi-input biological compound formulation using "mrp.bom" (物料清单模型)',
            'And a processing batch in "mrp.production" (生产订单模型)',
            'When the operator attempts to confirm recipe "action_confirm" with a calculated mixing entropy score "mixing_entropy" above 0.85 (当操作员尝试执行确认配方系统动作且计算出的混合熵得分字段值超过0.85阈值时)',
            'Then the quality engine must apply a 10.0% mixing entropy score penalty on "mixing_entropy_penalty" (系统必须自动在该批次中应用10.0%的混合熵惩罚比例字段值)',
            'And raise a ValidationError (并且抛出验证错误) with message "MIXING_ENTROPY_LIMIT_EXCEEDED" (包含"混合熵超限，批次质量评级降级"提示信息)'
        ])
