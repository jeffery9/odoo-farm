# -*- coding: utf-8 -*-
from odoo.addons.farm_core.tests.bdd_base import BddTransactionCase
from odoo.exceptions import UserError, ValidationError

class TestEpic130(BddTransactionCase):
    """ BDD Test Suite for Epic 130: Epic 130 Regenerative Agriculture & Soil Microbiome (再生农业与土壤微生物组生态修复管理体系) """

    def setUp(self):
        super(TestEpic130, self).setUp()

    def test_01_regenerative_som_and_fungitobacteria_ratio_checks(self):
        """
        Scenario: Regenerative SOM and Fungi-to-Bacteria Ratio checks (再生农业土壤有机质与真细菌比例核验与跟踪机制)
        Given soil parcel records managed under "stock.location" (库存库位模型)
        And the parcel registry is linked to soil health tracking under "agri.regenerative.soil" (再生农业土壤微生物模型)
        And the current soil organic matter "soil_organic_matter_som" is 4.5% (且当前土壤有机质比例字段值为4.5%)
        And the fungi-to-bacteria ratio "fungi_bacteria_ratio" is 1.2 (且当前真菌与细菌数量比例字段值为1.2)
        When a soil scientist logs a laboratory audit record (当土壤科学家登记实验室审计记录时)
        Then the system must update the regenerative score "soil_regen_score" to 85.0 on "agri.regenerative.soil" (系统必须在再生农业土壤微生物模型上将土壤再生综合评分字段值更新为85.0)
        And log an audit trail entry in "mail.message" (邮件消息模型) for compliance history (并在邮件消息模型中记录一条合规历史审计日志)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given soil parcel records managed under "stock.location" (库存库位模型)',
            'And the parcel registry is linked to soil health tracking under "agri.regenerative.soil" (再生农业土壤微生物模型)',
            'And the current soil organic matter "soil_organic_matter_som" is 4.5% (且当前土壤有机质比例字段值为4.5%)',
            'And the fungi-to-bacteria ratio "fungi_bacteria_ratio" is 1.2 (且当前真菌与细菌数量比例字段值为1.2)',
            'When a soil scientist logs a laboratory audit record (当土壤科学家登记实验室审计记录时)',
            'Then the system must update the regenerative score "soil_regen_score" to 85.0 on "agri.regenerative.soil" (系统必须在再生农业土壤微生物模型上将土壤再生综合评分字段值更新为85.0)',
            'And log an audit trail entry in "mail.message" (邮件消息模型) for compliance history (并在邮件消息模型中记录一条合规历史审计日志)'
        ])

    def test_02_prohibited_nonorganic_fertilizer_esg_penalty_block_esg(self):
        """
        Scenario: Prohibited Non-Organic Fertilizer ESG Penalty Block (禁用非有机化肥施用导致ESG评分扣减与高级品牌标识拦截机制)
        Given soil parcel records managed under "stock.location" (库存库位模型) and "agri.regenerative.soil" (再生农业土壤微生物模型)
        And the active regenerative rating "soil_regen_score" is 92.0 (且当前活跃的土壤再生综合评分字段值为92.0)
        When an agronomist attempts to log a synthetic fertilizer application "fertilizer_type" as "synthetic_nitrogen" (当农艺师尝试将施肥类型字段值登记为化学合成氮肥时)
        Then the validation engine must apply an immediate ESG score penalty of 40.0 points (系统验证引擎必须立即应用40.0分的ESG评分扣减惩罚)
        And update the "soil_regen_score" to 52.0 on "agri.regenerative.soil" (并相应地在再生农业土壤微生物模型上将土壤再生综合评分字段值更新为52.0)
        And restrict the premium regenerative certification brand labeling "brand_label_eligible" to "restricted" (并限制优质再生认证品牌标记字段值将其设置为受限状态)
        And raise a ValidationError (系统必须抛出验证错误) with message "Prohibited chemical application on regenerative soil location" (包含"再生农业土壤库位禁止施用化学合成物质"提示信息)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given soil parcel records managed under "stock.location" (库存库位模型) and "agri.regenerative.soil" (再生农业土壤微生物模型)',
            'And the active regenerative rating "soil_regen_score" is 92.0 (且当前活跃的土壤再生综合评分字段值为92.0)',
            'When an agronomist attempts to log a synthetic fertilizer application "fertilizer_type" as "synthetic_nitrogen" (当农艺师尝试将施肥类型字段值登记为化学合成氮肥时)',
            'Then the validation engine must apply an immediate ESG score penalty of 40.0 points (系统验证引擎必须立即应用40.0分的ESG评分扣减惩罚)',
            'And update the "soil_regen_score" to 52.0 on "agri.regenerative.soil" (并相应地在再生农业土壤微生物模型上将土壤再生综合评分字段值更新为52.0)',
            'And restrict the premium regenerative certification brand labeling "brand_label_eligible" to "restricted" (并限制优质再生认证品牌标记字段值将其设置为受限状态)',
            'And raise a ValidationError (系统必须抛出验证错误) with message "Prohibited chemical application on regenerative soil location" (包含"再生农业土壤库位禁止施用化学合成物质"提示信息)'
        ])

    def test_03_evapotranspiration_drip_irrigation_schedule_smart_bypass(self):
        """
        Scenario: Evapotranspiration Drip Irrigation Schedule Smart Bypass (蒸腾蒸发量气象预测滴灌灌溉排程自动自适应调节机制)
        Given daily weather forecast telemetry linked to soil locations under "stock.location" (库存库位模型) and "agri.regenerative.soil" (再生农业土壤微生物模型)
        And the scheduled drip irrigation duration "scheduled_duration_minutes" is 30.0 minutes (且计划的滴灌持续时长字段值为30.0分钟)
        When the microclimate weather station logs daily reference evapotranspiration "et0_forecast" of 6.5 mm (当微气候气象站记录的每日参考蒸发蒸腾量字段值达到6.5毫米时)
        Then the irrigation control scheduler must scale the drip duration to 36.0 minutes (灌溉控制调度程序必须自动按120.0%比例将滴灌持续时长调整为36.0分钟)
        And trigger the physical valve controller signal "valve_signal" status to "adaptive_override" on "agri.regenerative.soil" (并在再生农业土壤微生物模型上将阀门控制信号字段值标记为自适应覆盖状态)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given daily weather forecast telemetry linked to soil locations under "stock.location" (库存库位模型) and "agri.regenerative.soil" (再生农业土壤微生物模型)',
            'And the scheduled drip irrigation duration "scheduled_duration_minutes" is 30.0 minutes (且计划的滴灌持续时长字段值为30.0分钟)',
            'When the microclimate weather station logs daily reference evapotranspiration "et0_forecast" of 6.5 mm (当微气候气象站记录的每日参考蒸发蒸腾量字段值达到6.5毫米时)',
            'Then the irrigation control scheduler must scale the drip duration to 36.0 minutes (灌溉控制调度程序必须自动按120.0%比例将滴灌持续时长调整为36.0分钟)',
            'And trigger the physical valve controller signal "valve_signal" status to "adaptive_override" on "agri.regenerative.soil" (并在再生农业土壤微生物模型上将阀门控制信号字段值标记为自适应覆盖状态)'
        ])

    def test_04_tractor_scope_1_direct_emissions_audit_compile_scope_1(self):
        """
        Scenario: Tractor Scope 1 Direct Emissions Audit Compile (拖拉机田间作业任务Scope 1直接碳排放遥测自动核算与汇总机制)
        Given fleet tractor missions managed under "mrp.workorder" (作业任务模型) executing field tasks linked to soil locations in "stock.location" (库存库位模型)
        And the fuel consumption logged on completion "fuel_used_liters" is 45.0 L (且作业任务完成时记录的燃油消耗字段值为45.0升)
        When the work order executor completes the tractor mission (当作业执行主管完成该拖拉机作业任务时)
        Then the carbon calculation engine must compile the Scope 1 direct emissions "scope1_co2_kg" as 120.6 kg (碳排放计算引擎必须按每升2.68千克的转换系数将Scope 1直接排放量计算为120.6千克)
        And update the accumulated emission ledger "total_carbon_footprint" in "agri.regenerative.soil" (并且相应更新再生农业土壤微生物模型上的累计碳足迹字段值)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given fleet tractor missions managed under "mrp.workorder" (作业任务模型) executing field tasks linked to soil locations in "stock.location" (库存库位模型)',
            'And the fuel consumption logged on completion "fuel_used_liters" is 45.0 L (且作业任务完成时记录的燃油消耗字段值为45.0升)',
            'When the work order executor completes the tractor mission (当作业执行主管完成该拖拉机作业任务时)',
            'Then the carbon calculation engine must compile the Scope 1 direct emissions "scope1_co2_kg" as 120.6 kg (碳排放计算引擎必须按每升2.68千克的转换系数将Scope 1直接排放量计算为120.6千克)',
            'And update the accumulated emission ledger "total_carbon_footprint" in "agri.regenerative.soil" (并且相应更新再生农业土壤微生物模型上的累计碳足迹字段值)'
        ])

    def test_05_multilevel_cascade_safeguard_deletion_gating(self):
        """
        Scenario: Multi-Level Cascade Safeguard Deletion Gating (多级再生农业微生物土壤资产级联删除安全保护拦截机制)
        Given an active soil microbiome tracking record under "agri.regenerative.soil" (再生农业土壤微生物模型) linked to certified organic land locations in "stock.location" (库存库位模型)
        And there are active pending harvest operations "pending_harvest_count" set to 3 (且当前关联的待处理收获作业次数字段值为3)
        When a user attempts to physically delete the regenerative soil tracking ledger (当用户尝试物理删除该再生农业土壤微生物模型下的记录时)
        Then the cascade protection engine must block the deletion request (系统级联保护引擎必须拦截该删除请求)
        And raise a ValidationError (系统必须抛出验证错误) with message "Cannot delete active soil record with pending harvest operations" (包含"无法删除关联有待处理收获作业的活跃再生农业土壤记录"提示信息)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an active soil microbiome tracking record under "agri.regenerative.soil" (再生农业土壤微生物模型) linked to certified organic land locations in "stock.location" (库存库位模型)',
            'And there are active pending harvest operations "pending_harvest_count" set to 3 (且当前关联的待处理收获作业次数字段值为3)',
            'When a user attempts to physically delete the regenerative soil tracking ledger (当用户尝试物理删除该再生农业土壤微生物模型下的记录时)',
            'Then the cascade protection engine must block the deletion request (系统级联保护引擎必须拦截该删除请求)',
            'And raise a ValidationError (系统必须抛出验证错误) with message "Cannot delete active soil record with pending harvest operations" (包含"无法删除关联有待处理收获作业的活跃再生农业土壤记录"提示信息)'
        ])

    def test_06_soil_microbiome_genetic_bank_conservation_lock_verification(self):
        """
        Scenario: Soil Microbiome Genetic Bank Conservation Lock Verification (土壤益生菌群基因保护库安全封锁校验)
        Given a rare microbial strain lot under "stock.lot" (批次模型) linked to a soil quality record under "agri.regenerative.soil" (再生农业土壤微生物模型)
        And the strain has an active biosecurity level "risk_level" set to "restricted" (且该菌株生物安全级别字段值设置为受限级别)
        And the genetic bank conservation lock "is_locked" is true on "agri.regenerative.soil" (且再生农业土壤微生物模型上的基因库保护锁字段值为真)
        When an operator attempts to release a bio-fertilizer shipment under "stock.picking" (当操作员尝试释放库存拣货单模型下的生物活性菌肥出库拣货时)
        Then the validation engine must block the shipment and raise a ValidationError (系统验证引擎必须拦截该出库并抛出验证错误) with message "Microbial strain genetic conservation lock is active" (包含"益生菌株遗传安全保护锁已激活，禁止分发出库"提示信息)
        And reject any corresponding quant modifications under "stock.quant" (并拒绝库存量模型下任何相应的库存数量修改)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a rare microbial strain lot under "stock.lot" (批次模型) linked to a soil quality record under "agri.regenerative.soil" (再生农业土壤微生物模型)',
            'And the strain has an active biosecurity level "risk_level" set to "restricted" (且该菌株生物安全级别字段值设置为受限级别)',
            'And the genetic bank conservation lock "is_locked" is true on "agri.regenerative.soil" (且再生农业土壤微生物模型上的基因库保护锁字段值为真)',
            'When an operator attempts to release a bio-fertilizer shipment under "stock.picking" (当操作员尝试释放库存拣货单模型下的生物活性菌肥出库拣货时)',
            'Then the validation engine must block the shipment and raise a ValidationError (系统验证引擎必须拦截该出库并抛出验证错误) with message "Microbial strain genetic conservation lock is active" (包含"益生菌株遗传安全保护锁已激活，禁止分发出库"提示信息)',
            'And reject any corresponding quant modifications under "stock.quant" (并拒绝库存量模型下任何相应的库存数量修改)'
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
