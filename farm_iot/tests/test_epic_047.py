# -*- coding: utf-8 -*-
from odoo.addons.farm_core.tests.bdd_base import BddTransactionCase
from odoo.exceptions import UserError, ValidationError

class TestEpic047(BddTransactionCase):
    """ BDD Test Suite for Epic 047: Epic 047 Edge Orchestration & Active Control """

    def setUp(self):
        super(TestEpic047, self).setUp()

    def test_01_active_greenhouse_ventilation_valve_actuator_control(self):
        """
        Scenario: Active Greenhouse Ventilation Valve Actuator Control
        Given an active greenhouse climate controller under model "mrp.workorder" is monitoring "GREENHOUSE-ZONE-A"
        And temperature sensors log ambient temperature greater than 28.0°C (大棚环境温度大于 28.0 摄氏度)
        When the system triggers an active PLC command in model "agri.edge.plc.command" to adjust ventilation
        Then the edge actuator must open the exhaust ventilation valves to 100.0% open state
        And record a success confirmation code in the Level 2 "iiot.command.log" registry
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an active greenhouse climate controller under model "mrp.workorder" is monitoring "GREENHOUSE-ZONE-A"',
            'And temperature sensors log ambient temperature greater than 28.0°C (大棚环境温度大于 28.0 摄氏度)',
            'When the system triggers an active PLC command in model "agri.edge.plc.command" to adjust ventilation',
            'Then the edge actuator must open the exhaust ventilation valves to 100.0% open state',
            'And record a success confirmation code in the Level 2 "iiot.command.log" registry'
        ])

    def test_02_water_pump_pressure_dropping_interlock(self):
        """
        Scenario: Water Pump Pressure Dropping Interlock
        Given a main irrigation water pump line monitored under model "mrp.workorder"
        And the active watering line pressure drops below the minimum limit of 1.5 Bar (灌溉水泵水压低于 1.5 巴)
        When the edge controller executes the active safety interlock algorithm
        Then the system must instantly trigger a physical relay to activate the backup water pump
        And log an emergency interlock event "PUMP_LOW_PRESSURE_BYPASS" in "iiot.command.log"
        And automatically dispatch a high-priority equipment repair task in Odoo maintenance
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a main irrigation water pump line monitored under model "mrp.workorder"',
            'And the active watering line pressure drops below the minimum limit of 1.5 Bar (灌溉水泵水压低于 1.5 巴)',
            'When the edge controller executes the active safety interlock algorithm',
            'Then the system must instantly trigger a physical relay to activate the backup water pump',
            'And log an emergency interlock event "PUMP_LOW_PRESSURE_BYPASS" in "iiot.command.log"',
            'And automatically dispatch a high-priority equipment repair task in Odoo maintenance'
        ])

    def test_03_solenoid_dosing_valve_plc_pulse_gating(self):
        """
        Scenario: Solenoid Dosing Valve PLC Pulse Gating
        Given a liquid fertilizer dosing workorder in progress under model "mrp.workorder"
        And the active nutrient solution electrical conductivity (EC) sensor logs drop below 1.8 mS/cm (营养液电导率 EC 低于 1.8 mS/cm)
        When the PLC controller receives the low EC sensory threshold alert
        Then the system must compile and send a high-frequency dosing pulse command under "agri.edge.plc.command"
        And inject concentrated nutrient solution via solenoid pulses until EC stabilizes back to the 2.0 mS/cm setpoint
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a liquid fertilizer dosing workorder in progress under model "mrp.workorder"',
            'And the active nutrient solution electrical conductivity (EC) sensor logs drop below 1.8 mS/cm (营养液电导率 EC 低于 1.8 mS/cm)',
            'When the PLC controller receives the low EC sensory threshold alert',
            'Then the system must compile and send a high-frequency dosing pulse command under "agri.edge.plc.command"',
            'And inject concentrated nutrient solution via solenoid pulses until EC stabilizes back to the 2.0 mS/cm setpoint'
        ])

    def test_04_edge_controller_offline_safeguard(self):
        """
        Scenario: Edge Controller Offline Safeguard
        Given an active edge climate PLC controller synchronized with the Odoo "agri_iot" hub
        When the local Ethernet network connection is lost for greater than 10 minutes (边缘端通信离线超过 10 分钟)
        Then the edge hardware must automatically transition into its localized "autonomous fail-safe" safeguard mode (安全运行保障模式)
        And execute basic trickle scheduling locally based on cached agronomic parameters without core server connectivity
        And flag its heartbeat status as "sensory_failed" in Odoo once reconnection is established
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an active edge climate PLC controller synchronized with the Odoo "agri_iot" hub',
            'When the local Ethernet network connection is lost for greater than 10 minutes (边缘端通信离线超过 10 分钟)',
            'Then the edge hardware must automatically transition into its localized "autonomous fail-safe" safeguard mode (安全运行保障模式)',
            'And execute basic trickle scheduling locally based on cached agronomic parameters without core server connectivity',
            'And flag its heartbeat status as "sensory_failed" in Odoo once reconnection is established'
        ])

    def test_05_active_fan_exhaust_speed_scaling(self):
        """
        Scenario: Active Fan Exhaust Speed Scaling
        Given a humidity-sensitive curing and drying room monitored under model "mrp.workorder"
        And the current air sensory relative humidity logs exceed the high-boundary threshold of 70.0% (相对湿度超过 70.0%)
        When the speed scaling trigger algorithm executes under "agri.edge.plc.command"
        Then the system must scale the exhaust fan operating speeds from 30.0% to 100.0%
        And issue precise analog voltage speed commands (e.g., ramping output to 10.0V) to the physical variable frequency drive (VFD)
        And log the operational telemetry adjustment in the drying campaign chatter
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a humidity-sensitive curing and drying room monitored under model "mrp.workorder"',
            'And the current air sensory relative humidity logs exceed the high-boundary threshold of 70.0% (相对湿度超过 70.0%)',
            'When the speed scaling trigger algorithm executes under "agri.edge.plc.command"',
            'Then the system must scale the exhaust fan operating speeds from 30.0% to 100.0%',
            'And issue precise analog voltage speed commands (e.g., ramping output to 10.0V) to the physical variable frequency drive (VFD)',
            'And log the operational telemetry adjustment in the drying campaign chatter'
        ])

    def test_06_concurrency_command_row_lock_on_actuator_state_changes(self):
        """
        Scenario: Concurrency Command Row Lock on Actuator State Changes
        Given multiple edge sensory telemetry alerts received by the Odoo greenhouse controller
        And an active fertilization dosing mission under model "mrp.workorder" (作业任务)
        When the automation system generates concurrent PLC actuator commands under model "agri.edge.plc.command" (PLC控制指令)
        Then the database must acquire a row-level lock on the active actuator record to ensure serialized command execution (串行指令执行)
        And discard any conflicting out-of-order pulse commands to prevent actuator valve wear and chemical dosing contamination
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given multiple edge sensory telemetry alerts received by the Odoo greenhouse controller',
            'And an active fertilization dosing mission under model "mrp.workorder" (作业任务)',
            'When the automation system generates concurrent PLC actuator commands under model "agri.edge.plc.command" (PLC控制指令)',
            'Then the database must acquire a row-level lock on the active actuator record to ensure serialized command execution (串行指令执行)',
            'And discard any conflicting out-of-order pulse commands to prevent actuator valve wear and chemical dosing contamination'
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
