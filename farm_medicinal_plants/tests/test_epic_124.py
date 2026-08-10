# -*- coding: utf-8 -*-
from odoo.addons.farm_core.tests.bdd_base import BddTransactionCase
from odoo.exceptions import UserError, ValidationError

class TestEpic124(BddTransactionCase):
    """ BDD Test Suite for Epic 124: Epic 124 Medicinal Herbs Processing (中药材与炮制管理) """

    def setUp(self):
        super(TestEpic124, self).setUp()

    def test_01_gmp_certified_herb_extraction_active_temperature_gating_gmp(self):
        """
        Scenario: GMP Certified Herb Extraction active temperature Gating (GMP认证药材提取温度主动阈值管控)
        Given an extraction run under "mrp.production" (制造订单模型) linked to a GMP compliance log under "agri.herbs.gmp" (中药材认证运行记录模型)
        And the extraction run state "state" is "progress" (且制造订单状态字段值为进行中状态)
        When the sensor logs an extraction temperature "extraction_temp" of 72.0°C (当传感器记录的提取温度字段值为72.0°C时)
        Then the compliance engine must flag the run as out of tolerance (合规引擎必须将该批次运行标记为超出容差状态)
        And log an alert message "alert_message" containing "Temperature out of safe 75-85°C range" in "agri.herbs.gmp" (并在中药材认证运行记录模型上记录"温度超出75-85°C安全范围"的警告信息字段值)
        And automatically log a QC variance activity under "mail.activity" (并在邮件活动模型下自动记录一条质检偏差活动)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an extraction run under "mrp.production" (制造订单模型) linked to a GMP compliance log under "agri.herbs.gmp" (中药材认证运行记录模型)',
            'And the extraction run state "state" is "progress" (且制造订单状态字段值为进行中状态)',
            'When the sensor logs an extraction temperature "extraction_temp" of 72.0°C (当传感器记录的提取温度字段值为72.0°C时)',
            'Then the compliance engine must flag the run as out of tolerance (合规引擎必须将该批次运行标记为超出容差状态)',
            'And log an alert message "alert_message" containing "Temperature out of safe 75-85°C range" in "agri.herbs.gmp" (并在中药材认证运行记录模型上记录"温度超出75-85°C安全范围"的警告信息字段值)',
            'And automatically log a QC variance activity under "mail.activity" (并在邮件活动模型下自动记录一条质检偏差活动)'
        ])

    def test_02_active_bioactive_compound_concentration_brix_validations(self):
        """
        Scenario: Active Bioactive Compound Concentration brix validations (活性成分浓度糖度值及品质合规校验)
        Given a harvested batch herb lot extract evaluation under "stock.lot" (批次模型) linked to a compliance run under "agri.herbs.gmp" (中药材认证运行记录模型)
        And the lab results state "state" is "evaluated" (且化验结果状态字段值为已评估状态)
        When the chemical laboratory logs a brix result "active_brix" of 14.5% (当化验室记录的活性成分糖度值字段值为14.5%时)
        Then the quality engine must block premium brand labeling for the product (质量引擎必须拦截对该产品的优质品牌贴标)
        And update the label eligibility flag "is_premium" to false on "stock.lot" (并在批次模型上更新优质品牌资质字段值为假)
        And raise a QC warning "qc_warning" inside "agri.herbs.gmp" (并在中药材认证运行记录模型下产生质检警告字段值)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a harvested batch herb lot extract evaluation under "stock.lot" (批次模型) linked to a compliance run under "agri.herbs.gmp" (中药材认证运行记录模型)',
            'And the lab results state "state" is "evaluated" (且化验结果状态字段值为已评估状态)',
            'When the chemical laboratory logs a brix result "active_brix" of 14.5% (当化验室记录的活性成分糖度值字段值为14.5%时)',
            'Then the quality engine must block premium brand labeling for the product (质量引擎必须拦截对该产品的优质品牌贴标)',
            'And update the label eligibility flag "is_premium" to false on "stock.lot" (并在批次模型上更新优质品牌资质字段值为假)',
            'And raise a QC warning "qc_warning" inside "agri.herbs.gmp" (并在中药材认证运行记录模型下产生质检警告字段值)'
        ])

    def test_03_gxp_certified_operator_workstation_checkin_validation_gxp(self):
        """
        Scenario: GxP Certified Operator Workstation Check-In Validation (GxP认证操作员工作站登入资质安全校验)
        Given a GMP extraction workstation under "agri.herbs.gmp" (中药材认证运行记录模型)
        And an operator with a GxP qualification under "agri.gxp.certification" (GxP资质认证模型)
        And the certification verification state "state" is "expired" (且该认证状态字段值为已失效状态)
        When the operator attempts workstation check-in (当操作员尝试登入该工作站时)
        Then the validation engine must block the operator check-in access (系统验证引擎必须拦截该操作员的登入访问)
        And raise a ValidationError (系统必须抛出验证错误) with message "Operator GxP safety certification expired" (包含"操作员GxP安全认证已过期"提示信息)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a GMP extraction workstation under "agri.herbs.gmp" (中药材认证运行记录模型)',
            'And an operator with a GxP qualification under "agri.gxp.certification" (GxP资质认证模型)',
            'And the certification verification state "state" is "expired" (且该认证状态字段值为已失效状态)',
            'When the operator attempts workstation check-in (当操作员尝试登入该工作站时)',
            'Then the validation engine must block the operator check-in access (系统验证引擎必须拦截该操作员的登入访问)',
            'And raise a ValidationError (系统必须抛出验证错误) with message "Operator GxP safety certification expired" (包含"操作员GxP安全认证已过期"提示信息)'
        ])

    def test_04_unscheduled_breakdown_active_backtrack_selfhealing(self):
        """
        Scenario: Unscheduled Breakdown Active Backtrack Self-Healing (非计划停机故障主动追溯与自愈调度)
        Given an active medicinal herb processing schedule under "mrp.production" (制造订单模型)
        And the extraction machinery has a breakdown event "is_broken" set to true (且提取设备故障状态字段值已设置为真)
        When the system triggers unscheduled breakdown self-healing procedures (当系统触发非计划停机自愈自适应程序时)
        Then the engine must backtrack and reschedule all remaining active lots under "mrp.production" (系统调度引擎必须回溯并重新调度该制造订单模型下所有剩余的进行中批次)
        And log the rescheduling trace "reschedule_log" inside "agri.herbs.gmp" (并在中药材认证运行记录模型上记录详细的自愈重调度日志字段值)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an active medicinal herb processing schedule under "mrp.production" (制造订单模型)',
            'And the extraction machinery has a breakdown event "is_broken" set to true (且提取设备故障状态字段值已设置为真)',
            'When the system triggers unscheduled breakdown self-healing procedures (当系统触发非计划停机自愈自适应程序时)',
            'Then the engine must backtrack and reschedule all remaining active lots under "mrp.production" (系统调度引擎必须回溯并重新调度该制造订单模型下所有剩余的进行中批次)',
            'And log the rescheduling trace "reschedule_log" inside "agri.herbs.gmp" (并在中药材认证运行记录模型上记录详细的自愈重调度日志字段值)'
        ])

    def test_05_multilevel_cascade_safeguard_deletion_gating(self):
        """
        Scenario: Multi-Level Cascade Safeguard Deletion Gating (生产工艺多级级联删除安全保护拦截)
        Given an active extraction run record under "agri.herbs.gmp" (中药材认证运行记录模型) linked to ongoing active material moves under "stock.move" (库存移动模型)
        And the material move status "state" is "assigned" (且库存移动状态字段值为已分配状态)
        When the operator attempts to delete the extraction run record under "agri.herbs.gmp" (当操作员尝试删除该中药材认证运行记录模型上的记录时)
        Then the database must trigger cascade deletion gating and raise an IntegrityError (系统必须触发级联删除保护拦截并抛出完整性错误)
        And reject the deletion request, maintaining database integrity (并且拒绝删除，维持数据库的完整性)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an active extraction run record under "agri.herbs.gmp" (中药材认证运行记录模型) linked to ongoing active material moves under "stock.move" (库存移动模型)',
            'And the material move status "state" is "assigned" (且库存移动状态字段值为已分配状态)',
            'When the operator attempts to delete the extraction run record under "agri.herbs.gmp" (当操作员尝试删除该中药材认证运行记录模型上的记录时)',
            'Then the database must trigger cascade deletion gating and raise an IntegrityError (系统必须触发级联删除保护拦截并抛出完整性错误)',
            'And reject the deletion request, maintaining database integrity (并且拒绝删除，维持数据库的完整性)'
        ])

    def test_06_herbs_wip_shelf_life_degradation_rate_dynamic_update_wip(self):
        """
        Scenario: Herbs WIP Shelf Life Degradation Rate Dynamic Update (中药材WIP半成品货架期降解率动态更新)
        Given an active herb drying run under "mrp.production" (制造订单模型) linked to "agri.herbs.gmp" (中药材认证运行记录模型)
        And the current relative humidity sensor value "humidity" is 75.0% (且当前相对湿度传感器字段值为75.0%)
        When the environmental monitor reports an humidity spike to 88.0% (当环境监控器报告湿度飙升至88.0%时)
        Then the system must dynamically update the WIP degradation rate coefficient "degradation_rate" to 4.5% per hour (系统必须动态将WIP降解率系数调整为每小时4.5%)
        And record a high-humidity alert log "alert_message" inside "agri.herbs.gmp" (并在中药材认证运行记录模型上记录高湿警报日志字段值)
        And update the active drying mission state "state" to "progress" (并更新制造订单状态字段值为进行中状态)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an active herb drying run under "mrp.production" (制造订单模型) linked to "agri.herbs.gmp" (中药材认证运行记录模型)',
            'And the current relative humidity sensor value "humidity" is 75.0% (且当前相对湿度传感器字段值为75.0%)',
            'When the environmental monitor reports an humidity spike to 88.0% (当环境监控器报告湿度飙升至88.0%时)',
            'Then the system must dynamically update the WIP degradation rate coefficient "degradation_rate" to 4.5% per hour (系统必须动态将WIP降解率系数调整为每小时4.5%)',
            'And record a high-humidity alert log "alert_message" inside "agri.herbs.gmp" (并在中药材认证运行记录模型上记录高湿警报日志字段值)',
            'And update the active drying mission state "state" to "progress" (并更新制造订单状态字段值为进行中状态)'
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
