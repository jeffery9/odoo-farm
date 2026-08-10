# -*- coding: utf-8 -*-
from odoo.addons.farm_core.tests.bdd_base import BddTransactionCase
from odoo.exceptions import UserError, ValidationError

class TestEpic017(BddTransactionCase):
    """ BDD Test Suite for Epic 017: Epic 017 Tea Industry Management """

    def setUp(self):
        super(TestEpic017, self).setUp()

    def test_01_seasonal_flush_and_altitude_fingerprint_tracking(self):
        """
        Scenario: Seasonal flush and altitude fingerprint tracking
        Given a tea harvest event with "stock.lot" linked to parcel data
        When the system records the flush type (e.g. Pre-Qingming, Pre-Rain)
        Then the harvest lot must automatically inherit the parcel's altitude and slope fingerprints
        And the "tea_season" and "elevation_m" must be recorded as core quality dimensions on "stock.lot"
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a tea harvest event with "stock.lot" linked to parcel data',
            'When the system records the flush type (e.g. Pre-Qingming, Pre-Rain)',
            'Then the harvest lot must automatically inherit the parcel's altitude and slope fingerprints',
            'And the "tea_season" and "elevation_m" must be recorded as core quality dimensions on "stock.lot"'
        ])

    def test_02_tea_processing_recipe_modeling_and_rolling_passes(self):
        """
        Scenario: Tea processing recipe modeling and rolling passes
        Given a tea master defining a recipe in "farm.tea.recipe" for Oolong tea
        When processing parameters like "rolling_passes_count" is set to 4 and "target_moisture_percentage" is set to 5.0%
        Then the system must validate these against the BoM standards in "mrp.workorder"
        And ensure "rolling_passes_completed" is initialized to 0
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a tea master defining a recipe in "farm.tea.recipe" for Oolong tea',
            'When processing parameters like "rolling_passes_count" is set to 4 and "target_moisture_percentage" is set to 5.0%',
            'Then the system must validate these against the BoM standards in "mrp.workorder"',
            'And ensure "rolling_passes_completed" is initialized to 0'
        ])

    def test_03_tea_oxidation_fermentation_humidity_gating(self):
        """
        Scenario: Tea Oxidation Fermentation Humidity Gating
        Given a tea processing workorder in "mrp.workorder" during the oxidation (fermentation) stage
        And the active fermentation parameters are tracked in "agri.isl.tea.oxidation"
        When the environmental humidity reading registered by the IoT sensor drops below 85%
        Then the system must automatically raise an alarm alert via "AgriIncidentAlertMixin"
        And set the workorder state to "paused"
        And trigger an instruction to activate the micro-sprinklers
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a tea processing workorder in "mrp.workorder" during the oxidation (fermentation) stage',
            'And the active fermentation parameters are tracked in "agri.isl.tea.oxidation"',
            'When the environmental humidity reading registered by the IoT sensor drops below 85%',
            'Then the system must automatically raise an alarm alert via "AgriIncidentAlertMixin"',
            'And set the workorder state to "paused"',
            'And trigger an instruction to activate the micro-sprinklers'
        ])

    def test_04_multistage_traceability_from_fresh_leaf_to_finished_tea(self):
        """
        Scenario: Multi-stage traceability from fresh leaf to finished tea
        Given a consumer scans a finished tea package barcode linked to "stock.lot"
        When the portal displays the traceability information
        Then it must show the full chain from the specific tea garden parcel to the final processing artisan
        And include biochemical indices and oxidation logs from "agri.isl.tea.oxidation" linked via "AgriTraceabilityMixin"
        And support full bilingual English and Chinese (CN) display
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a consumer scans a finished tea package barcode linked to "stock.lot"',
            'When the portal displays the traceability information',
            'Then it must show the full chain from the specific tea garden parcel to the final processing artisan',
            'And include biochemical indices and oxidation logs from "agri.isl.tea.oxidation" linked via "AgriTraceabilityMixin"',
            'And support full bilingual English and Chinese (CN) display'
        ])

    def test_05_multilevel_cascade_safeguard_deletion_gating(self):
        """
        Scenario: Multi-Level Cascade Safeguard Deletion Gating (多级级联安全删除防护限制机制)
        Given an active tea production record is configured in "agri.tea.production" (茶叶生产模型) with status "draft" (草稿状态)
        And active physical traceability blocks are linked in "agri.isl.tea.oxidation" (茶叶氧化发酵记录模型)
        When a tea master attempts to delete the parent tea production record (当茶艺师尝试删除父级茶叶生产记录时)
        Then the system must execute cascade deletion check (系统必须执行级联删除检查)
        And raise a ValidationError (并且抛出验证错误) with message "Active traceability blocks exist, deletion blocked" (包含"存在活跃追溯块，删除拦截"提示信息)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an active tea production record is configured in "agri.tea.production" (茶叶生产模型) with status "draft" (草稿状态)',
            'And active physical traceability blocks are linked in "agri.isl.tea.oxidation" (茶叶氧化发酵记录模型)',
            'When a tea master attempts to delete the parent tea production record (当茶艺师尝试删除父级茶叶生产记录时)',
            'Then the system must execute cascade deletion check (系统必须执行级联删除检查)',
            'And raise a ValidationError (并且抛出验证错误) with message "Active traceability blocks exist, deletion blocked" (包含"存在活跃追溯块，删除拦截"提示信息)'
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
            'Given a crop parcel's soil stock lot in "stock.lot" (库存批次模型) with crop variety "Rose" (且作物物种已设置为玫瑰)',
            'And a smart evapotranspiration sensor registered in "iiot.device" (并且智能蒸腾量传感器已注册在工业物联网设备模型中)',
            'When the soil sensor logs an NPK reading drift of 25.0% (当土壤传感器记录到氮磷钾读数偏离比比例达到25.0%时)',
            'Then the system must trigger safe mode self-correction (系统必须自动执行安全模式自校准动作)',
            'And scale back the water drip runtime "drip_duration" to fallback 10.0 minutes (并且将滴灌时长字段值等比例缩减至备用时长值10.0分钟)',
            'And raise a ValidationError (并且系统抛出验证错误) with message "CRITICAL_SENSOR_DRIFT_DETECTED" (包含"传感器发生严重漂移，进入自愈模式"提示信息)'
        ])
