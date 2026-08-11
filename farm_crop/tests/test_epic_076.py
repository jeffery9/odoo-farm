# -*- coding: utf-8 -*-
from odoo.addons.farm_core.tests.bdd_base import BddTransactionCase
from odoo.exceptions import UserError, ValidationError

class TestEpic076(BddTransactionCase):
    """ BDD Test Suite for Epic 076: Epic 076 Precision Production & VRA (精密生产与变量施肥) """

    def setUp(self):
        super(TestEpic076, self).setUp()

    def test_01_dynamic_nutrient_prescription_dosage_calculation_based_on_soil_organic_matter(self):
        """
        Scenario: Dynamic nutrient prescription dosage calculation based on Soil Organic Matter
        Given a precision manufacturing order "mrp.production" (生产单) with an active prescription "agri.vra.prescription" (精准处方单) in status "draft" (草稿)
        When the target parcel's soil organic matter (土壤有机质) "soil_som" is logged as 1.5% (低碳指标)
        Then the precision engine automatically calculates the target dosage as 5.0 tons/hectare
        And scales up the target compost recipe component inputs on "stock.move" (库存移动) by 20.0% upon executing "action_confirm" (确认)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a precision manufacturing order "mrp.production" (生产单) with an active prescription "agri.vra.prescription" (精准处方单) in status "draft" (草稿)',
            'When the target parcel\'s soil organic matter (土壤有机质) "soil_som" is logged as 1.5% (低碳指标)',
            'Then the precision engine automatically calculates the target dosage as 5.0 tons/hectare',
            'And scales up the target compost recipe component inputs on "stock.move" (库存移动) by 20.0% upon executing "action_confirm" (确认)'
        ])

    def test_02_realtime_variable_rate_application_spray_valve_plc_control(self):
        """
        Scenario: Real-time variable rate application spray valve PLC control
        Given a tractor-mounted precision sprayer actively fertilizing a parcel with GPS telemetry connected to Odoo via PLC (可编程逻辑控制器)
        When the tractor spatial coordinates transition from High-SOM Zone A (高有机质区域A) to Low-SOM Zone B (低有机质区域B)
        Then the system triggers an active PLC instruction to adjust the sprayer VRA active pump (变量泵) flows by -15.0%
        And updates the real-time VRA pump flow (变量泵流量) "vra_pump_flow" to match the target dosage
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a tractor-mounted precision sprayer actively fertilizing a parcel with GPS telemetry connected to Odoo via PLC (可编程逻辑控制器)',
            'When the tractor spatial coordinates transition from High-SOM Zone A (高有机质区域A) to Low-SOM Zone B (低有机质区域B)',
            'Then the system triggers an active PLC instruction to adjust the sprayer VRA active pump (变量泵) flows by -15.0%',
            'And updates the real-time VRA pump flow (变量泵流量) "vra_pump_flow" to match the target dosage'
        ])

    def test_03_vra_prescription_flow_telemetry_failure_fallback(self):
        """
        Scenario: VRA prescription flow telemetry failure fallback
        Given a variable rate fertilizer spray run on "mrp.workorder" (工单) in status "active" (激活)
        When the spray flow sensors fail to report for over 30 seconds (变量流速传感器离线)
        Then the system triggers an automatic safety lock to shut down active spraying valves (关闭喷阀)
        And transitions the "mrp.workorder" (工单) status to "paused" (暂停) to prevent localized soil chemical damage
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a variable rate fertilizer spray run on "mrp.workorder" (工单) in status "active" (激活)',
            'When the spray flow sensors fail to report for over 30 seconds (变量流速传感器离线)',
            'Then the system triggers an automatic safety lock to shut down active spraying valves (关闭喷阀)',
            'And transitions the "mrp.workorder" (工单) status to "paused" (暂停) to prevent localized soil chemical damage'
        ])

    def test_04_soil_nitrogen_saturation_runoff_block(self):
        """
        Scenario: Soil Nitrogen saturation runoff block
        Given a precision VRA fertilization "mrp.workorder" (工单) in status "draft" (草稿)
        When pre-treatment soil tests register nitrogen levels (土壤氮含量) "soil_nitrogen" exceeding 150.0 kg/hectare (硝酸盐径流风险)
        Then the system raises a ValidationError (验证错误) "Nitrogen level exceeds safety threshold of 150 kg/hectare" (氮含量超过150公斤/公顷的安全阈值)
        And blocks the "mrp.workorder" (工单) from transitioning to "active" (激活) status
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a precision VRA fertilization "mrp.workorder" (工单) in status "draft" (草稿)',
            'When pre-treatment soil tests register nitrogen levels (土壤氮含量) "soil_nitrogen" exceeding 150.0 kg/hectare (硝酸盐径流风险)',
            'Then the system raises a ValidationError (验证错误) "Nitrogen level exceeds safety threshold of 150 kg/hectare" (氮含量超过150公斤/公顷的安全阈值)',
            'And blocks the "mrp.workorder" (工单) from transitioning to "active" (激活) status'
        ])

    def test_05_completed_vra_mass_balance_reconciliation(self):
        """
        Scenario: Completed VRA mass balance reconciliation
        Given a completed precision production VRA fertilization run under "mrp.production" (生产单)
        When the manufacturing order "mrp.production" (生产单) transitions to status "done" (完成)
        Then the system triggers "action_verify_reconciliation" (验证对账) to compile the actual material mass applied
        And validates that the total actual fertilizer mass applied matches the physical inventory consumption on "stock.move" (库存移动) within a 2.0% deviation limit
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a completed precision production VRA fertilization run under "mrp.production" (生产单)',
            'When the manufacturing order "mrp.production" (生产单) transitions to status "done" (完成)',
            'Then the system triggers "action_verify_reconciliation" (验证对账) to compile the actual material mass applied',
            'And validates that the total actual fertilizer mass applied matches the physical inventory consumption on "stock.move" (库存移动) within a 2.0% deviation limit'
        ])

    def test_06_vra_tractor_altimeter_sensor_drift_compensation(self):
        """
        Scenario: VRA Tractor Altimeter Sensor Drift Compensation (变量喷洒拖拉机高度传感器漂移补偿)
        Given an active variable rate fertilization run on the mission "mrp.workorder" (作业任务)
        When the tractor's ultrasonic altitude sensor "iiot.device" (智能物联网设备) registers a continuous sensor drift deviation exceeding "15.0%" (高度传感器温漂偏差超过15.0%)
        Then the system must trigger a safety warning flag on the prescription "agri.vra.prescription" (精准处方单)
        And automatically compensate the VRA spray valve output calculations based on backup GPS altitude data to prevent uneven nitrogen distribution
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an active variable rate fertilization run on the mission "mrp.workorder" (作业任务)',
            'When the tractor\'s ultrasonic altitude sensor "iiot.device" (智能物联网设备) registers a continuous sensor drift deviation exceeding "15.0%" (高度传感器温漂偏差超过15.0%)',
            'Then the system must trigger a safety warning flag on the prescription "agri.vra.prescription" (精准处方单)',
            'And automatically compensate the VRA spray valve output calculations based on backup GPS altitude data to prevent uneven nitrogen distribution'
        ])
