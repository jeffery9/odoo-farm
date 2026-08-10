# -*- coding: utf-8 -*-
from odoo.addons.farm_core.tests.bdd_base import BddTransactionCase
from odoo.exceptions import UserError, ValidationError

class TestEpic132(BddTransactionCase):
    """ BDD Test Suite for Epic 132: Epic 132 Agrivoltaics & Energy Microgrids (农光互补与能源微电网) """

    def setUp(self):
        super(TestEpic132, self).setUp()

    def test_01_solar_panel_tilt_solar_generation_kwh_tracking(self):
        """
        Scenario: Solar Panel Tilt solar generation kWh tracking (光伏农场面板倾角与发电量指标跟踪)
        Given a solar crop parcel under "stock.location" (库存位置模型) linked to an agrivoltaics grid record under "agri.agrivoltaics.grid" (农光互补网格记录模型)
        And the panel tilt angle "tilt_angle" is set to 35.0 degrees (且面板倾角字段值设置为35.0度)
        When the IoT inverter logs a power generation "generation_kwh" of 250.0 kWh (当物联网逆变器记录的发电量字段值为250.0千瓦时时)
        Then the system must calculate and update the total green energy generated "total_generation" on "agri.agrivoltaics.grid" (系统必须计算并在农光互补网格记录模型上更新总发电量字段值)
        And log the microgrid status "grid_status" as "optimal" (并记录微电网状态字段值为最佳状态)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a solar crop parcel under "stock.location" (库存位置模型) linked to an agrivoltaics grid record under "agri.agrivoltaics.grid" (农光互补网格记录模型)',
            'And the panel tilt angle "tilt_angle" is set to 35.0 degrees (且面板倾角字段值设置为35.0度)',
            'When the IoT inverter logs a power generation "generation_kwh" of 250.0 kWh (当物联网逆变器记录的发电量字段值为250.0千瓦时时)',
            'Then the system must calculate and update the total green energy generated "total_generation" on "agri.agrivoltaics.grid" (系统必须计算并在农光互补网格记录模型上更新总发电量字段值)',
            'And log the microgrid status "grid_status" as "optimal" (并记录微电网状态字段值为最佳状态)'
        ])

    def test_02_scope_2_electricity_indirect_emissions_compilation_2(self):
        """
        Scenario: Scope 2 Electricity indirect Emissions Compilation (范围2电力间接碳排放计算)
        Given a water pump location under "stock.location" (库存位置模型) linked to "agri.agrivoltaics.grid" (农光互补网格记录模型)
        And the electricity consumption meter logs a usage "electricity_kwh" of 120.0 kWh (且电耗计量表记录的用电量字段值为120.0千瓦时)
        When the compliance engine compiles the monthly indirect emissions (当合规引擎编译月度间接碳排放时)
        Then the system must multiply the electricity consumption by the regional grid factor "grid_emission_factor" of 0.52 kg CO2/kWh (系统必须将用电量乘以0.52公斤二氧化碳每千瓦时的区域电网排放因子)
        And write the calculated Scope 2 carbon footprint "scope_2_emissions" of 62.4 kg CO2 (并在农光互补网格记录模型上写入计算出的62.4公斤二氧化碳的范围2碳足迹字段值)
        And transition the emission record state "state" to "audited" (并更新排放记录状态字段值为已审计状态)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a water pump location under "stock.location" (库存位置模型) linked to "agri.agrivoltaics.grid" (农光互补网格记录模型)',
            'And the electricity consumption meter logs a usage "electricity_kwh" of 120.0 kWh (且电耗计量表记录的用电量字段值为120.0千瓦时)',
            'When the compliance engine compiles the monthly indirect emissions (当合规引擎编译月度间接碳排放时)',
            'Then the system must multiply the electricity consumption by the regional grid factor "grid_emission_factor" of 0.52 kg CO2/kWh (系统必须将用电量乘以0.52公斤二氧化碳每千瓦时的区域电网排放因子)',
            'And write the calculated Scope 2 carbon footprint "scope_2_emissions" of 62.4 kg CO2 (并在农光互补网格记录模型上写入计算出的62.4公斤二氧化碳的范围2碳足迹字段值)',
            'And transition the emission record state "state" to "audited" (并更新排放记录状态字段值为已审计状态)'
        ])

    def test_03_evapotranspiration_drip_irrigation_schedule_smart_bypass(self):
        """
        Scenario: Evapotranspiration Drip Irrigation Schedule Smart Bypass (基于蒸腾量预测的智能滴灌计划旁路自适应调整)
        Given a crop field location under "stock.location" (库存位置模型) managed under "agri.agrivoltaics.grid" (农光互补网格记录模型)
        And the daily reference evapotranspiration ET0 forecast is 6.5 mm (且日参考作物蒸腾量预测值为6.5毫米)
        When the automated irrigation scheduler processes the daily water missions under "mrp.workorder" (作业任务模型) (当自动灌溉调度器处理每日水利作业任务模型中的记录时)
        Then the system must scale the irrigation watering duration "duration" by 120.0% (系统必须将灌溉浇水时长字段值按120.0%比例放大)
        And update the microgrid water conservation status "conservation_status" to "bypass_active" (并在农光互补网格记录模型上更新水资源保护状态字段值为旁路生效状态)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a crop field location under "stock.location" (库存位置模型) managed under "agri.agrivoltaics.grid" (农光互补网格记录模型)',
            'And the daily reference evapotranspiration ET0 forecast is 6.5 mm (且日参考作物蒸腾量预测值为6.5毫米)',
            'When the automated irrigation scheduler processes the daily water missions under "mrp.workorder" (作业任务模型) (当自动灌溉调度器处理每日水利作业任务模型中的记录时)',
            'Then the system must scale the irrigation watering duration "duration" by 120.0% (系统必须将灌溉浇水时长字段值按120.0%比例放大)',
            'And update the microgrid water conservation status "conservation_status" to "bypass_active" (并在农光互补网格记录模型上更新水资源保护状态字段值为旁路生效状态)'
        ])

    def test_04_circular_biomass_cost_offset_credit_allocation(self):
        """
        Scenario: Circular Biomass Cost Offset Credit Allocation (循环经济生物质能成本抵消碳信用分配)
        Given a biomass crop waste transfer under "stock.move" (库存移动模型) from field locations to biogas digestors (且该移动属于从大田位置到沼气池的农作物废弃物移动)
        And the verified biomass waste weight is 1500.0 kg (且经验证的生物质废弃物重量为1500.0公斤)
        When the compliance manager validates the circular economy transfer transaction (当合规经理验证该循环经济转移交易时)
        Then the system must calculate and allocate an ESG carbon offset credit "offset_credits" of 120.0 points (系统必须计算并分配120.0分值的ESG碳抵消信用额度字段值)
        And post the offset value to reduce energy operating expenses on "agri.agrivoltaics.grid" (并在农光互补网格记录模型上入账抵消价值以降低能源运营成本)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a biomass crop waste transfer under "stock.move" (库存移动模型) from field locations to biogas digestors (且该移动属于从大田位置到沼气池的农作物废弃物移动)',
            'And the verified biomass waste weight is 1500.0 kg (且经验证的生物质废弃物重量为1500.0公斤)',
            'When the compliance manager validates the circular economy transfer transaction (当合规经理验证该循环经济转移交易时)',
            'Then the system must calculate and allocate an ESG carbon offset credit "offset_credits" of 120.0 points (系统必须计算并分配120.0分值的ESG碳抵消信用额度字段值)',
            'And post the offset value to reduce energy operating expenses on "agri.agrivoltaics.grid" (并在农光互补网格记录模型上入账抵消价值以降低能源运营成本)'
        ])

    def test_05_multilevel_cascade_safeguard_deletion_gating(self):
        """
        Scenario: Multi-Level Cascade Safeguard Deletion Gating (有源光伏作物位置多级级联删除安全保护拦截)
        Given an active agrivoltaics grid record under "agri.agrivoltaics.grid" (农光互补网格记录模型) linked to a physical solar crop parcel location under "stock.location" (库存位置模型)
        And the location is currently assigned to a running irrigation mission under "mrp.workorder" (作业任务模型) (且该位置当前已被分配至一个运行中的作业任务模型中)
        When the administrator attempts to delete the agrivoltaics grid record under "agri.agrivoltaics.grid" (当管理员尝试删除该农光互补网格记录模型上的记录时)
        Then the system must trigger cascade deletion gating and raise a ValidationError (系统必须触发级联删除保护拦截并抛出验证错误) with message "Cannot delete agrivoltaics grid linked to active locations" (包含"无法删除关联了有源位置的农光互补网格"提示信息)
        And reject the deletion, maintaining database reference integrity (并且拒绝删除，维护数据库引用完整性)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an active agrivoltaics grid record under "agri.agrivoltaics.grid" (农光互补网格记录模型) linked to a physical solar crop parcel location under "stock.location" (库存位置模型)',
            'And the location is currently assigned to a running irrigation mission under "mrp.workorder" (作业任务模型) (且该位置当前已被分配至一个运行中的作业任务模型中)',
            'When the administrator attempts to delete the agrivoltaics grid record under "agri.agrivoltaics.grid" (当管理员尝试删除该农光互补网格记录模型上的记录时)',
            'Then the system must trigger cascade deletion gating and raise a ValidationError (系统必须触发级联删除保护拦截并抛出验证错误) with message "Cannot delete agrivoltaics grid linked to active locations" (包含"无法删除关联了有源位置的农光互补网格"提示信息)',
            'And reject the deletion, maintaining database reference integrity (并且拒绝删除，维护数据库引用完整性)'
        ])

    def test_06_microgrid_cogeneration_clearing_margin_limit_enforcement(self):
        """
        Scenario: Microgrid Co-Generation Clearing Margin Limit Enforcement (微电网联合发电清算保证金限额合规核验)
        Given a microgrid energy trading account under "sale.order" (销售订单模型) linked to "agri.agrivoltaics.grid" (农光互补网格记录模型)
        And the co-generation contract required clearing margin limit "clearing_margin_limit" is 8000.0 USD (且联合发电合同要求的最低清算保证金限额字段值为8000.0美元)
        And the current active grid account ledger balance "margin_balance" is 6500.0 USD (且当前微电网账户实际保证金余额字段值为6500.0美元)
        When the grid controller attempts to process a co-generation energy sale to the main grid (当电网控制器尝试对大电网执行并网发电销售结算时)
        Then the financial system must block the settlement process under "account.move" (系统财务引擎必须拦截会计分录模型下的交易清算)
        And raise a ValidationError (系统必须抛出验证错误) with message "Microgrid account balance is below required co-generation safety margin" (包含"微电网账户余额低于要求的联合发电安全保证金限额"提示信息)
        And maintain the microgrid status "grid_status" as "optimal" (并保持微电网状态字段值为最佳状态)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a microgrid energy trading account under "sale.order" (销售订单模型) linked to "agri.agrivoltaics.grid" (农光互补网格记录模型)',
            'And the co-generation contract required clearing margin limit "clearing_margin_limit" is 8000.0 USD (且联合发电合同要求的最低清算保证金限额字段值为8000.0美元)',
            'And the current active grid account ledger balance "margin_balance" is 6500.0 USD (且当前微电网账户实际保证金余额字段值为6500.0美元)',
            'When the grid controller attempts to process a co-generation energy sale to the main grid (当电网控制器尝试对大电网执行并网发电销售结算时)',
            'Then the financial system must block the settlement process under "account.move" (系统财务引擎必须拦截会计分录模型下的交易清算)',
            'And raise a ValidationError (系统必须抛出验证错误) with message "Microgrid account balance is below required co-generation safety margin" (包含"微电网账户余额低于要求的联合发电安全保证金限额"提示信息)',
            'And maintain the microgrid status "grid_status" as "optimal" (并保持微电网状态字段值为最佳状态)'
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
