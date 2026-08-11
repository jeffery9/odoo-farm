# -*- coding: utf-8 -*-
from odoo.addons.farm_core.tests.bdd_base import BddTransactionCase
from odoo.exceptions import UserError, ValidationError

class TestEpic121(BddTransactionCase):
    """ BDD Test Suite for Epic 121: Epic 121 Agricultural Robotics Automation (农业机器人自动化) """

    def setUp(self):
        super(TestEpic121, self).setUp()

    def test_01_weedpicking_robot_mission_launch_verification(self):
        """
        Scenario: Weed-Picking Robot Mission Launch Verification (除草机器人作业任务启动校验)
        Given an autonomous weed-picking robot mission under "mrp.workorder" (作业任务模型) linked to a robotics run under "agri.robotics.run" (机器人运行记录模型)
        And the mission state "state" is "ready" (且作业任务状态字段值为准备就绪状态)
        And the robot's battery level "battery_level" is 15.0% (且机器人的电池电量百分比字段值为15.0%)
        When the system attempts to trigger the robot mission start (当系统尝试触发机器人作业任务启动时)
        Then the system must raise a ValidationError (系统必须抛出验证错误) with message "Battery level too low for mission launch" (包含"任务启动电池电量过低"提示信息)
        And block the state transition, keeping the mission state "state" as "ready" (并且阻止状态转变，保持作业任务状态字段值为准备就绪状态)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an autonomous weed-picking robot mission under "mrp.workorder" (作业任务模型) linked to a robotics run under "agri.robotics.run" (机器人运行记录模型)',
            'And the mission state "state" is "ready" (且作业任务状态字段值为准备就绪状态)',
            'And the robot\'s battery level "battery_level" is 15.0% (且机器人的电池电量百分比字段值为15.0%)',
            'When the system attempts to trigger the robot mission start (当系统尝试触发机器人作业任务启动时)',
            'Then the system must raise a ValidationError (系统必须抛出验证错误) with message "Battery level too low for mission launch" (包含"任务启动电池电量过低"提示信息)',
            'And block the state transition, keeping the mission state "state" as "ready" (并且阻止状态转变，保持作业任务状态字段值为准备就绪状态)'
        ])

    def test_02_realtime_robotic_laser_obstacle_stop(self):
        """
        Scenario: Real-time Robotic Laser Obstacle Stop (机器人激光雷达避障实时紧急停喷)
        Given a running weed-picking robot mission under "mrp.workorder" (作业任务模型) in state "progress" (且作业任务状态字段值为进行中状态)
        And the active robotics run under "agri.robotics.run" (机器人运行记录模型) has spray status "is_spraying" as true (且其喷洒状态字段值为真)
        When obstacle sensors log a distance "obstacle_distance" of 1.2 meters (当避障传感器记录的障碍物距离字段值为1.2米时)
        Then the controller must automatically trigger a dynamic spray pause (控制器必须自动触发动态喷洒暂停)
        And update the spray status "is_spraying_paused" to true on the robotics run under "agri.robotics.run" (并在机器人运行记录模型上更新是否暂停喷洒字段值为真)
        And log an activity under "mail.activity" (邮件活动模型) to alert the remote operator (以向远程操作员发出警报)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a running weed-picking robot mission under "mrp.workorder" (作业任务模型) in state "progress" (且作业任务状态字段值为进行中状态)',
            'And the active robotics run under "agri.robotics.run" (机器人运行记录模型) has spray status "is_spraying" as true (且其喷洒状态字段值为真)',
            'When obstacle sensors log a distance "obstacle_distance" of 1.2 meters (当避障传感器记录的障碍物距离字段值为1.2米时)',
            'Then the controller must automatically trigger a dynamic spray pause (控制器必须自动触发动态喷洒暂停)',
            'And update the spray status "is_spraying_paused" to true on the robotics run under "agri.robotics.run" (并在机器人运行记录模型上更新是否暂停喷洒字段值为真)',
            'And log an activity under "mail.activity" (邮件活动模型) to alert the remote operator (以向远程操作员发出警报)'
        ])

    def test_03_robotic_solarcharging_duty_cycle_bypass(self):
        """
        Scenario: Robotic Solar-Charging Duty Cycle Bypass (机器人太阳能充电工作周期自动旁路绕行)
        Given a running weed-picking robot mission under "mrp.workorder" (作业任务模型)
        And the robot's battery level "battery_level" is 25.0% (且机器人的电池电量百分比字段值为25.0%)
        And the local solar sensor logs a solar irradiance "solar_irradiance" of 850.0 W/m² (且本地光照传感器记录的太阳辐射强度字段值为850.0瓦特每平方米)
        When the weekly scheduler runs the active duty cycle (当每周调度程序运行当前工作周期时)
        Then the robot must bypass the normal weeding schedule and transition to dynamic charging status (机器人必须绕行常规除草计划并过渡到动态充电状态)
        And set the charge mode "charge_mode" to "solar_safe" on "agri.robotics.run" (并在机器人运行记录模型上设置充电模式字段值为安全太阳能充电状态)
        And ensure the mission state "state" remains as "progress" (并确保作业任务状态字段值保持为进行中状态)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a running weed-picking robot mission under "mrp.workorder" (作业任务模型)',
            'And the robot\'s battery level "battery_level" is 25.0% (且机器人的电池电量百分比字段值为25.0%)',
            'And the local solar sensor logs a solar irradiance "solar_irradiance" of 850.0 W/m² (且本地光照传感器记录的太阳辐射强度字段值为850.0瓦特每平方米)',
            'When the weekly scheduler runs the active duty cycle (当每周调度程序运行当前工作周期时)',
            'Then the robot must bypass the normal weeding schedule and transition to dynamic charging status (机器人必须绕行常规除草计划并过渡到动态充电状态)',
            'And set the charge mode "charge_mode" to "solar_safe" on "agri.robotics.run" (并在机器人运行记录模型上设置充电模式字段值为安全太阳能充电状态)',
            'And ensure the mission state "state" remains as "progress" (并确保作业任务状态字段值保持为进行中状态)'
        ])

    def test_04_high_wind_safety_drone_spray_launch_block(self):
        """
        Scenario: High Wind Safety Drone Spray Launch Block (高风速安全限制无人机喷洒启动拦截)
        Given a drone spray mission under "mrp.workorder" (作业任务模型) linked to "agri.robotics.run" (机器人运行记录模型)
        And the local weather sensor logs a wind speed "wind_speed" of 5.5 m/s (且本地天气传感器记录的风速字段值为5.5米每秒)
        When the supervisor attempts to confirm the spray launch (当主管尝试确认喷洒启动时)
        Then the system must block the launch process and raise a safety warning (系统必须拦截启动程序并抛出安全警告)
        And update the robotics run state "state" to "canceled" (并在机器人运行记录模型上更新状态字段值为已取消状态)
        And update the mission state "state" to "cancel" (并在作业任务模型上更新作业任务状态字段值为已取消状态)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a drone spray mission under "mrp.workorder" (作业任务模型) linked to "agri.robotics.run" (机器人运行记录模型)',
            'And the local weather sensor logs a wind speed "wind_speed" of 5.5 m/s (且本地天气传感器记录的风速字段值为5.5米每秒)',
            'When the supervisor attempts to confirm the spray launch (当主管尝试确认喷洒启动时)',
            'Then the system must block the launch process and raise a safety warning (系统必须拦截启动程序并抛出安全警告)',
            'And update the robotics run state "state" to "canceled" (并在机器人运行记录模型上更新状态字段值为已取消状态)',
            'And update the mission state "state" to "cancel" (并在作业任务模型上更新作业任务状态字段值为已取消状态)'
        ])

    def test_05_multilevel_cascade_deletion_gating_on_robots(self):
        """
        Scenario: Multi-Level Cascade Deletion Gating on Robots (机器人设备多级级联删除安全保护拦截)
        Given an active physical carrier under "agri.robotics.carrier" (机器人载具模型) linked to a robotics run record under "agri.robotics.run" (机器人运行记录模型)
        And the carrier is currently assigned to an active mission under "mrp.workorder" (且该载具当前已被分配至一个进行中的作业任务模型中)
        When the operator attempts to delete the robotics run record under "agri.robotics.run" (当操作员尝试删除该机器人运行记录模型上的记录时)
        Then the system must trigger cascade deletion gating and raise a deletion error (系统必须触发级联删除保护拦截并抛出删除错误)
        And reject the deletion, maintaining database reference integrity (并且拒绝删除，维护数据库引用完整性)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an active physical carrier under "agri.robotics.carrier" (机器人载具模型) linked to a robotics run record under "agri.robotics.run" (机器人运行记录模型)',
            'And the carrier is currently assigned to an active mission under "mrp.workorder" (且该载具当前已被分配至一个进行中的作业任务模型中)',
            'When the operator attempts to delete the robotics run record under "agri.robotics.run" (当操作员尝试删除该机器人运行记录模型上的记录时)',
            'Then the system must trigger cascade deletion gating and raise a deletion error (系统必须触发级联删除保护拦截并抛出删除错误)',
            'And reject the deletion, maintaining database reference integrity (并且拒绝删除，维护数据库引用完整性)'
        ])

    def test_06_swarm_drone_realtime_obstacle_bypass_routing(self):
        """
        Scenario: Swarm Drone Real-Time Obstacle Bypass Routing (群控无人机实时障碍物自动旁路航线调整)
        Given an active swarm drone spray mission under "mrp.workorder" (作业任务模型) in state "progress" (且作业任务状态字段值为进行中状态)
        And the associated coordination run under "agri.robotics.run" (机器人运行记录模型) has status "state" as "running" (且关联的机器人运行记录模型状态字段值为运行中状态)
        When the drone lidar sensors detect an unexpected obstacle at distance "obstacle_distance" of 3.5 meters (当无人机雷达传感器检测到3.5米处的突发障碍物时)
        Then the autopilot system must trigger a dynamic swarm drone obstacle bypass route calculation (自动驾驶系统必须触发群控无人机动态障碍物旁路航线计算)
        And update the navigation bypass status "bypass_active" to true on "agri.robotics.run" (并在机器人运行记录模型上更新是否启用旁路航线字段值为真)
        And ensure the swarm drone mission state "state" remains as "progress" (并确保群控无人机作业任务状态字段值保持为进行中状态)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an active swarm drone spray mission under "mrp.workorder" (作业任务模型) in state "progress" (且作业任务状态字段值为进行中状态)',
            'And the associated coordination run under "agri.robotics.run" (机器人运行记录模型) has status "state" as "running" (且关联的机器人运行记录模型状态字段值为运行中状态)',
            'When the drone lidar sensors detect an unexpected obstacle at distance "obstacle_distance" of 3.5 meters (当无人机雷达传感器检测到3.5米处的突发障碍物时)',
            'Then the autopilot system must trigger a dynamic swarm drone obstacle bypass route calculation (自动驾驶系统必须触发群控无人机动态障碍物旁路航线计算)',
            'And update the navigation bypass status "bypass_active" to true on "agri.robotics.run" (并在机器人运行记录模型上更新是否启用旁路航线字段值为真)',
            'And ensure the swarm drone mission state "state" remains as "progress" (并确保群控无人机作业任务状态字段值保持为进行中状态)'
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
