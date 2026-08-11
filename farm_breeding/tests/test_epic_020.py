# -*- coding: utf-8 -*-
from odoo.addons.farm_core.tests.bdd_base import BddTransactionCase
from odoo.exceptions import UserError, ValidationError

class TestEpic020(BddTransactionCase):
    """ BDD Test Suite for Epic 020: Epic 020 Nursery & Breeding """

    def setUp(self):
        super(TestEpic020, self).setUp()

    def test_01_nursery_factory_management_and_seedling_age_tracking(self):
        """
        Scenario: Nursery factory management and seedling age tracking
        Given a nursery lot in "agri.isl.lot.nursery" is in the "germination" stage
        When the nursery work is finished
        Then the system must trigger a "stock.picking" to move seedlings to the field
        And it should calculate the "Cumulative Seedling Age" as an initial parameter for the field tasks
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a nursery lot in "agri.isl.lot.nursery" is in the "germination" stage',
            'When the nursery work is finished',
            'Then the system must trigger a "stock.picking" to move seedlings to the field',
            'And it should calculate the "Cumulative Seedling Age" as an initial parameter for the field tasks'
        ])

    def test_02_germination_and_vigor_testing_for_seed_source_quality(self):
        """
        Scenario: Germination and vigor testing for seed source quality
        Given a batch of seeds is received on "stock.lot"
        When a germination test is performed in the lab and "germination_percentage" is recorded
        Then the system must use the "germination_percentage" to update the "Suggested Sowing Rate" in production orders
        And the record must conform to the bilingual quality report standard
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a batch of seeds is received on "stock.lot"',
            'When a germination test is performed in the lab and "germination_percentage" is recorded',
            'Then the system must use the "germination_percentage" to update the "Suggested Sowing Rate" in production orders',
            'And the record must conform to the bilingual quality report standard'
        ])

    def test_03_grafting_and_tissue_culture_loss_tracking(self):
        """
        Scenario: Grafting and tissue culture loss tracking
        Given a nursery manufacturing order (MO) in "mrp.production" for grafting
        When the process is complete
        Then the system must record the balance between "Input Scions/Seeds" and "Output Seedlings"
        And it should analyze the economic efficiency of different rootstock combinations
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a nursery manufacturing order (MO) in "mrp.production" for grafting',
            'When the process is complete',
            'Then the system must record the balance between "Input Scions/Seeds" and "Output Seedlings"',
            'And it should analyze the economic efficiency of different rootstock combinations'
        ])

    def test_04_pedigree_tracking_for_genetic_diversity(self):
        """
        Scenario: Pedigree tracking for genetic diversity
        Given a breeding program with multiple generations tracked on "agri.isl.lot.nursery"
        When I register a new variety cross in the system
        Then the system must record the maternal and paternal combinations and genetic traits using "germplasm_profile_id"
        And it should provide a visualization of the multi-generational pedigree tree
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a breeding program with multiple generations tracked on "agri.isl.lot.nursery"',
            'When I register a new variety cross in the system',
            'Then the system must record the maternal and paternal combinations and genetic traits using "germplasm_profile_id"',
            'And it should provide a visualization of the multi-generational pedigree tree'
        ])

    def test_05_dna_signature_genetic_quality_grs_gating_dnagrs(self):
        """
        Scenario: DNA Signature Genetic Quality GRS Gating (DNA特征遗传质量GRS安全闸门检测机制)
        Given an elite breeder seedling lot is registered on "product.template" (产品模板模型) with status "sel_active" (启用状态)
        When the lab performs a molecular genetic marker test and registers a failed "dna_authenticity_match" (当实验室执行分子遗传标记检测并登记DNA真实性匹配状态字段值为不匹配时)
        Then the system must raise a ValidationError (系统必须抛出验证错误) with message "DNA genetic signature mismatch" (包含"DNA特征不匹配"提示信息)
        And automatically set "mother_stock_eligible" to False (并且系统自动设置母本种质资格字段值为假) to block any mother-stock seed replication campaigns (以阻止其关联任何母本种子繁殖活动)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an elite breeder seedling lot is registered on "product.template" (产品模板模型) with status "sel_active" (启用状态)',
            'When the lab performs a molecular genetic marker test and registers a failed "dna_authenticity_match" (当实验室执行分子遗传标记检测并登记DNA真实性匹配状态字段值为不匹配时)',
            'Then the system must raise a ValidationError (系统必须抛出验证错误) with message "DNA genetic signature mismatch" (包含"DNA特征不匹配"提示信息)',
            'And automatically set "mother_stock_eligible" to False (并且系统自动设置母本种质资格字段值为假) to block any mother-stock seed replication campaigns (以阻止其关联任何母本种子繁殖活动)'
        ])

    def test_06_crop_parcel_evapotranspiration_sensor_drift(self):
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
            'Given a crop parcel\'s soil stock lot in "stock.lot" (库存批次模型) with crop variety "Rose" (且作物物种已设置为玫瑰)',
            'And a smart evapotranspiration sensor registered in "iiot.device" (并且智能蒸腾量传感器已注册在工业物联网设备模型中)',
            'When the soil sensor logs an NPK reading drift of 25.0% (当土壤传感器记录到氮磷钾读数偏离比比例达到25.0%时)',
            'Then the system must trigger safe mode self-correction (系统必须自动执行安全模式自校准动作)',
            'And scale back the water drip runtime "drip_duration" to fallback 10.0 minutes (并且将滴灌时长字段值等比例缩减至备用时长值10.0分钟)',
            'And raise a ValidationError (并且系统抛出验证错误) with message "CRITICAL_SENSOR_DRIFT_DETECTED" (包含"传感器发生严重漂移，进入自愈模式"提示信息)'
        ])
