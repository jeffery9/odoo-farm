from odoo import models, fields

class StockLotExtensionBreeding(models.Model):    _inherit = 'stock.lot'
    
    father_id = fields.Many2one('stock.lot', string="Father")
    mother_id = fields.Many2one('stock.lot', string="Mother")
    trait_score_avg = fields.Selection([('0', 'Low'), ('1', 'Normal'), ('2', 'High'), ('3', 'Excellent')], string="Average Trait Score")
    trait_value_ids = fields.One2many('farm.trait.value', 'lot_id', string="Traits")
