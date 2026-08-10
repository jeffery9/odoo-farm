# -*- coding: utf-8 -*-
from odoo.addons.farm_core.tests.bdd_base import BddTransactionCase
from odoo.exceptions import UserError, ValidationError

class TestEpic024(BddTransactionCase):
    """ BDD Test Suite for Epic 024: Epic 024 Net Vegetables Management """

    def setUp(self):
        super(TestEpic024, self).setUp()

    def test_01_sanitizer_washwater_chlorine_residual_gating(self):
        """
        Scenario: Sanitizer Wash-Water Chlorine Residual Gating
        Given an active vegetable wash-line workorder registered in "mrp.workorder"
        And water quality telemetry sensors monitoring the sanitizer wash tank
        When the chlorine sensor logs a reading below 100.0 PPM or above 200.0 PPM
        Then the system must automatically flag the active wash batch with a "Chemical Deviation" status
        And the system must pause all subsequent downstream packaging movements for this batch
        And the system must alert the workshop supervisor in the dashboard
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an active vegetable wash-line workorder registered in "mrp.workorder"',
            'And water quality telemetry sensors monitoring the sanitizer wash tank',
            'When the chlorine sensor logs a reading below 100.0 PPM or above 200.0 PPM',
            'Then the system must automatically flag the active wash batch with a "Chemical Deviation" status',
            'And the system must pause all subsequent downstream packaging movements for this batch',
            'And the system must alert the workshop supervisor in the dashboard'
        ])

    def test_02_microbial_salmonella_laboratory_gating(self):
        """
        Scenario: Microbial Salmonella Laboratory Gating
        Given a net vegetable lot awaiting commercial packaging in "agri.isl.net.veg"
        And the laboratory performing microbiological testing on the lot
        When the laboratory records the Salmonella test result as "Positive"
        Then the system must hard-lock the net vegetable lot from all picking delivery orders
        And the lot's global quality state must immediately transition to "Contaminated"
        And the system must display a high-visibility red warning banner in the Odoo lot view
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a net vegetable lot awaiting commercial packaging in "agri.isl.net.veg"',
            'And the laboratory performing microbiological testing on the lot',
            'When the laboratory records the Salmonella test result as "Positive"',
            'Then the system must hard-lock the net vegetable lot from all picking delivery orders',
            'And the lot\'s global quality state must immediately transition to "Contaminated"',
            'And the system must display a high-visibility red warning banner in the Odoo lot view'
        ])

    def test_03_washwater_chlorine_sensor_offline_fallback(self):
        """
        Scenario: Wash-Water Chlorine Sensor Offline Fallback
        Given a running vegetable washing workorder in "mrp.workorder"
        And active telemetry streaming chlorine concentration values
        When the chlorine telemetry sensor connection fails and stops reporting data
        Then the system must switch to the manual titration verification process
        And the system must force operators to log manual titration checks every 30 minutes
        And the system must block subsequent packaging validations if any manual checks are missed
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a running vegetable washing workorder in "mrp.workorder"',
            'And active telemetry streaming chlorine concentration values',
            'When the chlorine telemetry sensor connection fails and stops reporting data',
            'Then the system must switch to the manual titration verification process',
            'And the system must force operators to log manual titration checks every 30 minutes',
            'And the system must block subsequent packaging validations if any manual checks are missed'
        ])

    def test_04_realtime_dynamic_packing_line_yield_loss(self):
        """
        Scenario: Real-time Dynamic Packing Line Yield Loss
        Given a packaging run of fresh spinach inputting 500.0 kg of raw material
        And the packaging production order active in "mrp.production"
        When the finished packaged output is recorded and totals exactly 420.0 kg
        Then the system must calculate a scrap loss percentage of exactly 16.0%
        And the system must generate an automated yield alert since the scrap loss exceeds the 12.0% target limit
        And the system must log the scrap analysis under "agri.processing.yield"
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a packaging run of fresh spinach inputting 500.0 kg of raw material',
            'And the packaging production order active in "mrp.production"',
            'When the finished packaged output is recorded and totals exactly 420.0 kg',
            'Then the system must calculate a scrap loss percentage of exactly 16.0%',
            'And the system must generate an automated yield alert since the scrap loss exceeds the 12.0% target limit',
            'And the system must log the scrap analysis under "agri.processing.yield"'
        ])

    def test_05_coldroom_packing_geofence_gate(self):
        """
        Scenario: Cold-Room Packing Geofence Gate
        Given packaged salad lots which are required to reside in cold storage below 4.0°C
        And RFID or barcode geofence sensors active in the packaging facility
        When the geofence sensor detects that a lot is placed in packing zones above 15.0°C for longer than 30 minutes
        Then the system must automatically raise a biosecurity cold-chain warning in Odoo
        And the system must flag the affected salad lots for mandatory quality re-sampling
        And the system must block any stock transfer of these lots until cleared by quality control
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given packaged salad lots which are required to reside in cold storage below 4.0°C',
            'And RFID or barcode geofence sensors active in the packaging facility',
            'When the geofence sensor detects that a lot is placed in packing zones above 15.0°C for longer than 30 minutes',
            'Then the system must automatically raise a biosecurity cold-chain warning in Odoo',
            'And the system must flag the affected salad lots for mandatory quality re-sampling',
            'And the system must block any stock transfer of these lots until cleared by quality control'
        ])

    def test_06_salad_centrifugal_spin_dryer_motor_imbalance_detection_and_autovibration_braking(self):
        """
        Scenario: Salad Centrifugal Spin Dryer Motor Imbalance Detection and Auto-Vibration Braking
        Given a vegetable drying order in "mrp.production" (制造订单)
        And a spin-dryer workstation with active vibration telemetry monitoring
        When the spin-dryer sensor logs a motor imbalance reading exceeding 5.0 G-force
        Then the system must atomically trigger the emergency electromagnetic brake actuator to "Halt" (紧急制动)
        And set the drying mission "mrp.workorder" [mrp.workorder] (作业任务) status to "Failed" (已失效)
        And quarantine the affected net vegetable lot in "stock.lot" (库存批次) with status "Damaged" (已损坏) to prevent packaging
        And raise a "ValidationError" (验证错误) blocking any "stock.move" (库存移动) for this damaged lot
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a vegetable drying order in "mrp.production" (制造订单)',
            'And a spin-dryer workstation with active vibration telemetry monitoring',
            'When the spin-dryer sensor logs a motor imbalance reading exceeding 5.0 G-force',
            'Then the system must atomically trigger the emergency electromagnetic brake actuator to "Halt" (紧急制动)',
            'And set the drying mission "mrp.workorder" [mrp.workorder] (作业任务) status to "Failed" (已失效)',
            'And quarantine the affected net vegetable lot in "stock.lot" (库存批次) with status "Damaged" (已损坏) to prevent packaging',
            'And raise a "ValidationError" (验证错误) blocking any "stock.move" (库存移动) for this damaged lot'
        ])

    def test_07_recipe_highmixing_entropy_quality_penalty_gating(self):
        """
        Scenario: Recipe High-Mixing Entropy Quality Penalty Gating (配方物料高混合熵防错拦截门禁机制)
        Given a multi-input biological compound formulation using "mrp.bom" (物料清单模型)
        And a processing batch in "mrp.production" (生产订单模型)
        When the operator attempts to confirm recipe "action_confirm" with a calculated mixing entropy score "mixing_entropy" above 0.85 (当操作员尝试执行确认配方系统动作且计算出的混合熵得分字段值超过0.85阈值时)
        Then the quality engine must apply a 10.0% mixing entropy score penalty on "mixing_entropy_penalty" (系统必须自动在该批次中应用10.0%的混合熵惩罚比例字段值)
        And raise a ValidationError (并且抛出验证错误) with message "MIXING_ENTROPY_LIMIT_EXCEEDED" (包含"混合熵超限，批次质量评级降级"提示信息)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a multi-input biological compound formulation using "mrp.bom" (物料清单模型)',
            'And a processing batch in "mrp.production" (生产订单模型)',
            'When the operator attempts to confirm recipe "action_confirm" with a calculated mixing entropy score "mixing_entropy" above 0.85 (当操作员尝试执行确认配方系统动作且计算出的混合熵得分字段值超过0.85阈值时)',
            'Then the quality engine must apply a 10.0% mixing entropy score penalty on "mixing_entropy_penalty" (系统必须自动在该批次中应用10.0%的混合熵惩罚比例字段值)',
            'And raise a ValidationError (并且抛出验证错误) with message "MIXING_ENTROPY_LIMIT_EXCEEDED" (包含"混合熵超限，批次质量评级降级"提示信息)'
        ])
