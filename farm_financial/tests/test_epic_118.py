# -*- coding: utf-8 -*-
from odoo.addons.farm_core.tests.bdd_base import BddTransactionCase
from odoo.exceptions import UserError, ValidationError

class TestEpic118(BddTransactionCase):
    """ BDD Test Suite for Epic 118: Epic 118 Contract Farming & Farmer Settlement (订单农业与农户结算) """

    def setUp(self):
        super(TestEpic118, self).setUp()

    def test_01_base_price_adjustment_based_on_sugar_brix_grading_brix(self):
        """
        Scenario: Base Price Adjustment Based on Sugar Brix grading (基于含糖量Brix分级的合同基价调整)
        Given an active contract crop purchase order under "purchase.order" (采购订单模型) linked to "agri.contract.settlement" (合同结算模型)
        And the sugar concentration "sugar_brix_level" from lab analysis is 18.5% (且实验室分析的糖度含量字段值为18.5%)
        When the quality inspector records the Brix grading (质量检测员记录糖度评级) as a critical system action
        Then the system must calculate and apply a premium of 15.0% to the base contract price "base_contract_price" in the purchase order
        And save the adjusted settlement unit price "adjusted_unit_price" on the purchase order record under "purchase.order" (采购订单模型)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an active contract crop purchase order under "purchase.order" (采购订单模型) linked to "agri.contract.settlement" (合同结算模型)',
            'And the sugar concentration "sugar_brix_level" from lab analysis is 18.5% (且实验室分析的糖度含量字段值为18.5%)',
            'When the quality inspector records the Brix grading (质量检测员记录糖度评级) as a critical system action',
            'Then the system must calculate and apply a premium of 15.0% to the base contract price "base_contract_price" in the purchase order',
            'And save the adjusted settlement unit price "adjusted_unit_price" on the purchase order record under "purchase.order" (采购订单模型)'
        ])

    def test_02_cooperative_debt_netting_repayment_financial_settlement(self):
        """
        Scenario: Cooperative Debt Netting Repayment Financial Settlement (合作社债务双向抵销与还款财务结算)
        Given an outstanding input credit loan balance under "account.move" (会计分录模型) for a farmer under "res.partner" (业务伙伴模型)
        And the farmer delivers the harvested raw crops back to the cooperative under "stock.move" (库存移动模型)
        When the financial manager processes the harvest purchase settlement (财务经理处理收获物料采购结算) as a critical system action
        Then the settlement engine must automatically net purchase settlements against outstanding loan balances
        And generate a balanced payment voucher under "account.move" (会计分录模型) with net payment state "posted" (已过账状态)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an outstanding input credit loan balance under "account.move" (会计分录模型) for a farmer under "res.partner" (业务伙伴模型)',
            'And the farmer delivers the harvested raw crops back to the cooperative under "stock.move" (库存移动模型)',
            'When the financial manager processes the harvest purchase settlement (财务经理处理收获物料采购结算) as a critical system action',
            'Then the settlement engine must automatically net purchase settlements against outstanding loan balances',
            'And generate a balanced payment voucher under "account.move" (会计分录模型) with net payment state "posted" (已过账状态)'
        ])

    def test_03_dynamic_biological_asset_valuation_collateral_ledger(self):
        """
        Scenario: Dynamic Biological Asset Valuation Collateral Ledger (生物资产价值动态评估与担保账簿)
        Given a biological asset lot of crop on field secured as loan collateral under "stock.lot" (批次产品模型) linked to "agri.contract.settlement" (合同结算模型)
        And the certified yield forecast "certified_yield_forecast" drops by 30.0% due to pest monitoring alerts (且由于虫害监测警报导致经核证的预测产量字段值下降30.0%)
        When the loan manager re-evaluates the biological collateral valuation (信贷经理重新评估生物资产担保估值) as a critical system action
        Then the system must automatically recalculate collateral valuation "collateral_valuation" on the ledger
        And raise a credit risk alert "credit_risk_warning" with status "warning" (警告状态) on the partner record under "res.partner" (业务伙伴模型)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a biological asset lot of crop on field secured as loan collateral under "stock.lot" (批次产品模型) linked to "agri.contract.settlement" (合同结算模型)',
            'And the certified yield forecast "certified_yield_forecast" drops by 30.0% due to pest monitoring alerts (且由于虫害监测警报导致经核证的预测产量字段值下降30.0%)',
            'When the loan manager re-evaluates the biological collateral valuation (信贷经理重新评估生物资产担保估值) as a critical system action',
            'Then the system must automatically recalculate collateral valuation "collateral_valuation" on the ledger',
            'And raise a credit risk alert "credit_risk_warning" with status "warning" (警告状态) on the partner record under "res.partner" (业务伙伴模型)'
        ])

    def test_04_multientity_cooperative_cost_split_journal_entries(self):
        """
        Scenario: Multi-Entity Cooperative Cost Split Journal Entries (多实体合作社分摊费用会计分录)
        Given a cooperative harvesting campaign under "purchase.order" (采购订单模型) linked to "agri.contract.settlement" (合同结算模型)
        And the contractor billing and shared equipment costs are calculated (且已计算承包商账单及共享设备成本)
        When the accounting scheduler completes multi-entity cost splits (会计调度程序完成多实体成本分摊) as a critical system action
        Then the system must post balanced, proportional cost split journal entries under "account.move" (会计分录模型)
        And update the clearing state "clearing_state" to "cleared" (已结清状态) on "agri.contract.settlement" (合同结算模型)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a cooperative harvesting campaign under "purchase.order" (采购订单模型) linked to "agri.contract.settlement" (合同结算模型)',
            'And the contractor billing and shared equipment costs are calculated (且已计算承包商账单及共享设备成本)',
            'When the accounting scheduler completes multi-entity cost splits (会计调度程序完成多实体成本分摊) as a critical system action',
            'Then the system must post balanced, proportional cost split journal entries under "account.move" (会计分录模型)',
            'And update the clearing state "clearing_state" to "cleared" (已结清状态) on "agri.contract.settlement" (合同结算模型)'
        ])

    def test_05_loan_approval_financial_credit_rating_gating_check(self):
        """
        Scenario: Loan Approval Financial Credit Rating Gating Check (贷款审批信用评级门禁校验)
        Given a farmer credit loan application under "purchase.order" (采购订单模型) linked to "agri.contract.settlement" (合同结算模型)
        And the partner financial credit score "credit_score" is 520 points (且该业务伙伴的财务信用评分为520分)
        When the loan officer attempts to validate the credit loan (信贷专员尝试核准信用贷款) as a critical system action
        Then the system must block the credit loan validation
        And raise a ValidationError (验证错误): "Credit score below minimum required threshold (信用评分低于最低要求阈值)"
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a farmer credit loan application under "purchase.order" (采购订单模型) linked to "agri.contract.settlement" (合同结算模型)',
            'And the partner financial credit score "credit_score" is 520 points (且该业务伙伴的财务信用评分为520分)',
            'When the loan officer attempts to validate the credit loan (信贷专员尝试核准信用贷款) as a critical system action',
            'Then the system must block the credit loan validation',
            'And raise a ValidationError (验证错误): "Credit score below minimum required threshold (信用评分低于最低要求阈值)"'
        ])

    def test_06_contract_settlement_carbon_tax_penalty_split(self):
        """
        Scenario: Contract Settlement Carbon Tax Penalty Split (合同结算碳税罚款分摊)
        Given a farming settlement invoice under "account.move" (日记账分录模型) linked to "agri.contract.settlement" (合同结算模型) with status (状态) "draft" (草稿)
        And the harvesting contractor's tractor fleet exceeds its carbon quota
        When the settlement clerk attempts to validate the contract payment via action "action_calculate_contract_tax" (计算合同碳税动作)
        Then the system automatically posts a carbon tax penalty split invoice under "account.move" (日记账分录模型)
        And distributes the carbon penalty amount across responsible contractor partner accounts (在责任承包商伙伴账户之间分摊罚款金额)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a farming settlement invoice under "account.move" (日记账分录模型) linked to "agri.contract.settlement" (合同结算模型) with status (状态) "draft" (草稿)',
            "And the harvesting contractor's tractor fleet exceeds its carbon quota",
            'When the settlement clerk attempts to validate the contract payment via action "action_calculate_contract_tax" (计算合同碳税动作)',
            'Then the system automatically posts a carbon tax penalty split invoice under "account.move" (日记账分录模型)',
            'And distributes the carbon penalty amount across responsible contractor partner accounts (在责任承包商伙伴账户之间分摊罚款金额)'
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
