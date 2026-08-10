# -*- coding: utf-8 -*-
from odoo.addons.farm_core.tests.bdd_base import BddTransactionCase
from odoo.exceptions import UserError, ValidationError

class TestEpic070(BddTransactionCase):
    """ BDD Test Suite for Epic 070: Epic 070 Precision Fertilization System (精准施肥系统) """

    def setUp(self):
        super(TestEpic070, self).setUp()

    def test_01_soil_nitrogen_lab_test_gis_vra_prescription_map_upload_gis_vra(self):
        """
        Scenario: Soil Nitrogen Lab Test GIS VRA Prescription Map Upload (土壤氮测试GIS VRA处方图上传)
        Given a parcel fertilizing campaign under "agri.vra.fertilizer" (农业可变速率施肥模型) in state "draft" (草稿)
        When the agronomist uploads a VRA nitrogen prescription shapefile map "prescription_map_file" (可变速率施肥氮处方图文件)
        Then the system must validate that all spatial coordinate zones in the map reside within the legal boundary coordinates of the crop parcel
        And raise a ValidationError (验证错误) message "GIS Spatial Error: Prescription zone out of parcel boundaries" (空间地理错误：处方区域超出分块边界) if any coordinate falls outside
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a parcel fertilizing campaign under "agri.vra.fertilizer" (农业可变速率施肥模型) in state "draft" (草稿)',
            'When the agronomist uploads a VRA nitrogen prescription shapefile map "prescription_map_file" (可变速率施肥氮处方图文件)',
            'Then the system must validate that all spatial coordinate zones in the map reside within the legal boundary coordinates of the crop parcel',
            'And raise a ValidationError (验证错误) message "GIS Spatial Error: Prescription zone out of parcel boundaries" (空间地理错误：处方区域超出分块边界) if any coordinate falls outside'
        ])

    def test_02_vra_spray_valve_solenoid_plc_active_gating_plc(self):
        """
        Scenario: VRA Spray Valve Solenoid PLC Active Gating (可变速率喷洒阀电磁阀PLC主动控制)
        Given an active tractor sprayer with real-time GPS telemetry connected under "mrp.workorder" (制造工单)
        When the tractor's spatial coordinates transition from High-Nitrogen Zone A to Low-Nitrogen Zone B on the prescription map
        Then the system must trigger an active PLC relay command "set_nozzle_flow" (设置喷嘴流量) to reduce chemical spray nozzle flow rates by "30.0%" (下调30.0%流量)
        And log the flow change on the telemetry feed on "agri.vra.fertilizer" (农业可变速率施肥模型)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an active tractor sprayer with real-time GPS telemetry connected under "mrp.workorder" (制造工单)',
            'When the tractor's spatial coordinates transition from High-Nitrogen Zone A to Low-Nitrogen Zone B on the prescription map',
            'Then the system must trigger an active PLC relay command "set_nozzle_flow" (设置喷嘴流量) to reduce chemical spray nozzle flow rates by "30.0%" (下调30.0%流量)',
            'And log the flow change on the telemetry feed on "agri.vra.fertilizer" (农业可变速率施肥模型)'
        ])

    def test_03_vra_solenoid_offline_flow_fallback_vra(self):
        """
        Scenario: VRA Solenoid Offline Flow Fallback (VRA电磁阀离线流量备用方案)
        Given a tractor-mounted precision sprayer actively executing a fertilization workorder "mrp.workorder" (制造工单)
        When the real-time VRA telemetry connection with Odoo is lost (实时可变速率施肥遥测连接丢失) during active operations
        Then the sprayer's PLC must trigger an automatic safe-state, defaulting spray valves to a fixed nominal rate of "150.0 Liters/hectare" (150升/公顷的固定标称速率)
        And log a telemetry warning "Telemetry Lost: Defaulting to Nominal Flow" (遥测丢失：默认标称流量) on "agri.vra.fertilizer" (农业可变速率施肥模型)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a tractor-mounted precision sprayer actively executing a fertilization workorder "mrp.workorder" (制造工单)',
            'When the real-time VRA telemetry connection with Odoo is lost (实时可变速率施肥遥测连接丢失) during active operations',
            'Then the sprayer's PLC must trigger an automatic safe-state, defaulting spray valves to a fixed nominal rate of "150.0 Liters/hectare" (150升/公顷的固定标称速率)',
            'And log a telemetry warning "Telemetry Lost: Defaulting to Nominal Flow" (遥测丢失：默认标称流量) on "agri.vra.fertilizer" (农业可变速率施肥模型)'
        ])

    def test_04_soil_phosphorus_saturation_spray_gating(self):
        """
        Scenario: Soil Phosphorus Saturation Spray Gating (土壤磷饱和度喷洒控制闸)
        Given a precision fertilization workorder "mrp.workorder" (制造工单) scheduled for a parcel
        When soil laboratory reports on that parcel register a phosphorus saturation index greater than "80.0 PPM" (土壤实验室报告记录磷饱和度指数大于80.0 PPM)
        Then the system must raise a ValidationError (验证错误) message "Application Blocked: Soil phosphorus saturation limits exceeded" (施肥被阻止：已超出土壤磷饱和限制)
        And block the state transition of the workorder to "ready" (准备就绪) to prevent environmental nitrate runoff
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a precision fertilization workorder "mrp.workorder" (制造工单) scheduled for a parcel',
            'When soil laboratory reports on that parcel register a phosphorus saturation index greater than "80.0 PPM" (土壤实验室报告记录磷饱和度指数大于80.0 PPM)',
            'Then the system must raise a ValidationError (验证错误) message "Application Blocked: Soil phosphorus saturation limits exceeded" (施肥被阻止：已超出土壤磷饱和限制)',
            'And block the state transition of the workorder to "ready" (准备就绪) to prevent environmental nitrate runoff'
        ])

    def test_05_completed_vra_mass_balance_reconciliation_vra(self):
        """
        Scenario: Completed VRA Mass Balance Reconciliation (完成VRA物料平衡校对)
        Given a completed precision fertilization workorder "mrp.workorder" (制造工单) in state "done" (完成)
        When the cost accountant executes the monthly mass balance close-out under "agri.vra.fertilizer" (农业可变速率施肥模型)
        Then the system must compute the total fertilizer mass applied from tractor PLC flow meters and compare it against raw material consumption on "stock.move" (库存移动单)
        And verify that the mass deviation is within a tolerance range of "+/-5.0%" (物料量偏差处于正负5.0%公差范围内)
        And write the calculated "Mass Balance Score" (物料平衡得分) to the fertilization campaign log
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a completed precision fertilization workorder "mrp.workorder" (制造工单) in state "done" (完成)',
            'When the cost accountant executes the monthly mass balance close-out under "agri.vra.fertilizer" (农业可变速率施肥模型)',
            'Then the system must compute the total fertilizer mass applied from tractor PLC flow meters and compare it against raw material consumption on "stock.move" (库存移动单)',
            'And verify that the mass deviation is within a tolerance range of "+/-5.0%" (物料量偏差处于正负5.0%公差范围内)',
            'And write the calculated "Mass Balance Score" (物料平衡得分) to the fertilization campaign log'
        ])

    def test_06_vra_flow_sensor_calibration_drift_protection(self):
        """
        Scenario: VRA Flow Sensor Calibration Drift Protection (可变速率施肥流量传感器漂移保护)
        Given a precision fertilization campaign under "agri.vra.fertilizer" (农业可变速率施肥模型)
        When real-time flow meters "iiot.device" (智能物联网设备) during an active fertilization run register an active flow rate deviating from the target prescription flow rate by "30.0%" (流量偏差超过30.0%) for a continuous period of "10 seconds"
        Then the system must automatically pause the fertilizing mission "mrp.workorder" (作业任务) and transition its state to "blocked" (已阻断)
        And raise a ValidationError (验证错误) message "VRA Flow Drift: Mission paused for nozzle calibration" (变量施肥流量漂移：任务已挂起，需要校准喷嘴)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a precision fertilization campaign under "agri.vra.fertilizer" (农业可变速率施肥模型)',
            'When real-time flow meters "iiot.device" (智能物联网设备) during an active fertilization run register an active flow rate deviating from the target prescription flow rate by "30.0%" (流量偏差超过30.0%) for a continuous period of "10 seconds"',
            'Then the system must automatically pause the fertilizing mission "mrp.workorder" (作业任务) and transition its state to "blocked" (已阻断)',
            'And raise a ValidationError (验证错误) message "VRA Flow Drift: Mission paused for nozzle calibration" (变量施肥流量漂移：任务已挂起，需要校准喷嘴)'
        ])
