# -*- coding: utf-8 -*-
from odoo.addons.farm_core.tests.bdd_base import BddTransactionCase
from odoo.exceptions import UserError, ValidationError

class TestEpic027(BddTransactionCase):
    """ BDD Test Suite for Epic 027: Epic 027 Winery & Enology Management """

    def setUp(self):
        super(TestEpic027, self).setUp()

    def test_01_yeast_fermentation_temperature_cooling_jacket_actuator_regulation(self):
        """
        Scenario: Yeast fermentation temperature cooling jacket actuator regulation
        Given a wine batch undergoing white wine fermentation in a tank workcenter "mrp.workcenter"
        And the tank is registered via "agri.isl.wine.ferment" with cooling jackets connected to IoT valve actuators
        When the yeast fermentation temperature sensor registers a reading exceeding "18.0" °C
        Then the system must trigger automated cooling jacket coolant valves to open to the 100% position
        And record the temperature log and coolant valve state in Odoo to maintain optimal fermentation kinetics
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a wine batch undergoing white wine fermentation in a tank workcenter "mrp.workcenter"',
            'And the tank is registered via "agri.isl.wine.ferment" with cooling jackets connected to IoT valve actuators',
            'When the yeast fermentation temperature sensor registers a reading exceeding "18.0" °C',
            'Then the system must trigger automated cooling jacket coolant valves to open to the 100% position',
            'And record the temperature log and coolant valve state in Odoo to maintain optimal fermentation kinetics'
        ])

    def test_02_enological_laboratory_gate_for_bottling_block(self):
        """
        Scenario: Enological laboratory gate for bottling block
        Given a finished wine lot "stock.lot" undergoing pre-bottling laboratory analysis
        When the lab analyst records a free SO2 level exceeding "50.0" PPM
        And a residual sugar level of "4.5" g/L (exceeding the dry standard threshold)
        Then the "AgriQualityGateMixin" must block the bottling manufacturing packaging order
        And flag the wine lot's state as "Locked for Bottling" until chemical remediation is confirmed
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a finished wine lot "stock.lot" undergoing pre-bottling laboratory analysis',
            'When the lab analyst records a free SO2 level exceeding "50.0" PPM',
            'And a residual sugar level of "4.5" g/L (exceeding the dry standard threshold)',
            'Then the "AgriQualityGateMixin" must block the bottling manufacturing packaging order',
            'And flag the wine lot\'s state as "Locked for Bottling" until chemical remediation is confirmed'
        ])

    def test_03_fermentation_temperature_sensor_failure_safe_mode_trickle_cooling(self):
        """
        Scenario: Fermentation temperature sensor failure safe mode trickle cooling
        Given a red wine batch undergoing active fermentation in a tank
        When the tank temperature sensor fails and reports corrupted or null readings to the IoT gateway
        Then the system must transition the fermentation state to "SENSORY_FAILED"
        And trigger the cooling jacket coolant valve to open to a constant "10.0" percent trickle rate to prevent a thermal run-away spike
        And dispatch an emergency notification to the on-duty cellar master
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a red wine batch undergoing active fermentation in a tank',
            'When the tank temperature sensor fails and reports corrupted or null readings to the IoT gateway',
            'Then the system must transition the fermentation state to "SENSORY_FAILED"',
            'And trigger the cooling jacket coolant valve to open to a constant "10.0" percent trickle rate to prevent a thermal run-away spike',
            'And dispatch an emergency notification to the on-duty cellar master'
        ])

    def test_04_oak_barrel_aging_and_wood_asset_traceability(self):
        """
        Scenario: Oak barrel aging and wood asset traceability
        Given an oak barrel asset defined in "farm.winery.vessel" proxying "mrp.workcenter"
        And the barrel is configured with French Oak wood type, medium-plus toast level, and 2-years age
        When a wine lot is moved into this barrel lot via a registered "stock.move" for cellar aging
        Then the system must link the barrel's wood type, toast level, and aging history to the wine lot's digital terroir card
        And record this barrel contribution in the "AgriTraceabilityMixin" line history
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an oak barrel asset defined in "farm.winery.vessel" proxying "mrp.workcenter"',
            'And the barrel is configured with French Oak wood type, medium-plus toast level, and 2-years age',
            'When a wine lot is moved into this barrel lot via a registered "stock.move" for cellar aging',
            "Then the system must link the barrel's wood type, toast level, and aging history to the wine lot's digital terroir card",
            'And record this barrel contribution in the "AgriTraceabilityMixin" line history'
        ])

    def test_05_malolactic_fermentation_laboratory_check_and_stabilization_transition(self):
        """
        Scenario: Malolactic fermentation laboratory check and stabilization transition
        Given a red wine batch in post-primary fermentation undergoing malolactic fermentation
        When the laboratory analysis records malic acid concentration below "0.1" g/L
        Then the system must flag Malolactic Fermentation as "Complete" in the batch's enology logs
        And transition the wine production batch state to "Cold Stabilization"
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a red wine batch in post-primary fermentation undergoing malolactic fermentation',
            'When the laboratory analysis records malic acid concentration below "0.1" g/L',
            'Then the system must flag Malolactic Fermentation as "Complete" in the batch\'s enology logs',
            'And transition the wine production batch state to "Cold Stabilization"'
        ])

    def test_06_fermentation_tank_cooling_pump_power_interruption_and_backup_water_intake_trigger(self):
        """
        Scenario: Fermentation Tank Cooling Pump Power Interruption and Back-up Water Intake Trigger
        Given a winery fermentation batch in "stock.lot" (库存批次) inside a fermentation tank "mrp.workcenter" (工作中心)
        And the main cooling pump electric state in "agri.isl.wine.ferment" (酿造物联网记录) is "On" (运行中)
        When the electric current sensor registers a zero-current anomaly during active fermentation
        Then the system must atomically open the mechanical emergency backup reservoir water valve actuator to "100% Flow" (全流量)
        And transition the fermentation state to "Emergency Cooling" (紧急冷却)
        And generate an emergency repair mission "mrp.workorder" [mrp.workorder] (作业任务) for the maintenance crew
        And raise a "ValidationError" (验证错误) to prevent any "stock.move" (库存移动) for bottling of this batch
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a winery fermentation batch in "stock.lot" (库存批次) inside a fermentation tank "mrp.workcenter" (工作中心)',
            'And the main cooling pump electric state in "agri.isl.wine.ferment" (酿造物联网记录) is "On" (运行中)',
            'When the electric current sensor registers a zero-current anomaly during active fermentation',
            'Then the system must atomically open the mechanical emergency backup reservoir water valve actuator to "100% Flow" (全流量)',
            'And transition the fermentation state to "Emergency Cooling" (紧急冷却)',
            'And generate an emergency repair mission "mrp.workorder" [mrp.workorder] (作业任务) for the maintenance crew',
            'And raise a "ValidationError" (验证错误) to prevent any "stock.move" (库存移动) for bottling of this batch'
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
