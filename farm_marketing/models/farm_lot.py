from odoo import models, fields, api, _

class FarmPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    loyalty_points = fields.Float("Farm Loyalty Points", default=0.0)

class FarmSaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'

    # 预订模式 [Order Enhancement]
    is_preorder = fields.Boolean("Pre-order Reservation", help="Check to lock lots before confirmation.")
    reservation_expiry = fields.Datetime("Reservation Expiry")

    # 跨境合规 [US-040-06]
    export_country_id = fields.Many2one('res.country', string="Export Destination")
    is_export_compliant = fields.Boolean("Export Compliant", compute='_compute_export_compliance', store=True, precompute=True)

    @api.depends('export_country_id', 'order_line.product_id')
    def _compute_export_compliance(self):
        for order in self:
            if not order.export_country_id:
                order.is_export_compliant = True 
                continue
            # 简化的合规逻辑
            order.is_export_compliant = True

    def action_confirm(self):
        # 增加合规与锁定逻辑
        for order in self:
            if order.export_country_id and not order.is_export_compliant:
                from odoo.exceptions import UserError
                raise UserError(_("EXPORT BLOCK: Order contains products not compliant with %s regulations.") % order.export_country_id.name)
            
            # US-062-03: Channel Protection Whitelist check
            for line in order.order_line:
                if line.lot_id and line.lot_id.is_premium_brand:
                    if order.partner_id not in line.lot_id.allowed_partner_ids:
                        from odoo.exceptions import UserError
                        raise UserError(_("CHANNEL PROTECTION: Lot %s is reserved for premium channels. Customer %s is not in the whitelist!") % (line.lot_id.name, order.partner_id.name))
                
                # Quality Matching: Ensure lot meets line requirements
                if line.lot_id and line.required_integrity_score > 0:
                    if line.lot_id.integrity_score < line.required_integrity_score:
                        from odoo.exceptions import UserError
                        raise UserError(_("QUALITY MISMATCH: Lot %s score (%s) is below required %s.") % (line.lot_id.name, line.lot_id.integrity_score, line.required_integrity_score))

        res = super(FarmSaleOrder, self).action_confirm()
        for order in self:
            # 简单规则：1元 = 1分
            points = order.amount_total
            order.partner_id.loyalty_points += points
            order.message_post(body=_("LOYALTY: %s points added to customer.") % points)
        return res

class FarmSaleOrderLine(models.Model):
    _name = 'sale.order.line'
    _inherit = 'sale.order.line'

    lot_id = fields.Many2one('stock.lot', string="Reserved Lot") 
    required_integrity_score = fields.Float("Required Integrity", default=0.0)
    
    is_reserved = fields.Boolean("Is Locked", compute='_compute_reservation_status')

    def _compute_reservation_status(self):
        for line in self:
            line.is_reserved = bool(line.lot_id)

    def action_view_traceability(self):
        """ 跳转到该行关联批次的外部溯源页面 """
        self.ensure_one()
        # 寻找已分配的批次
        move = self.move_ids.filtered(lambda m: m.state == 'done')
        lot = self.lot_id or move.lot_ids[:1]
        if lot:
            return {
                'type': 'ir.actions.act_url',
                'url': lot.traceability_url,
                'target': 'new',
            }
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('No Lot Assigned'),
                'message': _('Traceability is available after delivery confirmation.'),
                'type': 'warning',
            }
        }

