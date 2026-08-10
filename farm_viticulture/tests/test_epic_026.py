# -*- coding: utf-8 -*-
from odoo.addons.farm_core.tests.bdd_base import BddTransactionCase
from odoo.exceptions import UserError, ValidationError

class TestEpic026(BddTransactionCase):
    """ BDD Test Suite for Epic 026: Epic 026 Viticulture Terroir Management """

    def setUp(self):
        super(TestEpic026, self).setUp()

    def test_01_soil_water_potential_sensors_precision_irrigation_gating(self):
        """
        Scenario: Soil water potential sensors precision irrigation gating
        Given a vineyard plot in the active growing stage tracked via "agri.isl.lot.vineyard" on "stock.location"
        And the plot has automated drip irrigation valves connected to IoT actuators
        When the soil water potential sensor registers a value below "-80.0" kPa (high water stress)
        Then the system must trigger a start command to the automated drip irrigation actuator
        And log the irrigation event with start timestamp, target duration, and water potential in Odoo
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a vineyard plot in the active growing stage tracked via "agri.isl.lot.vineyard" on "stock.location"',
            'And the plot has automated drip irrigation valves connected to IoT actuators',
            'When the soil water potential sensor registers a value below "-80.0" kPa (high water stress)',
            'Then the system must trigger a start command to the automated drip irrigation actuator',
            'And log the irrigation event with start timestamp, target duration, and water potential in Odoo'
        ])

    def test_02_grape_brixtoacid_ratio_maturity_check_and_harvesting_campaign_gating(self):
        """
        Scenario: Grape Brix-to-acid ratio maturity check and harvesting campaign gating
        Given a pre-harvest grape sample from a plot recorded under "agri.isl.lot.vineyard"
        When the lab analyst logs a sugar level of "24.5" Brix
        And the titratable acidity is recorded as "5.2" g/L
        Then the "AgriQualityGateMixin" must flag the vineyard block status as "Ready for Harvest"
        And the system must auto-generate a harvesting campaign plan with a high priority
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a pre-harvest grape sample from a plot recorded under "agri.isl.lot.vineyard"',
            'When the lab analyst logs a sugar level of "24.5" Brix',
            'And the titratable acidity is recorded as "5.2" g/L',
            'Then the "AgriQualityGateMixin" must flag the vineyard block status as "Ready for Harvest"',
            'And the system must auto-generate a harvesting campaign plan with a high priority'
        ])

    def test_03_soil_moisture_telemetry_sensor_connection_failure_and_etc_model_fallback(self):
        """
        Scenario: Soil moisture telemetry sensor connection failure and ETc model fallback
        Given a vineyard irrigation controller tracking active plots
        When the soil moisture sensors fail to report telemetry readings for more than 4 consecutive hours
        Then the system must transition the sensor status to "SENSORY_FAILED"
        And switch the irrigation schedule from sensor-gated to a weather-adjusted historical evapotranspiration (ETc) model
        And generate a manual sensor inspection task for the field technician
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a vineyard irrigation controller tracking active plots',
            'When the soil moisture sensors fail to report telemetry readings for more than 4 consecutive hours',
            'Then the system must transition the sensor status to "SENSORY_FAILED"',
            'And switch the irrigation schedule from sensor-gated to a weather-adjusted historical evapotranspiration (ETc) model',
            'And generate a manual sensor inspection task for the field technician'
        ])

    def test_04_critical_ambient_frost_warning_and_automated_active_protection(self):
        """
        Scenario: Critical ambient frost warning and automated active protection
        Given a vineyard location under active micro-climate monitoring
        When the IoT temperature sensor registers an ambient reading below "0.5" °C
        Then the system must trigger automated active protection by starting the active wind machines and water sprinklers
        And post a high-priority frost warning notification in Odoo Chatter and send SMS alerts to the vineyard master
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a vineyard location under active micro-climate monitoring',
            'When the IoT temperature sensor registers an ambient reading below "0.5" °C',
            'Then the system must trigger automated active protection by starting the active wind machines and water sprinklers',
            'And post a high-priority frost warning notification in Odoo Chatter and send SMS alerts to the vineyard master'
        ])

    def test_05_grape_pesticide_phi_harvest_blocker_and_chemical_safety_check(self):
        """
        Scenario: Grape pesticide PHI harvest blocker and chemical safety check
        Given a vineyard parcel location with recorded chemical spray treatments
        And the treatment has a Pre-Harvest Interval (PHI) of "14" days
        When a harvest workorder attempts to start "10" days after the chemical application date
        Then the system must hard-lock the harvest workorder validation
        And raise a "ValidationError" with the message "BIOSECURITY_PHI_VIOLATION: Harvest blocked due to active pesticide Pre-Harvest Interval"
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a vineyard parcel location with recorded chemical spray treatments',
            'And the treatment has a Pre-Harvest Interval (PHI) of "14" days',
            'When a harvest workorder attempts to start "10" days after the chemical application date',
            'Then the system must hard-lock the harvest workorder validation',
            'And raise a "ValidationError" with the message "BIOSECURITY_PHI_VIOLATION: Harvest blocked due to active pesticide Pre-Harvest Interval"'
        ])

    def test_06_irrigation_pipe_burst_fluid_pressure_drop_detection_and_autoshutoff_actuation(self):
        """
        Scenario: Irrigation Pipe Burst Fluid Pressure Drop Detection and Auto-Shutoff Actuation
        Given a vineyard plot in "stock.location" (库存位置) with an active irrigation system
        And fluid pressure sensors monitoring the main irrigation pipeline
        When the pipeline sensor registers a sudden pressure drop of 80% within 10 seconds while irrigation is "Active" (启用)
        Then the system must automatically trigger the emergency master water valve actuator to "Closed" (关闭) to prevent soil erosion
        And create a critical maintenance mission "mrp.workorder" [mrp.workorder] (作业任务) in "agri.isl.lot.vineyard" (葡萄园记录)
        And raise a "ValidationError" (验证错误) to halt any upcoming automated watering campaigns for this plot
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a vineyard plot in "stock.location" (库存位置) with an active irrigation system',
            'And fluid pressure sensors monitoring the main irrigation pipeline',
            'When the pipeline sensor registers a sudden pressure drop of 80% within 10 seconds while irrigation is "Active" (启用)',
            'Then the system must automatically trigger the emergency master water valve actuator to "Closed" (关闭) to prevent soil erosion',
            'And create a critical maintenance mission "mrp.workorder" [mrp.workorder] (作业任务) in "agri.isl.lot.vineyard" (葡萄园记录)',
            'And raise a "ValidationError" (验证错误) to halt any upcoming automated watering campaigns for this plot'
        ])

    def test_07_crop_parcel_evapotranspiration_sensor_drift(self):
        """
        Scenario: Crop Parcel Evapotranspiration Sensor Drift (作物地块水分蒸腾传感器异常漂移自愈控制)
        Given a crop parcel's soil stock lot in "stock.lot" (库存批次模型) with crop variety "Rose" (且作物物种已设置为玫瑰)
        And a smart evapotranspiration sensor registered in "iiot.device" (并且智能蒸腾量传感器已注册在工业物联网设备模型中)
        When the soil sensor logs an NPK reading drift of 25.0% (当土壤传感器记录到氮磷钾读数偏离比比例达到25.0%时)
        Then the system must trigger safe mode self-correction (系统必须自动执行安全模式自校准动作)
        And scale back the water drip runtime "drip_duration" to fallback 10.0 minutes (并且将滴灌时长字段值等比例缩减至备用时长值10.0分钟)
        And raise a ValidationError (并且系统抛出验证错误) with message "CRITICAL_SENSOR_DRIFT_DETECTED" (包含"传感器发生严重漂移，进入自愈模式"提示信息)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a crop parcel's soil stock lot in "stock.lot" (库存批次模型) with crop variety "Rose" (且作物物种已设置为玫瑰)',
            'And a smart evapotranspiration sensor registered in "iiot.device" (并且智能蒸腾量传感器已注册在工业物联网设备模型中)',
            'When the soil sensor logs an NPK reading drift of 25.0% (当土壤传感器记录到氮磷钾读数偏离比比例达到25.0%时)',
            'Then the system must trigger safe mode self-correction (系统必须自动执行安全模式自校准动作)',
            'And scale back the water drip runtime "drip_duration" to fallback 10.0 minutes (并且将滴灌时长字段值等比例缩减至备用时长值10.0分钟)',
            'And raise a ValidationError (并且系统抛出验证错误) with message "CRITICAL_SENSOR_DRIFT_DETECTED" (包含"传感器发生严重漂移，进入自愈模式"提示信息)'
        ])
