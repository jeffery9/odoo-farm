from odoo import models, fields, api, _

class FarmHoneyTask(models.Model):
    _inherit = 'farm.honey.task'

    # [US-SCENARIO-29] Honey Batch Integrity
    bloom_period = fields.Char("Bloom Period (Nectar Source)")
    antibiotic_free_cert = fields.Boolean("Antibiotic-Free Certified", default=False)

    def action_extract_honey(self):
        self.ensure_one()
        # Mocking the creation of a honey batch
        lot = self.env['stock.lot'].create({
            'name': f"HONEY-{self.name}",
            'product_id': self.product_id.id,
            'company_id': self.company_id.id,
        })
        return lot
