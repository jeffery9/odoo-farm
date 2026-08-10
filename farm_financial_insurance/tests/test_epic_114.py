# -*- coding: utf-8 -*-
from odoo.addons.farm_core.tests.bdd_base import BddTransactionCase
from odoo.exceptions import UserError, ValidationError

class TestEpic114(BddTransactionCase):
    """ BDD Test Suite for Epic 114: Epic 114 Agricultural Risk Management & Insurance (农业风险管理与保险) """

    def setUp(self):
        super(TestEpic114, self).setUp()

    def test_01_indexbased_weather_temperature_trigger_insurance_payouts(self):
        """
        Scenario: Index-Based Weather Temperature Trigger Insurance Payouts (基于天气指数的温度触发保险理赔)
        Given an active crop lot under "stock.lot" (库存批次模型) protected by weather index insurance under "agri.risk.insurance" (农业风险管理与保险模型)
        And the weather insurance flag "has_weather_insurance" is True (且天气保险标识字段值为真)
        And the logged sensor temperature "current_temperature" is -2.5 °C (且传感器记录温度字段值为-2.5摄氏度)
        And the policy frost trigger temperature "frost_trigger_temperature" is -2.0 °C (并且保单霜冻触发温度字段值为-2.0摄氏度)
        When the daily risk evaluation scheduler runs (当运行每日风险评估计划任务时)
        Then the system must automatically create index insurance payout lines (系统必须自动编译生成指数保险理赔明细)
        And update the claim status "insurance_payout_status" to "triggered" (并将理赔状态字段值更新为已触发状态)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an active crop lot under "stock.lot" (库存批次模型) protected by weather index insurance under "agri.risk.insurance" (农业风险管理与保险模型)',
            'And the weather insurance flag "has_weather_insurance" is True (且天气保险标识字段值为真)',
            'And the logged sensor temperature "current_temperature" is -2.5 °C (且传感器记录温度字段值为-2.5摄氏度)',
            'And the policy frost trigger temperature "frost_trigger_temperature" is -2.0 °C (并且保单霜冻触发温度字段值为-2.0摄氏度)',
            'When the daily risk evaluation scheduler runs (当运行每日风险评估计划任务时)',
            'Then the system must automatically create index insurance payout lines (系统必须自动编译生成指数保险理赔明细)',
            'And update the claim status "insurance_payout_status" to "triggered" (并将理赔状态字段值更新为已触发状态)'
        ])

    def test_02_biological_asset_dynamic_valuation_credit_risk_alert(self):
        """
        Scenario: Biological Asset Dynamic Valuation Credit Risk Alert (生物资产动态估值与信用风险预警)
        Given biological asset lots secured as loan collateral under "stock.lot" (库存批次模型) linked to "agri.risk.insurance" (农业风险管理与保险模型)
        And a disease alert under "agri.risk.insurance" logs "disease_alert_level" is "high" (且病害警报等级字段"disease_alert_level"为"high")
        And the estimated yield reduction "estimated_yield_reduction" is 25.0% (且预计减产百分比字段值为25.0%)
        When the collateral revaluation engine runs (当运行抵押物估值重新计算系统操作时)
        Then the system must reduce the collateral "biological_asset_valuation" by 25.0% (系统必须将生物资产估值字段值降低25.0%)
        And raise a Credit Risk alert (并触发信用风险警报) with message "Biological collateral valuation dropped below safety threshold. Margin call triggered." (包含提示“生物抵押物估值跌破安全阈值。已触发追加保证金通知。”的警告消息)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given biological asset lots secured as loan collateral under "stock.lot" (库存批次模型) linked to "agri.risk.insurance" (农业风险管理与保险模型)',
            'And a disease alert under "agri.risk.insurance" logs "disease_alert_level" is "high" (且病害警报等级字段"disease_alert_level"为"high")',
            'And the estimated yield reduction "estimated_yield_reduction" is 25.0% (且预计减产百分比字段值为25.0%)',
            'When the collateral revaluation engine runs (当运行抵押物估值重新计算系统操作时)',
            'Then the system must reduce the collateral "biological_asset_valuation" by 25.0% (系统必须将生物资产估值字段值降低25.0%)',
            'And raise a Credit Risk alert (并触发信用风险警报) with message "Biological collateral valuation dropped below safety threshold. Margin call triggered." (包含提示“生物抵押物估值跌破安全阈值。已触发追加保证金通知。”的警告消息)'
        ])

    def test_03_loan_approval_financial_credit_rating_gating_check(self):
        """
        Scenario: Loan Approval Financial Credit Rating Gating Check (贷款审批信用评级准入核值拦截)
        Given a farmer loan application under "agri.risk.insurance" (农业风险管理与保险模型) linked to a partner in "res.partner" (联系人模型)
        And the partner credit score "credit_score" is 540 points (且该客户信用分字段值为540分)
        When the financial manager attempts to validate the loan (当财务经理尝试执行贷款确认时)
        Then the system must block the validation and raise a ValidationError (系统必须拦截确认并抛出验证错误) with message "Credit score 540 is below the minimum required 550. Loan rejected." (包含提示“信用分540低于最低要求的550。贷款已拒绝。”的验证错误消息)
        And update the loan request status "loan_status" to "rejected" (并将贷款申请状态字段值更新为已拒绝状态)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a farmer loan application under "agri.risk.insurance" (农业风险管理与保险模型) linked to a partner in "res.partner" (联系人模型)',
            'And the partner credit score "credit_score" is 540 points (且该客户信用分字段值为540分)',
            'When the financial manager attempts to validate the loan (当财务经理尝试执行贷款确认时)',
            'Then the system must block the validation and raise a ValidationError (系统必须拦截确认并抛出验证错误) with message "Credit score 540 is below the minimum required 550. Loan rejected." (包含提示“信用分540低于最低要求的550。贷款已拒绝。”的验证错误消息)',
            'And update the loan request status "loan_status" to "rejected" (并将贷款申请状态字段值更新为已拒绝状态)'
        ])

    def test_04_cooperative_debt_netting_repayment_financial_settlement(self):
        """
        Scenario: Cooperative Debt Netting Repayment Financial Settlement (合作社债务轧差还款财务结算)
        Given a farmer crop purchase order under "purchase.order" (采购订单模型) linked to "agri.risk.insurance" (农业风险管理与保险模型)
        And the farmer outstanding credit loan balance "outstanding_loan_balance" is 12000.0 USD (且该农户未结信用贷款余额字段值为12000.0美元)
        And the delivered harvest lot value "delivered_harvest_value" is 15000.0 USD (且已交付的收获批次价值字段值为15000.0美元)
        When the contract settlement accountant runs debt netting (当合同结算会计运行债务轧差结算时)
        Then the system must automatically net the settlement writing "netted_payment_amount" is 3000.0 USD (系统必须自动对冲结算并写入实付结算金额字段值为3000.0美元)
        And reduce the partner's outstanding loan balance in "agri.risk.insurance" to 0.0 USD (并在农业风险管理与保险模型中将该客户的未结贷款余额字段值降低至0.0美元)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a farmer crop purchase order under "purchase.order" (采购订单模型) linked to "agri.risk.insurance" (农业风险管理与保险模型)',
            'And the farmer outstanding credit loan balance "outstanding_loan_balance" is 12000.0 USD (且该农户未结信用贷款余额字段值为12000.0美元)',
            'And the delivered harvest lot value "delivered_harvest_value" is 15000.0 USD (且已交付的收获批次价值字段值为15000.0美元)',
            'When the contract settlement accountant runs debt netting (当合同结算会计运行债务轧差结算时)',
            'Then the system must automatically net the settlement writing "netted_payment_amount" is 3000.0 USD (系统必须自动对冲结算并写入实付结算金额字段值为3000.0美元)',
            'And reduce the partner\'s outstanding loan balance in "agri.risk.insurance" to 0.0 USD (并在农业风险管理与保险模型中将该客户的未结贷款余额字段值降低至0.0美元)'
        ])

    def test_05_multifarm_worked_hectare_cost_split_settlements(self):
        """
        Scenario: Multi-Farm Worked Hectare Cost Split Settlements (多农场作业面积费用分摊结算)
        Given a cooperative harvesting campaign under "agri.risk.insurance" (农业风险管理与保险模型) covering multiple farms
        And the contractor harvesting bill under "account.move" (会计分录模型) is 8000.0 USD (且承包商收割账单金额字段值为8000.0美元)
        And the worked hectare split ratios "cooperative_cost_split" are registered proportionally (且已按比例注册各农场作业面积分摊比例字段值)
        When the cooperative coordinator generates the cost split (当合作社协调员生成费用分摊作业时)
        Then the system must automatically post cost splits to each member farm (系统必须自动将分摊费用过账到各成员农场财务账户中系统操作)
        And write balanced journal entries "account.move" for cooperative clearing (并为合作社轧差结算创建平衡的会计分录)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a cooperative harvesting campaign under "agri.risk.insurance" (农业风险管理与保险模型) covering multiple farms',
            'And the contractor harvesting bill under "account.move" (会计分录模型) is 8000.0 USD (且承包商收割账单金额字段值为8000.0美元)',
            'And the worked hectare split ratios "cooperative_cost_split" are registered proportionally (且已按比例注册各农场作业面积分摊比例字段值)',
            'When the cooperative coordinator generates the cost split (当合作社协调员生成费用分摊作业时)',
            'Then the system must automatically post cost splits to each member farm (系统必须自动将分摊费用过账到各成员农场财务账户中系统操作)',
            'And write balanced journal entries "account.move" for cooperative clearing (并为合作社轧差结算创建平衡的会计分录)'
        ])

    def test_06_csa_booking_rollback_on_risk_incident_trigger_csa(self):
        """
        Scenario: CSA Booking Rollback on Risk Incident Trigger (风险事件触发CSA预订自动回滚)
        Given a CSA subscriber sales order under "sale.order" (销售订单模型) linked to "agri.risk.insurance" (农业风险与保险模型) with status (状态) "sale" (已确认状态)
        And a major frost risk alert "frost_incident_active" (霜冻灾害激活) is set to True (真) for the crop lot
        When the risk coordinator triggers safety protection via action "action_trigger_insurance_rollback" (触发保险回滚动作)
        Then the system automatically rolls back the CSA subscription reservation
        And resets the sales order status (状态) to "draft" (草稿状态) under "sale.order" (销售订单模型)
        And releases the allocated crop quantities under "stock.move" (库存移动模型)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a CSA subscriber sales order under "sale.order" (销售订单模型) linked to "agri.risk.insurance" (农业风险与保险模型) with status (状态) "sale" (已确认状态)',
            'And a major frost risk alert "frost_incident_active" (霜冻灾害激活) is set to True (真) for the crop lot',
            'When the risk coordinator triggers safety protection via action "action_trigger_insurance_rollback" (触发保险回滚动作)',
            'Then the system automatically rolls back the CSA subscription reservation',
            'And resets the sales order status (状态) to "draft" (草稿状态) under "sale.order" (销售订单模型)',
            'And releases the allocated crop quantities under "stock.move" (库存移动模型)'
        ])

    def test_07_dynamic_credit_overdraft_transaction_savepoint_rollback(self):
        """
        Scenario: Dynamic Credit Overdraft Transaction Savepoint Rollback (合作社信用额度穿透事务保存点回滚防呆机制)
        Given a joint clearing balance account inside "account.move" (会计分录模型) with cooperative member status "active" (且合作社成员信用状态为活跃)
        And a dynamic credit limit registered in the virtual ledger (并且在虚拟账簿中登记了固定的动态额度上限)
        When a clearing transaction fails due to concurrent credit overdraft (当清算交易由于信用额度并发穿透导致处理失败时)
        Then the transaction engine must execute rollback to "cr.savepoint" (交易引擎必须强制执行事务回滚到指定的事务保存点)
        And raise a UserError (并且抛出用户错误) with message "CREDIT_OVERDRAFT_TRANSACTION_FAILED" (包含"信用额度超支交易回滚，防范资金坏账"提示信息)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a joint clearing balance account inside "account.move" (会计分录模型) with cooperative member status "active" (且合作社成员信用状态为活跃)',
            'And a dynamic credit limit registered in the virtual ledger (并且在虚拟账簿中登记了固定的动态额度上限)',
            'When a clearing transaction fails due to concurrent credit overdraft (当清算交易由于信用额度并发穿透导致处理失败时)',
            'Then the transaction engine must execute rollback to "cr.savepoint" (交易引擎必须强制执行事务回滚到指定的事务保存点)',
            'And raise a UserError (并且抛出用户错误) with message "CREDIT_OVERDRAFT_TRANSACTION_FAILED" (包含"信用额度超支交易回滚，防范资金坏账"提示信息)'
        ])
