# -*- coding: utf-8 -*-
from odoo.addons.farm_core.tests.bdd_base import BddTransactionCase
from odoo.exceptions import UserError, ValidationError

class TestEpic074(BddTransactionCase):
    """ BDD Test Suite for Epic 074: Epic 074 Post Harvest Quality Management (收获后质量管理) """

    def setUp(self):
        super(TestEpic074, self).setUp()

    def test_01_fruit_firmness_lab_test_grading_gating(self):
        """
        Scenario: Fruit Firmness Lab Test Grading Gating (水果硬度实验室测试分级控制闸)
        Given a quality inspection session under "agri.postharvest.qc" (收获后质检模型) in state "draft" (草稿)
        When the lab technician records average apple penetrometer firmness as "4.5 kg/cm²" (当实验员记录苹果平均硬度计硬度为4.5 kg/cm²，低于特级标准6.0 kg/cm²)
        Then the system must automatically downgrade the lot's quality grade from "Extra Fancy" (特一级) to "Grade B" (标准二级)
        And raise a ValidationError (验证错误) message "Labeling Blocked: Firmness below premium brand limits" (贴标被阻止：硬度低于特级品牌限制) if a user attempts to print premium barcode labels
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a quality inspection session under "agri.postharvest.qc" (收获后质检模型) in state "draft" (草稿)',
            'When the lab technician records average apple penetrometer firmness as "4.5 kg/cm²" (当实验员记录苹果平均硬度计硬度为4.5 kg/cm²，低于特级标准6.0 kg/cm²)',
            'Then the system must automatically downgrade the lot's quality grade from "Extra Fancy" (特一级) to "Grade B" (标准二级)',
            'And raise a ValidationError (验证错误) message "Labeling Blocked: Firmness below premium brand limits" (贴标被阻止：硬度低于特级品牌限制) if a user attempts to print premium barcode labels'
        ])

    def test_02_coldchain_transport_temperature_sensor_telemetry_failure(self):
        """
        Scenario: Cold-Chain Transport Temperature Sensor Telemetry Failure (冷链运输温度传感器遥测丢失处理)
        Given a refrigerated transport shipment tracked under "stock.picking" (库存调拨)
        When container temperature sensors fail to report telemetry updates for over "4 hours" (当冷藏集装箱温度传感器超过4小时未上报遥测更新)
        Then the system must flag the container's quality status on "agri.postharvest.qc" (收获后质检模型) as "Sensory Failed" (传感器故障)
        And dispatch an urgent alert "Telemetry Offline: Check refrigerated container power source" (遥测离线：检查冷藏箱电源) to the logistics coordinator dashboard
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a refrigerated transport shipment tracked under "stock.picking" (库存调拨)',
            'When container temperature sensors fail to report telemetry updates for over "4 hours" (当冷藏集装箱温度传感器超过4小时未上报遥测更新)',
            'Then the system must flag the container's quality status on "agri.postharvest.qc" (收获后质检模型) as "Sensory Failed" (传感器故障)',
            'And dispatch an urgent alert "Telemetry Offline: Check refrigerated container power source" (遥测离线：检查冷藏箱电源) to the logistics coordinator dashboard'
        ])

    def test_03_postharvest_fruit_disease_coldchain_lockout(self):
        """
        Scenario: Post-Harvest Fruit Disease Cold-Chain Lockout (收获后水果病害冷链异常锁定)
        Given an active cold-storage room under "stock.location" (库存库位)
        When indoor gas sensors register ethylene concentration exceeding "1.0 PPM" (当室内气体传感器记录乙烯浓度超过1.0 PPM，预示果实腐烂风险)
        Then the system must trigger an active PLC relay command "activate_maximum_cooling" (激活最大冷却) to reduce cooling coil temperature on the HVAC unit
        And lock the storage location quality status on "agri.postharvest.qc" (收获后质检模型) to state "alert" (报警) to quarantine infected lots
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an active cold-storage room under "stock.location" (库存库位)',
            'When indoor gas sensors register ethylene concentration exceeding "1.0 PPM" (当室内气体传感器记录乙烯浓度超过1.0 PPM，预示果实腐烂风险)',
            'Then the system must trigger an active PLC relay command "activate_maximum_cooling" (激活最大冷却) to reduce cooling coil temperature on the HVAC unit',
            'And lock the storage location quality status on "agri.postharvest.qc" (收获后质检模型) to state "alert" (报警) to quarantine infected lots'
        ])

    def test_04_apple_starch_index_starch_conversion_gating(self):
        """
        Scenario: Apple Starch Index Starch Conversion Gating (苹果淀粉指数转化率控制闸)
        Given a quality inspection record for harvested crop lots under "agri.postharvest.qc" (收获后质检模型)
        When the laboratory logs the iodine starch conversion index as "8" (当实验室记录碘-淀粉转化指数为8，表明淀粉几乎完全转化为糖，保质期极短)
        Then the system must automatically restrict the maximum warehouse storage duration for this lot to "14 days" (自动将该批次的最大仓库储存期限限制为14天)
        And raise a high-priority dispatch task under "sale.order" (销售订单) forcing immediate shipping to prevent shelf-life expiration
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a quality inspection record for harvested crop lots under "agri.postharvest.qc" (收获后质检模型)',
            'When the laboratory logs the iodine starch conversion index as "8" (当实验室记录碘-淀粉转化指数为8，表明淀粉几乎完全转化为糖，保质期极短)',
            'Then the system must automatically restrict the maximum warehouse storage duration for this lot to "14 days" (自动将该批次的最大仓库储存期限限制为14天)',
            'And raise a high-priority dispatch task under "sale.order" (销售订单) forcing immediate shipping to prevent shelf-life expiration'
        ])

    def test_05_complete_postharvest_gxp_treatment_traceability_gxp(self):
        """
        Scenario: Complete Post-Harvest GxP Treatment Traceability (完整收获后GxP处理溯源链路)
        Given an outgoing delivery picking under "stock.picking" (库存调拨) for export fruit lots
        When the system validates the export food safety tracing passport on "stock.lot" (库存批次)
        Then the system must verify that all mandatory post-harvest chemical wash and sanitization steps on "agri.postharvest.qc" (收获后质检模型) are recorded in state "completed" (已完成)
        And raise a ValidationError (验证错误) message "Traceability Defect: Mandatory chemical wash logs missing" (追溯缺陷：缺失强制性化学清洗记录) if any treatment log is absent
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an outgoing delivery picking under "stock.picking" (库存调拨) for export fruit lots',
            'When the system validates the export food safety tracing passport on "stock.lot" (库存批次)',
            'Then the system must verify that all mandatory post-harvest chemical wash and sanitization steps on "agri.postharvest.qc" (收获后质检模型) are recorded in state "completed" (已完成)',
            'And raise a ValidationError (验证错误) message "Traceability Defect: Mandatory chemical wash logs missing" (追溯缺陷：缺失强制性化学清洗记录) if any treatment log is absent'
        ])

    def test_06_coldstorage_power_loss_alternative_refrigeration_interlock(self):
        """
        Scenario: Cold-Storage Power Loss Alternative Refrigeration Interlock (冷库动力失电备用制冷联锁保护)
        Given cold-storage rooms tracked under "stock.location" (库存库位)
        When the smart power grid monitor "iiot.device" (智能物联网设备) registers a main power grid failure (主电网失电断电) lasting over "30 seconds"
        Then the system must trigger an active PLC relay command to automatically boot the emergency diesel backup cooling generator
        And update the location's status on "agri.postharvest.qc" (收获后质检模型) to "backup_power" (备用电运行) and dispatch a priority warning to the facility manager
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given cold-storage rooms tracked under "stock.location" (库存库位)',
            'When the smart power grid monitor "iiot.device" (智能物联网设备) registers a main power grid failure (主电网失电断电) lasting over "30 seconds"',
            'Then the system must trigger an active PLC relay command to automatically boot the emergency diesel backup cooling generator',
            'And update the location's status on "agri.postharvest.qc" (收获后质检模型) to "backup_power" (备用电运行) and dispatch a priority warning to the facility manager'
        ])
