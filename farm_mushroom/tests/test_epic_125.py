# -*- coding: utf-8 -*-
from odoo.addons.farm_core.tests.bdd_base import BddTransactionCase
from odoo.exceptions import UserError, ValidationError

class TestEpic125(BddTransactionCase):
    """ BDD Test Suite for Epic 125: Epic 125 Fungi Multi-Flush Management (真菌多潮栽培与菌菇批次管理) """

    def setUp(self):
        super(TestEpic125, self).setUp()

    def test_01_fungi_multiflush_harvest_yields_tracking(self):
        """
        Scenario: Fungi Multi-Flush harvest yields tracking (真菌多潮菇采收产量追踪机制)
        Given mushroom growing beds under "stock.lot" (批次模型) linked to a fungi flush run under "agri.fungi.flush" (真菌多潮记录模型)
        And the flush run state "state" is "fruiting" (且该运行状态字段值为出菇状态)
        When logging harvests, the system tracks flush numbers "flush_no" as "Flush 1" and applies yield calculations (当记录采收时系统对第1潮菇进行追踪并应用产量计算)
        Then the system must support multiple stock receipts under "stock.picking" (库存拣货单模型) for the same fungi flush run (系统必须支持在同一真菌多潮记录下生成多个库存拣货单模型的收货单据)
        And automatically tag the harvest receipts with the current flush identifier (并自动在收货单上标记当前潮次标识)
        And update the cumulative biological yield "total_yield" inside "agri.fungi.flush" (并在真菌多潮记录模型上更新累计生物产量字段值)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given mushroom growing beds under "stock.lot" (批次模型) linked to a fungi flush run under "agri.fungi.flush" (真菌多潮记录模型)',
            'And the flush run state "state" is "fruiting" (且该运行状态字段值为出菇状态)',
            'When logging harvests, the system tracks flush numbers "flush_no" as "Flush 1" and applies yield calculations (当记录采收时系统对第1潮菇进行追踪并应用产量计算)',
            'Then the system must support multiple stock receipts under "stock.picking" (库存拣货单模型) for the same fungi flush run (系统必须支持在同一真菌多潮记录下生成多个库存拣货单模型的收货单据)',
            'And automatically tag the harvest receipts with the current flush identifier (并自动在收货单上标记当前潮次标识)',
            'And update the cumulative biological yield "total_yield" inside "agri.fungi.flush" (并在真菌多潮记录模型上更新累计生物产量字段值)'
        ])

    def test_02_substrate_biological_asset_valuation_recalculation(self):
        """
        Scenario: Substrate Biological Asset Valuation recalculation (培养基质生物资产折旧重算评估)
        Given spent mushroom substrate lots under "stock.lot" (批次模型) linked to a biological valuation run under "agri.fungi.flush" (真菌多潮记录模型)
        And the current flush count "flush_no" is "Flush 3" (且当前采收潮次字段值为第3潮)
        When transitioning substrate lots to spent status "state" of "depleted" (当将栽培基质批次过渡到耗尽状态字段值时)
        Then the valuation engine must apply a 35.0% biological depreciation penalty "depreciation_rate" on the asset value (资产价值评估引擎必须在资产价值上应用35.0%的生物折旧率)
        And update the remaining book value "book_value" on the biological asset "agri.fungi.flush" (并在真菌多潮记录模型上更新剩余账面价值字段值)
        And log a valuation correction in "account.move" (并在会计分录模型中记录一条估值调整凭证)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given spent mushroom substrate lots under "stock.lot" (批次模型) linked to a biological valuation run under "agri.fungi.flush" (真菌多潮记录模型)',
            'And the current flush count "flush_no" is "Flush 3" (且当前采收潮次字段值为第3潮)',
            'When transitioning substrate lots to spent status "state" of "depleted" (当将栽培基质批次过渡到耗尽状态字段值时)',
            'Then the valuation engine must apply a 35.0% biological depreciation penalty "depreciation_rate" on the asset value (资产价值评估引擎必须在资产价值上应用35.0%的生物折旧率)',
            'And update the remaining book value "book_value" on the biological asset "agri.fungi.flush" (并在真菌多潮记录模型上更新剩余账面价值字段值)',
            'And log a valuation correction in "account.move" (并在会计分录模型中记录一条估值调整凭证)'
        ])

    def test_03_soil_organic_matter_som_spent_substrate_offsets_som(self):
        """
        Scenario: Soil Organic Matter SOM spent substrate offsets (土壤有机质SOM菌渣还田碳抵消)
        Given a soil enhancement mission under "mrp.workorder" (作业任务模型) using spent mushroom compost lots under "stock.lot" (批次模型)
        And the land location under "stock.location" (位置模型) has an active soil quality ledger in "agri.regenerative.soil" (再生土壤记录模型)
        When the worker completes the soil enhancement mission (当工人完成此土地改良作业任务时)
        Then the system must allocate soil organic matter SOM carbon offsets "som_carbon_offset" of 12.5 kg CO2e per kg compost (系统必须根据菌渣施用量按每千克12.5千克二氧化碳当量的比例分配土壤有机质SOM碳抵消信用额度)
        And update the land's cumulative carbon offset ledger "total_carbon_offset" in "agri.regenerative.soil" (并在再生土壤记录模型中更新该土地的累计碳抵消信用额度字段值)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a soil enhancement mission under "mrp.workorder" (作业任务模型) using spent mushroom compost lots under "stock.lot" (批次模型)',
            'And the land location under "stock.location" (位置模型) has an active soil quality ledger in "agri.regenerative.soil" (再生土壤记录模型)',
            'When the worker completes the soil enhancement mission (当工人完成此土地改良作业任务时)',
            'Then the system must allocate soil organic matter SOM carbon offsets "som_carbon_offset" of 12.5 kg CO2e per kg compost (系统必须根据菌渣施用量按每千克12.5千克二氧化碳当量的比例分配土壤有机质SOM碳抵消信用额度)',
            'And update the land's cumulative carbon offset ledger "total_carbon_offset" in "agri.regenerative.soil" (并在再生土壤记录模型中更新该土地的累计碳抵消信用额度字段值)'
        ])

    def test_04_jidoka_vessel_lock_on_substrate_quants(self):
        """
        Scenario: Jidoka Vessel Lock on Substrate Quants (吉多卡灭菌罐库存物理安全锁死联动)
        Given locked substrate pasteurization vessels managed under "agri.fungi.flush" (真菌多潮记录模型)
        And the vessel sterilization lock state "is_locked" is true (且该灭菌罐锁闭状态字段值为真)
        And associated inventory quantities under "stock.quant" (库存量模型)
        When the operator attempts to modify substrate inventory quants "quantity" during active pasteurization (当操作员尝试在进行中的灭菌过程中修改该灭菌罐关联的库存量模型中的数量字段值时)
        Then the Jidoka physical interlock must block the inventory transaction (吉多卡物理联动联锁装置必须拦截该库存交易)
        And raise a ValidationError (系统必须抛出验证错误) with message "Vessel sterilization active, inventory locked" (包含"灭菌罐灭菌进行中，库存已锁定"提示信息)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given locked substrate pasteurization vessels managed under "agri.fungi.flush" (真菌多潮记录模型)',
            'And the vessel sterilization lock state "is_locked" is true (且该灭菌罐锁闭状态字段值为真)',
            'And associated inventory quantities under "stock.quant" (库存量模型)',
            'When the operator attempts to modify substrate inventory quants "quantity" during active pasteurization (当操作员尝试在进行中的灭菌过程中修改该灭菌罐关联的库存量模型中的数量字段值时)',
            'Then the Jidoka physical interlock must block the inventory transaction (吉多卡物理联动联锁装置必须拦截该库存交易)',
            'And raise a ValidationError (系统必须抛出验证错误) with message "Vessel sterilization active, inventory locked" (包含"灭菌罐灭菌进行中，库存已锁定"提示信息)'
        ])

    def test_05_multilevel_cascade_safeguard_deletion_gating(self):
        """
        Scenario: Multi-Level Cascade Safeguard Deletion Gating (栽培床与多潮记录多级级联删除安全保护)
        Given an active fungi growing bed under "stock.lot" (批次模型) linked to a fungi flush record under "agri.fungi.flush" (真菌多潮记录模型)
        And the growing bed status "state" is "active" (且栽培床状态字段值为活跃状态)
        And associated substrate inventory records under "stock.quant" (库存量模型) exist (且存在关联的培养基质库存记录)
        When the operator attempts to delete the fungi flush record under "agri.fungi.flush" (当操作员尝试删除该真菌多潮记录模型下的记录时)
        Then the database must trigger a cascade deletion safeguard and raise a UserError (系统必须触发级联删除安全保护机制并抛出用户错误)
        And reject the deletion request, keeping the parent biological asset record intact (并且拒绝删除请求，保持父级生物资产记录完好无损)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an active fungi growing bed under "stock.lot" (批次模型) linked to a fungi flush record under "agri.fungi.flush" (真菌多潮记录模型)',
            'And the growing bed status "state" is "active" (且栽培床状态字段值为活跃状态)',
            'And associated substrate inventory records under "stock.quant" (库存量模型) exist (且存在关联的培养基质库存记录)',
            'When the operator attempts to delete the fungi flush record under "agri.fungi.flush" (当操作员尝试删除该真菌多潮记录模型下的记录时)',
            'Then the database must trigger a cascade deletion safeguard and raise a UserError (系统必须触发级联删除安全保护机制并抛出用户错误)',
            'And reject the deletion request, keeping the parent biological asset record intact (并且拒绝删除请求，保持父级生物资产记录完好无损)'
        ])

    def test_06_mushroom_substrate_wip_shelf_life_degradation_rate_dynamic_update_wip(self):
        """
        Scenario: Mushroom Substrate WIP Shelf Life Degradation Rate Dynamic Update (菌菇培养基质WIP半成品货架期降解率动态调整)
        Given an active fungi incubation lot under "stock.lot" (批次模型) linked to a fungi flush run under "agri.fungi.flush" (真菌多潮记录模型)
        And the substrate exposure temperature "ambient_temp" is 28.5°C (且基质暴露环境温度字段值为28.5°C)
        When the room temperature sensor logs a temperature spike to 32.5°C (当温控传感器记录环境温度骤升至32.5°C时)
        Then the system must update the substrate degradation rate "degradation_rate" to 8.0% per hour (系统必须将基质货架期降解率字段值动态更新为每小时8.0%)
        And recalculate the expected remaining substrate shelf life hours "book_value" on "agri.fungi.flush" (并在真菌多潮记录模型上重新评估剩余账面价值与预计货架期小时数字段值)
        And create an urgent temperature correction activity under "mail.activity" (并在邮件活动模型下自动生成紧急温控调整活动)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an active fungi incubation lot under "stock.lot" (批次模型) linked to a fungi flush run under "agri.fungi.flush" (真菌多潮记录模型)',
            'And the substrate exposure temperature "ambient_temp" is 28.5°C (且基质暴露环境温度字段值为28.5°C)',
            'When the room temperature sensor logs a temperature spike to 32.5°C (当温控传感器记录环境温度骤升至32.5°C时)',
            'Then the system must update the substrate degradation rate "degradation_rate" to 8.0% per hour (系统必须将基质货架期降解率字段值动态更新为每小时8.0%)',
            'And recalculate the expected remaining substrate shelf life hours "book_value" on "agri.fungi.flush" (并在真菌多潮记录模型上重新评估剩余账面价值与预计货架期小时数字段值)',
            'And create an urgent temperature correction activity under "mail.activity" (并在邮件活动模型下自动生成紧急温控调整活动)'
        ])

    def test_07_biological_asset_quarantine_solenoid_gate_interlock(self):
        """
        Scenario: Biological Asset Quarantine Solenoid Gate Interlock (生物资产疫病隔离区电磁阀强行锁定防护)
        Given a quarantined biological asset lot in "stock.matter.tracking" (物料跟踪模型) with status "quarantined" (隔离状态)
        And a quarantine geofence is defined with GPS coordinates "gps_lat" and "gps_lng" (并且使用地理坐标定义了防疫边界围栏)
        When a technician attempts to trigger open lock "open_gate" (当技术员尝试执行触发开启隔离栏物理阀门系统动作时)
        Then the IoT gateway must activate autoclave lock set "is_solenoid_locked" to true on physical solenoid (物联网网关必须强制激活物理电磁锁状态字段值为真)
        And raise a UserError (并且拦截开启操作并抛出用户错误) with message "SOLENOID_LOCKED_BIOSECURITY" (包含"电磁锁已强制闭锁，隔离区处于高危生物安全防护状态"提示信息)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a quarantined biological asset lot in "stock.matter.tracking" (物料跟踪模型) with status "quarantined" (隔离状态)',
            'And a quarantine geofence is defined with GPS coordinates "gps_lat" and "gps_lng" (并且使用地理坐标定义了防疫边界围栏)',
            'When a technician attempts to trigger open lock "open_gate" (当技术员尝试执行触发开启隔离栏物理阀门系统动作时)',
            'Then the IoT gateway must activate autoclave lock set "is_solenoid_locked" to true on physical solenoid (物联网网关必须强制激活物理电磁锁状态字段值为真)',
            'And raise a UserError (并且拦截开启操作并抛出用户错误) with message "SOLENOID_LOCKED_BIOSECURITY" (包含"电磁锁已强制闭锁，隔离区处于高危生物安全防护状态"提示信息)'
        ])