class FarmLotMarketing(models.Model):
    _name = 'stock.lot'
    _inherit = 'stock.lot'

    traceability_url = fields.Char("Traceability URL", compute='_compute_traceability_url')
    
    # US-062-03: Channel Protection
    is_premium_brand = fields.Boolean("Premium Brand Lot", default=False)
    allowed_partner_ids = fields.Many2many('res.partner', string="Allowed Premium Channels")

    # Formula: Integrity = (Base Score from QC) * Entity Multiplier
    integrity_score = fields.Float("Organic Integrity Score", compute='_compute_integrity_score', store=True, precompute=True)

    def _compute_integrity_score(self):
        for lot in self:
            # 1. Base Score calculation (from QC and inputs)
            geofence_compliance = 100.0 if lot.quality_status == 'healthy' else 80.0
            input_whitelist_rate = 100.0 if lot.quality_status == 'passed' else 70.0
            qc_pass_rate = 100.0 if lot.quality_status == 'passed' else 0.0
            
            base_score = (geofence_compliance * 0.4) + (input_whitelist_rate * 0.4) + (qc_pass_rate * 0.2)
            
            # 2. Entity Trust Multiplier [US-TECH-DNA-07]
            # Compliant = 1.0, Warning = 0.8, Non-compliant = 0.5
            multiplier = 1.0
            status = getattr(lot, 'entity_audit_status', 'compliant')
            if status == 'warning': multiplier = 0.8
            elif status == 'non_compliant': multiplier = 0.5
            
            final_score = base_score * multiplier
            lot.integrity_score = final_score
            
            if final_score < 60.0:
                lot.activity_schedule(
                    'mail.mail_activity_data_todo',
                    summary=_('Integrity Warning: Low Score (%s)') % final_score,
                    note=_('Lot %s has an integrity score below 60. Please investigate immediately.') % lot.name,
                    user_id=self.env.user.id # Should be quality manager
                )

    # Marketing Content [US-008-01]
    story_title = fields.Char("Growth Story Title")
    story_content = fields.Html("Growth Story Content")
    marketing_image_ids = fields.Many2many('ir.attachment', relation='stock_lot_marketing_image_rel', column1='lot_id', column2='attachment_id', string="Marketing Photos")
    
    # 溯源面板显示的指标快照
    avg_temp = fields.Float("Average Growth Temperature (℃)")
    water_purity = fields.Char("Water Purity Grade")

    # Expiry & Promotion [US-037-14]
    is_near_expiry = fields.Boolean('Near Expiry', compute='_compute_is_near_expiry')
    promotion_link_id = fields.Many2one('loyalty.program', string="Promotion Program", 
                                       help="Link to a promotion for clearing near-expiry stock")

    def _compute_is_near_expiry(self):
        today = fields.Date.today()
        for lot in self:
            if lot.expiration_date:
                delta = lot.expiration_date - today
                lot.is_near_expiry = 0 <= delta.days <= 7
            else:
                lot.is_near_expiry = False

    def get_full_traceability_data(self):
        """
        核心溯源算法：聚合该批次从种子到餐桌的全生命周期数据 [US-038-03, US-008-01]
        """
        self.ensure_one()
        
        # 1. 寻找生产来源 (Harvest MO)
        production = self.env['mrp.production'].search([('lot_producing_id', '=', self.id)], limit=1)
        task = production.agri_task_id
        
        data = {
            'lot_name': self.name,
            'product': self.product_id.display_name,
            'harvest_date': self.create_date,
            'plot': task.land_parcel_id.name if task else _('Unknown'),
            'gis': {'lat': task.gps_lat, 'lng': task.gps_lng} if task else False,
            'interventions': [],
            'inputs': [],
            'processing_history': []
        }

        if task:
            # 2. 任务下的所有农事干预
            for op in task.intervention_ids.sorted('date_finished'):
                data['interventions'].append({
                    'type': op.intervention_type,
                    'date': op.date_finished,
                    'worker': ", ".join(op.doer_ids.mapped('name')),
                    'procedure': op.procedure_name or op.name
                })
                # 3. 聚合投入品
                for move in op.move_raw_ids:
                    data['inputs'].append({
                        'product': move.product_id.name,
                        'qty': move.product_uom_qty,
                        'uom': move.product_uom.name,
                        'is_organic': move.product_id.is_safety_approved
                    })

        # 4. 追溯加工环节
        current_lot = self
        while current_lot.parent_lot_id:
            parent = current_lot.parent_lot_id
            proc_mo = self.env['mrp.production'].search([('lot_producing_id', '=', current_lot.id)], limit=1)
            data['processing_history'].append({
                'stage': _('Processing from %s') % parent.name,
                'mo': proc_mo.name if proc_mo else 'Manual',
                'date': current_lot.create_date
            })
            current_lot = parent

        return data

    def _compute_traceability_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for lot in self:
            lot.traceability_url = f"{base_url}/farm/trace/{lot.name}"

    def action_view_traceability(self):
        return True
