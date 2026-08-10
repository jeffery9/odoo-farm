# -*- coding: utf-8 -*-
from odoo.addons.farm_core.tests.bdd_base import BddTransactionCase
from odoo.exceptions import UserError, ValidationError

class TestEpic031(BddTransactionCase):
    """ BDD Test Suite for Epic 031: Epic 031 Epidemic Prevention & Biosafety """

    def setUp(self):
        super(TestEpic031, self).setUp()

    def test_01_active_infection_quarantine_zone_locks_on_inventory_moves(self):
        """
        Scenario: Active infection quarantine zone locks on inventory moves
        Given a farm parcel location under "agri.epidemic.zone" is marked with quarantine_state "quarantined"
        When an operator attempts to confirm a stock picking "stock.picking" to route materials into or out of this quarantined location
        Then the system must block the picking confirmation command
        And raise a strict "UserError" containing "QUARANTINE_LOCKED"
        And log a warning entry in the location's chatter
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a farm parcel location under "agri.epidemic.zone" is marked with quarantine_state "quarantined"',
            'When an operator attempts to confirm a stock picking "stock.picking" to route materials into or out of this quarantined location',
            'Then the system must block the picking confirmation command',
            'And raise a strict "UserError" containing "QUARANTINE_LOCKED"',
            'And log a warning entry in the location's chatter'
        ])

    def test_02_spray_drift_wind_speed_gating_for_chemical_treatments(self):
        """
        Scenario: Spray drift wind speed gating for chemical treatments
        Given a planned crop spraying workorder "mrp.workorder" on a parcel location
        When weather station telemetry sensors log a wind speed greater than "4.0" m/s
        Then the system must block the operator from starting the spraying workorder
        And flag the workorder state as "locked" with the reason "EXCESSIVE_WIND_DRIFT_RISK"
        And broadcast an alert notification to the farm manager
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a planned crop spraying workorder "mrp.workorder" on a parcel location',
            'When weather station telemetry sensors log a wind speed greater than "4.0" m/s',
            'Then the system must block the operator from starting the spraying workorder',
            'And flag the workorder state as "locked" with the reason "EXCESSIVE_WIND_DRIFT_RISK"',
            'And broadcast an alert notification to the farm manager'
        ])

    def test_03_quarantine_boundary_gps_geofence_tracking_and_veterinary_alert(self):
        """
        Scenario: Quarantine boundary GPS geofence tracking and veterinary alert
        Given a quarantined livestock lot "stock.lot" linked to a spatial boundary "agri.epidemic.zone"
        When real-time GPS telemetry logs of the livestock lot report coordinates deviating outside the geofenced zone boundary
        Then the system must immediately change the lot biosafety status to "CONTAINMENT_BREACH"
        And generate a high-priority emergency veterinary containment task "mrp.workorder"
        And dispatch SMS alert notifications to all on-duty security and containment personnel
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a quarantined livestock lot "stock.lot" linked to a spatial boundary "agri.epidemic.zone"',
            'When real-time GPS telemetry logs of the livestock lot report coordinates deviating outside the geofenced zone boundary',
            'Then the system must immediately change the lot biosafety status to "CONTAINMENT_BREACH"',
            'And generate a high-priority emergency veterinary containment task "mrp.workorder"',
            'And dispatch SMS alert notifications to all on-duty security and containment personnel'
        ])

    def test_04_veterinary_vaccine_preharvest_interval_phi_slaughter_blocker(self):
        """
        Scenario: Veterinary vaccine Pre-Harvest Interval (PHI) slaughter blocker
        Given a treated animal lot "stock.lot" with active veterinary vaccine or chemical drug injection logs
        And the drug has an active withdrawal interval that has not cleared yet
        When a processing workorder "mrp.production" attempts to schedule or confirm slaughtering for this lot
        Then the "AgriQualityGateMixin" must block the operation
        And raise a "ValidationError" indicating "BIOSECURITY_PHI_VIOLATION" with the calculated remaining withdrawal hours
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a treated animal lot "stock.lot" with active veterinary vaccine or chemical drug injection logs',
            'And the drug has an active withdrawal interval that has not cleared yet',
            'When a processing workorder "mrp.production" attempts to schedule or confirm slaughtering for this lot',
            'Then the "AgriQualityGateMixin" must block the operation',
            'And raise a "ValidationError" indicating "BIOSECURITY_PHI_VIOLATION" with the calculated remaining withdrawal hours'
        ])

    def test_05_disinfection_spray_vehicle_gate_sensor_interlock(self):
        """
        Scenario: Disinfection spray vehicle gate sensor interlock
        Given a high-security livestock barn gate monitored by physical security entry sensors
        When a feed delivery or transport vehicle attempts to check-in at the entry point
        And the disinfection spray pressure sensor validation is missing or logs a pressure below "2.5" Bar (disinfection failure)
        Then the system must lock the physical barn gate actuator, blocking vehicle entry
        And transition the entry activity state to "DISINFECTION_FAILED_BLOCKED"
        And capture and link a photo of the vehicle to the log
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a high-security livestock barn gate monitored by physical security entry sensors',
            'When a feed delivery or transport vehicle attempts to check-in at the entry point',
            'And the disinfection spray pressure sensor validation is missing or logs a pressure below "2.5" Bar (disinfection failure)',
            'Then the system must lock the physical barn gate actuator, blocking vehicle entry',
            'And transition the entry activity state to "DISINFECTION_FAILED_BLOCKED"',
            'And capture and link a photo of the vehicle to the log'
        ])

    def test_06_vehicle_disinfection_water_pump_pressure_loss_emergency_gate_lockout(self):
        """
        Scenario: Vehicle Disinfection Water Pump Pressure Loss Emergency Gate Lockout
        Given a vehicle transport order in "stock.picking" (库存拣货) arriving at a high-security livestock gate
        And the entry check-in activity is "Active" (进行中)
        When the disinfection water pump pressure sensor logs a drop below 0.5 Bar due to pump motor failure
        Then the system must atomically close and lock the physical gate actuator "agri.iot.switch" (物联网开关)
        And transition the picking status to "Blocked" (已被拦截) to prevent unauthorized biosecurity ingress
        And raise a "ValidationError" (验证错误) to halt the truck at the outer quarantine boundary
        And generate an emergency repair mission "mrp.workorder" [mrp.workorder] (作业任务) for the biosecurity maintenance technician
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a vehicle transport order in "stock.picking" (库存拣货) arriving at a high-security livestock gate',
            'And the entry check-in activity is "Active" (进行中)',
            'When the disinfection water pump pressure sensor logs a drop below 0.5 Bar due to pump motor failure',
            'Then the system must atomically close and lock the physical gate actuator "agri.iot.switch" (物联网开关)',
            'And transition the picking status to "Blocked" (已被拦截) to prevent unauthorized biosecurity ingress',
            'And raise a "ValidationError" (验证错误) to halt the truck at the outer quarantine boundary',
            'And generate an emergency repair mission "mrp.workorder" [mrp.workorder] (作业任务) for the biosecurity maintenance technician'
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
