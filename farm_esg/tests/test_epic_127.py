# -*- coding: utf-8 -*-
from odoo.addons.farm_core.tests.bdd_base import BddTransactionCase
from odoo.exceptions import UserError, ValidationError

class TestEpic127(BddTransactionCase):
    """ BDD Test Suite for Epic 127: Epic 127 Bioenergy ESG Marketplace (生物质能与ESG市场交易管理体系) """

    def setUp(self):
        super(TestEpic127, self).setUp()

    def test_01_crop_biomass_biogas_direct_offset_calculations(self):
        """
        Scenario: Crop Biomass Biogas direct offset calculations (作物生物质能沼气直接抵消计算机制)
        Given biomass transfers managed under "stock.move" (库存移动模型) linked to an ESG record under "agri.bioenergy.esg" (生物质能ESG模型)
        And the biomass transfer waste type "waste_type" is "crop_residue" (且该生物质转移废弃物类型字段值为农作物残余)
        When the operations manager logs a biomass weight "biomass_weight" of 5000.0 kg (当运营经理记录生物质重量字段值为5000.0千克时)
        Then the system must calculate the biogas yield volume "biogas_volume" as 600.0 m³ (系统必须计算出沼气产出量字段值为600.0立方米)
        And automatically record the carbon offset value "carbon_offset_kg" as 720.0 kg on "agri.bioenergy.esg" (并在生物质能ESG模型上自动记录碳抵消量字段值为720.0千克)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given biomass transfers managed under "stock.move" (库存移动模型) linked to an ESG record under "agri.bioenergy.esg" (生物质能ESG模型)',
            'And the biomass transfer waste type "waste_type" is "crop_residue" (且该生物质转移废弃物类型字段值为农作物残余)',
            'When the operations manager logs a biomass weight "biomass_weight" of 5000.0 kg (当运营经理记录生物质重量字段值为5000.0千克时)',
            'Then the system must calculate the biogas yield volume "biogas_volume" as 600.0 m³ (系统必须计算出沼气产出量字段值为600.0立方米)',
            'And automatically record the carbon offset value "carbon_offset_kg" as 720.0 kg on "agri.bioenergy.esg" (并在生物质能ESG模型上自动记录碳抵消量字段值为720.0千克)'
        ])

    def test_02_prohibited_nonorganic_fertilizer_esg_penalty_block_esg(self):
        """
        Scenario: Prohibited Non-Organic Fertilizer ESG Penalty Block (禁用非有机肥料的ESG惩罚性扣分与品牌拦截机制)
        Given an ESG rating evaluation record under "agri.bioenergy.esg" (生物质能ESG模型) with rating score "esg_rating_score" of 85.0 (且其信用评分字段值为85.0)
        And a synthetic fertilizer application logged under "agri.fertilizer.application" (且在肥料施用模型下记录了合成肥料施用数据)
        When the compliance engine evaluates the ESG penalty criteria (当合规引擎评估ESG惩罚标准时)
        Then the validation system must apply a score penalty "rating_penalty" of -40.0 points on "agri.bioenergy.esg" (验证系统必须在生物质能ESG模型上应用分值扣减-40.0分)
        And update the dynamic rating score "esg_rating_score" to 45.0 (并更新动态信用评分字段值为45.0)
        And strictly block premium organic brand seals on "stock.move" (并在库存移动模型上拦截优质有机品牌标签应用)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an ESG rating evaluation record under "agri.bioenergy.esg" (生物质能ESG模型) with rating score "esg_rating_score" of 85.0 (且其信用评分字段值为85.0)',
            'And a synthetic fertilizer application logged under "agri.fertilizer.application" (且在肥料施用模型下记录了合成肥料施用数据)',
            'When the compliance engine evaluates the ESG penalty criteria (当合规引擎评估ESG惩罚标准时)',
            'Then the validation system must apply a score penalty "rating_penalty" of -40.0 points on "agri.bioenergy.esg" (验证系统必须在生物质能ESG模型上应用分值扣减-40.0分)',
            'And update the dynamic rating score "esg_rating_score" to 45.0 (并更新动态信用评分字段值为45.0)',
            'And strictly block premium organic brand seals on "stock.move" (并在库存移动模型上拦截优质有机品牌标签应用)'
        ])

    def test_03_tractor_scope_1_direct_emissions_audit_compile_scope_1(self):
        """
        Scenario: Tractor Scope 1 Direct Emissions Audit Compile (拖拉机Scope 1直接排放数据采集与审计编译)
        Given a biomass hauling tractor mission under "mrp.workorder" (作业任务模型) linked to a bioenergy record under "agri.bioenergy.esg" (生物质能ESG模型)
        And the mission state "state" is "done" (且该作业任务状态字段值为已完成状态)
        When the auditor compiles the Scope 1 direct emissions "scope1_emissions" with diesel fuel consumed "fuel_consumed" of 45.0 L (当审计员使用柴油消耗量45.0升编译Scope 1直接排放数据时)
        Then the system must calculate fuel consumption using the conversion factor of 2.68 kg CO2 per liter (系统必须采用每升柴油2.68千克二氧化碳的转换系数计算燃油消耗)
        And update the Scope 1 direct emissions "scope1_emissions" to 120.6 kg CO2 on "agri.bioenergy.esg" (并在生物质能ESG模型上将Scope 1直接排放量字段值更新为120.6千克二氧化碳)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a biomass hauling tractor mission under "mrp.workorder" (作业任务模型) linked to a bioenergy record under "agri.bioenergy.esg" (生物质能ESG模型)',
            'And the mission state "state" is "done" (且该作业任务状态字段值为已完成状态)',
            'When the auditor compiles the Scope 1 direct emissions "scope1_emissions" with diesel fuel consumed "fuel_consumed" of 45.0 L (当审计员使用柴油消耗量45.0升编译Scope 1直接排放数据时)',
            'Then the system must calculate fuel consumption using the conversion factor of 2.68 kg CO2 per liter (系统必须采用每升柴油2.68千克二氧化碳的转换系数计算燃油消耗)',
            'And update the Scope 1 direct emissions "scope1_emissions" to 120.6 kg CO2 on "agri.bioenergy.esg" (并在生物质能ESG模型上将Scope 1直接排放量字段值更新为120.6千克二氧化碳)'
        ])

    def test_04_scope_2_electricity_indirect_emissions_compilation_scope_2(self):
        """
        Scenario: Scope 2 Electricity indirect Emissions Compilation (沼气压缩机Scope 2电力间接排放数据编译机制)
        Given energy monitoring on biogas compressors managed under "agri.energy.meter" (电能计量模型) linked to "agri.bioenergy.esg" (生物质能ESG模型)
        And the active electricity consumed "electricity_used" is 350.0 kWh (且当前用电量字段值为350.0度)
        When logging electricity consumption and applying the regional emission factor "emission_factor" of 0.5271 kg CO2 per kWh (当记录电力消耗并应用每度电0.5271千克二氧化碳的区域排放因子时)
        Then the system must calculate and write the indirect Scope 2 carbon footprint "scope2_emissions" as 184.485 kg CO2 (系统必须计算并将间接Scope 2碳足迹字段值写入为184.485千克二氧化碳)
        And update the energy source compliance status "source_status" to "verified" on "agri.bioenergy.esg" (并在生物质能ESG模型上将能源来源合规状态字段值更新为已验证状态)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given energy monitoring on biogas compressors managed under "agri.energy.meter" (电能计量模型) linked to "agri.bioenergy.esg" (生物质能ESG模型)',
            'And the active electricity consumed "electricity_used" is 350.0 kWh (且当前用电量字段值为350.0度)',
            'When logging electricity consumption and applying the regional emission factor "emission_factor" of 0.5271 kg CO2 per kWh (当记录电力消耗并应用每度电0.5271千克二氧化碳的区域排放因子时)',
            'Then the system must calculate and write the indirect Scope 2 carbon footprint "scope2_emissions" as 184.485 kg CO2 (系统必须计算并将间接Scope 2碳足迹字段值写入为184.485千克二氧化碳)',
            'And update the energy source compliance status "source_status" to "verified" on "agri.bioenergy.esg" (并在生物质能ESG模型上将能源来源合规状态字段值更新为已验证状态)'
        ])

    def test_05_carbon_neutral_offset_credit_allocation_som(self):
        """
        Scenario: Carbon Neutral Offset Credit Allocation (碳中和土壤有机质SOM碳信用额度分配与账务核算)
        Given certified soil organic matter SOM carbon offsets managed under "agri.regenerative.soil" (土壤再生记录模型)
        And the verified carbon offset amount "som_offset_credits" is 2.5 tCO2e (且经核验的碳抵消信用额度字段值为2.5吨二氧化碳当量)
        When the sustainability officer allocates the credit to the active ESG marketplace transaction under "agri.bioenergy.esg" (当可持续发展专员将该额度分配至生物质能ESG模型下的活跃ESG市场交易时)
        Then the system must verify the certification credentials and update the credit offset status "credit_status" to "allocated" on "agri.bioenergy.esg" (系统必须核验认证资质并将信用额度抵消状态字段值更新为已分配状态)
        And log the credit transfer details in the audit trail of "mail.thread" (并在邮件线程模型的审计轨迹中记录信用额度转移详情)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given certified soil organic matter SOM carbon offsets managed under "agri.regenerative.soil" (土壤再生记录模型)',
            'And the verified carbon offset amount "som_offset_credits" is 2.5 tCO2e (且经核验的碳抵消信用额度字段值为2.5吨二氧化碳当量)',
            'When the sustainability officer allocates the credit to the active ESG marketplace transaction under "agri.bioenergy.esg" (当可持续发展专员将该额度分配至生物质能ESG模型下的活跃ESG市场交易时)',
            'Then the system must verify the certification credentials and update the credit offset status "credit_status" to "allocated" on "agri.bioenergy.esg" (系统必须核验认证资质并将信用额度抵消状态字段值更新为已分配状态)',
            'And log the credit transfer details in the audit trail of "mail.thread" (并在邮件线程模型的审计轨迹中记录信用额度转移详情)'
        ])

    def test_06_esg_carbon_credit_clearing_margin_limit_enforcement_esg(self):
        """
        Scenario: ESG Carbon Credit Clearing Margin Limit Enforcement (ESG碳信用额度联合清算保证金限额合规校验)
        Given an ESG carbon credit trade under "sale.order" (销售订单模型) linked to a marketplace record under "agri.bioenergy.esg" (生物质能ESG模型)
        And the marketplace required joint clearing margin "clearing_margin_limit" is 15000.0 USD (且交易平台要求的最低联合清算保证金限额字段值为15000.0美元)
        And the active transaction's deposited margin balance "margin_balance" is 12500.0 USD (且当前交易已存入的实际保证金余额字段值为12500.0美元)
        When the financial controller attempts to validate the trade confirmation (当财务控制官尝试验证该交易确认时)
        Then the compliance engine must block the clearing transaction under "account.move" (系统合规引擎必须拦截会计分录模型下的交易清算)
        And raise a ValidationError (系统必须抛出验证错误) with message "Insufficient ESG trade clearing margin balance" (包含"ESG交易清算保证金余额不足"提示信息)
        And maintain the ESG record state "state" as "draft" (并保持生物质能交易记录状态字段值为草稿状态)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an ESG carbon credit trade under "sale.order" (销售订单模型) linked to a marketplace record under "agri.bioenergy.esg" (生物质能ESG模型)',
            'And the marketplace required joint clearing margin "clearing_margin_limit" is 15000.0 USD (且交易平台要求的最低联合清算保证金限额字段值为15000.0美元)',
            'And the active transaction's deposited margin balance "margin_balance" is 12500.0 USD (且当前交易已存入的实际保证金余额字段值为12500.0美元)',
            'When the financial controller attempts to validate the trade confirmation (当财务控制官尝试验证该交易确认时)',
            'Then the compliance engine must block the clearing transaction under "account.move" (系统合规引擎必须拦截会计分录模型下的交易清算)',
            'And raise a ValidationError (系统必须抛出验证错误) with message "Insufficient ESG trade clearing margin balance" (包含"ESG交易清算保证金余额不足"提示信息)',
            'And maintain the ESG record state "state" as "draft" (并保持生物质能交易记录状态字段值为草稿状态)'
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
