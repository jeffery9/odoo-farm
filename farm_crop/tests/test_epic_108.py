# -*- coding: utf-8 -*-
from odoo.addons.farm_core.tests.bdd_base import BddTransactionCase
from odoo.exceptions import UserError, ValidationError

class TestEpic108(BddTransactionCase):
    """ BDD Test Suite for Epic 108: Epic 108 Advanced VRA Algorithms Multi-Source Data Fusion (高级变量施肥多源数据融合) """

    def setUp(self):
        super(TestEpic108, self).setUp()

    def test_01_multisource_som_sensor_calibration_and_fusion_som(self):
        """
        Scenario: Multi-Source SOM Sensor Calibration and Fusion (多源SOM传感器校准与数据融合)
        Given a variety parcel mapping under "mrp.workorder" (任务模型) with state "draft" (草稿状态)
        And laboratory measurement for soil organic matter "som_lab_value" is 2.5% (并且实验室测定的土壤有机质含量字段值为2.5%)
        And drone sensor estimation "som_drone_value" is 2.8% (并且无人机估算的土壤有机质含量字段值为2.8%)
        And physical sensor reading "som_sensor_value" is 2.4% (并且物理车载传感器土壤有机质含量字段值为2.4%)
        When the agronomist requests to combine multi-source laboratory, drone, and soil sensors (当农艺师请求执行融合多源实验室、无人机与土壤传感器数据系统操作) under "agri.vra.fusion" (在高级变量施肥多源数据融合模型下)
        Then the system must execute apply weighted calibration offsets (+/-1.5%) (系统必须执行应用加权校准偏差值+/-1.5%系统操作)
        And output a single calibrated value in "fused_som_value" of 2.56% (并在融合后的土壤有机质含量字段中输出一个经校准的2.56%的数值)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a variety parcel mapping under "mrp.workorder" (任务模型) with state "draft" (草稿状态)',
            'And laboratory measurement for soil organic matter "som_lab_value" is 2.5% (并且实验室测定的土壤有机质含量字段值为2.5%)',
            'And drone sensor estimation "som_drone_value" is 2.8% (并且无人机估算的土壤有机质含量字段值为2.8%)',
            'And physical sensor reading "som_sensor_value" is 2.4% (并且物理车载传感器土壤有机质含量字段值为2.4%)',
            'When the agronomist requests to combine multi-source laboratory, drone, and soil sensors (当农艺师请求执行融合多源实验室、无人机与土壤传感器数据系统操作) under "agri.vra.fusion" (在高级变量施肥多源数据融合模型下)',
            'Then the system must execute apply weighted calibration offsets (+/-1.5%) (系统必须执行应用加权校准偏差值+/-1.5%系统操作)',
            'And output a single calibrated value in "fused_som_value" of 2.56% (并在融合后的土壤有机质含量字段中输出一个经校准的2.56%的数值)'
        ])

    def test_02_realtime_tractor_vra_valve_control(self):
        """
        Scenario: Real-time Tractor VRA Valve Control (实时拖拉机变量施肥阀门控制)
        Given an active variable rate mission under "mrp.workorder" (任务模型) with state "confirmed" (已确认状态)
        And the tractor VRA spray controller has loaded GPS polygon maps (且拖拉机变量喷洒控制器已加载GPS多边形地图)
        When the tractor coordinates "gps_coordinates" transition from High-SOM zone to Low-SOM zone (当拖拉机GPS经纬度坐标字段位置从高有机质区域过渡到低有机质区域时)
        Then the telemetry system under "agri.vra.fusion" must execute send nozzle flow adjustment commands (-15%) (在高级变量施肥多源数据融合模型下的遥测系统必须执行发送喷头流量调整指令-15%系统操作)
        And update the current target "nozzle_flow_rate" to match the prescription (并更新当前的喷头流量字段以匹配变量处方)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an active variable rate mission under "mrp.workorder" (任务模型) with state "confirmed" (已确认状态)',
            'And the tractor VRA spray controller has loaded GPS polygon maps (且拖拉机变量喷洒控制器已加载GPS多边形地图)',
            'When the tractor coordinates "gps_coordinates" transition from High-SOM zone to Low-SOM zone (当拖拉机GPS经纬度坐标字段位置从高有机质区域过渡到低有机质区域时)',
            'Then the telemetry system under "agri.vra.fusion" must execute send nozzle flow adjustment commands (-15%) (在高级变量施肥多源数据融合模型下的遥测系统必须执行发送喷头流量调整指令-15%系统操作)',
            'And update the current target "nozzle_flow_rate" to match the prescription (并更新当前的喷头流量字段以匹配变量处方)'
        ])

    def test_03_sensor_offline_fallback_safe_mode_irrigation(self):
        """
        Scenario: Sensor Offline Fallback Safe Mode Irrigation (传感器离线故障自动降级安全模式灌溉)
        Given an automated irrigation sequence under "mrp.workorder" (任务模型)
        And the field soil moisture sensor connection status "sensor_connection_status" is "online" (且田间土壤水分传感器连接状态字段值为在线状态)
        When the telemetry connection drops transitioning the state to "offline" (当遥测连接中断且状态转为离线状态时)
        Then the controller under "agri.vra.fusion" must execute switch controllers to safe fixed-rate duty-cycles (高级变量施肥多源数据融合模型下的控制器必须执行将控制器切换至安全固定比例循环模式系统操作)
        And transition the operation state to "safe_mode" (并将作业状态过渡到安全降级模式状态)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an automated irrigation sequence under "mrp.workorder" (任务模型)',
            'And the field soil moisture sensor connection status "sensor_connection_status" is "online" (且田间土壤水分传感器连接状态字段值为在线状态)',
            'When the telemetry connection drops transitioning the state to "offline" (当遥测连接中断且状态转为离线状态时)',
            'Then the controller under "agri.vra.fusion" must execute switch controllers to safe fixed-rate duty-cycles (高级变量施肥多源数据融合模型下的控制器必须执行将控制器切换至安全固定比例循环模式系统操作)',
            'And transition the operation state to "safe_mode" (并将作业状态过渡到安全降级模式状态)'
        ])

    def test_04_high_wind_safety_sprayer_launch_block(self):
        """
        Scenario: High Wind Safety Sprayer Launch Block (高风速安全喷洒设备启动拦截)
        Given a robotic drone spraying task under "mrp.workorder" (任务模型) with state "draft" (草稿状态)
        And weather sensor telemetry logs "wind_speed" of 5.2 m/s (且天气遥测传感器记录风速字段值为5.2米/秒)
        When the operator attempts to trigger the sprayer start command (当操作员尝试触发喷药机启动指令时)
        Then the safety system under "agri.vra.fusion" must execute block launch and cancel the mission (高级变量施肥多源数据融合模型下的安全系统必须执行拦截发射并取消任务系统操作)
        And update the mission state to "cancelled" (并更新任务状态为已取消状态)
        And raise a ValidationError (并抛出验证错误) with message "Wind speed exceeds safety limit of 4.0 m/s. Mission cancelled." (包含提示“风速超过4.0米/秒安全限制。作业已被取消。”的验证错误消息)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a robotic drone spraying task under "mrp.workorder" (任务模型) with state "draft" (草稿状态)',
            'And weather sensor telemetry logs "wind_speed" of 5.2 m/s (且天气遥测传感器记录风速字段值为5.2米/秒)',
            'When the operator attempts to trigger the sprayer start command (当操作员尝试触发喷药机启动指令时)',
            'Then the safety system under "agri.vra.fusion" must execute block launch and cancel the mission (高级变量施肥多源数据融合模型下的安全系统必须执行拦截发射并取消任务系统操作)',
            'And update the mission state to "cancelled" (并更新任务状态为已取消状态)',
            'And raise a ValidationError (并抛出验证错误) with message "Wind speed exceeds safety limit of 4.0 m/s. Mission cancelled." (包含提示“风速超过4.0米/秒安全限制。作业已被取消。”的验证错误消息)'
        ])

    def test_05_pretreatment_soil_runoff_compliance_block(self):
        """
        Scenario: Pre-Treatment Soil Runoff Compliance Block (施肥前土壤径流流失合规拦截)
        Given a scheduled nitrogen application task under "mrp.workorder" (任务模型) with state "draft" (草稿状态)
        And the local soil sensor logs "soil_nitrogen_runoff_level" of 165.0 kg/ha (且当地土壤传感器记录土壤氮流失水平字段值为165.0公斤/公顷)
        When the operator attempts to validate the mission (当操作员尝试验证该作业任务时)
        Then the safety system under "agri.vra.fusion" must execute block mission confirmation (高级变量施肥多源数据融合模型下的安全系统必须执行拦截任务确认系统操作)
        And raise a ValidationError (并抛出验证错误) with message "Pre-treatment soil nitrogen runoff levels exceed limit of 150.0 kg/ha. Operation blocked." (包含提示“施肥前土壤氮流失超过150.0公斤/公顷限制。操作已拦截。”的验证错误消息)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a scheduled nitrogen application task under "mrp.workorder" (任务模型) with state "draft" (草稿状态)',
            'And the local soil sensor logs "soil_nitrogen_runoff_level" of 165.0 kg/ha (且当地土壤传感器记录土壤氮流失水平字段值为165.0公斤/公顷)',
            'When the operator attempts to validate the mission (当操作员尝试验证该作业任务时)',
            'Then the safety system under "agri.vra.fusion" must execute block mission confirmation (高级变量施肥多源数据融合模型下的安全系统必须执行拦截任务确认系统操作)',
            'And raise a ValidationError (并抛出验证错误) with message "Pre-treatment soil nitrogen runoff levels exceed limit of 150.0 kg/ha. Operation blocked." (包含提示“施肥前土壤氮流失超过150.0公斤/公顷限制。操作已拦截。”的验证错误消息)'
        ])

    def test_06_circular_economy_biomass_gating_on_vra_nitrogen(self):
        """
        Scenario: Circular Economy Biomass Gating on VRA Nitrogen (高级变量施肥生物质流失门控)
        Given a variable nitrogen spraying prescription mission (变量氮肥喷洒作业任务) under "mrp.workorder" (任务模型) linked to "agri.vra.fusion" (高级变量施肥多源数据融合模型下)
        And the compost organic biomass component lacks active validation in circular ledger "biomass_certified"
        When the agronomist attempts to generate the prescription map via action "action_generate_prescription" (生成变量处方动作)
        Then the system blocks the generation and locks the task state (状态) in "draft" (草稿状态)
        And raises a ValidationError (验证错误) "ValidationError: Compost biomass lacks circular economy certification (验证错误：有机堆肥生物质缺少循环经济认证)"
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a variable nitrogen spraying prescription mission (变量氮肥喷洒作业任务) under "mrp.workorder" (任务模型) linked to "agri.vra.fusion" (高级变量施肥多源数据融合模型下)',
            'And the compost organic biomass component lacks active validation in circular ledger "biomass_certified"',
            'When the agronomist attempts to generate the prescription map via action "action_generate_prescription" (生成变量处方动作)',
            'Then the system blocks the generation and locks the task state (状态) in "draft" (草稿状态)',
            'And raises a ValidationError (验证错误) "ValidationError: Compost biomass lacks circular economy certification (验证错误：有机堆肥生物质缺少循环经济认证)"'
        ])

    def test_07_crop_parcel_evapotranspiration_sensor_drift(self):
        """
        Scenario: Crop Parcel Evapotranspiration Sensor Drift (作物地块水分蒸腾传感器异常漂移自愈控制)
        Given a crop parcel's soil stock lot in "stock.lot" (库存批次模型) with crop variety "Rose" (且作物物种已设置为玫瑰)
        And a smart evapotranspiration sensor registered in "iiot.device" (并且智能蒸腾量传感器已注册在工业物联网设备模型中)
        When the soil sensor logs an NPK reading drift of 25.0% (当土壤传感器记录到氮磷钾读数偏离比比例达到25.0%时)
        Then the system must trigger safe mode self-correction (系统必须自动执行安全模式自校准动作)
        And scale back the water drip runtime "drip_duration" to fallback 10.0 minutes (并且将滴灌时长字段值等比例缩减至备用时长值10.0分钟)
        And raise a ValidationError (并且系统抛出验证错误) with message "CRITICAL_SENSOR_DRIFT_DETECTED" (包含"传感器发生严重漂移，进入自愈模式"提示信息)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a crop parcel\'s soil stock lot in "stock.lot" (库存批次模型) with crop variety "Rose" (且作物物种已设置为玫瑰)',
            'And a smart evapotranspiration sensor registered in "iiot.device" (并且智能蒸腾量传感器已注册在工业物联网设备模型中)',
            'When the soil sensor logs an NPK reading drift of 25.0% (当土壤传感器记录到氮磷钾读数偏离比比例达到25.0%时)',
            'Then the system must trigger safe mode self-correction (系统必须自动执行安全模式自校准动作)',
            'And scale back the water drip runtime "drip_duration" to fallback 10.0 minutes (并且将滴灌时长字段值等比例缩减至备用时长值10.0分钟)',
            'And raise a ValidationError (并且系统抛出验证错误) with message "CRITICAL_SENSOR_DRIFT_DETECTED" (包含"传感器发生严重漂移，进入自愈模式"提示信息)'
        ])
