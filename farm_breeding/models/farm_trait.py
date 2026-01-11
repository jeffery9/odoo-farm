from odoo import models, fields, api

class FarmTraitValue(models.Model):
    _name = 'farm.trait.value'
    _description = 'Breeding Trait Value'

    name = fields.Char("Trait Name", required=True) # e.g., Yield, Disease Resistance
    value = fields.Char("Measured Value") # e.g., 500kg, High
    score = fields.Float("Score (0-10)", help="Numeric score for comparison")
    
    lot_id = fields.Many2one('stock.lot', string="Lot/Asset", ondelete='cascade')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)

class FarmLotBreeding(models.Model):
    _inherit = 'stock.lot'

    trait_value_ids = fields.One2many('farm.trait.value', 'lot_id', string="Traits")
    trait_score_avg = fields.Float("Average Trait Score", compute='_compute_trait_score_avg', store=True)

    @api.depends('trait_value_ids.score')
    def _compute_trait_score_avg(self):
        for lot in self:
            scores = lot.trait_value_ids.mapped('score')
            lot.trait_score_avg = sum(scores) / len(scores) if scores else 0.0
