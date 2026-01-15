from odoo import models, fields, api, _

class FarmScLicense(models.Model):
    _name = 'farm.sc.license'
    _description = 'Food Production License (SC)'

    name = fields.Char("License No.", required=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    expiry_date = fields.Date("Expiry Date", required=True)
    category_ids = fields.Many2many('farm.sc.category', string="Permitted Categories")
    is_active = fields.Boolean("Is Active", compute='_compute_is_active', store=True)

    @api.depends('expiry_date')
    def _compute_is_active(self):
        today = fields.Date.today()
        for rec in self:
            rec.is_active = rec.expiry_date and rec.expiry_date >= today

class FarmScCategory(models.Model):
    _name = 'farm.sc.category'
    _description = 'Food Production Category'

    name = fields.Char("Category Name", required=True)
    code = fields.Char("Category Code")
