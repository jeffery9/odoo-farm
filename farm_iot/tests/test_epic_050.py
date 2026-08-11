# -*- coding: utf-8 -*-
from odoo.addons.farm_core.tests.bdd_base import BddTransactionCase
from odoo.exceptions import UserError, ValidationError

class TestEpic050(BddTransactionCase):
    """ BDD Test Suite for Epic 050: Epic 050 Intelligent Irrigation Management """

    def setUp(self):
        super(TestEpic050, self).setUp()

    def test_01_soil_moisture_tension_solenoid_activation(self):
        """
        Scenario: Soil Moisture Tension Solenoid Activation
        Given an intelligent irrigation zone "ZONE-ORCHARD-03" under model "stock.location"
        And a physical solenoid valve configured in "agri.irrigation.valve" with code "VALVE-SOLENOID-03"
        And soil moisture sensors register water potential dropping below -80.0 kPa (土壤张力低于 -80 kPa 缺水严重)
        When the system's smart irrigation engine executes the water-demand evaluation
        Then the system must send an active PLC command to set the state of "VALVE-SOLENOID-03" to "open"
        And log an automatic irrigation execution log with starting parameters in Odoo
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an intelligent irrigation zone "ZONE-ORCHARD-03" under model "stock.location"',
            'And a physical solenoid valve configured in "agri.irrigation.valve" with code "VALVE-SOLENOID-03"',
            'And soil moisture sensors register water potential dropping below -80.0 kPa (土壤张力低于 -80 kPa 缺水严重)',
            "When the system's smart irrigation engine executes the water-demand evaluation",
            'Then the system must send an active PLC command to set the state of "VALVE-SOLENOID-03" to "open"',
            'And log an automatic irrigation execution log with starting parameters in Odoo'
        ])

    def test_02_irrigation_runtime_flow_rate_check(self):
        """
        Scenario: Irrigation Run-Time Flow Rate Check
        Given an active watering workorder executing on "VALVE-SOLENOID-03"
        When the inline digital flow sensor logs a real-time flow rate below 50.0% of the nominal target flow rate (水流流量低于目标值 50.0% 怀疑堵塞或漏水)
        Then the system must instantly trigger an emergency valve shutdown command setting "VALVE-SOLENOID-03" to "closed"
        And raise a plumbing alert "IRRIGATION_FLOW_RATE_ANOMALY" (灌溉流速异常报警) in Odoo
        And transition the watering workorder state to "paused" to protect the pump from dry running
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an active watering workorder executing on "VALVE-SOLENOID-03"',
            'When the inline digital flow sensor logs a real-time flow rate below 50.0% of the nominal target flow rate (水流流量低于目标值 50.0% 怀疑堵塞或漏水)',
            'Then the system must instantly trigger an emergency valve shutdown command setting "VALVE-SOLENOID-03" to "closed"',
            'And raise a plumbing alert "IRRIGATION_FLOW_RATE_ANOMALY" (灌溉流速异常报警) in Odoo',
            'And transition the watering workorder state to "paused" to protect the pump from dry running'
        ])

    def test_03_solenoid_offline_local_trickle_fallback(self):
        """
        Scenario: Solenoid Offline Local Trickle Fallback
        Given a physical solenoid valve "VALVE-SOLENOID-03" in an active watering cycle
        When the edge controller loses communication network connectivity with the central Odoo server (智能电磁阀离线)
        Then the local edge firmware must execute a safety watchdog timeout limit of 20 minutes (离线本地守护限制 20 分钟)
        And automatically shut off the solenoid valve "VALVE-SOLENOID-03" after 20 minutes to prevent soil saturation and root rot
        And log an offline interruption alert "OFFLINE_WATCHDOG_SHUTDOWN" upon next network synchronization
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a physical solenoid valve "VALVE-SOLENOID-03" in an active watering cycle',
            'When the edge controller loses communication network connectivity with the central Odoo server (智能电磁阀离线)',
            'Then the local edge firmware must execute a safety watchdog timeout limit of 20 minutes (离线本地守护限制 20 分钟)',
            'And automatically shut off the solenoid valve "VALVE-SOLENOID-03" after 20 minutes to prevent soil saturation and root rot',
            'And log an offline interruption alert "OFFLINE_WATCHDOG_SHUTDOWN" upon next network synchronization'
        ])

    def test_04_rain_forecast_solenoid_smart_bypass(self):
        """
        Scenario: Rain Forecast Solenoid Smart Bypass
        Given planned daily irrigation orders scheduled for organic parcel location "PARCEL-WEST-02"
        And weather forecast APIs predict cumulative rainfall greater than 25.0 mm within the next 12 hours (降雨量预测大于 25.0mm)
        When the smart irrigation planning script runs at 06:00 AM
        Then the system must automatically execute a "Smart Bypass" action (智能降雨规避)
        And cancel the planned solenoid valve activation orders for that parcel today
        And write a water conservation ledger record documenting the estimated liters of water resource saved
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given planned daily irrigation orders scheduled for organic parcel location "PARCEL-WEST-02"',
            'And weather forecast APIs predict cumulative rainfall greater than 25.0 mm within the next 12 hours (降雨量预测大于 25.0mm)',
            'When the smart irrigation planning script runs at 06:00 AM',
            'Then the system must automatically execute a "Smart Bypass" action (智能降雨规避)',
            'And cancel the planned solenoid valve activation orders for that parcel today',
            'And write a water conservation ledger record documenting the estimated liters of water resource saved'
        ])

    def test_05_multizone_irrigation_concurrency_scheduling(self):
        """
        Scenario: Multi-Zone Irrigation Concurrency Scheduling
        Given a commercial farm with multiple irrigation zones and a limited main water pump capacity
        And the main water pump can support a maximum concurrent flow of 2 active zones
        When a supervisor schedules irrigation across 5 distinct zones under model "agri.irrigation.valve"
        Then the system's scheduling algorithm must calculate non-overlapping run-time blocks (多分区非重叠轮灌调度)
        And restrict active solenoid valve operations to a maximum concurrency of 2 at any single timestamp
        And automatically log the multi-zone execution schedule in Odoo to maintain optimal operating water pressure
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a commercial farm with multiple irrigation zones and a limited main water pump capacity',
            'And the main water pump can support a maximum concurrent flow of 2 active zones',
            'When a supervisor schedules irrigation across 5 distinct zones under model "agri.irrigation.valve"',
            "Then the system's scheduling algorithm must calculate non-overlapping run-time blocks (多分区非重叠轮灌调度)",
            'And restrict active solenoid valve operations to a maximum concurrency of 2 at any single timestamp',
            'And automatically log the multi-zone execution schedule in Odoo to maintain optimal operating water pressure'
        ])

    def test_06_main_water_pump_capacity_transaction_lock_on_solenoid_opening(self):
        """
        Scenario: Main Water Pump Capacity Transaction Lock on Solenoid Opening
        Given a set of intelligent irrigation valves configured in "agri.irrigation.valve" (智能电磁阀)
        When an operator or automated script triggers the opening command (打开指令) for valve "VALVE-SOLENOID-03"
        Then the system must execute a SELECT FOR UPDATE lock on the main water pump location record
        And verify that opening this valve does not exceed the maximum concurrent flow capacity of the pump
        And raise a ValidationError with code "PUMP_CAPACITY_EXCEEDED" (主水泵流量负载超限，操作已被拒绝并挂起) if the pump is already operating at maximum capacity
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a set of intelligent irrigation valves configured in "agri.irrigation.valve" (智能电磁阀)',
            'When an operator or automated script triggers the opening command (打开指令) for valve "VALVE-SOLENOID-03"',
            'Then the system must execute a SELECT FOR UPDATE lock on the main water pump location record',
            'And verify that opening this valve does not exceed the maximum concurrent flow capacity of the pump',
            'And raise a ValidationError with code "PUMP_CAPACITY_EXCEEDED" (主水泵流量负载超限，操作已被拒绝并挂起) if the pump is already operating at maximum capacity'
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
