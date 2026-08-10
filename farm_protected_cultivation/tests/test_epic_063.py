# -*- coding: utf-8 -*-
from odoo.addons.farm_core.tests.bdd_base import BddTransactionCase
from odoo.exceptions import UserError, ValidationError

class TestEpic063(BddTransactionCase):
    """ BDD Test Suite for Epic 063: Epic 063 CEA & Vertical Farming (受控环境农业与垂直农业) """

    def setUp(self):
        super(TestEpic063, self).setUp()

    def test_01_led_spectral_light_ratio_plc_control_ledplc(self):
        """
        Scenario: LED Spectral Light Ratio PLC Control (LED光谱比例PLC自控调节)
        Given an active CEA environment monitoring record under agri.cea.environment (受控环境环境监测数据) for stock.location (库存位置) "VERTICAL-CHAMBER-10"
        And the crop variety growth stage is currently registered as "vegetative (营养生长阶)"
        When the crop status transitions to "flowering (开花结实期)"
        Then the system must trigger a PLC relay command of model agri.cea.plc.command (PLC自控指令)
        And adjust the LED spectrum output ratio (光谱输出比例) of Red:Blue (红:蓝) from "1:1" to "4:1"
        And log this action state as "executed (已执行)" with a timestamp in the sensor logs
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an active CEA environment monitoring record under agri.cea.environment (受控环境环境监测数据) for stock.location (库存位置) "VERTICAL-CHAMBER-10"',
            'And the crop variety growth stage is currently registered as "vegetative (营养生长阶)"',
            'When the crop status transitions to "flowering (开花结实期)"',
            'Then the system must trigger a PLC relay command of model agri.cea.plc.command (PLC自控指令)',
            'And adjust the LED spectrum output ratio (光谱输出比例) of Red:Blue (红:蓝) from "1:1" to "4:1"',
            'And log this action state as "executed (已执行)" with a timestamp in the sensor logs'
        ])

    def test_02_automated_hvac_circulation_fan_ventilation_trigger_hvac(self):
        """
        Scenario: Automated HVAC Circulation Fan Ventilation Trigger (自动HVAC循环风机排风触发)
        Given an intensive CEA indoor vertical farm location of model stock.location (库存位置)
        When relative humidity sensors (相对湿度传感器) log a humidity level of 78.5%, exceeding the critical threshold of 75.0%
        Then the system must immediately dispatch an active PLC signal of model agri.cea.plc.command (PLC自控指令)
        And power on the secondary HVAC air circulation exhaust fans (二级HVAC空气循环排风扇)
        And log an environmental event on agri.cea.environment (受控环境环境监测数据) with code "HUMIDITY_HIGH_TRIGGER (高湿度触发)"
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an intensive CEA indoor vertical farm location of model stock.location (库存位置)',
            'When relative humidity sensors (相对湿度传感器) log a humidity level of 78.5%, exceeding the critical threshold of 75.0%',
            'Then the system must immediately dispatch an active PLC signal of model agri.cea.plc.command (PLC自控指令)',
            'And power on the secondary HVAC air circulation exhaust fans (二级HVAC空气循环排风扇)',
            'And log an environmental event on agri.cea.environment (受控环境环境监测数据) with code "HUMIDITY_HIGH_TRIGGER (高湿度触发)"'
        ])

    def test_03_co2_injection_safety_interlock(self):
        """
        Scenario: CO2 Injection Safety Interlock (二氧化碳注入安全连锁自控)
        Given a closed vertical farming chamber of model stock.location (库存位置) "CHAMBER-05" with active LED lighting cycles
        When indoor carbon dioxide sensors (二氧化碳浓度传感器) register a CO2 level of 350.0 PPM, dropping below the safety floor of 400.0 PPM
        Then the system must trigger an active PLC command to open the carbon dioxide solenoid dosing valve (二氧化碳电磁计量阀)
        And keep the solenoid valve open until CO2 sensors log concentration reaching 1200.0 PPM
        And automatically execute a "close_valve (关闭电磁阀)" command of model agri.cea.plc.command (PLC自控指令) once the ceiling threshold is satisfied
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a closed vertical farming chamber of model stock.location (库存位置) "CHAMBER-05" with active LED lighting cycles',
            'When indoor carbon dioxide sensors (二氧化碳浓度传感器) register a CO2 level of 350.0 PPM, dropping below the safety floor of 400.0 PPM',
            'Then the system must trigger an active PLC command to open the carbon dioxide solenoid dosing valve (二氧化碳电磁计量阀)',
            'And keep the solenoid valve open until CO2 sensors log concentration reaching 1200.0 PPM',
            'And automatically execute a "close_valve (关闭电磁阀)" command of model agri.cea.plc.command (PLC自控指令) once the ceiling threshold is satisfied'
        ])

    def test_04_cea_temperature_sensor_offline_fallback_cea(self):
        """
        Scenario: CEA Temperature Sensor Offline Fallback (CEA温度传感器离线安全容灾保护)
        Given an active growing zone of model stock.location (库存位置) running real-time climate monitoring under agri.cea.environment (受控环境环境监测数据)
        When the room temperature sensor (室温传感器) fails to report or stream data to Odoo for over 15 minutes
        Then the system must transition the sensory status to "offline_failed (传感器故障离线)"
        And automatically trigger a safety backup cooling water pump PLC command (安全备用冷水泵PLC指令) at a constant 50.0% duty-cycle
        And log a critical sensor alert record of model agri.cea.sensor.alert (传感器警报日志) in the database with state "active (活动中)"
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an active growing zone of model stock.location (库存位置) running real-time climate monitoring under agri.cea.environment (受控环境环境监测数据)',
            'When the room temperature sensor (室温传感器) fails to report or stream data to Odoo for over 15 minutes',
            'Then the system must transition the sensory status to "offline_failed (传感器故障离线)"',
            'And automatically trigger a safety backup cooling water pump PLC command (安全备用冷水泵PLC指令) at a constant 50.0% duty-cycle',
            'And log a critical sensor alert record of model agri.cea.sensor.alert (传感器警报日志) in the database with state "active (活动中)"'
        ])

    def test_05_nutrient_film_technique_water_flow_blockage_gating_nft(self):
        """
        Scenario: Nutrient Film Technique Water Flow Blockage Gating (NFT营养液膜流速受阻安全备用)
        Given a Nutrient Film Technique (NFT) hydroponic channel system (NFT水培营养液管道循环系统) registered under stock.location (库存位置)
        When water flow sensors (水流速传感器) log a flow rate of 1.2 Liters/minute (升/分钟), dropping below the safety floor of 1.5 Liters/minute
        Then the system must instantly send an active PLC signal to power on the redundant backup water pump relay (冗余备用泵继电器)
        And raise an urgent maintenance task of model project.task (项目任务) on the operator dashboard with priority "3 (非常紧急)"
        And throw a ValidationError (验证错误): "NFT flow blockage - Redundant pump activated (NFT营养液管道流速阻塞，已启动备用泵)" on the active monitoring terminal
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a Nutrient Film Technique (NFT) hydroponic channel system (NFT水培营养液管道循环系统) registered under stock.location (库存位置)',
            'When water flow sensors (水流速传感器) log a flow rate of 1.2 Liters/minute (升/分钟), dropping below the safety floor of 1.5 Liters/minute',
            'Then the system must instantly send an active PLC signal to power on the redundant backup water pump relay (冗余备用泵继电器)',
            'And raise an urgent maintenance task of model project.task (项目任务) on the operator dashboard with priority "3 (非常紧急)"',
            'And throw a ValidationError (验证错误): "NFT flow blockage - Redundant pump activated (NFT营养液管道流速阻塞，已启动备用泵)" on the active monitoring terminal'
        ])

    def test_06_robotic_swarm_nutrient_sensor_drift_calibration_gate(self):
        """
        Scenario: Robotic Swarm Nutrient Sensor Drift Calibration Gate (机器人蜂群养分传感器漂移自动校准门禁)
        Given an active vertical farm robotic monitoring device (受控环境智能监测设备) of model iiot.device (物联设备) executing a nutrient feeding mission (养分饲喂任务) "mrp.workorder" (作业任务)
        When the pH/EC sensors log a calibration drift (传感器校准漂移) exceeding 5.0% in stock.location (库存位置)
        Then the system must automatically flag a sensor failure warning (传感器故障警告)
        And raise a ValidationError (验证错误): "Sensor drift exceeds tolerance limit (传感器温漂超出公差限制)" and pause the mission "mrp.workorder" (作业任务) until a certified self-calibration sequence (自动校准序列) is triggered and completed
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an active vertical farm robotic monitoring device (受控环境智能监测设备) of model iiot.device (物联设备) executing a nutrient feeding mission (养分饲喂任务) "mrp.workorder" (作业任务)',
            'When the pH/EC sensors log a calibration drift (传感器校准漂移) exceeding 5.0% in stock.location (库存位置)',
            'Then the system must automatically flag a sensor failure warning (传感器故障警告)',
            'And raise a ValidationError (验证错误): "Sensor drift exceeds tolerance limit (传感器温漂超出公差限制)" and pause the mission "mrp.workorder" (作业任务) until a certified self-calibration sequence (自动校准序列) is triggered and completed'
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
