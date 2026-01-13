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
    
    # Pedigree [US-01-04, US-10-02]
    sire_id = fields.Many2one('stock.lot', string="Sire (父本)", domain="[('gender', '=', 'male')]")
    dam_id = fields.Many2one('stock.lot', string="Dam (母本)", domain="[('gender', '=', 'female')]")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Mixed/Unknown')], default='other')

    def get_ancestors(self, depth=5):
        """ 递归获取祖先 ID 集合 """
        ancestors = set()
        if depth <= 0:
            return ancestors
        
        parents = (self.sire_id | self.dam_id).filtered(lambda x: x)
        for p in parents:
            ancestors.add(p.id)
            ancestors.update(p.get_ancestors(depth - 1))
        return ancestors

    def check_inbreeding_risk(self, partner_lot, max_depth=3):
        """ 检查与配偶是否存在近亲风险 """
        self.ensure_one()
        my_ancestors = self.get_ancestors(max_depth)
        partner_ancestors = partner_lot.get_ancestors(max_depth)
        
        common = my_ancestors.intersection(partner_ancestors)
        if common:
            names = self.env['stock.lot'].browse(list(common)).mapped('name')
            return _("INBREEDING RISK: Common ancestors found within %s generations: %s") % (max_depth, ", ".join(names))
        return False

    @api.depends('trait_value_ids.score')
    def _compute_trait_score_avg(self):
        for lot in self:
            scores = lot.trait_value_ids.mapped('score')
            lot.trait_score_avg = sum(scores) / len(scores) if scores else 0.0

    def action_compare_traits(self):
        """ 弹出性状对比向导 [US-10-02] """
        return {
            'name': _('Trait Performance Comparison'),
            'type': 'ir.actions.act_window',
            'res_model': 'farm.trait.comparison.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_lot_ids': self.ids}
        }
