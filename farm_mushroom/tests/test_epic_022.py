# -*- coding: utf-8 -*-
from odoo.addons.farm_core.tests.bdd_base import BddTransactionCase
from odoo.exceptions import UserError, ValidationError

class TestEpic022(BddTransactionCase):
    """ BDD Test Suite for Epic 022: Epic 022 Mushroom Management """

    def setUp(self):
        super(TestEpic022, self).setUp()

    def test_01_climatecontrolled_room_telemetry_tracking(self):
        """
        Scenario: Climate-Controlled Room Telemetry Tracking
        Given a mushroom growing room monitored via active IoT telemetry in "agri.isl.lot.mushroom"
        And the current mushroom cultivation batch is in its fruiting stage
        When the CO2 level sensor registers a reading exceeding 1200 PPM
        Then the system must trigger the automated exhaust fan ventilation actuator
        And the system must log the corrective action event in the environmental history log
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a mushroom growing room monitored via active IoT telemetry in "agri.isl.lot.mushroom"',
            'And the current mushroom cultivation batch is in its fruiting stage',
            'When the CO2 level sensor registers a reading exceeding 1200 PPM',
            'Then the system must trigger the automated exhaust fan ventilation actuator',
            'And the system must log the corrective action event in the environmental history log'
        ])

    def test_02_mushroom_heavy_metal_gating(self):
        """
        Scenario: Mushroom Heavy Metal Gating
        Given a harvested mushroom lot registered in "stock.lot"
        And a laboratory technician performing heavy metal analysis on the lot
        When the heavy metal laboratory analysis registers a cadmium concentration greater than 0.1 mg/kg
        Then the system must automatically quarantine the corresponding mushroom lot
        And the lot's quality state must transition to "Unfit for Consumption"
        And the system must block the lot from any packaging or inventory delivery moves
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a harvested mushroom lot registered in "stock.lot"',
            'And a laboratory technician performing heavy metal analysis on the lot',
            'When the heavy metal laboratory analysis registers a cadmium concentration greater than 0.1 mg/kg',
            'Then the system must automatically quarantine the corresponding mushroom lot',
            'And the lot\'s quality state must transition to "Unfit for Consumption"',
            'And the system must block the lot from any packaging or inventory delivery moves'
        ])

    def test_03_co2_sensor_failsafe_mode(self):
        """
        Scenario: CO2 Sensor Fail-Safe Mode
        Given an active mushroom cultivation batch tracked via "mrp.production"
        And the environmental controller monitoring the fruiting room
        When the room CO2 telemetry sensor goes offline and returns null values
        Then the system must automatically switch the exhaust ventilation actuator to fail-safe mode
        And the system must trigger a default duty-cycle of 15 minutes per hour for the exhaust fan
        And the system must generate a high-priority maintenance alert in the dashboard
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an active mushroom cultivation batch tracked via "mrp.production"',
            'And the environmental controller monitoring the fruiting room',
            'When the room CO2 telemetry sensor goes offline and returns null values',
            'Then the system must automatically switch the exhaust ventilation actuator to fail-safe mode',
            'And the system must trigger a default duty-cycle of 15 minutes per hour for the exhaust fan',
            'And the system must generate a high-priority maintenance alert in the dashboard'
        ])

    def test_04_multiflush_harvest_yield_decay(self):
        """
        Scenario: Multi-Flush Harvest Yield Decay
        Given a mushroom spawn log tracking multiple flush cycles
        And the expected harvest yield model initialized for the cultivation batch
        When the current harvest campaign is recorded and marked as Flush 3
        Then the expected yield estimation model must automatically apply a 40% yield decay reduction penalty
        And the system must update the target yield metric for the active "mrp.production" order
        And the system must log the flush performance deviation in the harvest history
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a mushroom spawn log tracking multiple flush cycles',
            'And the expected harvest yield model initialized for the cultivation batch',
            'When the current harvest campaign is recorded and marked as Flush 3',
            'Then the expected yield estimation model must automatically apply a 40% yield decay reduction penalty',
            'And the system must update the target yield metric for the active "mrp.production" order',
            'And the system must log the flush performance deviation in the harvest history'
        ])

    def test_05_mushroom_substrate_gxp_sterilization_validation(self):
        """
        Scenario: Mushroom Substrate GxP Sterilization Validation
        Given a compost substrate sterilization workorder in "mrp.workorder"
        And temperature sensors monitoring the core temperature of the compost autoclave
        When the core sterilization temperature stays below 121°C for the scheduled 30-minute sterilization block
        Then the system must transition the workorder state to "Sterilization Failed"
        And the system must lock subsequent inoculation operations associated with this compost batch
        And the system must raise a "ValidationError" if an operator attempts to bypass this safety gate
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a compost substrate sterilization workorder in "mrp.workorder"',
            'And temperature sensors monitoring the core temperature of the compost autoclave',
            'When the core sterilization temperature stays below 121°C for the scheduled 30-minute sterilization block',
            'Then the system must transition the workorder state to "Sterilization Failed"',
            'And the system must lock subsequent inoculation operations associated with this compost batch',
            'And the system must raise a "ValidationError" if an operator attempts to bypass this safety gate'
        ])

    def test_06_substrate_autoclave_seal_failure_gxp_emergency_depressurization_and_inoculation_lock(self):
        """
        Scenario: Substrate Autoclave Seal Failure GxP Emergency Depressurization and Inoculation Lock
        Given a compost substrate sterilization order in "mrp.production" (制造订单) using a designated autoclave workcenter
        And the sterilization mission "mrp.workorder" [mrp.workorder] (作业任务) status is "In Progress" (进行中)
        When the autoclave pressure sensor registers an abrupt pressure loss below 1.0 Bar during the active sterilization cycle
        Then the system must trigger an automated steam supply shutoff command to the physical actuator "agri.iot.switch" (物联网开关)
        And flag the compost substrate lot in "stock.lot" (库存批次) with status "Contaminated" (已污染)
        And raise a "ValidationError" (验证错误) to prevent any subsequent inoculation "stock.move" (库存移动) using this lot
        And log a GxP containment audit trail entry in Odoo chatter
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a compost substrate sterilization order in "mrp.production" (制造订单) using a designated autoclave workcenter',
            'And the sterilization mission "mrp.workorder" [mrp.workorder] (作业任务) status is "In Progress" (进行中)',
            'When the autoclave pressure sensor registers an abrupt pressure loss below 1.0 Bar during the active sterilization cycle',
            'Then the system must trigger an automated steam supply shutoff command to the physical actuator "agri.iot.switch" (物联网开关)',
            'And flag the compost substrate lot in "stock.lot" (库存批次) with status "Contaminated" (已污染)',
            'And raise a "ValidationError" (验证错误) to prevent any subsequent inoculation "stock.move" (库存移动) using this lot',
            'And log a GxP containment audit trail entry in Odoo chatter'
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
