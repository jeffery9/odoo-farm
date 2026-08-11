# -*- coding: utf-8 -*-
from odoo.addons.farm_core.tests.bdd_base import BddTransactionCase
from odoo.exceptions import UserError, ValidationError

class TestEpic065(BddTransactionCase):
    """ BDD Test Suite for Epic 065: Epic 065 Intensive Livestock Breeding (规模化畜牧育种管理) """

    def setUp(self):
        super(TestEpic065, self).setUp()

    def test_01_sow_gestation_cycle_pregnancy_detection_validation(self):
        """
        Scenario: Sow Gestation Cycle Pregnancy Detection Validation (母猪妊娠周期超声孕检自动排程)
        Given a breeding sow lot (育种母猪批次) "SOW-LOT-88" under stock.lot (库存批次) undergoing cycle monitoring in agri.livestock.breed (畜牧育种记录)
        And its breeding status is currently "inseminated (已配种)" with insemination_date (配种日期) set to 30 days ago
        When the Breeding Specialist (育种专家) logs a positive ultrasound pregnancy result (超声孕检阳性结果)
        Then the system must automatically transition the sow state in agri.livestock.breed (畜牧育种记录) to "pregnant (妊娠中)"
        And automatically calculate and schedule farrowing prep alerts (分娩准备警报) for Day 110 of the gestation cycle (Day 110/妊娠第110天)
        And write these tasks to the sow lot's activity calendar
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a breeding sow lot (育种母猪批次) "SOW-LOT-88" under stock.lot (库存批次) undergoing cycle monitoring in agri.livestock.breed (畜牧育种记录)',
            'And its breeding status is currently "inseminated (已配种)" with insemination_date (配种日期) set to 30 days ago',
            'When the Breeding Specialist (育种专家) logs a positive ultrasound pregnancy result (超声孕检阳性结果)',
            'Then the system must automatically transition the sow state in agri.livestock.breed (畜牧育种记录) to "pregnant (妊娠中)"',
            'And automatically calculate and schedule farrowing prep alerts (分娩准备警报) for Day 110 of the gestation cycle (Day 110/妊娠第110天)',
            "And write these tasks to the sow lot's activity calendar"
        ])

    def test_02_piglet_farrowing_litter_survival_metrics(self):
        """
        Scenario: Piglet Farrowing Litter Survival Metrics (仔猪分娩产仔存活率指标计算)
        Given an active farrowing event record of model agri.livestock.farrowing (仔猪分娩记录) linked to sow lot "SOW-LOT-88"
        When the farrowing supervisor logs the litter outcomes (分娩结果记录) as 12 Born Alive (活产数) and 1 Stillborn (死胎数)
        Then the system must compute the Litter Survival Percentage (窝存活率百分比) as 92.3%
        And update the farrowing analytics dashboard (分娩分析大屏) on agri.livestock.farrowing (仔猪分娩记录)
        And log this batch production yield under mrp.production (制造订单) with state "done (已完成)"
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an active farrowing event record of model agri.livestock.farrowing (仔猪分娩记录) linked to sow lot "SOW-LOT-88"',
            'When the farrowing supervisor logs the litter outcomes (分娩结果记录) as 12 Born Alive (活产数) and 1 Stillborn (死胎数)',
            'Then the system must compute the Litter Survival Percentage (窝存活率百分比) as 92.3%',
            'And update the farrowing analytics dashboard (分娩分析大屏) on agri.livestock.farrowing (仔猪分娩记录)',
            'And log this batch production yield under mrp.production (制造订单) with state "done (已完成)"'
        ])

    def test_03_breeding_insemination_incompatibility_gate(self):
        """
        Scenario: Breeding Insemination Incompatibility Gate (配种人工授精近交系数审查门禁)
        Given a planned artificial insemination task (人工授精计划) in agri.livestock.breed (畜牧育种记录)
        And a pedigree database of model agri.livestock.pedigree (畜牧系谱表) mapping ancestral generations (祖代关系)
        When the system compares the pedigree of male boar semen lot (公猪精液批次) "BOAR-SEM-77" to female sow lot "SOW-LOT-88"
        And calculates that their prospective inbreeding coefficient (近交系数) is 8.50%, exceeding the safety threshold of 6.25%
        Then the system must raise a ValidationError (验证错误): "Breeding blocked - Inbreeding coefficient exceeds threshold (配种已锁定，近交系数超出安全限制)"
        And block validation of the breeding contract, keeping its state as "unapproved (未批准)"
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a planned artificial insemination task (人工授精计划) in agri.livestock.breed (畜牧育种记录)',
            'And a pedigree database of model agri.livestock.pedigree (畜牧系谱表) mapping ancestral generations (祖代关系)',
            'When the system compares the pedigree of male boar semen lot (公猪精液批次) "BOAR-SEM-77" to female sow lot "SOW-LOT-88"',
            'And calculates that their prospective inbreeding coefficient (近交系数) is 8.50%, exceeding the safety threshold of 6.25%',
            'Then the system must raise a ValidationError (验证错误): "Breeding blocked - Inbreeding coefficient exceeds threshold (配种已锁定，近交系数超出安全限制)"',
            'And block validation of the breeding contract, keeping its state as "unapproved (未批准)"'
        ])

    def test_04_swine_heat_telemetry_sensor_offline_fallback(self):
        """
        Scenario: Swine Heat Telemetry Sensor Offline Fallback (母猪发情遥测传感器故障离线容灾)
        Given a group of sows registered under stock.lot (库存批次) wearing electronic heat monitoring collars (电子发情监测项圈) streaming data to agri.livestock.sensor.log (畜牧传感器日志)
        When the RF gateway connection (射频网关连接) fails to sync or stream data for over 12 hours (indicating sensor failure)
        Then the system must flag the sow monitoring status as "sensory_failed (传感器故障)"
        And automatically raise a daily manual heat-check checklist task (每日手动发情排查清单任务) of model project.task (项目任务) for the breeding technician
        And dispatch a notification to the vet director (兽医总监) via the chatter (沟通记录)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a group of sows registered under stock.lot (库存批次) wearing electronic heat monitoring collars (电子发情监测项圈) streaming data to agri.livestock.sensor.log (畜牧传感器日志)',
            'When the RF gateway connection (射频网关连接) fails to sync or stream data for over 12 hours (indicating sensor failure)',
            'Then the system must flag the sow monitoring status as "sensory_failed (传感器故障)"',
            'And automatically raise a daily manual heat-check checklist task (每日手动发情排查清单任务) of model project.task (项目任务) for the breeding technician',
            'And dispatch a notification to the vet director (兽医总监) via the chatter (沟通记录)'
        ])

    def test_05_gestation_barn_temperature_cooling_mist_interlock(self):
        """
        Scenario: Gestation Barn Temperature Cooling Mist Interlock (妊娠舍温度高热蒸发降温连锁自控)
        Given an intensive swine gestation barn (规模化妊娠母猪舍) monitored under stock.location (库存位置) "BARN-GEST-C"
        When ambient temperature sensors (室温传感器) log a reading of 32.5°C, exceeding the heat stress threshold (热应激阈值) of 32.0°C for pregnant sows
        Then the system must trigger active PLC relay commands of model agri.cea.plc.command (PLC自控指令)
        And start the evaporative cooling misting spray fans (蒸发降温喷雾风机) inside "BARN-GEST-C"
        And maintain misting until temperature drops below the safety floor of 26.0°C
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an intensive swine gestation barn (规模化妊娠母猪舍) monitored under stock.location (库存位置) "BARN-GEST-C"',
            'When ambient temperature sensors (室温传感器) log a reading of 32.5°C, exceeding the heat stress threshold (热应激阈值) of 32.0°C for pregnant sows',
            'Then the system must trigger active PLC relay commands of model agri.cea.plc.command (PLC自控指令)',
            'And start the evaporative cooling misting spray fans (蒸发降温喷雾风机) inside "BARN-GEST-C"',
            'And maintain misting until temperature drops below the safety floor of 26.0°C'
        ])

    def test_06_robotic_swarm_feed_dosing_calibration_drift_gating(self):
        """
        Scenario: Robotic Swarm Feed Dosing Calibration Drift Gating (饲喂机器人蜂群喂料计量漂移校准门禁)
        Given an automated breeding swine feed dosing robot (自动饲喂机器人) registered under model iiot.device (物联设备)
        And an active gestation feeding mission (活跃的妊娠饲喂任务) "mrp.workorder" (作业任务) inside barn stock.location (库存位置) "BARN-GEST-C"
        When the robot's onboard dosing sensor registers a calibration drift exceeding 5.0% during operation (称重给料传感器漂移大于5.0%)
        Then the system must automatically flag a dosing anomaly alarm (饲喂计量异常警报)
        And raise a ValidationError (验证错误): "Feed dosing calibration drift exceeded (给料传感器温漂超限)" and pause the mission "mrp.workorder" (作业任务) to prevent sow dietary health stress
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an automated breeding swine feed dosing robot (自动饲喂机器人) registered under model iiot.device (物联设备)',
            'And an active gestation feeding mission (活跃的妊娠饲喂任务) "mrp.workorder" (作业任务) inside barn stock.location (库存位置) "BARN-GEST-C"',
            "When the robot's onboard dosing sensor registers a calibration drift exceeding 5.0% during operation (称重给料传感器漂移大于5.0%)",
            'Then the system must automatically flag a dosing anomaly alarm (饲喂计量异常警报)',
            'And raise a ValidationError (验证错误): "Feed dosing calibration drift exceeded (给料传感器温漂超限)" and pause the mission "mrp.workorder" (作业任务) to prevent sow dietary health stress'
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
