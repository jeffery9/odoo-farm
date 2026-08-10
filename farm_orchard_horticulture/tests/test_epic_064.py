# -*- coding: utf-8 -*-
from odoo.addons.farm_core.tests.bdd_base import BddTransactionCase
from odoo.exceptions import UserError, ValidationError

class TestEpic064(BddTransactionCase):
    """ BDD Test Suite for Epic 064: Epic 064 Perennial Orchard Mgmt (多年生果园资产管理) """

    def setUp(self):
        super(TestEpic064, self).setUp()

    def test_01_orchard_tree_gis_coordinate_mapping_gis(self):
        """
        Scenario: Orchard Tree GIS Coordinate Mapping (果树GIS空间坐标定位映射)
        Given an orchard parcel (果园地块) "ORCHARD-BLOCK-D" under stock.location (库存位置) with defined polygon boundaries (多边形边界)
        And a perennial tree registration record of model agri.orchard.tree (果树档案) linked to stock.lot (库存批次) "TREE-LOT-5001"
        When the Horticulturist (园艺专家) imports planting logs containing GPS coordinates (GPS种植坐标) "34.0522 N, 118.2437 W"
        Then the system must validate that the coordinates reside within the legal boundaries of "ORCHARD-BLOCK-D"
        And write the coordinates to the spatial fields (空间定位字段) of agri.orchard.tree (果树档案) with status "active (正常)"
        And raise a ValidationError (验证错误): "Coordinates out of parcel boundary (坐标超出地块边界)" and block registration if coordinates reside outside the boundary
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an orchard parcel (果园地块) "ORCHARD-BLOCK-D" under stock.location (库存位置) with defined polygon boundaries (多边形边界)',
            'And a perennial tree registration record of model agri.orchard.tree (果树档案) linked to stock.lot (库存批次) "TREE-LOT-5001"',
            'When the Horticulturist (园艺专家) imports planting logs containing GPS coordinates (GPS种植坐标) "34.0522 N, 118.2437 W"',
            'Then the system must validate that the coordinates reside within the legal boundaries of "ORCHARD-BLOCK-D"',
            'And write the coordinates to the spatial fields (空间定位字段) of agri.orchard.tree (果树档案) with status "active (正常)"',
            'And raise a ValidationError (验证错误): "Coordinates out of parcel boundary (坐标超出地块边界)" and block registration if coordinates reside outside the boundary'
        ])

    def test_02_tree_rootstock_and_scion_lineage_registry(self):
        """
        Scenario: Tree Rootstock and Scion Lineage Registry (果树砧木与接穗嫁接谱系登记)
        Given a new tree lot record under stock.lot (库存批次)
        And a compatibility table under agri.graft.compatibility (嫁接兼容性配置) showing Scion "Gala (嘎啦接穗)" is compatible with Rootstock "M9 (M9砧木)"
        When the Horticulturist (园艺专家) registers a new tree planting lot in agri.orchard.tree (果树档案) specifying Scion variety "Gala" and Rootstock variety "M9"
        Then the system must validate variety compatibility via the grafting rule engine
        And write the graft lineage edge (嫁接谱系关系) in the database with status "verified (已审核)"
        And raise a ValidationError (验证错误): "Incompatible graft combination (嫁接组合不兼容)" if a non-compatible combination is requested
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a new tree lot record under stock.lot (库存批次)',
            'And a compatibility table under agri.graft.compatibility (嫁接兼容性配置) showing Scion "Gala (嘎啦接穗)" is compatible with Rootstock "M9 (M9砧木)"',
            'When the Horticulturist (园艺专家) registers a new tree planting lot in agri.orchard.tree (果树档案) specifying Scion variety "Gala" and Rootstock variety "M9"',
            'Then the system must validate variety compatibility via the grafting rule engine',
            'And write the graft lineage edge (嫁接谱系关系) in the database with status "verified (已审核)"',
            'And raise a ValidationError (验证错误): "Incompatible graft combination (嫁接组合不兼容)" if a non-compatible combination is requested'
        ])

    def test_03_cumulative_harvest_disease_exposure_check(self):
        """
        Scenario: Cumulative Harvest Disease Exposure Check (果树带病采收风险锁定)
        Given an orchard block "ORCHARD-BLOCK-D" of model stock.location (库存位置)
        And multiple trees registered under agri.orchard.tree (果树档案) inside this block have active Fire Blight disease logs (火疫病感染日志) under agri.orchard.disease.log (果园病害日志)
        When a worker attempts to schedule a harvesting workorder of model mrp.workorder (工序工单) targeting "ORCHARD-BLOCK-D"
        Then the system must automatically block harvesting from infected trees
        And raise a ValidationError (验证错误): "Harvest blocked due to active disease infection (因处于活跃病害感染中，采收已锁定)"
        And require prior sanitization audit approval of model agri.organic.audit (农业有机审计) before releasing the harvest lock
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an orchard block "ORCHARD-BLOCK-D" of model stock.location (库存位置)',
            'And multiple trees registered under agri.orchard.tree (果树档案) inside this block have active Fire Blight disease logs (火疫病感染日志) under agri.orchard.disease.log (果园病害日志)',
            'When a worker attempts to schedule a harvesting workorder of model mrp.workorder (工序工单) targeting "ORCHARD-BLOCK-D"',
            'Then the system must automatically block harvesting from infected trees',
            'And raise a ValidationError (验证错误): "Harvest blocked due to active disease infection (因处于活跃病害感染中，采收已锁定)"',
            'And require prior sanitization audit approval of model agri.organic.audit (农业有机审计) before releasing the harvest lock'
        ])

    def test_04_multiyear_pruning_activity_history(self):
        """
        Scenario: Multi-Year Pruning Activity History (多年生修剪活动历史台账)
        Given a perennial orchard tree group of model agri.orchard.tree (果树档案) in stock.lot (库存批次) "TREE-LOT-5001"
        And its tree status is set to "active (正常)"
        When the worker records an annual winter pruning task under agri.orchard.pruning.log (果园修剪日志) with quality code "Spur Thinning (短枝疏剪)" and cut count (修剪数) 15
        Then the system must write the history pruning log with state "completed (已完成)"
        And update the cumulative tree stress rating index (累积果树胁迫评分指数) on the tree record
        And log this transaction in the orchard tree's chatter (沟通记录) for multi-year crop load auditing
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a perennial orchard tree group of model agri.orchard.tree (果树档案) in stock.lot (库存批次) "TREE-LOT-5001"',
            'And its tree status is set to "active (正常)"',
            'When the worker records an annual winter pruning task under agri.orchard.pruning.log (果园修剪日志) with quality code "Spur Thinning (短枝疏剪)" and cut count (修剪数) 15',
            'Then the system must write the history pruning log with state "completed (已完成)"',
            'And update the cumulative tree stress rating index (累积果树胁迫评分指数) on the tree record',
            'And log this transaction in the orchard tree's chatter (沟通记录) for multi-year crop load auditing'
        ])

    def test_05_tree_mortality_replacement_registry(self):
        """
        Scenario: Tree Mortality Replacement Registry (死树核销与补植替代机制)
        Given an orchard block recording tree mortality surveys in agri.orchard.tree (果树档案)
        When the Horticulturist (园艺专家) sets a specific tree status to "Deceased (已死亡)" with cause of death (死因) "Root Rot (根腐病)"
        Then the system must trigger biological asset write-off (生物资产核销)
        And automatically generate a replacement task of model project.task (项目任务) on the operator dashboard
        And pre-select a compatible disease-resistant rootstock variety (预选兼容的抗病砧木品种) "Gisela 6 (吉塞拉6号)" based on soil pathogen logs
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an orchard block recording tree mortality surveys in agri.orchard.tree (果树档案)',
            'When the Horticulturist (园艺专家) sets a specific tree status to "Deceased (已死亡)" with cause of death (死因) "Root Rot (根腐病)"',
            'Then the system must trigger biological asset write-off (生物资产核销)',
            'And automatically generate a replacement task of model project.task (项目任务) on the operator dashboard',
            'And pre-select a compatible disease-resistant rootstock variety (预选兼容的抗病砧木品种) "Gisela 6 (吉塞拉6号)" based on soil pathogen logs'
        ])

    def test_06_uav_swarm_orchard_canopy_pruning_collision_interlock(self):
        """
        Scenario: UAV Swarm Orchard Canopy Pruning Collision Interlock (无人机蜂群果树修剪碰撞安全连锁拦截)
        Given a swarm of autonomous pruning UAVs (自主修剪无人机蜂群) registered under model iiot.device (物联设备)
        And an active pruning mission (活跃的果树修剪任务) "mrp.workorder" (作业任务) targeting tree lot "TREE-LOT-5001" under stock.lot (库存批次)
        When any UAV in the swarm registers battery level dropping below "15.0%" (电量低于15.0%) or a swarm proximity collision alarm (碰撞接近报警) triggers
        Then the system must instantly command the UAV swarm to trigger safe Return-To-Home (触发安全返航) and park
        And transition the mission "mrp.workorder" (作业任务) status to "paused (暂停)" to safeguard perennial tree assets
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a swarm of autonomous pruning UAVs (自主修剪无人机蜂群) registered under model iiot.device (物联设备)',
            'And an active pruning mission (活跃的果树修剪任务) "mrp.workorder" (作业任务) targeting tree lot "TREE-LOT-5001" under stock.lot (库存批次)',
            'When any UAV in the swarm registers battery level dropping below "15.0%" (电量低于15.0%) or a swarm proximity collision alarm (碰撞接近报警) triggers',
            'Then the system must instantly command the UAV swarm to trigger safe Return-To-Home (触发安全返航) and park',
            'And transition the mission "mrp.workorder" (作业任务) status to "paused (暂停)" to safeguard perennial tree assets'
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
            'Given a crop parcel's soil stock lot in "stock.lot" (库存批次模型) with crop variety "Rose" (且作物物种已设置为玫瑰)',
            'And a smart evapotranspiration sensor registered in "iiot.device" (并且智能蒸腾量传感器已注册在工业物联网设备模型中)',
            'When the soil sensor logs an NPK reading drift of 25.0% (当土壤传感器记录到氮磷钾读数偏离比比例达到25.0%时)',
            'Then the system must trigger safe mode self-correction (系统必须自动执行安全模式自校准动作)',
            'And scale back the water drip runtime "drip_duration" to fallback 10.0 minutes (并且将滴灌时长字段值等比例缩减至备用时长值10.0分钟)',
            'And raise a ValidationError (并且系统抛出验证错误) with message "CRITICAL_SENSOR_DRIFT_DETECTED" (包含"传感器发生严重漂移，进入自愈模式"提示信息)'
        ])
