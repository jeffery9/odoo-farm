from odoo import models, fields, api, _

class FarmTraitComparisonWizard(models.TransientModel):
    _name = 'farm.trait.comparison.wizard'
    _description = 'Lot Trait Comparison Wizard'

    lot_ids = fields.Many2many('stock.lot', string="Lots to Compare")
    
    line_ids = fields.One2many('farm.trait.comparison.line', 'wizard_id', string="Comparison Results")

    @api.onchange('lot_ids')
    def _onchange_lot_ids(self):
        self.line_ids = [(5, 0, 0)]
        lines = []
        for lot in self.lot_ids:
            for trait in lot.trait_value_ids:
                lines.append((0, 0, {
                    'lot_id': lot.id,
                    'trait_name': trait.name,
                    'value': trait.value,
                    'score': trait.score
                }))
        self.line_ids = lines

class FarmTraitComparisonLine(models.TransientModel):
    _name = 'farm.trait.comparison.line'
    _description = 'Trait Comparison Line'

    wizard_id = fields.Many2one('farm.trait.comparison.wizard')
    lot_id = fields.Many2one('stock.lot', string="Lot")
    trait_name = fields.Char("Trait")
    value = fields.Char("Value")
    score = fields.Float("Score")
