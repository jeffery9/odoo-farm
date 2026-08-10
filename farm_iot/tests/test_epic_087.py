# -*- coding: utf-8 -*-
from odoo.addons.farm_core.tests.bdd_base import BddTransactionCase
from odoo.exceptions import UserError, ValidationError

class TestEpic087(BddTransactionCase):
    """ BDD Test Suite for Epic 087: Epic 087 Integrated Agricultural IoT Platform (集成农业物联网平台) """

    def setUp(self):
        super(TestEpic087, self).setUp()

    def test_01_sensor_calibration_offsets(self):
        """
        Scenario: Sensor calibration offsets (传感器物理量标定偏差调节)
        Given active on-site weather sensors registered under "agri.iot.sensor" (物联网传感器) in state "active" (激活)
        When telemetry values are submitted via "action_receive_telemetry" (接收遥测数据)
        Then the system applies calibration offset adjustments of "+1.5%" to "humidity_reading" (湿度读数)
        And writes the calibrated readings to the database record
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given active on-site weather sensors registered under "agri.iot.sensor" (物联网传感器) in state "active" (激活)',
            'When telemetry values are submitted via "action_receive_telemetry" (接收遥测数据)',
            'Then the system applies calibration offset adjustments of "+1.5%" to "humidity_reading" (湿度读数)',
            'And writes the calibrated readings to the database record'
        ])

    def test_02_automated_device_control_and_relative_humidity_exhaust_fans(self):
        """
        Scenario: Automated device control and relative humidity exhaust fans (温室相对湿度超标自动开启排风机)
        Given relative humidity readings inside Greenhouse 2 "stock.location" (库存位置) in "active" (激活) state
        When sensor readings exceed "70.0%" threshold
        Then the system issues active PLC relay signals starting exhaust fan motors and opening ventilation louvers via "action_trigger_actuator" (触发执行器)
        And records status "on" (开启) on the ventilator record
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given relative humidity readings inside Greenhouse 2 "stock.location" (库存位置) in "active" (激活) state',
            'When sensor readings exceed "70.0%" threshold',
            'Then the system issues active PLC relay signals starting exhaust fan motors and opening ventilation louvers via "action_trigger_actuator" (触发执行器)',
            'And records status "on" (开启) on the ventilator record'
        ])

    def test_03_iot_sensor_connectivity_failure_and_safe_mode_fallback(self):
        """
        Scenario: IoT sensor connectivity failure and Safe Mode fallback (物联网传感器离线自动切入安全模式)
        Given an automated soil watering cycle "mrp.workorder" (生产工单) in status "ready" (准备就绪)
        When soil sensors fail to report for "15.0" minutes resulting in null readings
        Then the system switches irrigation controllers to safe fixed-rate duty-cycles "action_activate_safe_mode" (启动安全运行模式)
        And logs a warning on the system telemetry panel to avoid soil drying
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an automated soil watering cycle "mrp.workorder" (生产工单) in status "ready" (准备就绪)',
            'When soil sensors fail to report for "15.0" minutes resulting in null readings',
            'Then the system switches irrigation controllers to safe fixed-rate duty-cycles "action_activate_safe_mode" (启动安全运行模式)',
            'And logs a warning on the system telemetry panel to avoid soil drying'
        ])

    def test_04_realtime_tractor_vra_nozzles_on_zone_transitions_gps(self):
        """
        Scenario: Real-time tractor VRA nozzles on zone transitions (拖拉机变量喷头根据GPS坐标实时控制)
        Given GPS coordinates of a VRA sprayer tractor "maintenance.equipment" (设备/变量喷药车) executing a task
        When the tractor transitions from "High-SOM" (高有机质区) zone to "Low-SOM" (低有机质区) zone
        Then the system sends PLC nozzle flow adjustment commands of "-15.0%" matching the prescription maps via "action_send_plc_command" (发送PLC指令)
        And updates the active workorder "mrp.workorder" (生产工单) chemical consumption records
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given GPS coordinates of a VRA sprayer tractor "maintenance.equipment" (设备/变量喷药车) executing a task',
            'When the tractor transitions from "High-SOM" (高有机质区) zone to "Low-SOM" (低有机质区) zone',
            'Then the system sends PLC nozzle flow adjustment commands of "-15.0%" matching the prescription maps via "action_send_plc_command" (发送PLC指令)',
            'And updates the active workorder "mrp.workorder" (生产工单) chemical consumption records'
        ])

    def test_05_collar_lowbattery_alerts(self):
        """
        Scenario: Collar low-battery alerts (定位项圈低电量自动维护警报)
        Given active battery readings on a pasture tracking collar "agri.iot.sensor" (物联网传感器) in "active" (激活) status
        When the battery level drops below "20.0%"
        Then the system automatically creates a maintenance order "maintenance.equipment" (设备维护工单)
        And sets priority to high, prompting urgent technician replacement
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given active battery readings on a pasture tracking collar "agri.iot.sensor" (物联网传感器) in "active" (激活) status',
            'When the battery level drops below "20.0%"',
            'Then the system automatically creates a maintenance order "maintenance.equipment" (设备维护工单)',
            'And sets priority to high, prompting urgent technician replacement'
        ])

    def test_06_vra_nozzle_controller_offline_mcp_server_online_checking_fallback(self):
        """
        Scenario: VRA Nozzle Controller Offline MCP Server Online Checking Fallback
        Given a variables-rate sprayer product "product.template" (产品模板) linked to an active nozzle under "agri.iot.sensor" (物联网传感器) in state "active" (激活)
        When the PLC nozzle controller goes offline during a spraying mission "mrp.workorder" (作业任务) "WO-SPRAY-06"
        Then the platform triggers the MCP server online checking fallback (MCP服务在线检测容灾) to ping the backup field gateway
        And updates the sensor status to "warning" (警告) without interrupting the physical actuator operation
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a variables-rate sprayer product "product.template" (产品模板) linked to an active nozzle under "agri.iot.sensor" (物联网传感器) in state "active" (激活)',
            'When the PLC nozzle controller goes offline during a spraying mission "mrp.workorder" (作业任务) "WO-SPRAY-06"',
            'Then the platform triggers the MCP server online checking fallback (MCP服务在线检测容灾) to ping the backup field gateway',
            'And updates the sensor status to "warning" (警告) without interrupting the physical actuator operation'
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
