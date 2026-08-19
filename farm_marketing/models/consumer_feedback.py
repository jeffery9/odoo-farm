from odoo import models, fields, api, _

class FarmConsumerFeedback(models.Model):
    _name = 'farm.consumer.feedback'
    _description = 'Consumer C2M Feedback'
    _order = 'create_date desc'

    lot_id = fields.Many2one('stock.lot', string="Production Lot", required=True)
    product_id = fields.Many2one('product.template', related='lot_id.product_id', store=True)
    location_id = fields.Many2one('farm.location', string="Origin Parcel") # Derived from lot's production task
    
    # Feedback Data
    rating = fields.Selection([
        ('1', 'Poor'), ('2', 'Fair'), ('3', 'Good'), ('4', 'Great'), ('5', 'Excellent')
    ], string="Consumer Rating", required=True)
    
    taste_score = fields.Integer("Taste/Sweetness Score (1-10)")
    freshness_score = fields.Integer("Freshness Score (1-10)")
    comment = fields.Text("Consumer Comments")
    
    consumer_region = fields.Char("Consumer Region (City/Country)")
    
    # Link back to Production
    analysis_tag_ids = fields.Many2many('res.config.settings', 'farm_consumer_feedback_config_settings_rel', 'feedback_id', 'settings_id', string="Sentiment Tags") # Placeholder for AI sentiment

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # Auto-link location from lot's history
            if 'lot_id' in vals:
                lot = self.env['stock.lot'].browse(vals['lot_id'])
                # Mock: Find the location from the producing lot's linked tasks
                # (In real implementation, trace back through mrp.production)
                pass
        return super().create(vals_list)

class StockLot(models.Model):
    _inherit = 'stock.lot'

    feedback_ids = fields.One2many('farm.consumer.feedback', 'lot_id', string="Consumer Feedbacks")
    avg_consumer_rating = fields.Float("Avg Consumer Rating", compute='_compute_feedback_stats', store=True, precompute=True)

    @api.depends('feedback_ids.rating')
    def _compute_feedback_stats(self):
        for rec in self:
            ratings = [int(f.rating) for f in rec.feedback_ids]
            rec.avg_consumer_rating = sum(ratings) / len(ratings) if ratings else 0.0
