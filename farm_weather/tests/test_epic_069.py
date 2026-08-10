# -*- coding: utf-8 -*-
from odoo.addons.farm_core.tests.bdd_base import BddTransactionCase
from odoo.exceptions import UserError, ValidationError

class TestEpic069(BddTransactionCase):
    """ BDD Test Suite for Epic 069: Epic 069 Agricultural Weather Station (农业气象站) """

    def setUp(self):
        super(TestEpic069, self).setUp()

    def test_01_onsite_weather_evapotranspiration_drip_irrigation_schedule_adjustment(self):
        """
        Scenario: On-Site Weather Evapotranspiration Drip Irrigation Schedule Adjustment (现场天气蒸腾蒸发量滴灌时间表调整)
        Given soil moisture sensor locations "stock.location" (库存位置) linked to an on-site weather station "agri.weather.sensor" (农业天气传感器模型)
        When weather station calculations log a daily reference Evapotranspiration "ET0" greater than "6.0 mm" (每日参考蒸发蒸腾量大于6.0毫米)
        Then the system must automatically adjust the drip irrigation watering duration in the scheduler by "120%"
        And register the modification on the irrigation log with the message "ET0 High: Irrigation scaled to 120%" (高蒸发量：灌溉量调整至120%)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given soil moisture sensor locations "stock.location" (库存位置) linked to an on-site weather station "agri.weather.sensor" (农业天气传感器模型)',
            'When weather station calculations log a daily reference Evapotranspiration "ET0" greater than "6.0 mm" (每日参考蒸发蒸腾量大于6.0毫米)',
            'Then the system must automatically adjust the drip irrigation watering duration in the scheduler by "120%"',
            'And register the modification on the irrigation log with the message "ET0 High: Irrigation scaled to 120%" (高蒸发量：灌溉量调整至120%)'
        ])

    def test_02_frost_prediction_automated_wind_sprinkler_active_safety(self):
        """
        Scenario: Frost Prediction Automated Wind Sprinkler Active Safety (防霜冻预测自动风机洒水器主动安全)
        Given a vineyard orchard location "stock.location" (库存位置) equipped with automated anti-frost sprinklers and wind machines
        When the weather station forecast "agri.weather.sensor" (农业天气传感器模型) predicts ambient temperature dropping below "0.5°C" with a wind speed under "1.5 m/s"
        Then the system must trigger active PLC relay commands to power on anti-frost sprinklers and start wind machines
        And transition the station safety state to "active_protection" (主动防护) on the weather integration dashboard
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a vineyard orchard location "stock.location" (库存位置) equipped with automated anti-frost sprinklers and wind machines',
            'When the weather station forecast "agri.weather.sensor" (农业天气传感器模型) predicts ambient temperature dropping below "0.5°C" with a wind speed under "1.5 m/s"',
            'Then the system must trigger active PLC relay commands to power on anti-frost sprinklers and start wind machines',
            'And transition the station safety state to "active_protection" (主动防护) on the weather integration dashboard'
        ])

    def test_03_weather_station_telemetry_failure_fallback(self):
        """
        Scenario: Weather Station Telemetry Failure Fallback (气象站遥测失效备用方案)
        Given planned crop protection spraying workorders under "mrp.workorder" (制造工单) scheduled for today
        When the weather station "agri.weather.sensor" (农业天气传感器模型) goes offline with null telemetry updates for over "1 hour"
        Then the system must block the start validation of spraying workorders and raise a warning message "Weather Station Offline: Manual Wind Check Required" (气象站离线：需要手动风速校验)
        And default the safety status of the agricultural zone to "manual_check" (手动校验)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given planned crop protection spraying workorders under "mrp.workorder" (制造工单) scheduled for today',
            'When the weather station "agri.weather.sensor" (农业天气传感器模型) goes offline with null telemetry updates for over "1 hour"',
            'Then the system must block the start validation of spraying workorders and raise a warning message "Weather Station Offline: Manual Wind Check Required" (气象站离线：需要手动风速校验)',
            'And default the safety status of the agricultural zone to "manual_check" (手动校验)'
        ])

    def test_04_high_wind_crop_spraying_gating(self):
        """
        Scenario: High Wind Crop Spraying Gating (大风作物喷洒控制)
        Given an active chemical spraying workorder "mrp.workorder" (制造工单) in state "progress" (进行中)
        When the wind speed sensor on "agri.weather.sensor" (农业天气传感器模型) logs a wind speed exceeding "4.0 m/s" (风速超过4.0米/秒的农药飘移隐患)
        Then the system must automatically pause the active spraying workorder and transition its state to "blocked" (已阻断)
        And log the blocking reason as "High Wind Drift Risk: Spraying suspended" (大风飘移风险：喷洒已挂起)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an active chemical spraying workorder "mrp.workorder" (制造工单) in state "progress" (进行中)',
            'When the wind speed sensor on "agri.weather.sensor" (农业天气传感器模型) logs a wind speed exceeding "4.0 m/s" (风速超过4.0米/秒的农药飘移隐患)',
            'Then the system must automatically pause the active spraying workorder and transition its state to "blocked" (已阻断)',
            'And log the blocking reason as "High Wind Drift Risk: Spraying suspended" (大风飘移风险：喷洒已挂起)'
        ])

    def test_05_barometric_pressure_trend_rain_alerts(self):
        """
        Scenario: Barometric Pressure Trend Rain Alerts (气压趋势降雨警报)
        Given an active grain harvesting campaign running in the field
        When the barometric pressure sensor on "agri.weather.sensor" (农业天气传感器模型) logs a drop greater than "3.0 hPa" within a "3 hour" window
        Then the system must dispatch an urgent high-priority SMS/email alert to harvesting operators "res.users" (用户模型) stating "Barometric Drop: Cover harvested grains immediately" (气压骤降：请立即遮盖收获谷物)
        And set the campaign storm warning status to "storm_warning" (暴风雨预警)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an active grain harvesting campaign running in the field',
            'When the barometric pressure sensor on "agri.weather.sensor" (农业天气传感器模型) logs a drop greater than "3.0 hPa" within a "3 hour" window',
            'Then the system must dispatch an urgent high-priority SMS/email alert to harvesting operators "res.users" (用户模型) stating "Barometric Drop: Cover harvested grains immediately" (气压骤降：请立即遮盖收获谷物)',
            'And set the campaign storm warning status to "storm_warning" (暴风雨预警)'
        ])

    def test_06_weather_station_rainfall_sensor_drift_calibration(self):
        """
        Scenario: Weather Station Rainfall Sensor Drift Calibration (气象站雨量传感器漂移校对)
        Given an active weather integration under "agri.weather.sensor" (农业天气传感器模型)
        When comparing daily weather station accumulated rainfall with adjacent grid radar data and identifying a sensor drift deviation exceeding "25.0%" (传感器温漂偏差超过25.0%)
        Then the system must automatically flag the weather station's status on the dashboard as "drift_alert" (漂移预警)
        And trigger an automated manual validation activity "project.task" (项目任务) to calibrate the weather station rainfall sensor
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an active weather integration under "agri.weather.sensor" (农业天气传感器模型)',
            'When comparing daily weather station accumulated rainfall with adjacent grid radar data and identifying a sensor drift deviation exceeding "25.0%" (传感器温漂偏差超过25.0%)',
            'Then the system must automatically flag the weather station\'s status on the dashboard as "drift_alert" (漂移预警)',
            'And trigger an automated manual validation activity "project.task" (项目任务) to calibrate the weather station rainfall sensor'
        ])

    def test_07_greenhouse_controller_plc_connectivity_signal_loss_failsafe_plc(self):
        """
        Scenario: Greenhouse Controller PLC Connectivity Signal Loss Failsafe (大棚智能PLC网关连接丢失安全熔断机制)
        Given a greenhouse climate controller registered in "iiot.device" (工业物联网设备模型) with status "connected" (已连接状态)
        When the system detects a PLC heartbeat signal loss for over 15.0 seconds (当系统检测到PLC控制器心跳遥测信号丢失持续超过15.0秒时)
        Then the physical actuator must automatically trigger safe mode (物理执行器必须自动切换至安全状态自锁模式)
        And create an emergency alert log in "AgriIncidentAlertMixin" (并在农业事件警报混合模型上自动创建紧急故障告警日志)
        And raise a ValidationError (并且抛出验证错误) with message "PLC_HEARTBEAT_LOSS_SAFE_STATE" (包含"PLC心跳丢失，系统进入物理自锁安全保护状态"提示信息)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a greenhouse climate controller registered in "iiot.device" (工业物联网设备模型) with status "connected" (已连接状态)',
            'When the system detects a PLC heartbeat signal loss for over 15.0 seconds (当系统检测到PLC控制器心跳遥测信号丢失持续超过15.0秒时)',
            'Then the physical actuator must automatically trigger safe mode (物理执行器必须自动切换至安全状态自锁模式)',
            'And create an emergency alert log in "AgriIncidentAlertMixin" (并在农业事件警报混合模型上自动创建紧急故障告警日志)',
            'And raise a ValidationError (并且抛出验证错误) with message "PLC_HEARTBEAT_LOSS_SAFE_STATE" (包含"PLC心跳丢失，系统进入物理自锁安全保护状态"提示信息)'
        ])
