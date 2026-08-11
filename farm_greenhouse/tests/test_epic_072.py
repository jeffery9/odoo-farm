# -*- coding: utf-8 -*-
from odoo.addons.farm_core.tests.bdd_base import BddTransactionCase
from odoo.exceptions import UserError, ValidationError

class TestEpic072(BddTransactionCase):
    """ BDD Test Suite for Epic 072: Epic 072 Smart Greenhouse Control (智能温室控制) """

    def setUp(self):
        super(TestEpic072, self).setUp()

    def test_01_active_relative_humidity_exhaust_fan_solenoid_control(self):
        """
        Scenario: Active Relative Humidity Exhaust Fan Solenoid Control (相对湿度排气风扇电磁阀主动控制)
        Given an active greenhouse growing zone under "stock.location" (库存库位)
        When indoor relative humidity sensors register a humidity value of "75.0%" (当室内相对湿度传感器记录湿度值为75.0%)
        Then the system must trigger an active PLC relay command "open_ventilation_valve" (打开通风阀) to start exhaust fans and open louver panels
        And log the actuator action on the monitoring feed under "agri.greenhouse.plc" (温室PLC模型)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an active greenhouse growing zone under "stock.location" (库存库位)',
            'When indoor relative humidity sensors register a humidity value of "75.0%" (当室内相对湿度传感器记录湿度值为75.0%)',
            'Then the system must trigger an active PLC relay command "open_ventilation_valve" (打开通风阀) to start exhaust fans and open louver panels',
            'And log the actuator action on the monitoring feed under "agri.greenhouse.plc" (温室PLC模型)'
        ])

    def test_02_greenhouse_temperature_misting_solenoid_interlock(self):
        """
        Scenario: Greenhouse Temperature Misting Solenoid Interlock (温室温度喷雾降温电磁阀联锁)
        Given a growing zone inside the smart greenhouse
        When ambient temperature sensors register an indoor temperature of "32.5°C" (当环境温度传感器记录室内温度为32.5°C)
        Then the system must trigger an active PLC signal "activate_cooling_misting" (激活喷雾降温) to open the high-pressure misting line water solenoids
        And set the cooling system solenoid valve state on the PLC monitor to "on" (开启) until temperature drops below "26.0°C"
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a growing zone inside the smart greenhouse',
            'When ambient temperature sensors register an indoor temperature of "32.5°C" (当环境温度传感器记录室内温度为32.5°C)',
            'Then the system must trigger an active PLC signal "activate_cooling_misting" (激活喷雾降温) to open the high-pressure misting line water solenoids',
            'And set the cooling system solenoid valve state on the PLC monitor to "on" (开启) until temperature drops below "26.0°C"'
        ])

    def test_03_greenhouse_sensor_offline_failsafe_safeguard(self):
        """
        Scenario: Greenhouse Sensor Offline Fail-Safe Safeguard (温室传感器离线安全保护装置)
        Given a smart greenhouse actively logging real-time telemetry under "agri.greenhouse.plc" (温室PLC模型)
        When the indoor temperature and humidity sensors fail to report telemetry for over "15 minutes" (当室内温湿度传感器超过15分钟未上报遥测数据)
        Then the greenhouse controller must switch to an offline fail-safe duty-cycle, locking exhaust fan louver vents at a fixed safe state of "50.0% open" (将排气扇百叶通风阀锁死在50.0%开启的固定安全状态)
        And write a critical alert warning "Sensory Lost: Switch to Fail-Safe Mode" (温室传感器离线：切换到安全备份模式) into the system log
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a smart greenhouse actively logging real-time telemetry under "agri.greenhouse.plc" (温室PLC模型)',
            'When the indoor temperature and humidity sensors fail to report telemetry for over "15 minutes" (当室内温湿度传感器超过15分钟未上报遥测数据)',
            'Then the greenhouse controller must switch to an offline fail-safe duty-cycle, locking exhaust fan louver vents at a fixed safe state of "50.0% open" (将排气扇百叶通风阀锁死在50.0%开启的固定安全状态)',
            'And write a critical alert warning "Sensory Lost: Switch to Fail-Safe Mode" (温室传感器离线：切换到安全备份模式) into the system log'
        ])

    def test_04_greenhouse_soil_moisture_tension_solenoid_smart_bypass(self):
        """
        Scenario: Greenhouse Soil Moisture Tension Solenoid Smart Bypass (温室土壤水分张力电磁阀智能旁路)
        Given a scheduled irrigation workorder "mrp.workorder" (制造工单) to open watering solenoids for "15 minutes"
        When the greenhouse soil water potential sensors log a soil tension value of "-12.0 kPa" (当温室土壤水分张力传感器记录土壤张力值为-12.0 kPa，表明高水分饱和)
        Then the system must automatically bypass and block the watering solenoids from opening to prevent root mold and waterlogging
        And write an intervention warning "Irrigation Bypassed: Soil water potential indicates saturation" (灌溉旁路：土壤水分张力指示饱和) on the workorder record
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a scheduled irrigation workorder "mrp.workorder" (制造工单) to open watering solenoids for "15 minutes"',
            'When the greenhouse soil water potential sensors log a soil tension value of "-12.0 kPa" (当温室土壤水分张力传感器记录土壤张力值为-12.0 kPa，表明高水分饱和)',
            'Then the system must automatically bypass and block the watering solenoids from opening to prevent root mold and waterlogging',
            'And write an intervention warning "Irrigation Bypassed: Soil water potential indicates saturation" (灌溉旁路：土壤水分张力指示饱和) on the workorder record'
        ])

    def test_05_greenhouse_carbon_dioxide_concentration_valve(self):
        """
        Scenario: Greenhouse Carbon Dioxide Concentration Valve (温室二氧化碳浓度电磁阀控制)
        Given enclosed greenhouse zone during active LED lighting cycles
        When the carbon dioxide sensors register CO2 levels dropping below "450.0 PPM" (当二氧化碳传感器记录CO2浓度跌破450.0 PPM)
        Then the system must trigger an active PLC relay command "open_co2_valve" (打开二氧化碳阀门) to dose CO2 into the growing zone
        And automatically close the CO2 dosing valve when sensor readings reach "1000.0 PPM" (并在传感器读数达到1000.0 PPM时自动关闭二氧化碳投加阀)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given enclosed greenhouse zone during active LED lighting cycles',
            'When the carbon dioxide sensors register CO2 levels dropping below "450.0 PPM" (当二氧化碳传感器记录CO2浓度跌破450.0 PPM)',
            'Then the system must trigger an active PLC relay command "open_co2_valve" (打开二氧化碳阀门) to dose CO2 into the growing zone',
            'And automatically close the CO2 dosing valve when sensor readings reach "1000.0 PPM" (并在传感器读数达到1000.0 PPM时自动关闭二氧化碳投加阀)'
        ])

    def test_06_misting_highpressure_pump_failure_interlock(self):
        """
        Scenario: Misting High-Pressure Pump Failure Interlock (高压喷雾水泵异常故障保护联锁)
        Given an active greenhouse cooling system under "agri.greenhouse.plc" (温室PLC模型)
        When misting water solenoids are "on" (开启) but the water pressure sensor "iiot.device" (智能物联网设备) registers pump head pressure below "10.0 Bar" (检测到泵出口压力低于10.0巴，预示低压或泄露风险)
        Then the system must trigger an active PLC relay command to instantly shut off the high-pressure misting pump
        And transition the greenhouse controller status to "pump_failed" (水泵故障) while raising an urgent maintenance alert
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an active greenhouse cooling system under "agri.greenhouse.plc" (温室PLC模型)',
            'When misting water solenoids are "on" (开启) but the water pressure sensor "iiot.device" (智能物联网设备) registers pump head pressure below "10.0 Bar" (检测到泵出口压力低于10.0巴，预示低压或泄露风险)',
            'Then the system must trigger an active PLC relay command to instantly shut off the high-pressure misting pump',
            'And transition the greenhouse controller status to "pump_failed" (水泵故障) while raising an urgent maintenance alert'
        ])
