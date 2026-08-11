# -*- coding: utf-8 -*-
from odoo.addons.farm_core.tests.bdd_base import BddTransactionCase
from odoo.exceptions import UserError, ValidationError

class TestEpic060(BddTransactionCase):
    """ BDD Test Suite for Epic 060: Epic 060 Carbon ESG Ledger (碳排放与ESG账本) """

    def setUp(self):
        super(TestEpic060, self).setUp()

    def test_01_scope_1_direct_diesel_fuel_emission_compilation(self):
        """
        Scenario: Scope 1 Direct Diesel Fuel Emission Compilation
        Given a completed crop harvesting workorder under "mrp.workorder" (生产工单) has logged a machinery diesel consumption of 120.0 Liters
        When the supervisor closes and validates the workorder
        Then the system automatically triggers the Scope 1 emissions engine (自动触发Scope 1直排引擎)
        And calculates direct CO2 emissions using a conversion factor of 2.68 kg CO2 per Liter
        And posts a direct emissions log of 321.6 kg CO2e on the carbon ledger "agri.carbon.ledger" (碳排放账本) for the active "res.company" (公司)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a completed crop harvesting workorder under "mrp.workorder" (生产工单) has logged a machinery diesel consumption of 120.0 Liters',
            'When the supervisor closes and validates the workorder',
            'Then the system automatically triggers the Scope 1 emissions engine (自动触发Scope 1直排引擎)',
            'And calculates direct CO2 emissions using a conversion factor of 2.68 kg CO2 per Liter',
            'And posts a direct emissions log of 321.6 kg CO2e on the carbon ledger "agri.carbon.ledger" (碳排放账本) for the active "res.company" (公司)'
        ])

    def test_02_scope_2_indirect_electricity_emission_compilation(self):
        """
        Scenario: Scope 2 Indirect Electricity Emission Compilation
        Given a greenhouse climate-controlled workstation under "mrp.workcenter" (工作中心) has logged an electricity consumption of 1500.0 kWh
        When the monthly utility and energy evaluation routine runs
        Then the system automatically initiates the Scope 2 emission compiling pipeline (自动启动Scope 2碳排放计算流水线)
        And calculates indirect CO2 emissions using a standard regional power factor of 0.7 kg CO2 per kWh
        And records an indirect emissions log of 1050.0 kg CO2e on "agri.carbon.ledger" (碳排放账本)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a greenhouse climate-controlled workstation under "mrp.workcenter" (工作中心) has logged an electricity consumption of 1500.0 kWh',
            'When the monthly utility and energy evaluation routine runs',
            'Then the system automatically initiates the Scope 2 emission compiling pipeline (自动启动Scope 2碳排放计算流水线)',
            'And calculates indirect CO2 emissions using a standard regional power factor of 0.7 kg CO2 per kWh',
            'And records an indirect emissions log of 1050.0 kg CO2e on "agri.carbon.ledger" (碳排放账本)'
        ])

    def test_03_carbon_offset_soil_organic_matter_credits(self):
        """
        Scenario: Carbon Offset Soil Organic Matter Credits
        Given a soil composition laboratory report is registered under "agri.field.service" (田间服务记录)
        And the test registers a soil organic matter (SOM) increase of 0.5% over the past campaign
        When the compliance officer validates the laboratory findings
        Then the system calculates the organic carbon sequestration capacity
        And allocates a carbon offset credit of 2.5 Tons CO2e to the parcel's ledger card under "agri.esg.ledger" (ESG台账)
        And flags the credits as "active" (激活) with verified lab document reference
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a soil composition laboratory report is registered under "agri.field.service" (田间服务记录)',
            'And the test registers a soil organic matter (SOM) increase of 0.5% over the past campaign',
            'When the compliance officer validates the laboratory findings',
            'Then the system calculates the organic carbon sequestration capacity',
            'And allocates a carbon offset credit of 2.5 Tons CO2e to the parcel\'s ledger card under "agri.esg.ledger" (ESG台账)',
            'And flags the credits as "active" (激活) with verified lab document reference'
        ])

    def test_04_multilot_product_carbon_footprint_labeling(self):
        """
        Scenario: Multi-Lot Product Carbon Footprint Labeling
        Given a finished product lot of organic milling flour is created under "stock.lot" (库存批次)
        And the lot inherits combined emissions from its parent crop and processing batches
        When the consumer scans the tracking QR-code on the product's trace portal
        Then the system aggregates the total cumulative carbon footprint (Scope 1 + Scope 2) as 0.18 kg CO2e per kg product
        And dynamically displays the verified green carbon-neutral rating badge (绿色碳中和评级标章) on the portal page
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a finished product lot of organic milling flour is created under "stock.lot" (库存批次)',
            'And the lot inherits combined emissions from its parent crop and processing batches',
            "When the consumer scans the tracking QR-code on the product's trace portal",
            'Then the system aggregates the total cumulative carbon footprint (Scope 1 + Scope 2) as 0.18 kg CO2e per kg product',
            'And dynamically displays the verified green carbon-neutral rating badge (绿色碳中和评级标章) on the portal page'
        ])

    def test_05_annual_company_carbon_neutrality_audit(self):
        """
        Scenario: Annual Company Carbon Neutrality Audit
        Given a cooperative company "res.company" (公司) has recorded 120.0 Tons of annual greenhouse emissions on "agri.carbon.ledger" (碳排放账本)
        And the company has generated 135.0 Tons of verified methane biogas offsets on "agri.esg.ledger" (ESG台账)
        When the compliance auditor runs the annual sustainability audit tool
        Then the system determines that the company has achieved a net-negative carbon balance of -15.0 Tons CO2e
        And logs a certified Carbon Neutrality Index score of "A+" (碳中和指数A+评级) on the corporate dashboard
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a cooperative company "res.company" (公司) has recorded 120.0 Tons of annual greenhouse emissions on "agri.carbon.ledger" (碳排放账本)',
            'And the company has generated 135.0 Tons of verified methane biogas offsets on "agri.esg.ledger" (ESG台账)',
            'When the compliance auditor runs the annual sustainability audit tool',
            'Then the system determines that the company has achieved a net-negative carbon balance of -15.0 Tons CO2e',
            'And logs a certified Carbon Neutrality Index score of "A+" (碳中和指数A+评级) on the corporate dashboard'
        ])

    def test_06_carbon_ledger_audit_compilation_database_lock(self):
        """
        Scenario: Carbon Ledger Audit Compilation Database Lock
        Given a cooperative company registered as model "res.company" (公司)
        When the compliance auditor runs the annual sustainability audit tool to compile the Carbon Neutrality Index under model "agri.carbon.ledger" (碳排放账本)
        Then the system must apply a database-level write-lock FOR UPDATE (行级锁) on all the company's carbon ledger and ESG offset lines for the current fiscal year
        And prevent other concurrent emissions logging or credit liquidations under "agri.esg.ledger" (ESG台账) from modifying values until the audit is completed
        And raise a ValidationError with code "CARBON_LEDGER_LOCKED_FOR_AUDIT" (年度碳账本正处于审计锁定期，禁止更新数据) if any write operation is attempted during the locked audit session
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a cooperative company registered as model "res.company" (公司)',
            'When the compliance auditor runs the annual sustainability audit tool to compile the Carbon Neutrality Index under model "agri.carbon.ledger" (碳排放账本)',
            "Then the system must apply a database-level write-lock FOR UPDATE (行级锁) on all the company's carbon ledger and ESG offset lines for the current fiscal year",
            'And prevent other concurrent emissions logging or credit liquidations under "agri.esg.ledger" (ESG台账) from modifying values until the audit is completed',
            'And raise a ValidationError with code "CARBON_LEDGER_LOCKED_FOR_AUDIT" (年度碳账本正处于审计锁定期，禁止更新数据) if any write operation is attempted during the locked audit session'
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
