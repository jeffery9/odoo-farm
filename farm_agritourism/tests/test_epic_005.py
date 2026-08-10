# -*- coding: utf-8 -*-
from odoo.addons.farm_core.tests.bdd_base import BddTransactionCase
from odoo.exceptions import UserError, ValidationError

class TestEpic005(BddTransactionCase):
    """ BDD Test Suite for Epic 005: Epic 005 Agritourism & Experience """

    def setUp(self):
        super(TestEpic005, self).setUp()

    def test_01_picking_garden_activity_booking_and_checkin(self):
        """
        Scenario: Picking garden activity booking and check-in
        Given I am a tourist on the farm portal
        And the portal is in "Dual-language" mode
        When I book a picking activity
        Then the system should generate a QR code for check-in
        And when the QR code is scanned, the "action_checkin" must be triggered successfully
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given I am a tourist on the farm portal',
            'And the portal is in "Dual-language" mode',
            'When I book a picking activity',
            'Then the system should generate a QR code for check-in',
            'And when the QR code is scanned, the "action_checkin" must be triggered successfully'
        ])

    def test_02_picktosale_integration(self):
        """
        Scenario: "Pick-to-Sale" integration
        Given I am a farm owner
        And a sales order is created for a picking activity
        When the sales order is confirmed and a lot or parcel is specified
        Then the system must automatically reserve the stock via "stock.move.line"
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given I am a farm owner',
            'And a sales order is created for a picking activity',
            'When the sales order is confirmed and a lot or parcel is specified',
            'Then the system must automatically reserve the stock via "stock.move.line"'
        ])

    def test_03_interactive_diy_workshop_capacity_gating(self):
        """
        Scenario: Interactive DIY Workshop Capacity Gating
        Given a sales order line representing a farm experiential activity booking
        And a configured workstation daily capacity in model "mrp.workcenter"
        When the total registered visitor count exceeds the workstation's daily capacity
        Then confirming the sales order must raise a ValidationError for over-capacity
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a sales order line representing a farm experiential activity booking',
            'And a configured workstation daily capacity in model "mrp.workcenter"',
            'When the total registered visitor count exceeds the workstation's daily capacity',
            'Then confirming the sales order must raise a ValidationError for over-capacity'
        ])

    def test_04_farm_booking_daily_cap_limits(self):
        """
        Scenario: Farm Booking Daily Cap Limits
        Given a farm visit or lodging reservation using model "sale.order" with "agri.tourism.booking"
        And a maximum daily guest limit configured for the target date
        When I attempt to confirm a booking that pushes the total guest count above the daily limit
        Then the system must block the booking confirmation with a ValidationError of cap limits exceeded
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a farm visit or lodging reservation using model "sale.order" with "agri.tourism.booking"',
            'And a maximum daily guest limit configured for the target date',
            'When I attempt to confirm a booking that pushes the total guest count above the daily limit',
            'Then the system must block the booking confirmation with a ValidationError of cap limits exceeded'
        ])

    def test_05_booking_transaction_savepoint_rollback(self):
        """
        Scenario: Booking Transaction Savepoint Rollback (景区体验预订事务保存点回滚安全防呆拦截机制)
        Given a customer booking represented by a sales order in "sale.order" (销售订单模型)
        And an automated draft invoice generated in "account.move" (会计分录模型)
        When the system creates a database checkpoint using "cr.savepoint" (当系统通过事务保存点创建数据库检查点时)
        And the reservation of experiential slots fails due to concurrent booking conflicts (且体验项目配额由于高并发预订冲突导致锁定失败时)
        Then the system must execute rollback to the designated "cr.savepoint" (系统必须强制执行事务回滚到指定的事务保存点)
        And raise a UserError (并且抛出用户错误) with message "Booking transaction failed, draft reverted" (包含"预订事务处理失败，草稿发票已回滚"提示信息)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a customer booking represented by a sales order in "sale.order" (销售订单模型)',
            'And an automated draft invoice generated in "account.move" (会计分录模型)',
            'When the system creates a database checkpoint using "cr.savepoint" (当系统通过事务保存点创建数据库检查点时)',
            'And the reservation of experiential slots fails due to concurrent booking conflicts (且体验项目配额由于高并发预订冲突导致锁定失败时)',
            'Then the system must execute rollback to the designated "cr.savepoint" (系统必须强制执行事务回滚到指定的事务保存点)',
            'And raise a UserError (并且抛出用户错误) with message "Booking transaction failed, draft reverted" (包含"预订事务处理失败，草稿发票已回滚"提示信息)'
        ])

    def test_06_compliance_traceability_synthetics_prohibited_gating(self):
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
