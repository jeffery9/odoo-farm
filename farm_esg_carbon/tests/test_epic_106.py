# -*- coding: utf-8 -*-
from odoo.addons.farm_core.tests.bdd_base import BddTransactionCase
from odoo.exceptions import UserError, ValidationError

class TestEpic106(BddTransactionCase):
    """ BDD Test Suite for Epic 106: Epic 106 Supply Chain Carbon Footprint Tracking (供应链碳足迹追踪) """

    def setUp(self):
        super(TestEpic106, self).setUp()

    def test_01_tractor_scope_1_direct_emissions_audit_compile_1(self):
        """
        Scenario: Tractor Scope 1 Direct Emissions Audit Compile (拖拉机范围1直接排放审计编译)
        Given a fleet tractor mission (车队拖拉机作业任务) under "mrp.workorder" (任务模型) with state "draft" (草稿状态)
        And the vehicle has consumed 50.0 liters of diesel (并且该车辆已消耗50.0升柴油)
        When the workstation operator updates the mission status to "done" (当工作站操作员将任务状态更新为完成状态)
        Then the system must execute compile Scope 1 direct emissions (系统必须执行编译范围1直接排放系统操作) under the proxy model "agri.sc.carbon" (供应链碳足迹追踪模型)
        And calculate emissions using the conversion factor 2.68 kg CO2/L (并使用2.68 kg CO2/L转换因子计算排放量)
        And record a value of 134.0 kg CO2 in "carbon_footprint_kg_co2" (并在碳足迹公斤二氧化碳字段中记录134.0公斤的二氧化碳数值)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a fleet tractor mission (车队拖拉机作业任务) under "mrp.workorder" (任务模型) with state "draft" (草稿状态)',
            'And the vehicle has consumed 50.0 liters of diesel (并且该车辆已消耗50.0升柴油)',
            'When the workstation operator updates the mission status to "done" (当工作站操作员将任务状态更新为完成状态)',
            'Then the system must execute compile Scope 1 direct emissions (系统必须执行编译范围1直接排放系统操作) under the proxy model "agri.sc.carbon" (供应链碳足迹追踪模型)',
            'And calculate emissions using the conversion factor 2.68 kg CO2/L (并使用2.68 kg CO2/L转换因子计算排放量)',
            'And record a value of 134.0 kg CO2 in "carbon_footprint_kg_co2" (并在碳足迹公斤二氧化碳字段中记录134.0公斤的二氧化碳数值)'
        ])

    def test_02_product_carbon_footprint_score_calculation_on_lot(self):
        """
        Scenario: Product Carbon Footprint Score Calculation on Lot (批次产品碳足迹得分计算)
        Given a finished product lot (一个产成品批次) under "stock.lot" (批次模型) with state "draft" (草稿状态)
        And the lot has component trace records in "agri.sc.carbon" (并且该批次在供应链碳足迹追踪模型中具有组件追溯记录)
        When the quality manager requests to dynamically aggregate Scope 1/2/3 carbon footprint data (当质量经理请求执行动态汇总范围1/2/3碳足迹数据系统操作)
        Then the system must evaluate the combined direct and indirect emissions (系统必须评估汇总的直接与间接排放量)
        And transition the lot tracking record state to "confirmed" (并将批次追踪记录的状态过渡到已确认状态)
        And update the emissions class to "emissions_class" of 'A' (并更新排放等级字段为A级)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a finished product lot (一个产成品批次) under "stock.lot" (批次模型) with state "draft" (草稿状态)',
            'And the lot has component trace records in "agri.sc.carbon" (并且该批次在供应链碳足迹追踪模型中具有组件追溯记录)',
            'When the quality manager requests to dynamically aggregate Scope 1/2/3 carbon footprint data (当质量经理请求执行动态汇总范围1/2/3碳足迹数据系统操作)',
            'Then the system must evaluate the combined direct and indirect emissions (系统必须评估汇总的直接与间接排放量)',
            'And transition the lot tracking record state to "confirmed" (并将批次追踪记录的状态过渡到已确认状态)',
            'And update the emissions class to "emissions_class" of 'A' (并更新排放等级字段为A级)'
        ])

    def test_03_prohibited_nonorganic_fertilizer_esg_penalty_block_esg(self):
        """
        Scenario: Prohibited Non-Organic Fertilizer ESG Penalty Block (禁用非有机化肥ESG惩罚拦截)
        Given a field mission (一个大田作业任务) under "mrp.workorder" (任务模型)
        When the operator records a synthetic fertilizer application log (当操作员记录施用合成化肥日志时)
        Then the compliance engine must execute apply heavy penalty and restrict premium labeling (系统必须执行施加重度处罚扣减40分并限制优质标签系统操作) under "agri.sc.carbon" (供应链碳足迹追踪模型)
        And deduct 40.0 points from "esg_score_points" (并从ESG评分点字段中扣除40.0分)
        And raise a ValidationError (并抛出验证错误) with message "Prohibited synthetic fertilizer detected. ESG penalty applied." (包含提示“检测到禁用合成化肥。已施加ESG处罚。”的验证错误消息)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a field mission (一个大田作业任务) under "mrp.workorder" (任务模型)',
            'When the operator records a synthetic fertilizer application log (当操作员记录施用合成化肥日志时)',
            'Then the compliance engine must execute apply heavy penalty and restrict premium labeling (系统必须执行施加重度处罚扣减40分并限制优质标签系统操作) under "agri.sc.carbon" (供应链碳足迹追踪模型)',
            'And deduct 40.0 points from "esg_score_points" (并从ESG评分点字段中扣除40.0分)',
            'And raise a ValidationError (并抛出验证错误) with message "Prohibited synthetic fertilizer detected. ESG penalty applied." (包含提示“检测到禁用合成化肥。已施加ESG处罚。”的验证错误消息)'
        ])

    def test_04_scope_2_electricity_indirect_emissions_compilation_2(self):
        """
        Scenario: Scope 2 Electricity Indirect Emissions Compilation (范围2电力间接排放编译)
        Given a water pump station under "stock.location" (库位模型) with active energy monitoring (具有启用的电能监控)
        And the energy meter logs electricity consumption of 200.0 kWh in "electricity_kwh" (且电表在用电量千瓦时字段中记录了200.0千瓦时的用电量)
        When the system runs the carbon footprint compiler under "agri.sc.carbon" (当系统在供应链碳足迹追踪模型下运行碳排放编译器时)
        Then the compliance engine must execute multiply kWh by regional grid emission factors (合规引擎必须执行用电量乘区域电网排放因子系统操作)
        And save the calculated Scope 2 indirect emissions of 105.0 kg CO2 in "carbon_footprint_kg_co2" (并将计算出的105.0公斤二氧化碳范围2间接排放量保存到碳足迹公斤二氧化碳字段中)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a water pump station under "stock.location" (库位模型) with active energy monitoring (具有启用的电能监控)',
            'And the energy meter logs electricity consumption of 200.0 kWh in "electricity_kwh" (且电表在用电量千瓦时字段中记录了200.0千瓦时的用电量)',
            'When the system runs the carbon footprint compiler under "agri.sc.carbon" (当系统在供应链碳足迹追踪模型下运行碳排放编译器时)',
            'Then the compliance engine must execute multiply kWh by regional grid emission factors (合规引擎必须执行用电量乘区域电网排放因子系统操作)',
            'And save the calculated Scope 2 indirect emissions of 105.0 kg CO2 in "carbon_footprint_kg_co2" (并将计算出的105.0公斤二氧化碳范围2间接排放量保存到碳足迹公斤二氧化碳字段中)'
        ])

    def test_05_carbon_neutral_offset_credit_allocation(self):
        """
        Scenario: Carbon Neutral Offset Credit Allocation (碳中和抵消额度分配)
        Given a harvested crop lot (一个已收获作物批次) under "stock.lot" (批次模型) with state "confirmed" (已确认状态)
        And the soil parcel has 120.0 kg of carbon offset credits in "carbon_offset_credits" (且土壤地块在碳抵消额度字段中具有120.0公斤的碳抵消额度)
        When the compliance manager executes allocate carbon credits to reduce product-level carbon footprints (当合规经理执行分配碳额度以降低产品级碳足迹系统操作) under "agri.sc.carbon" (供应链碳足迹追踪模型)
        Then the net carbon footprint must be reduced proportionally (系统必须按比例扣减净碳足迹)
        And the proxy carbon tracking state must be updated to "done" (并且代理碳排放追踪状态必须更新为完成状态)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a harvested crop lot (一个已收获作物批次) under "stock.lot" (批次模型) with state "confirmed" (已确认状态)',
            'And the soil parcel has 120.0 kg of carbon offset credits in "carbon_offset_credits" (且土壤地块在碳抵消额度字段中具有120.0公斤的碳抵消额度)',
            'When the compliance manager executes allocate carbon credits to reduce product-level carbon footprints (当合规经理执行分配碳额度以降低产品级碳足迹系统操作) under "agri.sc.carbon" (供应链碳足迹追踪模型)',
            'Then the net carbon footprint must be reduced proportionally (系统必须按比例扣减净碳足迹)',
            'And the proxy carbon tracking state must be updated to "done" (并且代理碳排放追踪状态必须更新为完成状态)'
        ])

    def test_06_scope_3_supply_chain_limit_override_block_3(self):
        """
        Scenario: Scope 3 Supply Chain Limit Override Block (范围3供应链排放限额重载拦截)
        Given a product tracking record under "agri.sc.carbon" (供应链碳足迹追踪模型) with Scope 3 emissions exceeding limit
        And the associated picking under "stock.picking" (库存调拨模型) has status "assigned" (已保留/准备就绪)
        When the logistics manager attempts to execute override request via action "action_approve_override" (批准超载动作)
        Then the system blocks the override execution
        And raises a ValidationError (验证错误) "ValidationError: Scope 3 carbon override rejected (验证错误：范围3碳超载申请被拒绝)"
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a product tracking record under "agri.sc.carbon" (供应链碳足迹追踪模型) with Scope 3 emissions exceeding limit',
            'And the associated picking under "stock.picking" (库存调拨模型) has status "assigned" (已保留/准备就绪)',
            'When the logistics manager attempts to execute override request via action "action_approve_override" (批准超载动作)',
            'Then the system blocks the override execution',
            'And raises a ValidationError (验证错误) "ValidationError: Scope 3 carbon override rejected (验证错误：范围3碳超载申请被拒绝)"'
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
