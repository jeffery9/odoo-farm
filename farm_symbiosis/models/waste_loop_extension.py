from odoo import models, fields, api, _

class AgriManureBatch(models.Model):
    _inherit = 'agri.manure.batch'

    state = fields.Selection([
        ('draft', 'Draft'),
        ('processing', 'Processing (Composting/Biogas)'),
        ('completed', 'Completed'),
        ('disposed', 'Disposed Externally')
    ], default='draft', tracking=True)

    def action_process(self):
        """ 
        [US-SYMBIOSIS-01] Eco-Loop Trigger 
        Automatically generate a recycling intervention (Composting/Biogas) 
        from raw agricultural waste.
        """
        for batch in self:
            if batch.disposal_method in ['composting', 'biogas']:
                batch.state = 'processing'
                
                # Auto-generate a conversion intervention in the Eco-system
                intervention_type = 'tillage' # Maps roughly to processing
                
                intervention = self.env['mrp.production'].create({
                    'product_id': batch.fertilizer_product_id.id,
                    'product_qty': batch.quantity * 0.4, # Mock conversion rate: 40% yield
                    'intervention_type': intervention_type,
                    'origin': batch.batch_no,
                    # We might link it directly to the symbiosis module via related fields
                })
                
                batch.message_post(body=_("Eco-Symbiosis: Triggered %s intervention %s to recycle %skg of raw waste.") % (
                    batch.disposal_method, intervention.name, batch.quantity
                ))
            elif batch.disposal_method == 'transfer_third_party':
                batch.state = 'disposed'
                batch.message_post(body=_("Waste transferred to third party."))
            else:
                batch.state = 'completed'
                batch.message_post(body=_("Waste applied directly to field."))

