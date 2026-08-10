# -*- coding: utf-8 -*-
from odoo.addons.farm_core.tests.bdd_base import BddTransactionCase
from odoo.exceptions import UserError, ValidationError

class TestEpic133(BddTransactionCase):
    """ BDD Test Suite for Epic 133: Epic 133 Swarm Robotics Coordination (群控机器人协同) """

    def setUp(self):
        super(TestEpic133, self).setUp()

    def test_01_swarm_robotics_collision_avoidance_checks(self):
        """
        Scenario: Swarm Robotics collision avoidance checks (群控机器人避障防撞实时校验)
        Given a swarm robotic mission under "mrp.workorder" (作业任务模型) linked to a coordination record under "agri.swarm.coord" (群控机器人协同记录模型)
        And the mission state "state" is "progress" (且作业任务状态字段值为进行中状态)
        And the speed of robot Alpha "speed_alpha" is 850.0 mm/s (且机器人Alpha的速度字段值为850.0毫米每秒)
        When robot Beta logs coordinates "coordinates_beta" within 1.2 meters of Alpha (当机器人Beta记录的坐标距离Alpha在1.2米以内时)
        Then the coordination system must trigger collision avoidance and adjust speeds (协同系统必须触发防撞保护并调整速度)
        And update the path clearance status "is_clear" to false on "agri.swarm.coord" (并在群控机器人协同记录模型上更新路径净空状态字段值为假)
        And set robot Alpha target speed "target_speed" to 0.0 mm/s to prevent collision (并将机器人Alpha的目标速度字段值设置为0.0毫米每秒以防止碰撞)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a swarm robotic mission under "mrp.workorder" (作业任务模型) linked to a coordination record under "agri.swarm.coord" (群控机器人协同记录模型)',
            'And the mission state "state" is "progress" (且作业任务状态字段值为进行中状态)',
            'And the speed of robot Alpha "speed_alpha" is 850.0 mm/s (且机器人Alpha的速度字段值为850.0毫米每秒)',
            'When robot Beta logs coordinates "coordinates_beta" within 1.2 meters of Alpha (当机器人Beta记录的坐标距离Alpha在1.2米以内时)',
            'Then the coordination system must trigger collision avoidance and adjust speeds (协同系统必须触发防撞保护并调整速度)',
            'And update the path clearance status "is_clear" to false on "agri.swarm.coord" (并在群控机器人协同记录模型上更新路径净空状态字段值为假)',
            'And set robot Alpha target speed "target_speed" to 0.0 mm/s to prevent collision (并将机器人Alpha的目标速度字段值设置为0.0毫米每秒以防止碰撞)'
        ])

    def test_02_realtime_tractor_sprayer_vra_valve_adjustment_vra(self):
        """
        Scenario: Real-time Tractor Sprayer VRA Valve Adjustment (实时拖拉机喷洒机VRA阀门开度协同调整)
        Given a swarm robotic mission under "mrp.workorder" (作业任务模型) executing spray routines managed under "agri.swarm.coord" (群控机器人协同记录模型)
        And the sprayer currently traverses a High-SOM (high soil organic matter) zone (且喷洒机当前正在穿过高土壤有机质区域)
        When the RTK-GNSS GPS coordinates "gps_coordinates" transition into a Low-SOM zone (当GPS坐标字段值过渡到低土壤有机质区域时)
        Then the coordination system must compute a dynamic nozzle flow rate decrease of 15.0% (协同系统必须计算并降低15.0%的动态喷嘴流量比率)
        And write the new nozzle adjustment command "nozzle_flow_rate" of 85.0% on "agri.swarm.coord" (并在群控机器人协同记录模型上写入85.0%的新喷嘴流量比率指令字段值)
        And update the active mission state "state" to "progress" (并更新作业任务状态字段值为进行中状态)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a swarm robotic mission under "mrp.workorder" (作业任务模型) executing spray routines managed under "agri.swarm.coord" (群控机器人协同记录模型)',
            'And the sprayer currently traverses a High-SOM (high soil organic matter) zone (且喷洒机当前正在穿过高土壤有机质区域)',
            'When the RTK-GNSS GPS coordinates "gps_coordinates" transition into a Low-SOM zone (当GPS坐标字段值过渡到低土壤有机质区域时)',
            'Then the coordination system must compute a dynamic nozzle flow rate decrease of 15.0% (协同系统必须计算并降低15.0%的动态喷嘴流量比率)',
            'And write the new nozzle adjustment command "nozzle_flow_rate" of 85.0% on "agri.swarm.coord" (并在群控机器人协同记录模型上写入85.0%的新喷嘴流量比率指令字段值)',
            'And update the active mission state "state" to "progress" (并更新作业任务状态字段值为进行中状态)'
        ])

    def test_03_sensor_offline_fallback_safe_mode_irrigation(self):
        """
        Scenario: Sensor Offline Fallback Safe Mode Irrigation (传感器离线自动降级安全滴灌模式切换)
        Given a swarm irrigation mission under "mrp.workorder" (作业任务模型) coordinated under "agri.swarm.coord" (群控机器人协同记录模型)
        And the soil moisture sensor "sensor_status" is online (且土壤湿度传感器状态字段值为在线状态)
        When telemetry fails and logs the sensor status "sensor_status" as offline (当遥测失败且记录的传感器状态字段值为离线状态时)
        Then the coordination system must raise an offline warning (协同系统必须发出离线警告)
        And automatically transition the swarm to safe mode "safe_mode" as true on "agri.swarm.coord" (并在群控机器人协同记录模型上自动过渡到安全模式字段值为真)
        And fallback to a fixed-rate watering schedule, keeping the mission state "state" as "progress" (并且降级回退到固定比例浇水计划，保持作业任务状态字段值为进行中状态)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a swarm irrigation mission under "mrp.workorder" (作业任务模型) coordinated under "agri.swarm.coord" (群控机器人协同记录模型)',
            'And the soil moisture sensor "sensor_status" is online (且土壤湿度传感器状态字段值为在线状态)',
            'When telemetry fails and logs the sensor status "sensor_status" as offline (当遥测失败且记录的传感器状态字段值为离线状态时)',
            'Then the coordination system must raise an offline warning (协同系统必须发出离线警告)',
            'And automatically transition the swarm to safe mode "safe_mode" as true on "agri.swarm.coord" (并在群控机器人协同记录模型上自动过渡到安全模式字段值为真)',
            'And fallback to a fixed-rate watering schedule, keeping the mission state "state" as "progress" (并且降级回退到固定比例浇水计划，保持作业任务状态字段值为进行中状态)'
        ])

    def test_04_obstacle_sensor_collision_solenoid_spray_pause(self):
        """
        Scenario: Obstacle Sensor Collision Solenoid Spray Pause (避障传感器测距紧急停喷与电磁阀关闭)
        Given an active robotic sprayer swarm mission under "mrp.workorder" (作业任务模型) in state "progress" (且作业任务状态字段值为进行中状态)
        And the active robotic control status "is_active" is true on "agri.swarm.coord" (且群控机器人协同记录模型上的运行状态字段值为真)
        When distance sensors log an obstacle distance "obstacle_distance" of 2.5 meters (当距离传感器记录的障碍物距离字段值为2.5米时)
        Then the controller must command immediate motor stops and close the spray solenoid valves (控制器必须下达立即停机指令并关闭喷洒电磁阀)
        And update the spray valve state "is_solenoid_closed" to true on "agri.swarm.coord" (并在群控机器人协同记录模型上更新电磁阀关闭状态字段值为真)
        And keep the mission state "state" in "progress" (并保持作业任务状态字段值为进行中状态)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an active robotic sprayer swarm mission under "mrp.workorder" (作业任务模型) in state "progress" (且作业任务状态字段值为进行中状态)',
            'And the active robotic control status "is_active" is true on "agri.swarm.coord" (且群控机器人协同记录模型上的运行状态字段值为真)',
            'When distance sensors log an obstacle distance "obstacle_distance" of 2.5 meters (当距离传感器记录的障碍物距离字段值为2.5米时)',
            'Then the controller must command immediate motor stops and close the spray solenoid valves (控制器必须下达立即停机指令并关闭喷洒电磁阀)',
            'And update the spray valve state "is_solenoid_closed" to true on "agri.swarm.coord" (并在群控机器人协同记录模型上更新电磁阀关闭状态字段值为真)',
            'And keep the mission state "state" in "progress" (并保持作业任务状态字段值为进行中状态)'
        ])

    def test_05_high_wind_safety_sprayer_launch_block(self):
        """
        Scenario: High Wind Safety Sprayer Launch Block (超风速安全策略拦截作业任务启动)
        Given a robotic sprayer swarm mission under "mrp.workorder" (作业任务模型) in state "ready" (且作业任务状态字段值为准备就绪状态)
        And the swarm's wind safety limit "wind_limit" is set to 4.0 m/s on "agri.swarm.coord" (且群控机器人协同记录模型上的风速安全限制字段值为4.0米每秒)
        When weather telemetry logs a local wind speed "wind_speed" of 5.2 m/s (当天气遥测记录的本地风速字段值为5.2米每秒时)
        Then the coordination system must block the launcher and raise a ValidationError (协同系统必须拦截启动器并抛出验证错误) with message "Wind speed exceeds safety limits for swarm spray mission" (包含"风速超过群控喷洒任务安全限制"提示信息)
        And update the mission state "state" to "cancel" (并在作业任务模型上更新作业任务状态字段值为已取消状态)
        And set the coordination run status "state" to "canceled" on "agri.swarm.coord" (并在群控机器人协同记录模型上设置运行状态字段值为已取消状态)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a robotic sprayer swarm mission under "mrp.workorder" (作业任务模型) in state "ready" (且作业任务状态字段值为准备就绪状态)',
            'And the swarm\'s wind safety limit "wind_limit" is set to 4.0 m/s on "agri.swarm.coord" (且群控机器人协同记录模型上的风速安全限制字段值为4.0米每秒)',
            'When weather telemetry logs a local wind speed "wind_speed" of 5.2 m/s (当天气遥测记录的本地风速字段值为5.2米每秒时)',
            'Then the coordination system must block the launcher and raise a ValidationError (协同系统必须拦截启动器并抛出验证错误) with message "Wind speed exceeds safety limits for swarm spray mission" (包含"风速超过群控喷洒任务安全限制"提示信息)',
            'And update the mission state "state" to "cancel" (并在作业任务模型上更新作业任务状态字段值为已取消状态)',
            'And set the coordination run status "state" to "canceled" on "agri.swarm.coord" (并在群控机器人协同记录模型上设置运行状态字段值为已取消状态)'
        ])

    def test_06_swarm_drone_obstacle_detection_and_realtime_bypass(self):
        """
        Scenario: Swarm Drone Obstacle Detection and Real-Time Bypass (群控无人机障碍物实时自动旁路避障)
        Given an active swarm drone harvesting mission under "mrp.workorder" (作业任务模型) in state "progress" (且作业任务状态字段值为进行中状态)
        And the coordination profile "coordination_state" is "optimal" on "agri.swarm.coord" (且群控机器人协同记录模型上的协同状态字段值为最佳状态)
        When drone telemetry logs a lidar-detected high-voltage wire obstacle "obstacle_distance" of 4.5 meters (当无人机遥测记录雷达在4.5米处探测到高压线障碍物时)
        Then the coordination engine must calculate a localized swarm drone bypass path trajectory (协同引擎必须计算局部群控无人机旁路避障路径航线)
        And update the navigation bypass flag "bypass_active" to true on "agri.swarm.coord" (并在群控机器人协同记录模型上更新是否启用旁路航线字段值为真)
        And ensure the mission state "state" remains as "progress" (并确保作业任务状态字段值保持为进行中状态)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an active swarm drone harvesting mission under "mrp.workorder" (作业任务模型) in state "progress" (且作业任务状态字段值为进行中状态)',
            'And the coordination profile "coordination_state" is "optimal" on "agri.swarm.coord" (且群控机器人协同记录模型上的协同状态字段值为最佳状态)',
            'When drone telemetry logs a lidar-detected high-voltage wire obstacle "obstacle_distance" of 4.5 meters (当无人机遥测记录雷达在4.5米处探测到高压线障碍物时)',
            'Then the coordination engine must calculate a localized swarm drone bypass path trajectory (协同引擎必须计算局部群控无人机旁路避障路径航线)',
            'And update the navigation bypass flag "bypass_active" to true on "agri.swarm.coord" (并在群控机器人协同记录模型上更新是否启用旁路航线字段值为真)',
            'And ensure the mission state "state" remains as "progress" (并确保作业任务状态字段值保持为进行中状态)'
        ])

    def test_07_swarm_drone_obstacle_detection_adaptive_mission_pause(self):
        """
        Scenario: Swarm Drone Obstacle Detection Adaptive Mission Pause (作业无人机蜂群物理避障与任务降级自愈控制)
        Given an active autonomous aerial spray mission in "mrp.workorder" (作业任务模型) with status "progress" (进行中状态)
        And a smart spray nozzle registered in "iiot.device" (并且智能喷洒喷嘴已注册在物联网设备模型中)
        When the drone sensor registers an obstacle proximity of less than 3.0 meters (当无人机距离传感器记录的障碍物物理距离小于3.0米时)
        Then the swarm autopilot must automatically scale down the speed "target_speed" (飞控程序必须自动降低作业飞行速度字段值)
        And pause the spray action, raising a ValidationError (并且暂停喷洒喷头动作并抛出验证错误) with message "OBSTACLE_DETECTED_MISSION_PAUSED" (包含"检测到障碍物，作业自动挂起"提示信息)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an active autonomous aerial spray mission in "mrp.workorder" (作业任务模型) with status "progress" (进行中状态)',
            'And a smart spray nozzle registered in "iiot.device" (并且智能喷洒喷嘴已注册在物联网设备模型中)',
            'When the drone sensor registers an obstacle proximity of less than 3.0 meters (当无人机距离传感器记录的障碍物物理距离小于3.0米时)',
            'Then the swarm autopilot must automatically scale down the speed "target_speed" (飞控程序必须自动降低作业飞行速度字段值)',
            'And pause the spray action, raising a ValidationError (并且暂停喷洒喷头动作并抛出验证错误) with message "OBSTACLE_DETECTED_MISSION_PAUSED" (包含"检测到障碍物，作业自动挂起"提示信息)'
        ])
