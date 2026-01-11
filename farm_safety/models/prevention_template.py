from odoo import models, fields, api

class FarmPreventionTemplate(models.Model):
    _name = 'farm.prevention.template'
    _description = 'Agri-Prevention Template'

    name = fields.Char("Template Name", required=True)
    active = fields.Boolean(default=True)
    line_ids = fields.One2many('farm.prevention.line', 'template_id', string="Operations")
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)

class FarmPreventionLine(models.Model):
    _name = 'farm.prevention.line'
    _description = 'Prevention Operation Line'
    _order = 'delay_days asc'

    template_id = fields.Many2one('farm.prevention.template', ondelete='cascade')
    name = fields.Char("Operation Name", required=True)
    delay_days = fields.Integer("Delay Days (T+N)", default=0, help="Days after task start to perform this operation.")
    
    # 预设投入品（可选）
    product_id = fields.Many2one('product.product', string="Vaccine/Medicine", help="Predefined input for this operation.")
    qty = fields.Float("Quantity", default=1.0)

class FarmLotQuarantine(models.Model):
    _inherit = 'stock.lot'

    is_quarantined = fields.Boolean("In Quarantine (隔离中)", default=False, tracking=True)
    quarantine_reason = fields.Text("Quarantine Reason")
    quarantine_start_date = fields.Date("Quarantine Start")

    def action_quarantine(self, reason):
        self.write({
            'is_quarantined': True,
            'quarantine_reason': reason,
            'quarantine_start_date': fields.Date.today()
        })
        self.message_post(body=_("BIO-SAFETY ALERT: Asset put into quarantine. Reason: %s") % reason)

    def action_release_quarantine(self):
        self.write({'is_quarantined': False})
        self.message_post(body=_("BIO-SAFETY: Asset released from quarantine."))

class StockPickingQuarantine(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        """ 隔离拦截逻辑 [US-34] """
        for picking in self:
            for move in picking.move_ids:
                for lot in move.lot_ids:
                    if lot.is_quarantined:
                        from odoo.exceptions import UserError
                        raise UserError(_("BIO-SAFETY BLOCK: Lot %s is currently in QUARANTINE. No movement or sale is allowed!") % lot.name)
        return super().button_validate()
