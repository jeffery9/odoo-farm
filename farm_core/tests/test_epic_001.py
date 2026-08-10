# -*- coding: utf-8 -*-
from odoo.addons.farm_core.tests.bdd_base import BddTransactionCase
from odoo.exceptions import UserError, ValidationError

class TestEpic001(BddTransactionCase):
    """ BDD Test Suite for Epic 001: Epic 001 Agricultural Master Data """

    def setUp(self):
        super(TestEpic001, self).setUp()

    def test_01_multiformat_activity_classification(self):
        """
        Scenario: Multi-format activity classification
        Given I am a farm manager
        And the system supports "Planting", "Livestock", and "Aquaculture" activity families
        When I create a new project of family "Planting"
        Then the project should have a sequence starting with "P"
        And the UI should display specific properties for "Planting"
        And if I create a new project of family "Livestock"
        Then the project should have a sequence starting with "L"
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given I am a farm manager',
            'And the system supports "Planting", "Livestock", and "Aquaculture" activity families',
            'When I create a new project of family "Planting"',
            'Then the project should have a sequence starting with "P"',
            'And the UI should display specific properties for "Planting"',
            'And if I create a new project of family "Livestock"',
            'Then the project should have a sequence starting with "L"'
        ])

    def test_02_land_parcel_boundary_verification(self):
        """
        Scenario: Land parcel boundary verification
        Given a parcel location "Location-A" registered on model "stock.location"
        And a configured polygon boundary of GeoJSON coordinates on the "stock.location" record
        When I record a soil moisture event at coordinates "gps_lat: 34.0522" and "gps_lng: -118.2437"
        Then the system must check whether the GPS point is inside the parcel polygon
        And if it is outside, raise a ValidationError blocking the record
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a parcel location "Location-A" registered on model "stock.location"',
            'And a configured polygon boundary of GeoJSON coordinates on the "stock.location" record',
            'When I record a soil moisture event at coordinates "gps_lat: 34.0522" and "gps_lng: -118.2437"',
            'Then the system must check whether the GPS point is inside the parcel polygon',
            'And if it is outside, raise a ValidationError blocking the record'
        ])

    def test_03_parentchild_cycle_pedigree_prevention(self):
        """
        Scenario: Parent-child cycle pedigree prevention
        Given a biological asset lot "Piglet-01" of model "stock.lot" linked to "agri.biological.asset"
        When I attempt to update its parent lineage, setting its "father_id" to "Piglet-01"
        Then the ORM must raise a ValidationError preventing recursive self-inheritance
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a biological asset lot "Piglet-01" of model "stock.lot" linked to "agri.biological.asset"',
            'When I attempt to update its parent lineage, setting its "father_id" to "Piglet-01"',
            'Then the ORM must raise a ValidationError preventing recursive self-inheritance'
        ])

    def test_04_sales_gating_for_noncommercial_breeding_stock(self):
        """
        Scenario: Sales gating for non-commercial breeding stock
        Given a biological product lot with breeding generation "G1" on model "stock.lot"
        When a sales order line is confirmed for this product
        Then the system must validate the "agri_generation" of all lines
        And if it is a non-commercial generation, raise a ValidationError blocking the order
        And create an administrative review task activity for the "Compliance Manager"
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a biological product lot with breeding generation "G1" on model "stock.lot"',
            'When a sales order line is confirmed for this product',
            'Then the system must validate the "agri_generation" of all lines',
            'And if it is a non-commercial generation, raise a ValidationError blocking the order',
            'And create an administrative review task activity for the "Compliance Manager"'
        ])

    def test_05_concurrent_master_data_registration_lock(self):
        """
        Scenario: Concurrent Master Data Registration Lock (主数据并发注册锁安全保护机制)
        Given a farm owner registers a new vendor in "res.partner" (合作伙伴模型)
        And the database activates an registration lock on "concurrency.lock" (并发锁模型) with status "locked" (已锁定状态)
        When another administrator attempts to register a vendor with the identical tax identifier (当另一位管理员尝试注册具有相同纳税人识别号的供应商时)
        Then the ORM must raise a UserError (系统必须抛出用户错误) with message "CONCURRENT_REGISTRATION" (包含"并发注册冲突"提示信息)
        And the transaction must execute rollback (并且系统必须执行事务回滚) to prevent duplicate records (以防止生成重复的供应商记录)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a farm owner registers a new vendor in "res.partner" (合作伙伴模型)',
            'And the database activates an registration lock on "concurrency.lock" (并发锁模型) with status "locked" (已锁定状态)',
            'When another administrator attempts to register a vendor with the identical tax identifier (当另一位管理员尝试注册具有相同纳税人识别号的供应商时)',
            'Then the ORM must raise a UserError (系统必须抛出用户错误) with message "CONCURRENT_REGISTRATION" (包含"并发注册冲突"提示信息)',
            'And the transaction must execute rollback (并且系统必须执行事务回滚) to prevent duplicate records (以防止生成重复的供应商记录)'
        ])

    def test_06_core_registration_concurrency_bypass_check(self):
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
