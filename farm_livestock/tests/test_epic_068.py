# -*- coding: utf-8 -*-
from odoo.addons.farm_core.tests.bdd_base import BddTransactionCase
from odoo.exceptions import UserError, ValidationError

class TestEpic068(BddTransactionCase):
    """ BDD Test Suite for Epic 068: Epic 068 Livestock Health Monitoring (畜牧健康监测) """

    def setUp(self):
        super(TestEpic068, self).setUp()

    def test_01_swine_thermal_eartag_fever_quarantine_gate(self):
        """
        Scenario: Swine Thermal Ear-Tag Fever Quarantine Gate (生猪耳标体温发热隔离控制)
        Given a swine animal lot "stock.lot" (库存批次) registered under "agri.livestock.health" (畜牧健康监测模型) in state "monitored" (监视中)
        When the thermal RFID ear-tag telemetry logs an average body temperature of "41.2°C" (耳标遥测记录平均体温为41.2°C) which is greater than 40.5°C
        Then the system must set the health state to "quarantined" (已隔离) on the "agri.livestock.health" (畜牧健康监测模型) record
        And the system must block shipping validations for this animal lot on "stock.picking" (库存拣货单) with a ValidationError (验证错误) message "Animal Quarantine: Shipment blocked due to fever" (动物隔离：因发热阻断发运)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a swine animal lot "stock.lot" (库存批次) registered under "agri.livestock.health" (畜牧健康监测模型) in state "monitored" (监视中)',
            'When the thermal RFID ear-tag telemetry logs an average body temperature of "41.2°C" (耳标遥测记录平均体温为41.2°C) which is greater than 40.5°C',
            'Then the system must set the health state to "quarantined" (已隔离) on the "agri.livestock.health" (畜牧健康监测模型) record',
            'And the system must block shipping validations for this animal lot on "stock.picking" (库存拣货单) with a ValidationError (验证错误) message "Animal Quarantine: Shipment blocked due to fever" (动物隔离：因发热阻断发运)'
        ])

    def test_02_automated_sick_swine_pen_isolation_task(self):
        """
        Scenario: Automated Sick Swine Pen Isolation Task (自动病畜栏隔离任务)
        Given a quarantined piglet record in "agri.livestock.health" (畜牧健康监测模型) with an active fever alert state
        When the system registers the fever alert event
        Then the system must automatically create a high-priority veterinary task "project.task" (项目任务)
        And pre-populate the task description with the animal's RFID "rfid_tag_code" (无线射频识别耳标码) and assign it to the livestock technician for physical isolation in a dedicated pen
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a quarantined piglet record in "agri.livestock.health" (畜牧健康监测模型) with an active fever alert state',
            'When the system registers the fever alert event',
            'Then the system must automatically create a high-priority veterinary task "project.task" (项目任务)',
            'And pre-populate the task description with the animal\'s RFID "rfid_tag_code" (无线射频识别耳标码) and assign it to the livestock technician for physical isolation in a dedicated pen'
        ])

    def test_03_veterinary_medical_treatment_gxp_withdrawal_log_gxp(self):
        """
        Scenario: Veterinary Medical Treatment GxP Withdrawal Log (兽医治疗GxP休药期记录)
        Given a sick animal lot under treatment in "agri.livestock.health" (畜牧健康监测模型)
        When the veterinarian logs the administration of drug "Penicillin" (青霉素) with an active chemical ingredient
        Then the system must calculate the mandatory GxP chemical withdrawal duration of "14 days" (14天强制休药期)
        And write the exact withdrawal end date "withdrawal_end_date" (休药截止日期) to the underlying animal's stock lot "stock.lot" (库存批次) record
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a sick animal lot under treatment in "agri.livestock.health" (畜牧健康监测模型)',
            'When the veterinarian logs the administration of drug "Penicillin" (青霉素) with an active chemical ingredient',
            'Then the system must calculate the mandatory GxP chemical withdrawal duration of "14 days" (14天强制休药期)',
            'And write the exact withdrawal end date "withdrawal_end_date" (休药截止日期) to the underlying animal\'s stock lot "stock.lot" (库存批次) record'
        ])

    def test_04_eartag_rf_telemetry_gateway_offline_fallback(self):
        """
        Scenario: Ear-Tag RF Telemetry Gateway Offline Fallback (耳标无线遥测网关离线备用方案)
        Given swine pens equipped with active RFID health tracking gateways
        When the RF gateway connection is lost and registers no ear-tag updates for over "6 hours" (射频网关连接丢失超过6小时无数据更新)
        Then the system must transition the tracking state to "sensory_failed" (传感器失效) on "agri.livestock.health" (畜牧健康监测模型)
        And automatically generate an urgent checklist task "project.task" (项目任务) for a daily manual temperature and clinical heat check (每日手动温度与临床热度检查)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given swine pens equipped with active RFID health tracking gateways',
            'When the RF gateway connection is lost and registers no ear-tag updates for over "6 hours" (射频网关连接丢失超过6小时无数据更新)',
            'Then the system must transition the tracking state to "sensory_failed" (传感器失效) on "agri.livestock.health" (畜牧健康监测模型)',
            'And automatically generate an urgent checklist task "project.task" (项目任务) for a daily manual temperature and clinical heat check (每日手动温度与临床热度检查)'
        ])

    def test_05_veterinary_vaccine_phi_verification_lock_phi(self):
        """
        Scenario: Veterinary Vaccine PHI Verification Lock (兽医疫苗安全间隔期PHI验证锁)
        Given an animal stock lot "stock.lot" (库存批次) scheduled for processing on a manufacturing order "mrp.production" (制造订单)
        When the quality assurance system checks the lot against active vaccine Pre-Harvest Interval (宰前安全休药期) withdrawal end dates
        Then the system must raise a ValidationError (验证错误) message "Processing Blocked: Active Pre-Harvest Interval Withdrawal" (禁止加工：仍处于宰前安全休药期内) if the current date is before the "withdrawal_end_date" (休药截止日期)
        And block the state transition of the manufacturing order to "confirmed" (已确认)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an animal stock lot "stock.lot" (库存批次) scheduled for processing on a manufacturing order "mrp.production" (制造订单)',
            'When the quality assurance system checks the lot against active vaccine Pre-Harvest Interval (宰前安全休药期) withdrawal end dates',
            'Then the system must raise a ValidationError (验证错误) message "Processing Blocked: Active Pre-Harvest Interval Withdrawal" (禁止加工：仍处于宰前安全休药期内) if the current date is before the "withdrawal_end_date" (休药截止日期)',
            'And block the state transition of the manufacturing order to "confirmed" (已确认)'
        ])

    def test_06_autonomous_swine_sorting_gate_biosafety_lock(self):
        """
        Scenario: Autonomous Swine Sorting Gate Biosafety Lock (自主生猪分选闸生物安全锁)
        Given an automated pneumatic sorting gate device "iiot.device" (智能物联网设备) managed under "agri.livestock.health" (畜牧健康监测模型)
        When an animal lot "stock.lot" (库存批次) with status "quarantined" (已隔离) passes through the RFID reader
        Then the system must trigger an active PLC relay command to lock the normal pen gate and force the isolation gate to "open" (开启)
        And raise a ValidationError (验证错误) message "Sorting Prohibited: Quarantine animal redirected" (分选禁止：隔离期动物已重定向) if manual override is attempted without veterinarian credentials
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an automated pneumatic sorting gate device "iiot.device" (智能物联网设备) managed under "agri.livestock.health" (畜牧健康监测模型)',
            'When an animal lot "stock.lot" (库存批次) with status "quarantined" (已隔离) passes through the RFID reader',
            'Then the system must trigger an active PLC relay command to lock the normal pen gate and force the isolation gate to "open" (开启)',
            'And raise a ValidationError (验证错误) message "Sorting Prohibited: Quarantine animal redirected" (分选禁止：隔离期动物已重定向) if manual override is attempted without veterinarian credentials'
        ])

    def test_07_biological_asset_quarantine_solenoid_gate_interlock(self):
        """
        Scenario: Biological Asset Quarantine Solenoid Gate Interlock (生物资产疫病隔离区电磁阀强行锁定防护)
        Given a quarantined biological asset lot in "stock.matter.tracking" (物料跟踪模型) with status "quarantined" (隔离状态)
        And a quarantine geofence is defined with GPS coordinates "gps_lat" and "gps_lng" (并且使用地理坐标定义了防疫边界围栏)
        When a technician attempts to trigger open lock "open_gate" (当技术员尝试执行触发开启隔离栏物理阀门系统动作时)
        Then the IoT gateway must activate autoclave lock set "is_solenoid_locked" to true on physical solenoid (物联网网关必须强制激活物理电磁锁状态字段值为真)
        And raise a UserError (并且拦截开启操作并抛出用户错误) with message "SOLENOID_LOCKED_BIOSECURITY" (包含"电磁锁已强制闭锁，隔离区处于高危生物安全防护状态"提示信息)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a quarantined biological asset lot in "stock.matter.tracking" (物料跟踪模型) with status "quarantined" (隔离状态)',
            'And a quarantine geofence is defined with GPS coordinates "gps_lat" and "gps_lng" (并且使用地理坐标定义了防疫边界围栏)',
            'When a technician attempts to trigger open lock "open_gate" (当技术员尝试执行触发开启隔离栏物理阀门系统动作时)',
            'Then the IoT gateway must activate autoclave lock set "is_solenoid_locked" to true on physical solenoid (物联网网关必须强制激活物理电磁锁状态字段值为真)',
            'And raise a UserError (并且拦截开启操作并抛出用户错误) with message "SOLENOID_LOCKED_BIOSECURITY" (包含"电磁锁已强制闭锁，隔离区处于高危生物安全防护状态"提示信息)'
        ])
