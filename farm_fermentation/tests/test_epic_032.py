# -*- coding: utf-8 -*-
from odoo.addons.farm_core.tests.bdd_base import BddTransactionCase
from odoo.exceptions import UserError, ValidationError

class TestEpic032(BddTransactionCase):
    """ BDD Test Suite for Epic 032: Epic 032 Traditional Fermentation Management """

    def setUp(self):
        super(TestEpic032, self).setUp()

    def test_01_soy_sauce_koji_mold_assay_checks_and_starter_inoculation_lock(self):
        """
        Scenario: Soy sauce koji mold assay checks and starter inoculation lock
        Given a soy sauce fermenting jar lot registered under "agri.isl.lot.ferment"
        When microbiological lab assays register active koji mold density below "1.0e6" CFU/g
        Then the system must automatically change the jar lot status to "MOLD_GROWTH_DEVIATION"
        And lock the jar lot from undergoing downstream extraction or pressing moves
        And generate an automated corrective workorder "mrp.workorder" for manual starter yeast re-inoculation
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a soy sauce fermenting jar lot registered under "agri.isl.lot.ferment"',
            'When microbiological lab assays register active koji mold density below "1.0e6" CFU/g',
            'Then the system must automatically change the jar lot status to "MOLD_GROWTH_DEVIATION"',
            'And lock the jar lot from undergoing downstream extraction or pressing moves',
            'And generate an automated corrective workorder "mrp.workorder" for manual starter yeast re-inoculation'
        ])

    def test_02_aflatoxin_heavy_metal_raw_material_intake_quality_gating(self):
        """
        Scenario: Aflatoxin heavy metal raw material intake quality gating
        Given a raw material soybean intake shipment under "stock.picking"
        When the laboratory inspector records an aflatoxin assay concentration of "6.2" PPB (above the food safety threshold of "5.0" PPB)
        Then the "AgriQualityGateMixin" must flag the raw lot as "CRITICAL_FAIL_REJECT"
        And block the receipt confirmation of the picking "stock.picking"
        And automatically generate a return-to-supplier shipping order
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a raw material soybean intake shipment under "stock.picking"',
            'When the laboratory inspector records an aflatoxin assay concentration of "6.2" PPB (above the food safety threshold of "5.0" PPB)',
            'Then the "AgriQualityGateMixin" must flag the raw lot as "CRITICAL_FAIL_REJECT"',
            'And block the receipt confirmation of the picking "stock.picking"',
            'And automatically generate a return-to-supplier shipping order'
        ])

    def test_03_fermentation_jar_solar_tracking_sensor_telemetry_offline_fallback(self):
        """
        Scenario: Fermentation jar solar tracking sensor telemetry offline fallback
        Given a series of traditional fermentation jars monitored by IoT solar tracking temperature sensors
        When the jar telemetry sensors fail and report null readings to the gateway for over "4" hours
        Then the system must flag the jar group's monitoring status as "SENSORY_FAILED"
        And automatically generate and assign a daily manual thermal inspection task "mrp.workorder" for the respective jar row
        And log a telemetry loss ticket in the system
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a series of traditional fermentation jars monitored by IoT solar tracking temperature sensors',
            'When the jar telemetry sensors fail and report null readings to the gateway for over "4" hours',
            'Then the system must flag the jar group\'s monitoring status as "SENSORY_FAILED"',
            'And automatically generate and assign a daily manual thermal inspection task "mrp.workorder" for the respective jar row',
            'And log a telemetry loss ticket in the system'
        ])

    def test_04_summer_sunshade_sails_automatic_activation_on_high_ambient_temperature(self):
        """
        Scenario: Summer sun-shade sails automatic activation on high ambient temperature
        Given a natural soy sauce fermentation aging field with automated sun-shade sails
        When the ambient meteorological sensor logs a temperature reading greater than "42.0" °C during summer sun exposure
        Then the system must trigger the actuator command to deploy the physical sun-shade sails
        And log the temperature breach event and sails deployment in Odoo Chatter
        And transition the field's climate state to "SHADED_PROTECTIVE"
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a natural soy sauce fermentation aging field with automated sun-shade sails',
            'When the ambient meteorological sensor logs a temperature reading greater than "42.0" °C during summer sun exposure',
            'Then the system must trigger the actuator command to deploy the physical sun-shade sails',
            'And log the temperature breach event and sails deployment in Odoo Chatter',
            'And transition the field\'s climate state to "SHADED_PROTECTIVE"'
        ])

    def test_05_vinegar_aging_acidity_level_check_and_bottling_lock(self):
        """
        Scenario: Vinegar aging acidity level check and bottling lock
        Given a traditionally aged vinegar lot in aging vat "stock.lot"
        When the laboratory quality analysis records total titratable acidity of "4.8" % (below the bottling standard of "5.5" %)
        Then the system must lock the vat lot from being used in any bottling packaging order "mrp.production"
        And flag the lot quality state as "ACIDITY_DEFICIENT_HOLD"
        And force-reroute the lot destination for an extended aging cycle
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a traditionally aged vinegar lot in aging vat "stock.lot"',
            'When the laboratory quality analysis records total titratable acidity of "4.8" % (below the bottling standard of "5.5" %)',
            'Then the system must lock the vat lot from being used in any bottling packaging order "mrp.production"',
            'And flag the lot quality state as "ACIDITY_DEFICIENT_HOLD"',
            'And force-reroute the lot destination for an extended aging cycle'
        ])

    def test_06_sunshade_sail_deploy_actuator_failure_and_manual_intervention_override_dispatch(self):
        """
        Scenario: Sun-Shade Sail Deploy Actuator Failure and Manual Intervention Override Dispatch
        Given a soy sauce fermenting jar lot in "stock.lot" (库存批次) registered under "agri.isl.lot.ferment" (发酵物联日志)
        And the automated shade sails system is configured with ambient heat sensors
        When the ambient temperature registers 45.0 °C but the sails deploy actuator fails to verify its fully deployed position within 5 minutes
        Then the system must trigger a high-visibility warning in the control room
        And automatically transition the climate state to "Actuator Failed" (设备故障)
        And dispatch an urgent physical manual mitigation mission "mrp.workorder" [mrp.workorder] (作业任务) to cover the jars with manual straw mats
        And raise a "ValidationError" (验证错误) if an operator attempts to dismiss the alarm without performing the manual override
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a soy sauce fermenting jar lot in "stock.lot" (库存批次) registered under "agri.isl.lot.ferment" (发酵物联日志)',
            'And the automated shade sails system is configured with ambient heat sensors',
            'When the ambient temperature registers 45.0 °C but the sails deploy actuator fails to verify its fully deployed position within 5 minutes',
            'Then the system must trigger a high-visibility warning in the control room',
            'And automatically transition the climate state to "Actuator Failed" (设备故障)',
            'And dispatch an urgent physical manual mitigation mission "mrp.workorder" [mrp.workorder] (作业任务) to cover the jars with manual straw mats',
            'And raise a "ValidationError" (验证错误) if an operator attempts to dismiss the alarm without performing the manual override'
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
