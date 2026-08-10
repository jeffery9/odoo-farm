# -*- coding: utf-8 -*-
from odoo.addons.farm_core.tests.bdd_base import BddTransactionCase
from odoo.exceptions import UserError, ValidationError

class TestEpic038(BddTransactionCase):
    """ BDD Test Suite for Epic 038: Epic 038 Agri-Quality Inspection """

    def setUp(self):
        super(TestEpic038, self).setUp()

    def test_01_multistage_laboratory_sampling_and_sequential_quality_gate_releases(self):
        """
        Scenario: Multi-stage laboratory sampling and sequential quality gate releases
        Given a processed honey batch lot "HON-QC-2026-90" awaiting quality approval
        And the quality inspection rules require passing tests at "Intake", "In-Process", and "Finished" stages
        When I submit passing chemical reports for "Intake" and "In-Process" stages in "agri.qc.sample"
        But the "Finished" stage microbiological assay is still pending
        Then the system must hold the lot's overall release status in "Awaiting Quality Release" (待检中 / Awaiting Quality Release)
        And raise a validation lock preventing inventory delivery orders or stock transfers from confirming
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a processed honey batch lot "HON-QC-2026-90" awaiting quality approval',
            'And the quality inspection rules require passing tests at "Intake", "In-Process", and "Finished" stages',
            'When I submit passing chemical reports for "Intake" and "In-Process" stages in "agri.qc.sample"',
            'But the "Finished" stage microbiological assay is still pending',
            'Then the system must hold the lot\'s overall release status in "Awaiting Quality Release" (待检中 / Awaiting Quality Release)',
            'And raise a validation lock preventing inventory delivery orders or stock transfers from confirming'
        ])

    def test_02_sensory_panel_taste_scores_verification_blocking_premium_classification(self):
        """
        Scenario: Sensory panel taste scores verification blocking premium classification
        Given a premium winery batch lot "CAB-RES-2026-X1" undergoing evaluation
        And the sensory panel taste test scores average 81.5 points on the 100-point OIV scale
        When I record the sensory panel results in "agri.qc.sample"
        Then the system must block the lot from receiving the premium "Reserve Speciale" classification label (since average is < 85.0)
        And downgrade the target labeling category to standard "Vieux Rouge"
        And write a downgrade notification in the Odoo chatter
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a premium winery batch lot "CAB-RES-2026-X1" undergoing evaluation',
            'And the sensory panel taste test scores average 81.5 points on the 100-point OIV scale',
            'When I record the sensory panel results in "agri.qc.sample"',
            'Then the system must block the lot from receiving the premium "Reserve Speciale" classification label (since average is < 85.0)',
            'And downgrade the target labeling category to standard "Vieux Rouge"',
            'And write a downgrade notification in the Odoo chatter'
        ])

    def test_03_nonconforming_microbiological_lot_quarantine_hold_and_hard_lock(self):
        """
        Scenario: Non-conforming microbiological lot quarantine hold and hard lock
        Given a completed processed milk quality inspection record
        And the laboratory reports detect Listeria pathogen concentration as "Positive" (阳性)
        When the inspector saves this failed laboratory result in "agri.qc.sample"
        Then the system must atomically set the associated lot "MILK-RAW-2026-88" quality state to "Quarantined"
        And block all sales orders, stock picking moves, and delivery invoices for this lot
        And trigger a critical alarm "Exception Disposal" activity for the Quality Director
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a completed processed milk quality inspection record',
            'And the laboratory reports detect Listeria pathogen concentration as "Positive" (阳性)',
            'When the inspector saves this failed laboratory result in "agri.qc.sample"',
            'Then the system must atomically set the associated lot "MILK-RAW-2026-88" quality state to "Quarantined"',
            'And block all sales orders, stock picking moves, and delivery invoices for this lot',
            'And trigger a critical alarm "Exception Disposal" activity for the Quality Director'
        ])

    def test_04_approved_lot_final_quality_release_requiring_retained_control_sample_registration(self):
        """
        Scenario: Approved lot final quality release requiring retained control sample registration
        Given a premium wheat seed lot "WHEAT-SEED-99" undergoing final quality verification
        And all chemical, purity, and germination rate inspections are passed
        When the Quality Manager attempts to approve the "Quality Release"
        Then the system must force the operator to register a physically retained control sample lot location
        And validate that the retention quantity is at least 500.0 g and retention expiry date is set to "2027-08-09"
        And block final verification approval if the retained sample register is incomplete
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a premium wheat seed lot "WHEAT-SEED-99" undergoing final quality verification',
            'And all chemical, purity, and germination rate inspections are passed',
            'When the Quality Manager attempts to approve the "Quality Release"',
            'Then the system must force the operator to register a physically retained control sample lot location',
            'And validate that the retention quantity is at least 500.0 g and retention expiry date is set to "2027-08-09"',
            'And block final verification approval if the retained sample register is incomplete'
        ])

    def test_05_expired_laboratory_analytical_equipment_calibration_blocking_sample_entry(self):
        """
        Scenario: Expired laboratory analytical equipment calibration blocking sample entry
        Given a laboratory Gas Chromatograph (GC-MS) equipment "LAB-GC-01" registered under "maintenance.equipment"
        And the equipment's scheduled calibration expiration date was "2026-08-01" which is in the past
        When a laboratory technician attempts to log the linalool purity ratio using equipment "LAB-GC-01"
        Then the system must raise a ValidationError with message "EQUIPMENT_CALIBRATION_EXPIRED" (分析仪器校准超期，测试失效，严禁录入结果)
        And prevent the quality check record from being marked as "Passed"
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a laboratory Gas Chromatograph (GC-MS) equipment "LAB-GC-01" registered under "maintenance.equipment"',
            'And the equipment\'s scheduled calibration expiration date was "2026-08-01" which is in the past',
            'When a laboratory technician attempts to log the linalool purity ratio using equipment "LAB-GC-01"',
            'Then the system must raise a ValidationError with message "EQUIPMENT_CALIBRATION_EXPIRED" (分析仪器校准超期，测试失效，严禁录入结果)',
            'And prevent the quality check record from being marked as "Passed"'
        ])

    def test_06_automated_physical_autoclave_door_lock_actuator_control_based_on_thermocouple_sensor_stabilization(self):
        """
        Scenario: Automated physical autoclave door lock actuator control based on thermocouple sensor stabilization
        Given a laboratory sterilization autoclave "LAB-AUTO-03" with an active thermocouple telemetry sensor
        And the autoclave door physical actuator lock state is "Locked" (锁定 / Locked)
        When the thermocouple temperature logs drop below 80.0 °C and chamber pressure falls below 0.1 Bar
        Then the system must trigger the physical door lock actuator to "Unlocked" (解锁 / Unlocked)
        And log the GxP decompression safety validation event on the workorder chatter
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a laboratory sterilization autoclave "LAB-AUTO-03" with an active thermocouple telemetry sensor',
            'And the autoclave door physical actuator lock state is "Locked" (锁定 / Locked)',
            'When the thermocouple temperature logs drop below 80.0 °C and chamber pressure falls below 0.1 Bar',
            'Then the system must trigger the physical door lock actuator to "Unlocked" (解锁 / Unlocked)',
            'And log the GxP decompression safety validation event on the workorder chatter'
        ])

    def test_07_quality_lab_autoclave_temperature_sensor_disconnect_and_secondary_mechanical_safety_lock_trigger(self):
        """
        Scenario: Quality Lab Autoclave Temperature Sensor Disconnect and Secondary Mechanical Safety Lock Trigger
        Given a laboratory sterilization autoclave registered in "maintenance.equipment" (设备保养)
        And the autoclave door physical lock status is "Locked" (锁定 / Locked)
        When the core thermocouple telemetry sensor fails and returns null values during the active sterilization run
        Then the system must immediately switch the backup mechanical pressure safety valve to "Active" (启用)
        And raise a "ValidationError" (验证错误) blocking the laboratory technician from saving any sample test records for this sterilization batch
        And transition the sterilization mission "mrp.workorder" [mrp.workorder] (作业任务) status to "SENSORY_FAILED" (传感器异常)
        And log a critical autoclave safety breach in the equipment's chatter
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a laboratory sterilization autoclave registered in "maintenance.equipment" (设备保养)',
            'And the autoclave door physical lock status is "Locked" (锁定 / Locked)',
            'When the core thermocouple telemetry sensor fails and returns null values during the active sterilization run',
            'Then the system must immediately switch the backup mechanical pressure safety valve to "Active" (启用)',
            'And raise a "ValidationError" (验证错误) blocking the laboratory technician from saving any sample test records for this sterilization batch',
            'And transition the sterilization mission "mrp.workorder" [mrp.workorder] (作业任务) status to "SENSORY_FAILED" (传感器异常)',
            "And log a critical autoclave safety breach in the equipment's chatter"
        ])
