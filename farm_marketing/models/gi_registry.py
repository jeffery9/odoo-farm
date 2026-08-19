from odoo import models, fields, api, _

class AgriGIRegistry(models.Model):
    """ US-062-02: Geographical Indication (GI) Registry """
    _name = 'agri.gi.registry'
    _description = 'Geographical Indication Registry'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("GI Name", required=True, translate=True) # e.g. "West Lake Longjing Tea"
    code = fields.Char("GI Code", required=True, help="National GI protection code")
    product_template_id = fields.Many2one('product.template', string="Protected Product")
    
    protection_area_id = fields.Many2one('farm.location', string="Protection Area (GIS)", domain=[('is_land_parcel', '=', True)])
    
    authority_name = fields.Char("Issuing Authority")
<<<<<<< HEAD
    certificate_attachment_ids = fields.Many2many('ir.attachment', 'agri_gi_registry_ir_attachment_rel', 'registry_id', 'attachment_id', string="GI Certificates")
=======
    certificate_attachment_ids = fields.Many2many('ir.attachment', 'agri_gi_registry_attachment_rel', 'registry_id', 'attachment_id', string="GI Certificates")
>>>>>>> 5351cad217860264bdd3ca8394fa45a799fce3d0
    
    is_active = fields.Boolean("Active", default=True)
    description = fields.Text("GI Description", translate=True)

class StockLot(models.Model):
    _inherit = 'stock.lot'

    gi_registry_id = fields.Many2one('agri.gi.registry', string="GI Registry")
    gi_security_code = fields.Char("GI Anti-counterfeit Code", readonly=True, copy=False)

    def action_generate_gi_code(self):
        """ US-062-02: Simulate generation of unique GI anti-counterfeit code """
        for lot in self:
            if lot.gi_registry_id and not lot.gi_security_code:
                # In real scenario, call national API
                import uuid
                lot.gi_security_code = f"GI-{lot.gi_registry_id.code}-{str(uuid.uuid4())[:8].upper()}"
                lot.message_post(body=_("GI Anti-counterfeit code generated: %s") % lot.gi_security_code)
