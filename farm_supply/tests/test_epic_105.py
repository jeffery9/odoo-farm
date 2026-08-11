# -*- coding: utf-8 -*-
from odoo.addons.farm_core.tests.bdd_base import BddTransactionCase
from odoo.exceptions import UserError, ValidationError

class TestEpic105(BddTransactionCase):
    """ BDD Test Suite for Epic 105: Epic 105 Supply Chain Risk Management (Epic 105 供应链风险管理) """

    def setUp(self):
        super(TestEpic105, self).setUp()

    def test_01_coldchain_transport_temperature_sensor_telemetry_failure(self):
        """
        Scenario: Cold-Chain Transport Temperature Sensor Telemetry Failure (冷链运输温度传感器遥测故障)
        Given a refrigerated transport stock.picking (库存拣货/调拨) record tracked by agri.sc.risk (供应链风险)
        When the temperature sensor "transit_temp_sensor" (运输温度传感器) fails to report telemetry for over 4.0 hours
        And sets "telemetry_failed" (遥测故障) to True (真)
        Then the system automatically transitions the picking's risk "safety_status" (安全状态) to "failed" (故障)
        And issues a critical dispatch alert to alternative cold-chain carriers
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a refrigerated transport stock.picking (库存拣货/调拨) record tracked by agri.sc.risk (供应链风险)',
            'When the temperature sensor "transit_temp_sensor" (运输温度传感器) fails to report telemetry for over 4.0 hours',
            'And sets "telemetry_failed" (遥测故障) to True (真)',
            'Then the system automatically transitions the picking\'s risk "safety_status" (安全状态) to "failed" (故障)',
            'And issues a critical dispatch alert to alternative cold-chain carriers'
        ])

    def test_02_stock_quant_vessel_lock_jidoka_safeguard(self):
        """
        Scenario: Stock Quant Vessel Lock Jidoka Safeguard (库存数量容器锁定人字型/自働化安全防护)
        Given physical stock quants inside a fermentation vessel stock.location (库存位置)
        And the vessel has "vessel_lock_active" (容器锁定激活) set to True (真)
        When an operator attempts to manually change quantities under stock.quant (库存数量)
        Then the Jidoka interlock triggers transaction check "_check_vessel_lock" (检查容器锁定)
        And blocks the modification raising a ValidationError (验证错误) "ValidationError: Fermentation vessel is locked (验证错误：发酵容器已锁定)"
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given physical stock quants inside a fermentation vessel stock.location (库存位置)',
            'And the vessel has "vessel_lock_active" (容器锁定激活) set to True (真)',
            'When an operator attempts to manually change quantities under stock.quant (库存数量)',
            'Then the Jidoka interlock triggers transaction check "_check_vessel_lock" (检查容器锁定)',
            'And blocks the modification raising a ValidationError (验证错误) "ValidationError: Fermentation vessel is locked (验证错误：发酵容器已锁定)"'
        ])

    def test_03_evapotranspiration_drip_irrigation_schedule_smart_bypass(self):
        """
        Scenario: Evapotranspiration Drip Irrigation Schedule Smart Bypass (蒸腾作用滴灌计划智能绕过)
        Given daily evapotranspiration forecasts in the environmental risk register
        When the reference "evapotranspiration_rate" (蒸腾速率) ET0 exceeds 6.0 mm
        Then the irrigation controller triggers smart bypass action "action_scale_irrigation_duration" (按比例缩放灌溉时长动作)
        And automatically increases the duration of drip irrigation watering lines by 120.0%
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given daily evapotranspiration forecasts in the environmental risk register',
            'When the reference "evapotranspiration_rate" (蒸腾速率) ET0 exceeds 6.0 mm',
            'Then the irrigation controller triggers smart bypass action "action_scale_irrigation_duration" (按比例缩放灌溉时长动作)',
            'And automatically increases the duration of drip irrigation watering lines by 120.0%'
        ])

    def test_04_multilot_organic_source_gxp_verification_gating_gxp(self):
        """
        Scenario: Multi-Lot Organic Source GxP Verification Gating (多批次有机来源GxP验证门控)
        Given a compiled finished product lot under stock.lot (库存批次) ready for premium branding
        When the quality inspector runs phytosanitary audit action "action_verify_organic_components" (验证有机原料动作) on component lots linked via "component_lot_ids" (原料批次列表)
        And one of the ingredient lots has "gxp_certified" (GxP已认证) set to False (假) due to expired audit logs
        Then the system blocks the premium branding label validation
        And raises a ValidationError (验证错误) "ValidationError: Component GxP certification expired (验证错误：原料GxP认证已过期)"
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a compiled finished product lot under stock.lot (库存批次) ready for premium branding',
            'When the quality inspector runs phytosanitary audit action "action_verify_organic_components" (验证有机原料动作) on component lots linked via "component_lot_ids" (原料批次列表)',
            'And one of the ingredient lots has "gxp_certified" (GxP已认证) set to False (假) due to expired audit logs',
            'Then the system blocks the premium branding label validation',
            'And raises a ValidationError (验证错误) "ValidationError: Component GxP certification expired (验证错误：原料GxP认证已过期)"'
        ])

    def test_05_cascade_deletion_block_on_active_carriers(self):
        """
        Scenario: Cascade Deletion Block on Active Carriers (对激活承运商的级联删除阻断)
        Given active risk tracking records under agri.sc.risk (供应链风险)
        And active logistics carrier res.partner (业务伙伴) records link to this risk record via "carrier_id" (承运商ID)
        When an administrator attempts to perform "unlink" (取消关联/删除) on the risk record
        Then the system blocks the deletion request
        And raises a UserError (用户错误) "UserError: Cannot delete record, active carriers depend on it (用户错误：无法删除记录，存在依赖的激活承运商)"
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given active risk tracking records under agri.sc.risk (供应链风险)',
            'And active logistics carrier res.partner (业务伙伴) records link to this risk record via "carrier_id" (承运商ID)',
            'When an administrator attempts to perform "unlink" (取消关联/删除) on the risk record',
            'Then the system blocks the deletion request',
            'And raises a UserError (用户错误) "UserError: Cannot delete record, active carriers depend on it (用户错误：无法删除记录，存在依赖的激活承运商)"'
        ])

    def test_06_supply_chain_carbon_tax_penalty_audit_rollback(self):
        """
        Scenario: Supply Chain Carbon Tax Penalty Audit Rollback (供应链碳税处罚审计结算回滚)
        Given a carbon tax penalty split invoice under account.move (会计分录) tracked under agri.sc.risk (供应链风险)
        And the linked logistics carrier res.partner (业务伙伴) has an active risk alert "esg_risk_alert" (ESG风险警报) set to True (真)
        When the finance clerk attempts to post the clearing transaction via action "action_post" (过账动作)
        Then the system blocks the transaction posting
        And rolls back the invoice status (状态) to "draft" (草稿)
        And raises a ValidationError (验证错误) "ValidationError: ESG risk score too high for clearing (验证错误：清算对象的ESG风险评分过高)"
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a carbon tax penalty split invoice under account.move (会计分录) tracked under agri.sc.risk (供应链风险)',
            'And the linked logistics carrier res.partner (业务伙伴) has an active risk alert "esg_risk_alert" (ESG风险警报) set to True (真)',
            'When the finance clerk attempts to post the clearing transaction via action "action_post" (过账动作)',
            'Then the system blocks the transaction posting',
            'And rolls back the invoice status (状态) to "draft" (草稿)',
            'And raises a ValidationError (验证错误) "ValidationError: ESG risk score too high for clearing (验证错误：清算对象的ESG风险评分过高)"'
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
