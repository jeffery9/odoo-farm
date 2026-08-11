# -*- coding: utf-8 -*-
from odoo.addons.farm_core.tests.bdd_base import BddTransactionCase
from odoo.exceptions import UserError, ValidationError

class TestEpic111(BddTransactionCase):
    """ BDD Test Suite for Epic 111: Epic 111 VRA Equipment Smart Coordination (VRA设备智能协同) """

    def setUp(self):
        super(TestEpic111, self).setUp()

    def test_01_tractor_autonomous_gps_coordinate_flight_plan_upload_gps(self):
        """
        Scenario: Tractor Autonomous GPS Coordinate Flight Plan Upload (拖拉机自主GPS坐标航线图上传)
        Given a core Odoo mission under "mrp.workorder" (作业任务模型) accessed via "agri.vra.coordination" (VRA设备智能协同模型)
        And a GPS flight plan file "flight_plan_path_coordinates" is uploaded (且GPS航线文件字段已上传)
        When the dispatcher executes compiling path instructions (执行编译路径指令) as a critical system action
        Then the system must validate coordinates against parcel boundaries (验证坐标是否超出地块边界) under "stock.location" (库存位置模型)
        And update coordinate status to "mapped" (已映射状态)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a core Odoo mission under "mrp.workorder" (作业任务模型) accessed via "agri.vra.coordination" (VRA设备智能协同模型)',
            'And a GPS flight plan file "flight_plan_path_coordinates" is uploaded (且GPS航线文件字段已上传)',
            'When the dispatcher executes compiling path instructions (执行编译路径指令) as a critical system action',
            'Then the system must validate coordinates against parcel boundaries (验证坐标是否超出地块边界) under "stock.location" (库存位置模型)',
            'And update coordinate status to "mapped" (已映射状态)'
        ])

    def test_02_realtime_tractor_sprayer_vra_valve_adjustment_vra(self):
        """
        Scenario: Real-time Tractor Sprayer VRA Valve Adjustment (拖拉机喷雾器实时VRA电磁阀流量调节)
        Given an active variable rate sprayer tractor mission under "mrp.workorder" (作业任务模型) linked to "agri.vra.coordination" (VRA设备智能协同模型)
        And the tractor transitions from high soil organic matter zone to low soil organic matter zone (且拖拉机从高有机质区域过渡到低有机质区域)
        When the controller evaluates soil sensor feedback (评估土壤传感器反馈) as a critical system action
        Then the system must issue flow adjustment commands (发出流量调节指令) to decrease "valve_opening_percentage" by 15.0%
        And update the valve command state to "adjusted" (已调节状态)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an active variable rate sprayer tractor mission under "mrp.workorder" (作业任务模型) linked to "agri.vra.coordination" (VRA设备智能协同模型)',
            'And the tractor transitions from high soil organic matter zone to low soil organic matter zone (且拖拉机从高有机质区域过渡到低有机质区域)',
            'When the controller evaluates soil sensor feedback (评估土壤传感器反馈) as a critical system action',
            'Then the system must issue flow adjustment commands (发出流量调节指令) to decrease "valve_opening_percentage" by 15.0%',
            'And update the valve command state to "adjusted" (已调节状态)'
        ])

    def test_03_sensor_offline_fallback_safe_mode_irrigation(self):
        """
        Scenario: Sensor Offline Fallback Safe Mode Irrigation (传感器离线故障自动降级为安全模式灌溉)
        Given automated watering missions under "mrp.workorder" (作业任务模型) managed by "agri.vra.coordination" (VRA设备智能协同模型)
        When soil sensors fail to report telemetry and the sensor state is "offline" (离线状态)
        Then the control system must trigger safe mode bypass (触发安全模式旁路) and set "irrigation_fallback_active" to True (真)
        And switch controller irrigation water durations (切换控制器灌溉时长) to safe fixed-rate "fallback_fixed_duty_cycle" of 30.0 minutes
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given automated watering missions under "mrp.workorder" (作业任务模型) managed by "agri.vra.coordination" (VRA设备智能协同模型)',
            'When soil sensors fail to report telemetry and the sensor state is "offline" (离线状态)',
            'Then the control system must trigger safe mode bypass (触发安全模式旁路) and set "irrigation_fallback_active" to True (真)',
            'And switch controller irrigation water durations (切换控制器灌溉时长) to safe fixed-rate "fallback_fixed_duty_cycle" of 30.0 minutes'
        ])

    def test_04_obstacle_sensor_collision_solenoid_spray_pause(self):
        """
        Scenario: Obstacle Sensor Collision Solenoid Spray Pause (避障传感器触发防撞电机停机与喷嘴紧急关闭)
        Given active robotic sprayer missions under "mrp.workorder" (作业任务模型) managed by "agri.vra.coordination" (VRA设备智能协同模型)
        And the distance sensor logs an obstacle distance "obstacle_distance" of 2.8 meters (且距离传感器记录的障碍物距离字段值为2.8米)
        When the control system runs the collision detection loop (运行防撞检测循环)
        Then the vehicle controller must command immediate motor stop (发出立即停机指令) and update "motor_speed" to 0.0 km/h
        And close all nozzle valves (关闭所有喷头阀门) setting "nozzle_valve_state" to "closed" (关闭状态)
        And raise a Warning alert (触发用户警报) with message "Obstacle detected within safety range. Emergency shutdown initiated." (安全范围内检测到障碍物警报)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given active robotic sprayer missions under "mrp.workorder" (作业任务模型) managed by "agri.vra.coordination" (VRA设备智能协同模型)',
            'And the distance sensor logs an obstacle distance "obstacle_distance" of 2.8 meters (且距离传感器记录的障碍物距离字段值为2.8米)',
            'When the control system runs the collision detection loop (运行防撞检测循环)',
            'Then the vehicle controller must command immediate motor stop (发出立即停机指令) and update "motor_speed" to 0.0 km/h',
            'And close all nozzle valves (关闭所有喷头阀门) setting "nozzle_valve_state" to "closed" (关闭状态)',
            'And raise a Warning alert (触发用户警报) with message "Obstacle detected within safety range. Emergency shutdown initiated." (安全范围内检测到障碍物警报)'
        ])

    def test_05_high_wind_safety_sprayer_launch_block(self):
        """
        Scenario: High Wind Safety Sprayer Launch Block (大风天气安全超限拦截喷洒启动)
        Given scheduled plant protection spraying missions under "mrp.workorder" (作业任务模型) linked to "agri.vra.coordination" (VRA设备智能协同模型)
        And local wind speed sensor logs "wind_speed" is 4.5 m/s (且当地风速传感器记录风速字段值为4.5米/秒)
        When the operator attempts to start the spraying mission (尝试启动喷洒作业任务) under "agri.vra.coordination" (VRA设备智能协同模型)
        Then the system must block the launch raising a ValidationError (验证错误) with message "Local wind speed exceeds safety limit of 4.0 m/s. Sprayer launch blocked." (大风天气安全超限拦截验证错误)
        And update the mission state in "mrp.workorder" (作业任务模型) to "cancel" (取消状态)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given scheduled plant protection spraying missions under "mrp.workorder" (作业任务模型) linked to "agri.vra.coordination" (VRA设备智能协同模型)',
            'And local wind speed sensor logs "wind_speed" is 4.5 m/s (且当地风速传感器记录风速字段值为4.5米/秒)',
            'When the operator attempts to start the spraying mission (尝试启动喷洒作业任务) under "agri.vra.coordination" (VRA设备智能协同模型)',
            'Then the system must block the launch raising a ValidationError (验证错误) with message "Local wind speed exceeds safety limit of 4.0 m/s. Sprayer launch blocked." (大风天气安全超限拦截验证错误)',
            'And update the mission state in "mrp.workorder" (作业任务模型) to "cancel" (取消状态)'
        ])

    def test_06_smart_sprayer_biomass_gating_safeguard(self):
        """
        Scenario: Smart Sprayer Biomass Gating Safeguard (智能喷洒生物质质控门控保护)
        Given a smart plant protection spraying mission under "mrp.workorder" (作业任务模型) linked to "agri.vra.coordination" (VRA设备智能协同模型)
        And the organic fertilizer batch lacks circular economy verification "biomass_carbon_index_validated"
        When the coordination controller executes the biomass check via action "action_verify_biomass_carbon" (验证生物质碳指数动作)
        Then the coordination system blocks the start of the sprayer mission
        And updates the mission state in "mrp.workorder" (作业任务模型) to "cancel" (取消状态)
        And raises a ValidationError (验证错误) "ValidationError: Sprayer blocked due to low circular biomass index (验证错误：因循环生物质指数过低拦截喷洒)"
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a smart plant protection spraying mission under "mrp.workorder" (作业任务模型) linked to "agri.vra.coordination" (VRA设备智能协同模型)',
            'And the organic fertilizer batch lacks circular economy verification "biomass_carbon_index_validated"',
            'When the coordination controller executes the biomass check via action "action_verify_biomass_carbon" (验证生物质碳指数动作)',
            'Then the coordination system blocks the start of the sprayer mission',
            'And updates the mission state in "mrp.workorder" (作业任务模型) to "cancel" (取消状态)',
            'And raises a ValidationError (验证错误) "ValidationError: Sprayer blocked due to low circular biomass index (验证错误：因循环生物质指数过低拦截喷洒)"'
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
            'Given a crop parcel\'s soil stock lot in "stock.lot" (库存批次模型) with crop variety "Rose" (且作物物种已设置为玫瑰)',
            'And a smart evapotranspiration sensor registered in "iiot.device" (并且智能蒸腾量传感器已注册在工业物联网设备模型中)',
            'When the soil sensor logs an NPK reading drift of 25.0% (当土壤传感器记录到氮磷钾读数偏离比比例达到25.0%时)',
            'Then the system must trigger safe mode self-correction (系统必须自动执行安全模式自校准动作)',
            'And scale back the water drip runtime "drip_duration" to fallback 10.0 minutes (并且将滴灌时长字段值等比例缩减至备用时长值10.0分钟)',
            'And raise a ValidationError (并且系统抛出验证错误) with message "CRITICAL_SENSOR_DRIFT_DETECTED" (包含"传感器发生严重漂移，进入自愈模式"提示信息)'
        ])
