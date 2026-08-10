# -*- coding: utf-8 -*-
from odoo.addons.farm_core.tests.bdd_base import BddTransactionCase
from odoo.exceptions import UserError, ValidationError

class TestEpic094(BddTransactionCase):
    """ BDD Test Suite for Epic 094: Epic 094 Smart Livestock Management """

    def setUp(self):
        super(TestEpic094, self).setUp()

    def test_01_swine_thermal_eartag_fever_quarantine_gate(self):
        """
        Scenario: Swine Thermal Ear-Tag Fever Quarantine Gate
        Given pasture swine lots monitored under "agri.livestock.smart" (智能畜牧管理) with a specific lot "stock.lot" (库存批次) "SWI-LOT-01" in status "healthy" (健康)
        When active RFID thermal ear-tag telemetry logs body temperature (体温) greater than 40.5°C with a reading of 41.2°C
        Then the system automatically sets field "active_fever" (活跃发热) to true
        And transitions livestock health state to "quarantined" (已隔离) and blocks outbound transfer pickings "stock.picking" (库存拣货) with validation error message "Fever Quarantine Lock" (高烧隔离锁定)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given pasture swine lots monitored under "agri.livestock.smart" (智能畜牧管理) with a specific lot "stock.lot" (库存批次) "SWI-LOT-01" in status "healthy" (健康)',
            'When active RFID thermal ear-tag telemetry logs body temperature (体温) greater than 40.5°C with a reading of 41.2°C',
            'Then the system automatically sets field "active_fever" (活跃发热) to true',
            'And transitions livestock health state to "quarantined" (已隔离) and blocks outbound transfer pickings "stock.picking" (库存拣货) with validation error message "Fever Quarantine Lock" (高烧隔离锁定)'
        ])

    def test_02_automated_sick_animal_veterinary_isolation_task(self):
        """
        Scenario: Automated Sick Animal Veterinary Isolation Task
        Given an animal lot "stock.lot" (库存批次) "SWI-LOT-01" with active fever "active_fever" (活跃发热) registered as true under "agri.livestock.smart" (智能畜牧管理)
        When the fever quarantine is registered by the system
        Then the system creates a high-priority veterinary check-up task (兽医检查任务) on the dashboard under "mrp.workorder" (生产工单) "WO-VET-101"
        And sets workorder description to "Isolate and Inspect Fever Swine SWI-LOT-01" (隔离并检查发烧生猪) and changes status to "ready" (准备就绪)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an animal lot "stock.lot" (库存批次) "SWI-LOT-01" with active fever "active_fever" (活跃发热) registered as true under "agri.livestock.smart" (智能畜牧管理)',
            'When the fever quarantine is registered by the system',
            'Then the system creates a high-priority veterinary check-up task (兽医检查任务) on the dashboard under "mrp.workorder" (生产工单) "WO-VET-101"',
            'And sets workorder description to "Isolate and Inspect Fever Swine SWI-LOT-01" (隔离并检查发烧生猪) and changes status to "ready" (准备就绪)'
        ])

    def test_03_veterinary_penicillin_medical_treatment_withdrawal_logs(self):
        """
        Scenario: Veterinary Penicillin Medical Treatment Withdrawal Logs
        Given a sick quarantined animal lot "stock.lot" (库存批次) "SWI-LOT-02" under "agri.livestock.smart" (智能畜牧管理) in status "quarantined" (已隔离)
        When the veterinarian logs drug treatment "Penicillin" (青霉素注射治疗) with system action "log_treatment" (记录药物治疗)
        Then the system computes antibiotic withdrawal duration of 14 days and writes the withdrawal end date field "withdrawal_end_date" (停药期截止日期) to the lot
        And flags compliance state "esg_compliance" (符合性状态) as "restricted" (受限) until the withdrawal end date is reached
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a sick quarantined animal lot "stock.lot" (库存批次) "SWI-LOT-02" under "agri.livestock.smart" (智能畜牧管理) in status "quarantined" (已隔离)',
            'When the veterinarian logs drug treatment "Penicillin" (青霉素注射治疗) with system action "log_treatment" (记录药物治疗)',
            'Then the system computes antibiotic withdrawal duration of 14 days and writes the withdrawal end date field "withdrawal_end_date" (停药期截止日期) to the lot',
            'And flags compliance state "esg_compliance" (符合性状态) as "restricted" (受限) until the withdrawal end date is reached'
        ])

    def test_04_swine_eartag_telemetry_gateway_connection_timeout_fallback(self):
        """
        Scenario: Swine Ear-Tag Telemetry Gateway Connection Timeout Fallback
        Given pasture pens monitored by RFID gateway receivers under "agri.livestock.smart" (智能畜牧管理)
        When gateway connection fails to report for 6 hours (null ear-tag updates)
        Then the system triggers telemetry fallback action "trigger_gateway_fallback" (触发网关容灾)
        And transitions tracking status field "state" (状态) to "sensory_failed" (传感器异常) and adds manual heat-check checklists to the herdsman's mobile dashboard
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given pasture pens monitored by RFID gateway receivers under "agri.livestock.smart" (智能畜牧管理)',
            'When gateway connection fails to report for 6 hours (null ear-tag updates)',
            'Then the system triggers telemetry fallback action "trigger_gateway_fallback" (触发网关容灾)',
            'And transitions tracking status field "state" (状态) to "sensory_failed" (传感器异常) and adds manual heat-check checklists to the herdsman's mobile dashboard'
        ])

    def test_05_veterinary_vaccine_phi_verification_lock(self):
        """
        Scenario: Veterinary Vaccine PHI Verification Lock
        Given a processed meat animal lot "stock.lot" (库存批次) "SWI-LOT-03" scheduled for delivery under picking "stock.picking" (库存拣货) "OUT-SWI-101"
        When validating the stock picking and checking active vaccine withdrawal periods (疫苗停药期/休药期)
        Then the system blocks stock move validation "action_assign" (保留库存) if the animal's withdrawal period is active
        And raises validation error message "Active Vaccine PHI Withdrawal Lockout" (活性疫苗休药期未届满锁定)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a processed meat animal lot "stock.lot" (库存批次) "SWI-LOT-03" scheduled for delivery under picking "stock.picking" (库存拣货) "OUT-SWI-101"',
            'When validating the stock picking and checking active vaccine withdrawal periods (疫苗停药期/休药期)',
            'Then the system blocks stock move validation "action_assign" (保留库存) if the animal's withdrawal period is active',
            'And raises validation error message "Active Vaccine PHI Withdrawal Lockout" (活性疫苗休药期未届满锁定)'
        ])

    def test_06_rfid_quarantine_receiver_tampering_cybersecurity_encryption_lock(self):
        """
        Scenario: RFID Quarantine Receiver Tampering Cybersecurity Encryption Lock
        Given swine lots "stock.lot" (库存批次) "SWI-LOT-06" in state "quarantined" (已隔离) under "agri.livestock.smart" (智能畜牧管理)
        When the RFID quarantine gateway receiver detects an unauthorized access or brute-force packet signature
        Then the system executes a cybersecurity encryption lock (网络安全加密锁定) to freeze the physical quarantine sorting gates
        And raises a validation error (验证错误: "Quarantine gateway tampered, physical gates locked") to prevent swine escaping
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given swine lots "stock.lot" (库存批次) "SWI-LOT-06" in state "quarantined" (已隔离) under "agri.livestock.smart" (智能畜牧管理)',
            'When the RFID quarantine gateway receiver detects an unauthorized access or brute-force packet signature',
            'Then the system executes a cybersecurity encryption lock (网络安全加密锁定) to freeze the physical quarantine sorting gates',
            'And raises a validation error (验证错误: "Quarantine gateway tampered, physical gates locked") to prevent swine escaping'
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
