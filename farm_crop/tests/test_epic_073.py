# -*- coding: utf-8 -*-
from odoo.addons.farm_core.tests.bdd_base import BddTransactionCase
from odoo.exceptions import UserError, ValidationError

class TestEpic073(BddTransactionCase):
    """ BDD Test Suite for Epic 073: Epic 073 Weed Identification & Control (杂草识别与控制) """

    def setUp(self):
        super(TestEpic073, self).setUp()

    def test_01_drone_weed_infestation_classification_gis_map_ingestion_gis(self):
        """
        Scenario: Drone Weed Infestation Classification GIS Map Ingestion (无人机杂草分布分类GIS地图导入)
        Given a weed logging session under "agri.weed.log" (杂草识别与记录模型) in state "draft" (草稿)
        When the agronomist uploads a multi-spectrum weed classification coordinate map "weed_classification_map" (多光谱杂草分类图)
        Then the system must validate that all coordinate points reside entirely within the legal geographical bounds of the target crop parcel
        And raise a ValidationError (验证错误) message "GIS Spatial Error: Weed coordinate points out of parcel boundaries" (空间地理错误：杂草坐标点超出土地分块边界限制) if any point falls outside
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a weed logging session under "agri.weed.log" (杂草识别与记录模型) in state "draft" (草稿)',
            'When the agronomist uploads a multi-spectrum weed classification coordinate map "weed_classification_map" (多光谱杂草分类图)',
            'Then the system must validate that all coordinate points reside entirely within the legal geographical bounds of the target crop parcel',
            'And raise a ValidationError (验证错误) message "GIS Spatial Error: Weed coordinate points out of parcel boundaries" (空间地理错误：杂草坐标点超出土地分块边界限制) if any point falls outside'
        ])

    def test_02_spot_spraying_drone_vra_valve_plc_control_plc(self):
        """
        Scenario: Spot Spraying Drone VRA Valve PLC Control (无人机定点喷洒可变速率电磁阀PLC控制)
        Given an active drone spot-spraying flight under "mrp.workorder" (制造工单) in state "in_progress" (进行中)
        When the drone's real-time GPS coordinates transition from Clean Zone A to Weed Infestation Zone B (当无人机实时GPS坐标由无草区A过渡到杂草受害区B时)
        Then the system must trigger an active PLC relay command "open_spray_nozzle_vra" (打开VRA定点喷雾喷嘴) to scale spraying nozzle output to "100.0%" (调整喷嘴输出至100.0%流量)
        And adjust nozzle output back to "0.0%" when entering a clean zone
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an active drone spot-spraying flight under "mrp.workorder" (制造工单) in state "in_progress" (进行中)',
            'When the drone's real-time GPS coordinates transition from Clean Zone A to Weed Infestation Zone B (当无人机实时GPS坐标由无草区A过渡到杂草受害区B时)',
            'Then the system must trigger an active PLC relay command "open_spray_nozzle_vra" (打开VRA定点喷雾喷嘴) to scale spraying nozzle output to "100.0%" (调整喷嘴输出至100.0%流量)',
            'And adjust nozzle output back to "0.0%" when entering a clean zone'
        ])

    def test_03_drone_spraying_wind_speed_flight_gating(self):
        """
        Scenario: Drone Spraying Wind Speed Flight Gating (无人机定点喷洒风速安全控制闸)
        Given a scheduled drone chemical weed control campaign under "mrp.workorder" (制造工单)
        When local weather wind speed sensors log wind speed values exceeding "4.0 m/s" (当本地气象站风速传感器记录风速超过4.0米/秒，面临药剂漂移风险)
        Then the system must raise a ValidationError (验证错误) message "Spraying Blocked: Wind speed exceeds safe drift threshold" (喷洒被阻止：风速超出安全漂移阈值)
        And set the flight execution status on "agri.weed.log" (杂草识别与记录模型) to "aborted" (已中止)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a scheduled drone chemical weed control campaign under "mrp.workorder" (制造工单)',
            'When local weather wind speed sensors log wind speed values exceeding "4.0 m/s" (当本地气象站风速传感器记录风速超过4.0米/秒，面临药剂漂移风险)',
            'Then the system must raise a ValidationError (验证错误) message "Spraying Blocked: Wind speed exceeds safe drift threshold" (喷洒被阻止：风速超出安全漂移阈值)',
            'And set the flight execution status on "agri.weed.log" (杂草识别与记录模型) to "aborted" (已中止)'
        ])

    def test_04_spatial_coordinates_drone_spray_valve_offline_fallback(self):
        """
        Scenario: Spatial Coordinates Drone Spray Valve Offline Fallback (地理空间坐标无人机喷洒阀离线安全机制)
        Given an active spot-spraying drone survey under "agri.weed.log" (杂草识别与记录模型)
        When real-time GPS and nozzle flow telemetry communication with Odoo is lost during active operations (当实时GPS与喷头流量遥测通信在作业中丢失)
        Then the drone's localized PLC must automatically shut off chemical spraying valves and trigger Return-To-Home mode (无人机本地PLC必须自动关闭化学药剂喷洒电磁阀并启动安全返航)
        And log a telemetry warning "GPS Telemetry Lost: Flow Shutoff & Safe RTH Initiated" (GPS遥测丢失：关闭喷洒流量并启动安全返航) on the campaign record
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an active spot-spraying drone survey under "agri.weed.log" (杂草识别与记录模型)',
            'When real-time GPS and nozzle flow telemetry communication with Odoo is lost during active operations (当实时GPS与喷头流量遥测通信在作业中丢失)',
            'Then the drone's localized PLC must automatically shut off chemical spraying valves and trigger Return-To-Home mode (无人机本地PLC必须自动关闭化学药剂喷洒电磁阀并启动安全返航)',
            'And log a telemetry warning "GPS Telemetry Lost: Flow Shutoff & Safe RTH Initiated" (GPS遥测丢失：关闭喷洒流量并启动安全返航) on the campaign record'
        ])

    def test_05_completed_spot_spraying_chemical_balance_verification(self):
        """
        Scenario: Completed Spot Spraying Chemical Balance Verification (定点喷洒化学药剂用量平衡验证)
        Given a completed spot-sprowing workorder "mrp.workorder" (制造工单) in state "done" (完成)
        When the warehouse manager reconciles the herbicide raw inventory on "stock.move" (库存移动单)
        Then the system must calculate and verify that the actual herbicide volume consumed matches the calculated prescription map requirements within a tolerance of "+/-5.0%"
        And write the calculated "Chemical Balance Score" (药剂物料平衡得分) to the "agri.weed.log" (杂草识别与记录模型) record
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a completed spot-sprowing workorder "mrp.workorder" (制造工单) in state "done" (完成)',
            'When the warehouse manager reconciles the herbicide raw inventory on "stock.move" (库存移动单)',
            'Then the system must calculate and verify that the actual herbicide volume consumed matches the calculated prescription map requirements within a tolerance of "+/-5.0%"',
            'And write the calculated "Chemical Balance Score" (药剂物料平衡得分) to the "agri.weed.log" (杂草识别与记录模型) record'
        ])

    def test_06_spot_spraying_uav_altitude_deviant_drift_gating(self):
        """
        Scenario: Spot Spraying UAV Altitude Deviant Drift Gating (无人机定点喷洒高度偏差漂移控制闸)
        Given an active spot-spraying drone survey under "agri.weed.log" (杂草识别与记录模型)
        When the drone's radar altimeter "iiot.device" (智能物联网设备) registers an active flight altitude deviating from the safe spraying altitude limit by "2.0 meters" (飞行高度偏差超过2.0米，面临漂移超标风险)
        Then the system must trigger an active PLC relay command to pause chemical spray valves and pause the spraying mission "mrp.workorder" (作业任务)
        And write a telemetry warning "Altitude Drift: Nozzle spray paused" (高度漂移：喷淋已暂停) to the pilot dashboard
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an active spot-spraying drone survey under "agri.weed.log" (杂草识别与记录模型)',
            'When the drone's radar altimeter "iiot.device" (智能物联网设备) registers an active flight altitude deviating from the safe spraying altitude limit by "2.0 meters" (飞行高度偏差超过2.0米，面临漂移超标风险)',
            'Then the system must trigger an active PLC relay command to pause chemical spray valves and pause the spraying mission "mrp.workorder" (作业任务)',
            'And write a telemetry warning "Altitude Drift: Nozzle spray paused" (高度漂移：喷淋已暂停) to the pilot dashboard'
        ])
