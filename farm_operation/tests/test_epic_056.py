# -*- coding: utf-8 -*-
from odoo.addons.farm_core.tests.bdd_base import BddTransactionCase
from odoo.exceptions import UserError, ValidationError

class TestEpic056(BddTransactionCase):
    """ BDD Test Suite for Epic 056: Epic 056 Field Operations Services (田间作业服务) """

    def setUp(self):
        super(TestEpic056, self).setUp()

    def test_01_outsourced_harvester_contract_settlement_hectares_split(self):
        """
        Scenario: Outsourced Harvester Contract Settlement Hectares Split
        Given an outsourced harvesting contractor service contract is created as a purchase order under "purchase.order" (采购订单)
        And the contract specifies a total harvesting service fee of 15000.0 USD
        When the contractor completes the harvesting work recorded under "agri.field.service" (田间服务记录) across 3 distinct cooperative farms:
        Then the system must automatically split and allocate the contract settlement cost lines in the draft invoice "account.move" (应付账单):
        And the cost distribution is posted to each farm's corresponding analytical account "account.analytic.account" (分析账户)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an outsourced harvesting contractor service contract is created as a purchase order under "purchase.order" (采购订单)',
            'And the contract specifies a total harvesting service fee of 15000.0 USD',
            'When the contractor completes the harvesting work recorded under "agri.field.service" (田间服务记录) across 3 distinct cooperative farms:',
            'Then the system must automatically split and allocate the contract settlement cost lines in the draft invoice "account.move" (应付账单):',
            'And the cost distribution is posted to each farm\'s corresponding analytical account "account.analytic.account" (分析账户)'
        ])

    def test_02_contractor_quality_score_price_adjustments_and_penalties(self):
        """
        Scenario: Contractor Quality Score Price Adjustments and Penalties
        Given an outsourced harvesting service contract under "purchase.order" (采购订单) with a target contract value of 10000.0 USD
        And the quality control contract requires grain damage to be below 3.0%
        When the quality audit report under "agri.field.service" (田间服务记录) registers a grain damage of 4.5% yielding a contractor quality score of 78 points (78分质量评分)
        Then the system automatically triggers a damage penalty validation rule (触发货损赔偿校验规则)
        And automatically applies a 10.0% penalty reduction (10% 罚金扣减) of 1000.0 USD on the draft supplier invoice "account.move" (应付账单)
        And logs the quality penalty justification "Grain damage exceeded 3.0% limit" in the record chatter
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an outsourced harvesting service contract under "purchase.order" (采购订单) with a target contract value of 10000.0 USD',
            'And the quality control contract requires grain damage to be below 3.0%',
            'When the quality audit report under "agri.field.service" (田间服务记录) registers a grain damage of 4.5% yielding a contractor quality score of 78 points (78分质量评分)',
            'Then the system automatically triggers a damage penalty validation rule (触发货损赔偿校验规则)',
            'And automatically applies a 10.0% penalty reduction (10% 罚金扣减) of 1000.0 USD on the draft supplier invoice "account.move" (应付账单)',
            'And logs the quality penalty justification "Grain damage exceeded 3.0% limit" in the record chatter'
        ])

    def test_03_shared_harvester_allocation_booking_and_priority_schedule(self):
        """
        Scenario: Shared Harvester Allocation Booking and Priority Schedule
        Given a shared contractor-owned harvesting machine is registered in "maintenance.equipment" (设备档案)
        And Farm A and Farm B attempt to schedule overlapping service reservations under "agri.field.service" (田间服务记录) for the same date
        When the scheduling engine runs the booking prioritization algorithm
        Then the system automatically allocates the booking priority to the farm with higher crop maturity index
        And schedules non-overlapping service missions, moving the secondary farm's request to "scheduled" (已排程) status
        And sends automated push notifications to both farm operators
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a shared contractor-owned harvesting machine is registered in "maintenance.equipment" (设备档案)',
            'And Farm A and Farm B attempt to schedule overlapping service reservations under "agri.field.service" (田间服务记录) for the same date',
            'When the scheduling engine runs the booking prioritization algorithm',
            'Then the system automatically allocates the booking priority to the farm with higher crop maturity index',
            'And schedules non-overlapping service missions, moving the secondary farm\'s request to "scheduled" (已排程) status',
            'And sends automated push notifications to both farm operators'
        ])

    def test_04_contractor_service_validation_gps_flight_log_match_checks(self):
        """
        Scenario: Contractor Service Validation GPS Flight Log Match Checks
        Given a service contractor submits a billing invoice for crop pesticide spraying under "purchase.order" (采购订单)
        And the contractor claims spraying coverage of 10.0 hectares in their invoice lines
        When the system retrieves the contractor's drone spatial flight logs from "agri.drone.flight" (无人机飞行记录)
        And the flight log analysis computes the actual sprayed coordinate polygon area as 8.5 hectares
        Then the system flags the invoice verification as "Discrepancy" (数据异常)
        And raises a ValidationError "Billed area exceeds actual flight log area by more than 2.0% tolerance" (计费面积超出实际飞行日志面积，且超过2%容差) to block payment approval
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a service contractor submits a billing invoice for crop pesticide spraying under "purchase.order" (采购订单)',
            'And the contractor claims spraying coverage of 10.0 hectares in their invoice lines',
            'When the system retrieves the contractor\'s drone spatial flight logs from "agri.drone.flight" (无人机飞行记录)',
            'And the flight log analysis computes the actual sprayed coordinate polygon area as 8.5 hectares',
            'Then the system flags the invoice verification as "Discrepancy" (数据异常)',
            'And raises a ValidationError "Billed area exceeds actual flight log area by more than 2.0% tolerance" (计费面积超出实际飞行日志面积，且超过2%容差) to block payment approval'
        ])

    def test_05_contractor_gxp_active_audit_and_certification_gating(self):
        """
        Scenario: Contractor GxP Active Audit and Certification Gating
        Given a high-security chemical spraying service is requested under "agri.field.service" (田间服务记录)
        When a purchase manager attempts to confirm a related purchase order under "purchase.order" (采购订单)
        Then the system checks the contractor partner profile under "res.partner" (业务伙伴) for active GxP chemical certificates
        And if the contractor's GxP certification is expired or missing, the system blocks the confirmation (阻断确认)
        And raises a UserError "Contractor lacks an active GxP certification" (供应商缺少有效的GxP资质证书) to restrict operation
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a high-security chemical spraying service is requested under "agri.field.service" (田间服务记录)',
            'When a purchase manager attempts to confirm a related purchase order under "purchase.order" (采购订单)',
            'Then the system checks the contractor partner profile under "res.partner" (业务伙伴) for active GxP chemical certificates',
            "And if the contractor's GxP certification is expired or missing, the system blocks the confirmation (阻断确认)",
            'And raises a UserError "Contractor lacks an active GxP certification" (供应商缺少有效的GxP资质证书) to restrict operation'
        ])

    def test_06_contractor_purchase_invoice_row_lock_during_quality_penalty_netting(self):
        """
        Scenario: Contractor Purchase Invoice Row Lock during Quality Penalty Netting
        Given an outsourced harvesting service contract under "purchase.order" (采购订单)
        And a draft supplier invoice under model "account.move" (应付账单)
        When the quality inspector validates the quality audit score under model "agri.field.service" (田间服务记录)
        Then the system must acquire a pessimistic database row lock FOR UPDATE (获取行级锁) on both the related purchase order and draft invoice records
        And verify that the contract values have not been modified or cleared by another billing queue
        And raise a ValidationError with code "CONTRACT_INVOICE_LOCKED" (采购账单正在清算处理中，无法获取排他锁) to block the netting transaction if a concurrency lock collision occurs
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an outsourced harvesting service contract under "purchase.order" (采购订单)',
            'And a draft supplier invoice under model "account.move" (应付账单)',
            'When the quality inspector validates the quality audit score under model "agri.field.service" (田间服务记录)',
            'Then the system must acquire a pessimistic database row lock FOR UPDATE (获取行级锁) on both the related purchase order and draft invoice records',
            'And verify that the contract values have not been modified or cleared by another billing queue',
            'And raise a ValidationError with code "CONTRACT_INVOICE_LOCKED" (采购账单正在清算处理中，无法获取排他锁) to block the netting transaction if a concurrency lock collision occurs'
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
