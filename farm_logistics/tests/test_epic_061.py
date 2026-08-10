# -*- coding: utf-8 -*-
from odoo.addons.farm_core.tests.bdd_base import BddTransactionCase
from odoo.exceptions import UserError, ValidationError

class TestEpic061(BddTransactionCase):
    """ BDD Test Suite for Epic 061: Epic 061 Reverse Recall Tracking (反向召回追踪) """

    def setUp(self):
        super(TestEpic061, self).setUp()

    def test_01_outbound_defective_lot_ingestion_and_recall_campaign_isolation(self):
        """
        Scenario: Outbound Defective Lot Ingestion and Recall Campaign Isolation (出库缺陷批次录入与召回活动隔离)
        Given an outbound product lot (出库产品批次) "HON-LOT-401" with a confirmed chemical contamination report (化学污染报告)
        And the lot resides on multiple validated stock.picking (库存拣货) delivery orders
        When a recall campaign (召回活动) of model agri.recall.campaign (农业召回活动) is initialized with state "draft (草稿)"
        And the Quality Director (质量总监) triggers "action_compile_shipping_history (编译发运历史)"
        Then the system must identify all impacted customer delivery orders of model stock.picking (库存拣货)
        And force their state to "locked (锁定)" under stock.lot (库存批次)
        And block any subsequent outbound shipment of "HON-LOT-401" with a ValidationError (验证错误): "Cannot ship recalled lot (无法发运已被召回的批次)"
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an outbound product lot (出库产品批次) "HON-LOT-401" with a confirmed chemical contamination report (化学污染报告)',
            'And the lot resides on multiple validated stock.picking (库存拣货) delivery orders',
            'When a recall campaign (召回活动) of model agri.recall.campaign (农业召回活动) is initialized with state "draft (草稿)"',
            'And the Quality Director (质量总监) triggers "action_compile_shipping_history (编译发运历史)"',
            'Then the system must identify all impacted customer delivery orders of model stock.picking (库存拣货)',
            'And force their state to "locked (锁定)" under stock.lot (库存批次)',
            'And block any subsequent outbound shipment of "HON-LOT-401" with a ValidationError (验证错误): "Cannot ship recalled lot (无法发运已被召回的批次)"'
        ])

    def test_02_upstream_ancestral_lot_rootcause_discovery(self):
        """
        Scenario: Upstream Ancestral Lot Root-Cause Discovery (上游祖先批次根因诊断)
        Given a recalled honey batch lot (召回蜂蜜批次) "HON-LOT-401" under stock.lot (库存批次)
        And this lot was produced from multiple agricultural inputs via mrp.production (制造订单)
        When the Quality Director (质量总监) triggers the recursive reverse lineage trace (递归反向谱系追踪) using "action_find_root_cause (寻找根因)"
        Then the system must recursively traverse all upstream raw materials back to their source harvest lots
        And identify the raw honey comb input lot (原始蜂巢投入批次) "COMB-RAW-12" as the sole root-cause (唯一根因) due to pesticide detection (农药检出)
        And log this root-cause on the agri.recall.campaign (农业召回活动) dossier (卷宗)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a recalled honey batch lot (召回蜂蜜批次) "HON-LOT-401" under stock.lot (库存批次)',
            'And this lot was produced from multiple agricultural inputs via mrp.production (制造订单)',
            'When the Quality Director (质量总监) triggers the recursive reverse lineage trace (递归反向谱系追踪) using "action_find_root_cause (寻找根因)"',
            'Then the system must recursively traverse all upstream raw materials back to their source harvest lots',
            'And identify the raw honey comb input lot (原始蜂巢投入批次) "COMB-RAW-12" as the sole root-cause (唯一根因) due to pesticide detection (农药检出)',
            'And log this root-cause on the agri.recall.campaign (农业召回活动) dossier (卷宗)'
        ])

    def test_03_downstream_comingled_lot_containment(self):
        """
        Scenario: Downstream Co-Mingled Lot Containment (下游共混批次全面封锁)
        Given a contaminated raw material lot (受污染原材料批次) "COMB-RAW-12" identified under stock.lot (库存批次)
        When the system executes "action_quarantine_downstream (隔离下游)" to trace all sibling/child lots blended with this raw material
        Then the system must identify all downstream child batches processed across all mrp.production (制造订单)
        And automatically change their lot status to "quarantine (隔离)" on stock.lot (库存批次)
        And raise a ValidationError (验证错误): "Lot is under quarantine lockdown (批次处于隔离锁定中)" if any operator attempts to confirm a sales order of model sale.order (销售订单) containing any of these quarantined child lots
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a contaminated raw material lot (受污染原材料批次) "COMB-RAW-12" identified under stock.lot (库存批次)',
            'When the system executes "action_quarantine_downstream (隔离下游)" to trace all sibling/child lots blended with this raw material',
            'Then the system must identify all downstream child batches processed across all mrp.production (制造订单)',
            'And automatically change their lot status to "quarantine (隔离)" on stock.lot (库存批次)',
            'And raise a ValidationError (验证错误): "Lot is under quarantine lockdown (批次处于隔离锁定中)" if any operator attempts to confirm a sales order of model sale.order (销售订单) containing any of these quarantined child lots'
        ])

    def test_04_recalled_picking_customer_email_notification(self):
        """
        Scenario: Recalled Picking Customer Email Notification (受召回拣货客户邮件告知)
        Given an active recall campaign (活动的召回工程) of model agri.recall.campaign (农业召回活动) containing 5 validated delivery orders of model stock.picking (库存拣货)
        When the Quality Director (质量总监) changes the campaign state to "active (活动中)"
        Then the system must compile a list of unique customer contacts of model res.partner (业务伙伴) from the affected stock.picking (库存拣货)
        And automatically dispatch GxP-compliant bilingual email notifications (符合GxP规范的双语邮件通知) using the mail.template (邮件模板) "recall_notification_template (召回通知模板)"
        And log the email delivery status as "sent (已发送)" on the recall campaign's chatter (沟通记录)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an active recall campaign (活动的召回工程) of model agri.recall.campaign (农业召回活动) containing 5 validated delivery orders of model stock.picking (库存拣货)',
            'When the Quality Director (质量总监) changes the campaign state to "active (活动中)"',
            'Then the system must compile a list of unique customer contacts of model res.partner (业务伙伴) from the affected stock.picking (库存拣货)',
            'And automatically dispatch GxP-compliant bilingual email notifications (符合GxP规范的双语邮件通知) using the mail.template (邮件模板) "recall_notification_template (召回通知模板)"',
            'And log the email delivery status as "sent (已发送)" on the recall campaign\'s chatter (沟通记录)'
        ])

    def test_05_complete_recall_reconciliation_ledger(self):
        """
        Scenario: Complete Recall Reconciliation Ledger (完整召回物料平衡台账)
        Given a recall campaign (召回工程) of model agri.recall.campaign (农业召回活动) with state "active (活动中)"
        And the actual returned physical mass (实际退回的物理重量) of lot "HON-LOT-401" is registered as 450.0 kg (公斤)
        And the total shipped mass (总发运重量) of lot "HON-LOT-401" was recorded as 500.0 kg (公斤)
        When the Quality Director (质量总监) triggers "action_close_campaign (关闭活动)"
        Then the system must compute the Reconciliation Score (平衡率得分) as 90.0% (recovered-to-shipped mass ratio/退回对发运重量比)
        And write this score to the material reconciliation ledger (物料平衡台账) in agri.recall.campaign (农业召回活动)
        And transition the campaign state to "closed (已关闭)"
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a recall campaign (召回工程) of model agri.recall.campaign (农业召回活动) with state "active (活动中)"',
            'And the actual returned physical mass (实际退回的物理重量) of lot "HON-LOT-401" is registered as 450.0 kg (公斤)',
            'And the total shipped mass (总发运重量) of lot "HON-LOT-401" was recorded as 500.0 kg (公斤)',
            'When the Quality Director (质量总监) triggers "action_close_campaign (关闭活动)"',
            'Then the system must compute the Reconciliation Score (平衡率得分) as 90.0% (recovered-to-shipped mass ratio/退回对发运重量比)',
            'And write this score to the material reconciliation ledger (物料平衡台账) in agri.recall.campaign (农业召回活动)',
            'And transition the campaign state to "closed (已关闭)"'
        ])

    def test_06_autonomous_swarm_harvest_recall_lockdown(self):
        """
        Scenario: Autonomous Swarm Harvest Recall Lockdown (自主无人机蜂群采收召回锁定)
        Given a recalled crop product lot (受召回作物产品批次) "HON-LOT-401" of model stock.lot (库存批次)
        And an active harvesting mission (活动的采收任务) "mrp.workorder" (作业任务) scheduled with this lot or location
        When the Quality Director (质量总监) changes the campaign state of model agri.recall.campaign (农业召回活动) to "active (活动中)"
        Then the system must command the connected robotic device (连接的机器人设备) of model iiot.device (物联设备) to immediately abort active operations (中止当前作业)
        And raise a ValidationError (验证错误): "Cannot proceed with mission, targeted lot is recalled (无法继续执行任务，目标批次已被召回)" if any operator attempts to transition the mission "mrp.workorder" (作业任务) state to "ready (准备就绪)" or "active (激活中)"
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a recalled crop product lot (受召回作物产品批次) "HON-LOT-401" of model stock.lot (库存批次)',
            'And an active harvesting mission (活动的采收任务) "mrp.workorder" (作业任务) scheduled with this lot or location',
            'When the Quality Director (质量总监) changes the campaign state of model agri.recall.campaign (农业召回活动) to "active (活动中)"',
            'Then the system must command the connected robotic device (连接的机器人设备) of model iiot.device (物联设备) to immediately abort active operations (中止当前作业)',
            'And raise a ValidationError (验证错误): "Cannot proceed with mission, targeted lot is recalled (无法继续执行任务，目标批次已被召回)" if any operator attempts to transition the mission "mrp.workorder" (作业任务) state to "ready (准备就绪)" or "active (激活中)"'
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
