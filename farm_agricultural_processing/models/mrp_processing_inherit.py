from odoo import models, fields, api, _

class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    sc_category_id = fields.Many2one('farm.sc.category', string="SC Category")

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    def action_confirm(self):
        """ [US-14-21] SC Range Check for industry specific requirements """
        for mo in self:
            if mo.bom_id and mo.bom_id.sc_category_id:
                license = self.env['farm.sc.license'].search([
                    ('company_id', '=', mo.company_id.id),
                    ('is_active', '=', True),
                    ('category_ids', 'in', mo.bom_id.sc_category_id.id)
                ], limit=1)
                if not license:
                    from odoo.exceptions import UserError
                    raise UserError(_("SC COMPLIANCE ERROR: Company does not have a valid SC license for category '%s'!") % mo.bom_id.sc_category_id.name)
        return super(MrpProduction, self).action_confirm()
