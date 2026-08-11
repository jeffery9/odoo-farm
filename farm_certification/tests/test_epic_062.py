# -*- coding: utf-8 -*-
from odoo.addons.farm_core.tests.bdd_base import BddTransactionCase
from odoo.exceptions import UserError, ValidationError

class TestEpic062(BddTransactionCase):
    """ BDD Test Suite for Epic 062: Epic 062 Brand Organic Integrity (有机品牌诚信保护) """

    def setUp(self):
        super(TestEpic062, self).setUp()

    def test_01_nonorganic_component_bom_organic_gating_bom(self):
        """
        Scenario: Non-Organic Component BOM Organic Gating (非有机原料BOM审查门禁)
        Given a processed product lot (加工产品批次) "ORG-JAM-202" undergoing certification verification under agri.organic.audit (农业有机审计)
        And its Bill of Materials of model mrp.bom (物料清单) defines multiple raw material ingredients
        When the system analyzes the batch components via "action_verify_bom_organic_status (验证物料清单有机状态)"
        And finds that raw ingredient lot "SUGAR-NONORG-99" has its organic_badge_active (有机徽章激活) field set to False (为假) on stock.lot (库存批次)
        Then the system must raise a ValidationError (验证错误): "BOM contains non-organic ingredient (物料清单中包含非有机原料)"
        And automatically set the "organic_badge_active (有机徽章激活)" field to False (为假) on lot "ORG-JAM-202"
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a processed product lot (加工产品批次) "ORG-JAM-202" undergoing certification verification under agri.organic.audit (农业有机审计)',
            'And its Bill of Materials of model mrp.bom (物料清单) defines multiple raw material ingredients',
            'When the system analyzes the batch components via "action_verify_bom_organic_status (验证物料清单有机状态)"',
            'And finds that raw ingredient lot "SUGAR-NONORG-99" has its organic_badge_active (有机徽章激活) field set to False (为假) on stock.lot (库存批次)',
            'Then the system must raise a ValidationError (验证错误): "BOM contains non-organic ingredient (物料清单中包含非有机原料)"',
            'And automatically set the "organic_badge_active (有机徽章激活)" field to False (为假) on lot "ORG-JAM-202"'
        ])

    def test_02_adjacent_chemical_drift_gis_gating_gis(self):
        """
        Scenario: Adjacent Chemical Drift GIS Gating (相邻化学品漂移GIS监测门禁)
        Given an organic farming land parcel (有机农田地块) "PARCEL-ORG-A" registered under stock.location (库存位置)
        When pesticide spraying logs under agri.field.service (农事服务记录) register a spray operation of chemical pesticide (化学农药喷洒作业) on an adjacent parcel "PARCEL-CONV-B" within 10.0 meters of boundary coordinates
        Then the system must automatically flag "PARCEL-ORG-A" as "at_risk (有漂移风险)" on its stock.location (库存位置)
        And schedule an immediate, high-priority organic soil audit task (有机土壤审计任务) of model agri.organic.audit (农业有机审计)
        And lock organic label printing for all crops harvested from "PARCEL-ORG-A" until a passing soil test is uploaded
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an organic farming land parcel (有机农田地块) "PARCEL-ORG-A" registered under stock.location (库存位置)',
            'When pesticide spraying logs under agri.field.service (农事服务记录) register a spray operation of chemical pesticide (化学农药喷洒作业) on an adjacent parcel "PARCEL-CONV-B" within 10.0 meters of boundary coordinates',
            'Then the system must automatically flag "PARCEL-ORG-A" as "at_risk (有漂移风险)" on its stock.location (库存位置)',
            'And schedule an immediate, high-priority organic soil audit task (有机土壤审计任务) of model agri.organic.audit (农业有机审计)',
            'And lock organic label printing for all crops harvested from "PARCEL-ORG-A" until a passing soil test is uploaded'
        ])

    def test_03_organic_status_propagation_on_delivery(self):
        """
        Scenario: Organic Status Propagation on Delivery (发运时有机属性级联验证)
        Given an outgoing delivery order of model stock.picking (库存拣货) containing crop lots scheduled for premium shipment
        And the picking is in state "assigned (已保留)"
        When the warehouse operator attempts to perform "button_validate (验证出库)"
        Then the system must iterate through all linked stock.move (库存移动) records
        And verify that every linked stock.lot (库存批次) has "organic_badge_active (有机徽章激活)" set to True (为真)
        And raise a ValidationError (验证错误): "Unverified organic lot detected in moves (检测到发运移动中包含未验证的有机构成)" and block validation if any lot is unverified
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an outgoing delivery order of model stock.picking (库存拣货) containing crop lots scheduled for premium shipment',
            'And the picking is in state "assigned (已保留)"',
            'When the warehouse operator attempts to perform "button_validate (验证出库)"',
            'Then the system must iterate through all linked stock.move (库存移动) records',
            'And verify that every linked stock.lot (库存批次) has "organic_badge_active (有机徽章激活)" set to True (为真)',
            'And raise a ValidationError (验证错误): "Unverified organic lot detected in moves (检测到发运移动中包含未验证的有机构成)" and block validation if any lot is unverified'
        ])

    def test_04_prohibited_synthetic_fertilizer_soil_audit_lockout(self):
        """
        Scenario: Prohibited Synthetic Fertilizer Soil Audit Lockout (禁用合成氮肥超标惩罚锁死)
        Given a certified organic crop parcel (已认证的有机作物地块) "PARCEL-ORG-A" under stock.location (库存位置)
        When an annual soil audit record under agri.organic.audit (农业有机审计) registers a soil synthetic nitrogen level (合成氮含量) of 0.08%, exceeding the threshold of 0.05%
        Then the system must transition the parcel's certification state to "suspended (已吊销)"
        And strip its organic badge for a mandatory 36-month recovery period (36个月强制恢复期)
        And raise a ValidationError (验证错误): "Parcel is suspended from organic operations (该地块已被暂停有机作业资质)" if a crop planting workorder of model mrp.workorder (工序工单) is scheduled as organic on this parcel
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a certified organic crop parcel (已认证的有机作物地块) "PARCEL-ORG-A" under stock.location (库存位置)',
            'When an annual soil audit record under agri.organic.audit (农业有机审计) registers a soil synthetic nitrogen level (合成氮含量) of 0.08%, exceeding the threshold of 0.05%',
            'Then the system must transition the parcel\'s certification state to "suspended (已吊销)"',
            'And strip its organic badge for a mandatory 36-month recovery period (36个月强制恢复期)',
            'And raise a ValidationError (验证错误): "Parcel is suspended from organic operations (该地块已被暂停有机作业资质)" if a crop planting workorder of model mrp.workorder (工序工单) is scheduled as organic on this parcel'
        ])

    def test_05_annual_organic_audit_expiration_block(self):
        """
        Scenario: Annual Organic Audit Expiration Block (年度有机审计超期自动降级)
        Given a certified organic cooperative farm partner (已认证的有机合作社农场伙伴) of model res.partner (业务伙伴)
        When their scheduled annual organic audit date passes without registration of a valid passing audit certificate of model agri.organic.audit (农业有机审计)
        Then the system must trigger a cron job (定时任务) that automatically shifts their partner organic state to "expired (已超期)"
        And block all premium organic labeling on outbound stock.picking (库存拣货) orders for their crop lots
        And force the shipping system to print conventional standard labels (常规普通标签) instead
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a certified organic cooperative farm partner (已认证的有机合作社农场伙伴) of model res.partner (业务伙伴)',
            'When their scheduled annual organic audit date passes without registration of a valid passing audit certificate of model agri.organic.audit (农业有机审计)',
            'Then the system must trigger a cron job (定时任务) that automatically shifts their partner organic state to "expired (已超期)"',
            'And block all premium organic labeling on outbound stock.picking (库存拣货) orders for their crop lots',
            'And force the shipping system to print conventional standard labels (常规普通标签) instead'
        ])

    def test_06_robotic_swarm_spraying_organic_boundary_gating(self):
        """
        Scenario: Robotic Swarm Spraying Organic Boundary Gating (智能喷洒机器人蜂群有机边界拦截)
        Given a robotic sprayer device (智能喷洒机器人设备) of model iiot.device (物联设备) executing a chemical spraying mission (化学品喷洒任务) "mrp.workorder" (作业任务)
        When the system's geofencing detection (地理围栏检测) registers the device entering an organic certified parcel buffer zone of model stock.location (库存位置)
        Then the system must automatically flag a chemical drift warning (化学品漂移警告)
        And command the robotic device (机器人设备) to instantly shut off spraying nozzles to protect organic certification
        And block the mission "mrp.workorder" (作业任务) state from transitioning to "done (完成)" under a ValidationError (验证错误): "Chemical spraying aborted due to organic boundary violation (因侵入有机边界，化学喷洒已中止)"
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a robotic sprayer device (智能喷洒机器人设备) of model iiot.device (物联设备) executing a chemical spraying mission (化学品喷洒任务) "mrp.workorder" (作业任务)',
            "When the system's geofencing detection (地理围栏检测) registers the device entering an organic certified parcel buffer zone of model stock.location (库存位置)",
            'Then the system must automatically flag a chemical drift warning (化学品漂移警告)',
            'And command the robotic device (机器人设备) to instantly shut off spraying nozzles to protect organic certification',
            'And block the mission "mrp.workorder" (作业任务) state from transitioning to "done (完成)" under a ValidationError (验证错误): "Chemical spraying aborted due to organic boundary violation (因侵入有机边界，化学喷洒已中止)"'
        ])

    def test_07_compliance_traceability_synthetics_prohibited_gating(self):
        """
        Scenario: Compliance Traceability Synthetics Prohibited Gating (合规营销标签及违禁化学添加物拦截机制)
        Given an organic crop lot registered in "product.template" (产品模板模型) with status "organic" (有机认证状态)
        When a dynamic laboratory chemical test logs a positive "prohibited_synthetics" (当实验检测到任何呈阳性的违禁化学添加物残留时)
        Then the brand compliance engine must automatically strip organic status on "agri.brand.marketing" (品牌合规引擎必须自动剥离该产品标签上的有机认证资格)
        And raise a ValidationError (并且系统抛出验证错误) with message "PROHIBITED_SYNTHETICS_DETECTED" (包含"检测到违禁化学物残留，降级销售"提示信息)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an organic crop lot registered in "product.template" (产品模板模型) with status "organic" (有机认证状态)',
            'When a dynamic laboratory chemical test logs a positive "prohibited_synthetics" (当实验检测到任何呈阳性的违禁化学添加物残留时)',
            'Then the brand compliance engine must automatically strip organic status on "agri.brand.marketing" (品牌合规引擎必须自动剥离该产品标签上的有机认证资格)',
            'And raise a ValidationError (并且系统抛出验证错误) with message "PROHIBITED_SYNTHETICS_DETECTED" (包含"检测到违禁化学物残留，降级销售"提示信息)'
        ])
