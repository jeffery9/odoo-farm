# -*- coding: utf-8 -*-
from odoo.addons.farm_core.tests.bdd_base import BddTransactionCase
from odoo.exceptions import UserError, ValidationError

class TestEpic044(BddTransactionCase):
    """ BDD Test Suite for Epic 044: Epic 044 Precision Production Foundation """

    def setUp(self):
        super(TestEpic044, self).setUp()

    def test_01_grain_moisture_target_blending_gating(self):
        """
        Scenario: Grain Moisture Target Blending Gating
        Given a grain milling production order "MO-MILL-2026-001" under model "mrp.production"
        And the target grain moisture level specification limit is set to a maximum of 14.5%
        When the warehouse operator issues a raw wheat lot "LOT-WHEAT-RAW-55" with a registered moisture content of 15.8% to the production order
        Then the system must block the production start operation, raising a ValidationError (原粮水分 15.8% 超过上限 14.5%，禁止投料生产)
        And mandate that a prior drying workorder step is executed on the wheat lot before reissue
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a grain milling production order "MO-MILL-2026-001" under model "mrp.production"',
            'And the target grain moisture level specification limit is set to a maximum of 14.5%',
            'When the warehouse operator issues a raw wheat lot "LOT-WHEAT-RAW-55" with a registered moisture content of 15.8% to the production order',
            'Then the system must block the production start operation, raising a ValidationError (原粮水分 15.8% 超过上限 14.5%，禁止投料生产)',
            'And mandate that a prior drying workorder step is executed on the wheat lot before reissue'
        ])

    def test_02_realtime_production_yield_deviation_alert(self):
        """
        Scenario: Real-time Production Yield Deviation Alert
        Given an active processing campaign "MO-PASTE-01" of model "mrp.production" converting raw tomatoes into concentrated paste
        And the target processing standard yield is configured as 15.0% compared to input mass
        When the operator records the completed output paste mass which corresponds to an actual yield of 11.8%
        Then the system must generate a high-priority quality deviation alert inside model "agri.precision.yield" (出率严重偏离预警)
        And log the negative yield deviation percentage of 3.2% as a critical warning in the manufacturing order chatter
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an active processing campaign "MO-PASTE-01" of model "mrp.production" converting raw tomatoes into concentrated paste',
            'And the target processing standard yield is configured as 15.0% compared to input mass',
            'When the operator records the completed output paste mass which corresponds to an actual yield of 11.8%',
            'Then the system must generate a high-priority quality deviation alert inside model "agri.precision.yield" (出率严重偏离预警)',
            'And log the negative yield deviation percentage of 3.2% as a critical warning in the manufacturing order chatter'
        ])

    def test_03_dynamic_recipe_material_scaling(self):
        """
        Scenario: Dynamic Recipe Material Scaling
        Given an organic fertilizer compounding recipe represented by Bill of Materials (BoM) "BOM-FERT-ORG" under model "mrp.bom"
        And the BoM defines components for a standard 100.0 kg output batch: 60.0 kg nitrogen compound and 40.0 kg potassium compound
        When the production planner scales the manufacturing order target output to 500.0 kg
        Then the system must dynamically recalculate the required component input lines to exactly 300.0 kg nitrogen compound and 200.0 kg potassium compound (配方原料等比动态缩放)
        And write the adjusted quantities to the scheduled production order materials lines
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an organic fertilizer compounding recipe represented by Bill of Materials (BoM) "BOM-FERT-ORG" under model "mrp.bom"',
            'And the BoM defines components for a standard 100.0 kg output batch: 60.0 kg nitrogen compound and 40.0 kg potassium compound',
            'When the production planner scales the manufacturing order target output to 500.0 kg',
            'Then the system must dynamically recalculate the required component input lines to exactly 300.0 kg nitrogen compound and 200.0 kg potassium compound (配方原料等比动态缩放)',
            'And write the adjusted quantities to the scheduled production order materials lines'
        ])

    def test_04_production_run_jidoka_safety_lock(self):
        """
        Scenario: Production Run Jidoka Safety Lock
        Given an active extraction mill workorder "WO-EXTRACT-04" of model "mrp.workorder" in state "ready"
        And the thermal warning threshold for the milling workcenter "MILL-WC-01" is set to 85.0 °C
        When the telemetry sensors of "MILL-WC-01" register an operating temperature of 87.5 °C (thermal threat)
        Then the system must trigger an emergency Jidoka safety lock (自働化安全锁停)
        And atomically transition the workorder status to "paused"
        And dispatch a critical alert event block to the PLC controller to cut motor power and sound the alarm
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an active extraction mill workorder "WO-EXTRACT-04" of model "mrp.workorder" in state "ready"',
            'And the thermal warning threshold for the milling workcenter "MILL-WC-01" is set to 85.0 °C',
            'When the telemetry sensors of "MILL-WC-01" register an operating temperature of 87.5 °C (thermal threat)',
            'Then the system must trigger an emergency Jidoka safety lock (自働化安全锁停)',
            'And atomically transition the workorder status to "paused"',
            'And dispatch a critical alert event block to the PLC controller to cut motor power and sound the alarm'
        ])

    def test_05_batch_quality_release_validation_check(self):
        """
        Scenario: Batch Quality Release Validation Check
        Given a completed crop oil manufacturing production run "MO-OIL-889" of model "mrp.production" awaiting final warehouse stock receipt
        And the quality control registry requires complete laboratory chemical assays for "Purity" and "Heavy Metals"
        When the warehouse worker attempts to validate the stock move to receive the finished oil into the storage location
        And the required laboratory assays are missing or incomplete in "agri.qc.sample"
        Then the system must hard-block the stock transfer validation, raising a ValidationError (质检结果未入库，成品油禁止入库/出货)
        And log an incomplete quality compliance flag on the target stock lot profile
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a completed crop oil manufacturing production run "MO-OIL-889" of model "mrp.production" awaiting final warehouse stock receipt',
            'And the quality control registry requires complete laboratory chemical assays for "Purity" and "Heavy Metals"',
            'When the warehouse worker attempts to validate the stock move to receive the finished oil into the storage location',
            'And the required laboratory assays are missing or incomplete in "agri.qc.sample"',
            'Then the system must hard-block the stock transfer validation, raising a ValidationError (质检结果未入库，成品油禁止入库/出货)',
            'And log an incomplete quality compliance flag on the target stock lot profile'
        ])

    def test_06_ingredient_inventory_row_lock_during_production_recipe_scaling(self):
        """
        Scenario: Ingredient Inventory Row Lock during Production Recipe Scaling
        Given a grain milling production order "MO-MILL-2026-001" under model "mrp.production" (生产订单)
        And a Bill of Materials under model "mrp.bom" (物料清单)
        When the production manager confirms the scaled material allocation (确认投料分配)
        Then the system must apply a row lock on the target stock lot records under model "stock.lot" (库存批次) using SELECT FOR UPDATE
        And raise a ValidationError with code "INGREDIENT_ALREADY_ALLOCATED" (原料批次已被并发生产订单占用，锁定失败) if another active production run is allocating the same lots
        And block the confirmation to prevent duplicate batch depletion
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a grain milling production order "MO-MILL-2026-001" under model "mrp.production" (生产订单)',
            'And a Bill of Materials under model "mrp.bom" (物料清单)',
            'When the production manager confirms the scaled material allocation (确认投料分配)',
            'Then the system must apply a row lock on the target stock lot records under model "stock.lot" (库存批次) using SELECT FOR UPDATE',
            'And raise a ValidationError with code "INGREDIENT_ALREADY_ALLOCATED" (原料批次已被并发生产订单占用，锁定失败) if another active production run is allocating the same lots',
            'And block the confirmation to prevent duplicate batch depletion'
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
