# -*- coding: utf-8 -*-
from odoo.addons.farm_core.tests.bdd_base import BddTransactionCase
from odoo.exceptions import UserError, ValidationError

class TestEpic112(BddTransactionCase):
    """ BDD Test Suite for Epic 112: Epic 112 AI Driven Predictive Maintenance (AI驱动的预测性维护) """

    def setUp(self):
        super(TestEpic112, self).setUp()

    def test_01_asset_vibration_and_temperature_tolerance_violation_alerts(self):
        """
        Scenario: Asset Vibration and Temperature Tolerance Violation Alerts (设备振动与温度超标预警)
        Given a machinery asset under "maintenance.equipment" (机械设备模型) linked to "agri.predictive.maint" (智能预测性维护模型)
        And the sensor telemetry logs "vibration_amplitude" is 8.5 mm/s (且遥测日志记录的振动幅度字段值为8.5毫米/秒)
        And the motor temperature "motor_temperature" is 86.0 °C (并且电机温度字段值为86.0摄氏度)
        When the predictive engine evaluates asset health (评估资产健康状态) as a critical system action
        Then the system must trigger an alert (触发预警) updating "health_index" to "warning" (警告状态)
        And log a telemetry warning message (记录遥测警报日志) in "maintenance.equipment" (机械设备模型)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a machinery asset under "maintenance.equipment" (机械设备模型) linked to "agri.predictive.maint" (智能预测性维护模型)',
            'And the sensor telemetry logs "vibration_amplitude" is 8.5 mm/s (且遥测日志记录的振动幅度字段值为8.5毫米/秒)',
            'And the motor temperature "motor_temperature" is 86.0 °C (并且电机温度字段值为86.0摄氏度)',
            'When the predictive engine evaluates asset health (评估资产健康状态) as a critical system action',
            'Then the system must trigger an alert (触发预警) updating "health_index" to "warning" (警告状态)',
            'And log a telemetry warning message (记录遥测警报日志) in "maintenance.equipment" (机械设备模型)'
        ])

    def test_02_automated_low_battery_telemetry_maintenance_orders(self):
        """
        Scenario: Automated Low Battery Telemetry Maintenance Orders (牧场定位项圈低电量自动触发维护单)
        Given an active livestock tracking collar asset under "maintenance.equipment" (机械设备模型) with status "operational" (在用状态)
        And the pasture telemetry reports collar battery "collar_battery_level" is 18.0% (且牧场遥测系统上报的定位圈剩余电量字段值为18.0%)
        When the battery check scheduler runs (运行电池检查计划任务) under "agri.predictive.maint" (智能预测性维护模型)
        Then the system must automatically create a maintenance request (自动创建维护保养请求)
        And update the asset state "health_index" to "critical" (紧急状态)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an active livestock tracking collar asset under "maintenance.equipment" (机械设备模型) with status "operational" (在用状态)',
            'And the pasture telemetry reports collar battery "collar_battery_level" is 18.0% (且牧场遥测系统上报的定位圈剩余电量字段值为18.0%)',
            'When the battery check scheduler runs (运行电池检查计划任务) under "agri.predictive.maint" (智能预测性维护模型)',
            'Then the system must automatically create a maintenance request (自动创建维护保养请求)',
            'And update the asset state "health_index" to "critical" (紧急状态)'
        ])

    def test_03_unscheduled_breakdown_active_backtrack_selfhealing(self):
        """
        Scenario: Unscheduled Breakdown Active Backtrack Self-Healing (突发设备故障自动追溯与自愈重排产)
        Given an active sorting line workstation under "maintenance.equipment" (机械设备模型) in state "operational" (运行中状态)
        And several processing missions under "mrp.workorder" (作业任务模型) are scheduled on this workstation (且有多个作业任务已排产于此工作站)
        When a sudden breakdown switches the equipment state "equipment_state" to "breakdown" (故障状态)
        Then the self-healing planner under "agri.predictive.maint" (智能预测性维护模型) must backtrack and reschedule remaining lots (执行追溯并将剩余批次重新调度) to backup workstations
        And update all impacted "mrp.workorder" (作业任务模型) states to "ready" (就绪状态)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an active sorting line workstation under "maintenance.equipment" (机械设备模型) in state "operational" (运行中状态)',
            'And several processing missions under "mrp.workorder" (作业任务模型) are scheduled on this workstation (且有多个作业任务已排产于此工作站)',
            'When a sudden breakdown switches the equipment state "equipment_state" to "breakdown" (故障状态)',
            'Then the self-healing planner under "agri.predictive.maint" (智能预测性维护模型) must backtrack and reschedule remaining lots (执行追溯并将剩余批次重新调度) to backup workstations',
            'And update all impacted "mrp.workorder" (作业任务模型) states to "ready" (就绪状态)'
        ])

    def test_04_ai_predictive_asset_lifespan_and_failure_forecasts_ai(self):
        """
        Scenario: AI Predictive Asset Lifespan and Failure Forecasts (AI预测设备剩余寿命及故障预估)
        Given historical maintenance and sensor logging logs under "maintenance.equipment" (机械设备模型)
        When the AI prognostic model evaluates predictive statistics (评估预测性统计数据) under "agri.predictive.maint" (智能预测性维护模型)
        Then the system must calculate and write "predicted_rul" (计算并写入预测剩余寿命) to be 120.0 hours
        And schedule a preventive calibration maintenance request (自动生成预防性校验保养请求) before 120.0 hours
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given historical maintenance and sensor logging logs under "maintenance.equipment" (机械设备模型)',
            'When the AI prognostic model evaluates predictive statistics (评估预测性统计数据) under "agri.predictive.maint" (智能预测性维护模型)',
            'Then the system must calculate and write "predicted_rul" (计算并写入预测剩余寿命) to be 120.0 hours',
            'And schedule a preventive calibration maintenance request (自动生成预防性校验保养请求) before 120.0 hours'
        ])

    def test_05_gxp_certified_technician_checkin_validation(self):
        """
        Scenario: GxP Certified Technician Check-In Validation (符合药典规范/良好农业规范的持证技术员签到校验)
        Given an automated processing line under "maintenance.equipment" (机械设备模型) requiring GxP standard maintenance (要求GxP规范维护)
        And a maintenance technician record under "res.partner" (联系人模型) with GxP safety certification "has_gxp_certification" set to False (假)
        When the technician attempts to check-in or claim a maintenance request (尝试签到或认领维护保养请求) as a critical system action
        Then the system must block the action and raise a ValidationError (验证错误) with message "Technician lacks active GxP certification. Access denied." (技术人员缺少激活的GxP证书验证错误)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an automated processing line under "maintenance.equipment" (机械设备模型) requiring GxP standard maintenance (要求GxP规范维护)',
            'And a maintenance technician record under "res.partner" (联系人模型) with GxP safety certification "has_gxp_certification" set to False (假)',
            'When the technician attempts to check-in or claim a maintenance request (尝试签到或认领维护保养请求) as a critical system action',
            'Then the system must block the action and raise a ValidationError (验证错误) with message "Technician lacks active GxP certification. Access denied." (技术人员缺少激活的GxP证书验证错误)'
        ])

    def test_06_predictive_maintenance_carbon_tax_penalty_allocation(self):
        """
        Scenario: Predictive Maintenance Carbon Tax Penalty Allocation (预测性维护泄露碳税分摊)
        Given a mechanical equipment record under "maintenance.equipment" (机械设备模型) with status "repairs"
        And the carbon leakage audit log reports direct emissions of 250.0 kg CO2 in "leakage_emissions"
        When the maintenance director triggers calculation action "action_calculate_maintenance_emissions" (计算维护排放量动作)
        Then the system posts the calculated carbon tax penalty under "account.move" (日记账分录模型) with status (状态) "draft" (草稿)
        And splits the penalty fee across the responsible workshop centers (在责任车间中心之间分摊处罚金额)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a mechanical equipment record under "maintenance.equipment" (机械设备模型) with status "repairs"',
            'And the carbon leakage audit log reports direct emissions of 250.0 kg CO2 in "leakage_emissions"',
            'When the maintenance director triggers calculation action "action_calculate_maintenance_emissions" (计算维护排放量动作)',
            'Then the system posts the calculated carbon tax penalty under "account.move" (日记账分录模型) with status (状态) "draft" (草稿)',
            'And splits the penalty fee across the responsible workshop centers (在责任车间中心之间分摊处罚金额)'
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
