# -*- coding: utf-8 -*-
from odoo.addons.farm_core.tests.bdd_base import BddTransactionCase
from odoo.exceptions import UserError, ValidationError

class TestEpic040(BddTransactionCase):
    """ BDD Test Suite for Epic 040: Epic 040 Advanced Industry & Compliance """

    def setUp(self):
        super(TestEpic040, self).setUp()

    def test_01_export_destination_chemical_pesticide_maximum_residue_limit_mrl_checks(self):
        """
        Scenario: Export destination chemical pesticide maximum residue limit (MRL) checks
        Given a sales order "SO-2026-EXP-01" with destination country "Japan" (JP)
        And the order is linked to fresh apple lot "APP-LOT-Picual-09"
        When the Japan compliance audit engine is executed for pesticide residue maximum limits
        And the lot's lab results show Acetamiprid concentration of 0.25 mg/kg (exceeding Japan's limit of 0.1 mg/kg, though below local limit of 0.5 mg/kg)
        Then the system must block the sales order confirmation
        And raise a compliance validation warning "EXPORT_MRL_LIMIT_EXCEEDED" (检测到日本农残最大限量超标，严禁出口该批次)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a sales order "SO-2026-EXP-01" with destination country "Japan" (JP)',
            'And the order is linked to fresh apple lot "APP-LOT-Picual-09"',
            'When the Japan compliance audit engine is executed for pesticide residue maximum limits',
            'And the lot's lab results show Acetamiprid concentration of 0.25 mg/kg (exceeding Japan's limit of 0.1 mg/kg, though below local limit of 0.5 mg/kg)',
            'Then the system must block the sales order confirmation',
            'And raise a compliance validation warning "EXPORT_MRL_LIMIT_EXCEEDED" (检测到日本农残最大限量超标，严禁出口该批次)'
        ])

    def test_02_exportimport_customs_phytosanitary_certificate_validation_block(self):
        """
        Scenario: Export-import customs phytosanitary certificate validation block
        Given an international shipping "stock.picking" to export premium seed lot "SEED-EXP-99" to the European Union (EU)
        And the customs compliance engine "agri.compliance.engine" is tracking the required documentation
        When the warehouse operator attempts to validate the shipping delivery
        And the mandatory phytosanitary certificate (植物检疫证书) is either missing, expired, or unlinked in Odoo attachments
        Then the system must block the validation departure with state "Customs Blocked"
        And raise a UserError with message "CUSTOMS_PHYTOSANITARY_CERT_REQUIRED" (缺失有效的出口植物检疫证书，发货已被拦截)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an international shipping "stock.picking" to export premium seed lot "SEED-EXP-99" to the European Union (EU)',
            'And the customs compliance engine "agri.compliance.engine" is tracking the required documentation',
            'When the warehouse operator attempts to validate the shipping delivery',
            'And the mandatory phytosanitary certificate (植物检疫证书) is either missing, expired, or unlinked in Odoo attachments',
            'Then the system must block the validation departure with state "Customs Blocked"',
            'And raise a UserError with message "CUSTOMS_PHYTOSANITARY_CERT_REQUIRED" (缺失有效的出口植物检疫证书，发货已被拦截)'
        ])

    def test_03_workstation_continuous_compliance_violations_automatically_updating_company_esg_risk_index(self):
        """
        Scenario: Workstation continuous compliance violations automatically updating company ESG risk index
        Given a farm processing workstation "Milling Station Alpha" under active regulation audit
        And the company's baseline ESG sustainability risk index is recorded as "95.0"
        When a supervisor logs a critical non-compliance violation (e.g., unauthorized chemical input dumping)
        Then the system must generate a continuous compliance audit log in "agri.compliance.engine"
        And automatically decrease the company's global ESG sustainability risk index to "82.5"
        And dispatch a high-priority remediation task to the compliance supervisor's Odoo dashboard
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a farm processing workstation "Milling Station Alpha" under active regulation audit',
            'And the company's baseline ESG sustainability risk index is recorded as "95.0"',
            'When a supervisor logs a critical non-compliance violation (e.g., unauthorized chemical input dumping)',
            'Then the system must generate a continuous compliance audit log in "agri.compliance.engine"',
            'And automatically decrease the company's global ESG sustainability risk index to "82.5"',
            'And dispatch a high-priority remediation task to the compliance supervisor's Odoo dashboard'
        ])

    def test_04_water_reservoir_security_unauthorized_tampering_and_automated_inlet_valve_shutdown(self):
        """
        Scenario: Water reservoir security unauthorized tampering and automated inlet valve shutdown
        Given a bulk water reservoir location "Main Reservoir A" feeding livestock barns
        And an active food defense monitoring system connected via IoT security gateways
        When the reservoir fence infrared or physical hatch sensor registers an unauthorized access tampers signature
        Then the system must atomically trigger a physical emergency shutdown of the water inlet valves
        And lock the outbound irrigation "mrp.workorder" records
        And trigger a loud security alarm siren and send immediate high-priority SMS alerts to the security director
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a bulk water reservoir location "Main Reservoir A" feeding livestock barns',
            'And an active food defense monitoring system connected via IoT security gateways',
            'When the reservoir fence infrared or physical hatch sensor registers an unauthorized access tampers signature',
            'Then the system must atomically trigger a physical emergency shutdown of the water inlet valves',
            'And lock the outbound irrigation "mrp.workorder" records',
            'And trigger a loud security alarm siren and send immediate high-priority SMS alerts to the security director'
        ])

    def test_05_geographical_indication_gi_boundary_coordinate_polygon_checks_and_label_lock(self):
        """
        Scenario: Geographical Indication (GI) boundary coordinate polygon checks and label lock
        Given a premium ham lot "HAM-GI-2026-05" which is marketed under the Geographical Indication "Parma Ham" (帕尔玛火腿 / Parma Ham)
        And the legal GI boundary is defined as a coordinate polygon in Odoo's GIS mapping system
        When the lot's raw agricultural material harvesting location coordinates "31.2304, 121.4737" are checked against the GI boundary coordinates
        And the coordinates are found to reside outside the legally designated GI boundary coordinates polygon
        Then the system must lock all Geographical Indication label and barcode printing for this lot
        And raise a ValidationError with message "GEOGRAPHICAL_INDICATION_BOUNDARY_VIOLATION" (原材料非地理标志保护产区，严禁打印地理标志专用标签)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a premium ham lot "HAM-GI-2026-05" which is marketed under the Geographical Indication "Parma Ham" (帕尔玛火腿 / Parma Ham)',
            'And the legal GI boundary is defined as a coordinate polygon in Odoo's GIS mapping system',
            'When the lot's raw agricultural material harvesting location coordinates "31.2304, 121.4737" are checked against the GI boundary coordinates',
            'And the coordinates are found to reside outside the legally designated GI boundary coordinates polygon',
            'Then the system must lock all Geographical Indication label and barcode printing for this lot',
            'And raise a ValidationError with message "GEOGRAPHICAL_INDICATION_BOUNDARY_VIOLATION" (原材料非地理标志保护产区，严禁打印地理标志专用标签)'
        ])

    def test_06_water_reservoir_security_sensor_gateway_loss_and_emergency_physical_lock_actuation(self):
        """
        Scenario: Water Reservoir Security Sensor Gateway Loss and Emergency physical Lock Actuation
        Given a bulk water reservoir location under surveillance by Odoo's food defense engine "agri.compliance.engine" (合规审计引擎)
        And the security gate lock status is "Locked" (锁定)
        When the infrared boundary sensor gateway crashes and loses power during a high-alert security period
        Then the system must atomically trigger a physical fail-safe mechanical bolt actuator to lock the water outflow valves to "Closed" (关闭)
        And lock all active irrigation missions "mrp.workorder" [mrp.workorder] (作业任务) associated with this reservoir
        And flag the reservoir water source status in "stock.quant" (商品库存) as "Untrusted" (安全受疑)
        And raise a "ValidationError" (验证错误) requiring an in-person physical biosecurity audit sign-off to restore water flow
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a bulk water reservoir location under surveillance by Odoo's food defense engine "agri.compliance.engine" (合规审计引擎)',
            'And the security gate lock status is "Locked" (锁定)',
            'When the infrared boundary sensor gateway crashes and loses power during a high-alert security period',
            'Then the system must atomically trigger a physical fail-safe mechanical bolt actuator to lock the water outflow valves to "Closed" (关闭)',
            'And lock all active irrigation missions "mrp.workorder" [mrp.workorder] (作业任务) associated with this reservoir',
            'And flag the reservoir water source status in "stock.quant" (商品库存) as "Untrusted" (安全受疑)',
            'And raise a "ValidationError" (验证错误) requiring an in-person physical biosecurity audit sign-off to restore water flow'
        ])

    def test_07_core_registration_concurrency_bypass_check(self):
        """
        Scenario: Core Registration Concurrency Bypass Check (核心主数据并发注册绕过防御机制)
        Given a system configuration in "res.partner" (核心注册配置模型) with status "active" (活跃状态)
        And a registration lock "concurrency_lock" is set to "locked" (并且并发锁状态字段值设置为已锁定状态)
        When another system administrator attempts to write (当另一位系统管理员尝试写入数据时)
        Then the ORM registry must block the write action and raise a UserError (注册表必须拦截写入动作并抛出用户错误) with message "REGISTRY_LOCK_ACTIVE" (包含"注册表已被并发锁定"提示信息)
        And execute rollback (并且系统必须执行事务回滚) to restore physical state integrity (以恢复物理状态完整性)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a system configuration in "res.partner" (核心注册配置模型) with status "active" (活跃状态)',
            'And a registration lock "concurrency_lock" is set to "locked" (并且并发锁状态字段值设置为已锁定状态)',
            'When another system administrator attempts to write (当另一位系统管理员尝试写入数据时)',
            'Then the ORM registry must block the write action and raise a UserError (注册表必须拦截写入动作并抛出用户错误) with message "REGISTRY_LOCK_ACTIVE" (包含"注册表已被并发锁定"提示信息)',
            'And execute rollback (并且系统必须执行事务回滚) to restore physical state integrity (以恢复物理状态完整性)'
        ])
