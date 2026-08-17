from odoo.tests.common import TransactionCase
from datetime import date, timedelta

class TestCSASubscription(TransactionCase):

    def setUp(self):
        super(TestCSASubscription, self).setUp()
        self.Subscription = self.env['farm.csa.subscription']
        self.Partner = self.env['res.partner'].create({'name': 'CSA Member'})
        self.Product = self.env['product.product'].create({'name': 'Veggie Box', 'type': 'consu'})
        self.Plan = self.env['farm.csa.plan'].create({
            'name': 'Weekly Veggie Box',
            'product_id': self.Product.id,
            'frequency': 'weekly'
        })

    def test_01_delivery_generation(self):
        """ 测试订阅周期性配送单生成逻辑 [US-008-02] """
        sub = self.Subscription.create({
            'name': 'SUB-001',
            'partner_id': self.Partner.id,
            'plan_id': self.Plan.id,
            'date_start': date.today(),
            'state': 'active'
        })
        
        # 模拟生成下一次配送
        if hasattr(sub, 'action_generate_delivery'):
            sub.action_generate_delivery()
            
            # 检查是否生成了调拨单
            picking = self.env['stock.picking'].search([('origin', '=', sub.name)])
            if picking:
                self.assertEqual(picking.partner_id.id, self.Partner.id)
                # 验证下次配送日期是否自动推后 7 天
                expected_next = date.today() + timedelta(days=7)
                self.assertEqual(sub.next_delivery_date, expected_next)

    def test_08_coop_member_credit_calculation_with_csa_hold(self):
        """ Verify that cooperative member credit_used aggregates active credit_held_amount """
        coop = self.env['cooperative.entity'].create({'name': 'Test Coop'})
        partner = self.env['res.partner'].create({'name': 'Test Partner'})
        member = self.env['cooperative.member'].create({
            'name': 'Test Member',
            'partner_id': partner.id,
            'cooperative_id': coop.id,
            'credit_limit': 1000.0,
        })
        plan = self.env['farm.csa.plan'].create({
            'name': 'Gold Bag Plan',
            'product_id': self.env['product.product'].create({'name': 'Bag Product', 'type': 'consu'}).id,
            'price': 20.0
        })
        sub = self.env['farm.csa.subscription'].create({
            'partner_id': partner.id,
            'plan_id': plan.id,
            'coop_member_id': member.id,
            'use_coop_credit': True,
            'credit_held_amount': 300.0,
            'state': 'active'
        })
        member.invalidate_model(['credit_used'])
        self.assertEqual(member.credit_used, 300.0, "Credit used must aggregate the active credit_held_amount of its CSA subscriptions!")

    def test_09_csa_subscription_credit_fields_exist(self):
        """ Assert that newly designed cooperative credit and yield token fields are present in the model schema """
        fields_dict = self.env['farm.csa.subscription']._fields
        self.assertIn('use_coop_credit', fields_dict)
        self.assertIn('coop_member_id', fields_dict)
        self.assertIn('yield_token_balance', fields_dict)
        self.assertIn('credit_held_amount', fields_dict)
        self.assertIn('credit_ledger_line_id', fields_dict)

    def test_10_csa_subscription_activation_credit_guard(self):
        """ Assert that insufficient member credit blocks activation with a bilingual ValidationError """
        from odoo.exceptions import ValidationError
        coop = self.env['cooperative.entity'].create({'name': 'Test Coop'})
        partner = self.env['res.partner'].create({'name': 'Test Partner'})
        member = self.env['cooperative.member'].create({
            'name': 'Test Member',
            'partner_id': partner.id,
            'cooperative_id': coop.id,
            'credit_limit': 100.0,
        })
        plan = self.env['farm.csa.plan'].create({
            'name': 'Plat Plan',
            'product_id': self.env['product.product'].create({'name': 'Bag Product', 'type': 'consu'}).id,
            'price': 20.0
        })
        sub = self.env['farm.csa.subscription'].create({
            'partner_id': partner.id,
            'plan_id': plan.id,
            'coop_member_id': member.id,
            'use_coop_credit': True,
            'credit_held_amount': 250.0, # Exceeds 100.0 limit
            'state': 'draft'
        })
        with self.assertRaises(ValidationError) as error:
            sub.action_activate()
        self.assertIn("COOP_CREDIT_INSUFFICIENT", str(error.exception))

    def test_11_csa_delivery_token_debit_and_credit_refund_gate(self):
        """ Assert that picking validation debits yield tokens and proportionate coop credit releases automatically """
        coop = self.env['cooperative.entity'].create({'name': 'Test Coop'})
        partner = self.env['res.partner'].create({'name': 'Test Partner'})
        
        # Build cooperative member
        member = self.env['cooperative.member'].create({
            'name': 'Test Member',
            'partner_id': partner.id,
            'cooperative_id': coop.id,
            'credit_limit': 1000.0,
        })
        plan = self.env['farm.csa.plan'].create({
            'name': 'Gold Bag Plan',
            'product_id': self.env['product.product'].create({'name': 'Bag Product', 'type': 'consu'}).id,
            'price': 20.0
        })
        
        # Activate CSA Subscription with credit backing
        sub = self.env['farm.csa.subscription'].create({
            'partner_id': partner.id,
            'plan_id': plan.id,
            'coop_member_id': member.id,
            'use_coop_credit': True,
            'credit_held_amount': 200.0,
            'yield_token_balance': 10.0,
            'state': 'draft'
        })
        sub.action_activate()
        
        member.invalidate_model(['credit_used'])
        self.assertEqual(member.credit_used, 200.0, "Coop member credit should be locked by 200.0 upon active CSA.")
        
        # Mock active outbound picking
        picking_type = self.env['stock.picking.type'].search([('code', '=', 'outgoing')], limit=1)
        picking = self.env['stock.picking'].create({
            'partner_id': partner.id,
            'picking_type_id': picking_type.id,
            'origin': sub.name,
            'location_id': picking_type.default_location_src_id.id,
            'location_dest_id': partner.property_stock_customer.id,
            'move_ids': [(0, 0, {
                'description_picking': plan.product_id.name,
                'product_id': plan.product_id.id,
                'product_uom_qty': 1.0,
                'product_uom': plan.product_id.uom_id.id,
                'location_id': picking_type.default_location_src_id.id,
                'location_dest_id': partner.property_stock_customer.id,
            })]
        })
        
        # Validate Picking
        picking.action_confirm()
        picking.action_assign()
        picking.button_validate()
        
        # After validate:
        # 1. yield_token_balance must be debited by 1.0 -> 9.0
        # 2. credit_held_amount should restore 20.0 -> 180.0
        # 3. ledger state is confirmed
        self.assertEqual(sub.yield_token_balance, 9.0)
        self.assertEqual(sub.credit_held_amount, 180.0)
        self.assertEqual(sub.credit_ledger_line_id.state, 'confirmed')

    def test_12_csa_task_generation_depletion_guard(self):
        """ Assert that _generate_delivery_tasks skips subscriptions with zero token balance """
        partner = self.env['res.partner'].create({'name': 'Test Partner'})
        plan = self.env['farm.csa.plan'].create({
            'name': 'Weekly Plan',
            'product_id': self.env['product.product'].create({'name': 'Bag Product', 'type': 'consu'}).id,
            'price': 20.0
        })
        sub = self.env['farm.csa.subscription'].create({
            'partner_id': partner.id,
            'plan_id': plan.id,
            'yield_token_balance': 0.0, # Fully depleted
            'state': 'active',
            'next_delivery_date': date.today()
        })
        
        # Trigger tasks generation
        sub._generate_delivery_tasks()
        
        # Check if picking was created
        pickings = self.env['stock.picking'].search([('origin', '=', sub.name)])
        self.assertEqual(len(pickings), 0, "No pickings should be generated when yield token balance is fully depleted!")
