from odoo import models, fields, api, _

class FarmApicultureProduction(models.Model):
    _inherit = 'farm.apiculture.production'
    
    # [US-SCENARIO-29] Honey Batch Integrity
    bloom_period = fields.Char("Bloom Period (Nectar Source)")
    antibiotic_free_cert = fields.Boolean("Antibiotic-Free Certified", default=False)
    
    def action_extract_honey(self):
        self.ensure_one()
        # Mocking the creation of a honey batch
        lot = self.env['stock.lot'].create({
            'name': f"HONEY-{self.name}",
            'product_id': self.product_id.id,
            'company_id': self.env.company.id
        })
        
        # Link lab results if available
        qc_checks = self.env['agri.quality.check'].search([('production_id', '=', self.id)])
        anti_biotic_pass = any(qc.check_type == 'chemical' and qc.result == 'pass' for qc in qc_checks)
        
        if anti_biotic_pass:
            self.antibiotic_free_cert = True
            
        self.message_post(body=_("Extracted Honey Lot %s from %s bloom.") % (lot.name, self.bloom_period))
        return lot
