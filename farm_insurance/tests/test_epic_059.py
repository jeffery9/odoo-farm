# -*- coding: utf-8 -*-
from odoo.addons.farm_core.tests.bdd_base import BddTransactionCase
from odoo.exceptions import UserError, ValidationError

class TestEpic059(BddTransactionCase):
    """ BDD Test Suite for Epic 059: Epic 059 Agricultural Risk Insurance (农业风险保险) """

    def setUp(self):
        super(TestEpic059, self).setUp()

    def test_01_extreme_wind_weather_index_claim_trigger(self):
        """
        Scenario: Extreme Wind Weather Index Claim Trigger
        Given an active crop insurance policy is registered under "agri.insurance.policy" (农业保险单)
        And the policy specifies an extreme wind index trigger threshold of 20.0 m/s
        When the local telemetry weather station sensors log wind speeds of 22.5 m/s
        Then the system automatically triggers a draft insurance claim file (自动创建草稿理赔单)
        And dispatches an automated on-site verification mission under "agri.field.service" (田间服务记录) for adjusters
        And updates the claim record status to "filed" (已报案)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an active crop insurance policy is registered under "agri.insurance.policy" (农业保险单)',
            'And the policy specifies an extreme wind index trigger threshold of 20.0 m/s',
            'When the local telemetry weather station sensors log wind speeds of 22.5 m/s',
            'Then the system automatically triggers a draft insurance claim file (自动创建草稿理赔单)',
            'And dispatches an automated on-site verification mission under "agri.field.service" (田间服务记录) for adjusters',
            'And updates the claim record status to "filed" (已报案)'
        ])

    def test_02_drought_heat_index_insurance_audit_scheduling(self):
        """
        Scenario: Drought Heat Index Insurance Audit Scheduling
        Given an organic farming crop insurance policy under "agri.insurance.policy" (农业保险单)
        And the drought index trigger is set to 15 consecutive drought days (温度大于35°C且降雨量小于1.0mm)
        When the system's weather database audit registers the 16th consecutive drought day for Corn Parcel B
        Then the system automatically schedules an on-site crop health damage audit task under "agri.field.service" (田间服务记录)
        And flags the insurance policy record with a high-risk priority alert (标记高风险警报)
        And writes the drought telemetry logs to the insurance policy record chatter
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an organic farming crop insurance policy under "agri.insurance.policy" (农业保险单)',
            'And the drought index trigger is set to 15 consecutive drought days (温度大于35°C且降雨量小于1.0mm)',
            "When the system's weather database audit registers the 16th consecutive drought day for Corn Parcel B",
            'Then the system automatically schedules an on-site crop health damage audit task under "agri.field.service" (田间服务记录)',
            'And flags the insurance policy record with a high-risk priority alert (标记高风险警报)',
            'And writes the drought telemetry logs to the insurance policy record chatter'
        ])

    def test_03_flood_rainfall_index_claim_automatic_processing(self):
        """
        Scenario: Flood Rainfall Index Claim Automatic Processing
        Given a crop parcel monitored under an active insurance policy "agri.insurance.policy" (农业保险单)
        When rainfall sensors log a precipitation of 120.0 mm within a 24-hour window
        Then the system automatically generates a flood damage claim sheet
        And computes a damage confidence score of 92.0% based on historical flood modeling
        And transitions the claim record status to "under_review" (审查中)
        And attaches the spatial sensor logs to the claim documentation file
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a crop parcel monitored under an active insurance policy "agri.insurance.policy" (农业保险单)',
            'When rainfall sensors log a precipitation of 120.0 mm within a 24-hour window',
            'Then the system automatically generates a flood damage claim sheet',
            'And computes a damage confidence score of 92.0% based on historical flood modeling',
            'And transitions the claim record status to "under_review" (审查中)',
            'And attaches the spatial sensor logs to the claim documentation file'
        ])

    def test_04_crop_damage_negligence_protection_and_claim_block(self):
        """
        Scenario: Crop Damage Negligence Protection and Claim Block
        Given a frost insurance policy under "agri.insurance.policy" (农业保险单) is active for Tea Parcel A
        And the policy requires a minimum soil moisture content of 20.0% to prevent root frost death
        When the farmer attempts to manually file a frost damage claim in "agri.insurance.policy" (农业保险单)
        And the system queries soil moisture sensor telemetry indicating moisture levels were neglected at 12.0% prior to the frost event
        Then the system blocks the claim confirmation process (阻断理赔确认流程)
        And raises a ValidationError "Claim blocked due to crop hydration neglect prior to freeze" (由于低温前植被缺水疏于管理，理赔申请已被拒绝)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a frost insurance policy under "agri.insurance.policy" (农业保险单) is active for Tea Parcel A',
            'And the policy requires a minimum soil moisture content of 20.0% to prevent root frost death',
            'When the farmer attempts to manually file a frost damage claim in "agri.insurance.policy" (农业保险单)',
            'And the system queries soil moisture sensor telemetry indicating moisture levels were neglected at 12.0% prior to the frost event',
            'Then the system blocks the claim confirmation process (阻断理赔确认流程)',
            'And raises a ValidationError "Claim blocked due to crop hydration neglect prior to freeze" (由于低温前植被缺水疏于管理，理赔申请已被拒绝)'
        ])

    def test_05_insurance_payout_financial_settlement_netting(self):
        """
        Scenario: Insurance Payout Financial Settlement Netting
        Given an approved insurance claim under "agri.insurance.policy" (农业保险单) with a payout value of 5000.0 USD
        And the farmer has an outstanding cooperative inventory debt of 3500.0 USD logged under "account.move" (应收账单)
        When the financial manager executes the settlement netting automated run
        Then the system automatically nets the insurance payout against the outstanding cooperative debt (自动抵扣合作社欠款)
        And generates a clearing netting journal entry under "account.move" (日记账分录)
        And creates a net payment invoice of 1500.0 USD for the final bank transfer settlement
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an approved insurance claim under "agri.insurance.policy" (农业保险单) with a payout value of 5000.0 USD',
            'And the farmer has an outstanding cooperative inventory debt of 3500.0 USD logged under "account.move" (应收账单)',
            'When the financial manager executes the settlement netting automated run',
            'Then the system automatically nets the insurance payout against the outstanding cooperative debt (自动抵扣合作社欠款)',
            'And generates a clearing netting journal entry under "account.move" (日记账分录)',
            'And creates a net payment invoice of 1500.0 USD for the final bank transfer settlement'
        ])

    def test_06_insurance_claim_payout_settlement_concurrency_lock(self):
        """
        Scenario: Insurance Claim Payout Settlement Concurrency Lock
        Given an approved insurance claim under "agri.insurance.policy" (农业保险单)
        And an outstanding cooperative customer invoice under model "account.move" (应收账单)
        When the financial manager executes the settlement netting automated run (确认债务轧差抵扣)
        Then the system must acquire a database row lock FOR UPDATE on both the insurance claim and invoice records
        And verify that neither record has been modified or cleared by a concurrent bank transfer or credit queue
        And raise a ValidationError with code "SETTLEMENT_RECORD_LOCKED" (理赔单或账单正在进行清算，请勿重复操作) to abort and roll back the transaction if a lock collision occurs
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an approved insurance claim under "agri.insurance.policy" (农业保险单)',
            'And an outstanding cooperative customer invoice under model "account.move" (应收账单)',
            'When the financial manager executes the settlement netting automated run (确认债务轧差抵扣)',
            'Then the system must acquire a database row lock FOR UPDATE on both the insurance claim and invoice records',
            'And verify that neither record has been modified or cleared by a concurrent bank transfer or credit queue',
            'And raise a ValidationError with code "SETTLEMENT_RECORD_LOCKED" (理赔单或账单正在进行清算，请勿重复操作) to abort and roll back the transaction if a lock collision occurs'
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
