# -*- coding: utf-8 -*-
from odoo.addons.farm_core.tests.bdd_base import BddTransactionCase
from odoo.exceptions import UserError, ValidationError

class TestEpic071(BddTransactionCase):
    """ BDD Test Suite for Epic 071: Epic 071 Drone Based Crop Monitoring (无人机作物监测) """

    def setUp(self):
        super(TestEpic071, self).setUp()

    def test_01_drone_ndvi_crop_canopy_health_gis_map_upload_ndvigis(self):
        """
        Scenario: Drone NDVI Crop Canopy Health GIS Map Upload (无人机NDVI作物冠层健康GIS地图上传)
        Given a drone survey campaign under "agri.drone.survey" (无人机测绘模型) in state "draft" (草稿)
        When the drone operator uploads a multispectral NDVI orthomosaic map "ndvi_orthomosaic_map" (多光谱NDVI正射影像图)
        Then the system must validate that the spatial coordinate boundaries of the image reside entirely within the legal bounds of the target "stock.location" (库存库位)
        And set the survey record status to "imported" (已导入) upon successful verification
        And raise a ValidationError (验证错误) message "GIS Spatial Error: Image boundaries out of parcel coordinate limits" (空间地理错误：影像边界超出土地分块坐标限制) if any boundary falls outside
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a drone survey campaign under "agri.drone.survey" (无人机测绘模型) in state "draft" (草稿)',
            'When the drone operator uploads a multispectral NDVI orthomosaic map "ndvi_orthomosaic_map" (多光谱NDVI正射影像图)',
            'Then the system must validate that the spatial coordinate boundaries of the image reside entirely within the legal bounds of the target "stock.location" (库存库位)',
            'And set the survey record status to "imported" (已导入) upon successful verification',
            'And raise a ValidationError (验证错误) message "GIS Spatial Error: Image boundaries out of parcel coordinate limits" (空间地理错误：影像边界超出土地分块坐标限制) if any boundary falls outside'
        ])

    def test_02_multispectrum_ndvi_crop_disease_location_identification_ndvi(self):
        """
        Scenario: Multi-Spectrum NDVI Crop Disease Location Identification (多光谱NDVI作物病害位置识别与巡检报警)
        Given an imported drone survey campaign under "agri.drone.survey" (无人机测绘模型) in state "imported" (已导入)
        When the spatial analytics engine identifies a coordinate zone with NDVI values below "0.35" (空间分析引擎识别出NDVI值低于0.35的坐标区域)
        Then the system must automatically create a high-priority scouting activity "mrp.workorder" (制造工单) with the target GPS coordinate "Latitude: 30.267, Longitude: 120.155"
        And set the scouting workorder state to "ready" (准备就绪)
        And write a telemetry warning "Anomaly Detected: NDVI stress threshold breached" (检测到异常：NDVI受胁迫阈值突破) into the survey analysis log
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an imported drone survey campaign under "agri.drone.survey" (无人机测绘模型) in state "imported" (已导入)',
            'When the spatial analytics engine identifies a coordinate zone with NDVI values below "0.35" (空间分析引擎识别出NDVI值低于0.35的坐标区域)',
            'Then the system must automatically create a high-priority scouting activity "mrp.workorder" (制造工单) with the target GPS coordinate "Latitude: 30.267, Longitude: 120.155"',
            'And set the scouting workorder state to "ready" (准备就绪)',
            'And write a telemetry warning "Anomaly Detected: NDVI stress threshold breached" (检测到异常：NDVI受胁迫阈值突破) into the survey analysis log'
        ])

    def test_03_drone_survey_wind_launch_gating(self):
        """
        Scenario: Drone Survey Wind Launch Gating (无人机测绘风速起飞控制闸)
        Given a planned drone survey under "agri.drone.survey" (无人机测绘模型) in state "assigned" (已指派)
        When the local weather station registers real-time wind speeds exceeding "5.5 m/s" (实时风速超过5.5米/秒)
        Then the system must raise a ValidationError (验证错误) message "Flight Blocked: Wind speed exceeds drone launch limits" (飞行被阻止：风速超出无人机起飞限制)
        And force the drone survey flight state to "aborted" (已中止) to protect physical assets
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a planned drone survey under "agri.drone.survey" (无人机测绘模型) in state "assigned" (已指派)',
            'When the local weather station registers real-time wind speeds exceeding "5.5 m/s" (实时风速超过5.5米/秒)',
            'Then the system must raise a ValidationError (验证错误) message "Flight Blocked: Wind speed exceeds drone launch limits" (飞行被阻止：风速超出无人机起飞限制)',
            'And force the drone survey flight state to "aborted" (已中止) to protect physical assets'
        ])

    def test_04_drone_telemetry_lowbattery_obstacle_emergency_rth(self):
        """
        Scenario: Drone Telemetry Low-Battery Obstacle Emergency RTH (无人机遥测低电量应急返航机制)
        Given an active drone survey campaign "agri.drone.survey" (无人机测绘模型) in state "in_progress" (进行中)
        When the drone's IoT real-time telemetry registers battery level dropping below "15.0%" (物联网实时遥测显示电池电量跌破15.0%)
        Then the system must trigger an automatic safe Return-To-Home event and command the drone's PLC controller to return (触发自动安全返航事件并向无人机PLC控制器发出返航指令)
        And write a telemetry warning "Emergency Alert: Low battery detected, initiating RTH hold" (紧急警报：检测到低电量，启动应急返航挂起)
        And transition the survey campaign status to "paused" (已暂停)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an active drone survey campaign "agri.drone.survey" (无人机测绘模型) in state "in_progress" (进行中)',
            'When the drone's IoT real-time telemetry registers battery level dropping below "15.0%" (物联网实时遥测显示电池电量跌破15.0%)',
            'Then the system must trigger an automatic safe Return-To-Home event and command the drone's PLC controller to return (触发自动安全返航事件并向无人机PLC控制器发出返航指令)',
            'And write a telemetry warning "Emergency Alert: Low battery detected, initiating RTH hold" (紧急警报：检测到低电量，启动应急返航挂起)',
            'And transition the survey campaign status to "paused" (已暂停)'
        ])

    def test_05_drone_photo_metadata_crop_variety_calibration(self):
        """
        Scenario: Drone Photo Metadata Crop Variety Calibration (无人机照片元数据作物种类校对)
        Given high-resolution crop canopy photos associated with "stock.lot" (库存批次) for calibration
        When the image processor extracts the embedded EXIF metadata timestamp "2026-08-09 10:00:00"
        Then the system must validate that the EXIF timestamp falls within the active cultivation start and harvest date range of the crop lot
        And raise a ValidationError (验证错误) message "Mismatched timestamp for variety validation" (时间戳与品种验证不匹配) if the photo date is outside the valid cultivation window
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given high-resolution crop canopy photos associated with "stock.lot" (库存批次) for calibration',
            'When the image processor extracts the embedded EXIF metadata timestamp "2026-08-09 10:00:00"',
            'Then the system must validate that the EXIF timestamp falls within the active cultivation start and harvest date range of the crop lot',
            'And raise a ValidationError (验证错误) message "Mismatched timestamp for variety validation" (时间戳与品种验证不匹配) if the photo date is outside the valid cultivation window'
        ])

    def test_06_uav_connectivity_lost_signal_safe_landing(self):
        """
        Scenario: UAV Connectivity Lost Signal Safe Landing (无人机连接丢失信号异常安全着陆)
        Given an active drone survey campaign "agri.drone.survey" (无人机测绘模型) in state "in_progress" (进行中)
        When the UAV's real-time IoT gateway "iiot.device" (智能物联网设备) registers a connectivity signal loss lasting over "45 seconds" (遥测连接丢失超过45秒)
        Then the system must automatically flag the flight status as "signal_lost" (信号丢失)
        And trigger an emergency automated PLC waypoint landing procedure to command the drone to land safely at the nearest predefined coordinates (触发紧急自动安全降落程序并向无人机PLC发出就近安全降落指令)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an active drone survey campaign "agri.drone.survey" (无人机测绘模型) in state "in_progress" (进行中)',
            'When the UAV's real-time IoT gateway "iiot.device" (智能物联网设备) registers a connectivity signal loss lasting over "45 seconds" (遥测连接丢失超过45秒)',
            'Then the system must automatically flag the flight status as "signal_lost" (信号丢失)',
            'And trigger an emergency automated PLC waypoint landing procedure to command the drone to land safely at the nearest predefined coordinates (触发紧急自动安全降落程序并向无人机PLC发出就近安全降落指令)'
        ])
