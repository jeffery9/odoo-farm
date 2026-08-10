# -*- coding: utf-8 -*-
from odoo.addons.farm_core.tests.bdd_base import BddTransactionCase
from odoo.exceptions import UserError, ValidationError

class TestEpic067(BddTransactionCase):
    """ BDD Test Suite for Epic 067: Epic 067 Agri OPE Intelligence (农业运行智能) """

    def setUp(self):
        super(TestEpic067, self).setUp()

    def test_01_workstation_overall_equipment_effectiveness_oee_analysis_oee(self):
        """
        Scenario: Workstation Overall Equipment Effectiveness OEE Analysis (工作站全局设备效率OEE分析)
        Given active sorting line machinery registered under "agri.ope.analytics" (农业运行分析模型)
        When the system runs the monthly OEE calculation (执行月度OEE计算) on "res.company" (公司模型)
        Then the system must compute the Overall Equipment Effectiveness score based on "availability * performance * quality" (可用性 * 表现性 * 质量)
        And log the resulting OEE score (记录生成的OEE分数) on the company dashboard "res.company" (公司仪表板) for real-time visibility
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given active sorting line machinery registered under "agri.ope.analytics" (农业运行分析模型)',
            'When the system runs the monthly OEE calculation (执行月度OEE计算) on "res.company" (公司模型)',
            'Then the system must compute the Overall Equipment Effectiveness score based on "availability * performance * quality" (可用性 * 表现性 * 质量)',
            'And log the resulting OEE score (记录生成的OEE分数) on the company dashboard "res.company" (公司仪表板) for real-time visibility'
        ])

    def test_02_automatic_machinery_downtime_tracking(self):
        """
        Scenario: Automatic Machinery Downtime Tracking (自动机械停机时间追踪)
        Given a packing line workcenter "mrp.workcenter" (工作中心) equipped with active PLC stop sensors
        When the sensors log a continuous stop duration greater than "5 minutes" (持续停机时间大于5分钟)
        Then the system must automatically generate an unscheduled downtime record in "agri.ope.analytics" (农业运行分析模型) with state set to "draft" (草稿)
        And prompt the operator via a PWA notification to select a downtime reason code "downtime_reason_id" (停机原因代码)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a packing line workcenter "mrp.workcenter" (工作中心) equipped with active PLC stop sensors',
            'When the sensors log a continuous stop duration greater than "5 minutes" (持续停机时间大于5分钟)',
            'Then the system must automatically generate an unscheduled downtime record in "agri.ope.analytics" (农业运行分析模型) with state set to "draft" (草稿)',
            'And prompt the operator via a PWA notification to select a downtime reason code "downtime_reason_id" (停机原因代码)'
        ])

    def test_03_harvesting_labor_productivity_index(self):
        """
        Scenario: Harvesting Labor Productivity Index (收获劳动生产率指数)
        Given closed harvesting campaigns with logged timesheets under "account.analytic.line" (分析工时单行)
        And total harvested crop mass recorded on the output stock lot "stock.lot" (库存批次)
        When the analytics engine (分析引擎) runs the labor rollup calculation
        Then the system must calculate the operator labor productivity index as "kilograms harvested per hour" (每小时收获的千克数) in "agri.ope.analytics" (农业运行分析模型)
        And display the labor rankings on the supervisor dashboard (在主管仪表板上显示劳动效率排名)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given closed harvesting campaigns with logged timesheets under "account.analytic.line" (分析工时单行)',
            'And total harvested crop mass recorded on the output stock lot "stock.lot" (库存批次)',
            'When the analytics engine (分析引擎) runs the labor rollup calculation',
            'Then the system must calculate the operator labor productivity index as "kilograms harvested per hour" (每小时收获的千克数) in "agri.ope.analytics" (农业运行分析模型)',
            'And display the labor rankings on the supervisor dashboard (在主管仪表板上显示劳动效率排名)'
        ])

    def test_04_operational_bottleneck_wip_pressure_warnings(self):
        """
        Scenario: Operational Bottleneck WIP Pressure Warnings (运行瓶颈在制品队列压力警告)
        Given a multi-stage vegetable processing line with sorting and washing workcenters "mrp.workcenter" (工作中心)
        When the work-in-progress "WIP" queue size in the sorting workstation exceeds maximum capacity by "30%" (在制品排队大小超过最大容量的30%) while the washing workstation is idle (空闲)
        Then the system must trigger a visual yellow warning alert (黄色视觉警告警报) on "agri.ope.analytics" (农业运行分析模型)
        And flag the sorting workstation status as "bottleneck" (瓶颈) on the live production flow monitor
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a multi-stage vegetable processing line with sorting and washing workcenters "mrp.workcenter" (工作中心)',
            'When the work-in-progress "WIP" queue size in the sorting workstation exceeds maximum capacity by "30%" (在制品排队大小超过最大容量的30%) while the washing workstation is idle (空闲)',
            'Then the system must trigger a visual yellow warning alert (黄色视觉警告警报) on "agri.ope.analytics" (农业运行分析模型)',
            'And flag the sorting workstation status as "bottleneck" (瓶颈) on the live production flow monitor'
        ])

    def test_05_fuel_resource_efficiency_analytics(self):
        """
        Scenario: Fuel Resource Efficiency Analytics (燃料资源效率分析)
        Given fleet tractor GPS telemetry and fuel levels integrated under "agri.ope.analytics" (农业运行分析模型)
        When the cost accounting engine compiles crop parcel operating costs for a harvesting season
        Then the system must calculate tractor fuel efficiency metrics in "Liters consumed per hectare worked" (每工作公顷消耗的升数)
        And log the resource KPI on the parcel cost ledger (在土地分块成本账簿上记录该资源关键绩效指标)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given fleet tractor GPS telemetry and fuel levels integrated under "agri.ope.analytics" (农业运行分析模型)',
            'When the cost accounting engine compiles crop parcel operating costs for a harvesting season',
            'Then the system must calculate tractor fuel efficiency metrics in "Liters consumed per hectare worked" (每工作公顷消耗的升数)',
            'And log the resource KPI on the parcel cost ledger (在土地分块成本账簿上记录该资源关键绩效指标)'
        ])

    def test_06_autonomous_harvester_battery_failsafe_mission_suspense(self):
        """
        Scenario: Autonomous Harvester Battery Failsafe Mission Suspense (自主收获机器人电池失效任务挂起)
        Given an autonomous harvesting robotics device "iiot.device" (智能物联网设备) active in the field
        When the robotics device registers an active battery level dropping below "20.0%" (电池电量跌破20.0%) during a harvesting mission "mrp.workorder" (作业任务)
        Then the system must automatically pause the mission "mrp.workorder" (作业任务) and transition its status to "blocked" (已阻断)
        And trigger an automated safe docking station return protocol to prevent dead battery field recovery
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an autonomous harvesting robotics device "iiot.device" (智能物联网设备) active in the field',
            'When the robotics device registers an active battery level dropping below "20.0%" (电池电量跌破20.0%) during a harvesting mission "mrp.workorder" (作业任务)',
            'Then the system must automatically pause the mission "mrp.workorder" (作业任务) and transition its status to "blocked" (已阻断)',
            'And trigger an automated safe docking station return protocol to prevent dead battery field recovery'
        ])

    def test_07_esg_carbon_limit_excess_supply_chain_gating_block(self):
        """
        Scenario: ESG Carbon Limit Excess Supply Chain Gating Block (碳排放配方超限集成供应链硬性拦截机制)
        Given a supply chain transfer plan registered in "stock.picking" (库存拣货模型) with carbon footprint tracked in "agri.esg.ledger" (ESG碳排放账簿模型)
        When the calculated emission of the shipment exceeds the allotted carbon quota "carbon_quota" (当该笔运输计划计算出的总碳排放量超过分配的碳排放配额字段值时)
        Then the supply chain gateway must automatically freeze the shipping state and block validation (供应链网关必须自动冻结该拣货单状态并强行拦截校验操作)
        And raise a ValidationError (并且系统抛出验证错误) with message "CARBON_QUOTA_EXCEEDED_SHIPMENT_BLOCKED" (包含"碳排放指标超支，拣货单自动锁定阻断"提示信息)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a supply chain transfer plan registered in "stock.picking" (库存拣货模型) with carbon footprint tracked in "agri.esg.ledger" (ESG碳排放账簿模型)',
            'When the calculated emission of the shipment exceeds the allotted carbon quota "carbon_quota" (当该笔运输计划计算出的总碳排放量超过分配的碳排放配额字段值时)',
            'Then the supply chain gateway must automatically freeze the shipping state and block validation (供应链网关必须自动冻结该拣货单状态并强行拦截校验操作)',
            'And raise a ValidationError (并且系统抛出验证错误) with message "CARBON_QUOTA_EXCEEDED_SHIPMENT_BLOCKED" (包含"碳排放指标超支，拣货单自动锁定阻断"提示信息)'
        ])
