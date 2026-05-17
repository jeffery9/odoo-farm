from odoo import models, fields, api, _
from odoo.exceptions import UserError

class MrpWorkcenter(models.Model):
    _inherit = 'mrp.workcenter'

    last_allergen_id = fields.Many2one('agri.allergen', string="Last Processed Allergen", readonly=True)
    requires_cip = fields.Boolean("Requires CIP", default=False, readonly=True, help="Clean-In-Place required to clear allergen contamination.")
    last_cip_date = fields.Datetime("Last CIP Certified", readonly=True)

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    def action_confirm(self):
        """
        [US-SCENARIO-38] CIP Routing & Allergen Traceability
        Physically lock the production line if it is contaminated by a previous allergen
        and a certified CIP (Clean-In-Place) has not been performed.
        """
        # First, check the work centers assigned to this MO's routing
        for mo in self:
            # We assume a single workcenter per MO for this simplified scenario
            # Normally this would check workorders
            if hasattr(mo, 'workorder_ids') and mo.workorder_ids:
                workcenters = mo.workorder_ids.mapped('workcenter_id')
            else:
                # If no routing, maybe check a default workcenter if set
                # For testing, let's just check all if not specific, or skip if none
                continue
                
            for wc in workcenters:
                if wc.requires_cip:
                    raise UserError(_("FATAL FOOD SAFETY LOCK: Workcenter '%s' is contaminated with allergen '%s'. You must perform a certified CIP (Clean-In-Place) before processing a new batch.") % (
                        wc.name, wc.last_allergen_id.name
                    ))
                    
        return super().action_confirm()

    def button_mark_done(self):
        res = super().button_mark_done()
        
        # When MO finishes, contaminate the workcenter if the product has allergens
        for mo in self:
            allergens = mo.product_id.allergen_ids if hasattr(mo.product_id, 'allergen_ids') else self.env['agri.allergen']
            if allergens:
                # For simplicity, just pick the first one
                allergen = allergens[0]
                if hasattr(mo, 'workorder_ids') and mo.workorder_ids:
                    workcenters = mo.workorder_ids.mapped('workcenter_id')
                    for wc in workcenters:
                        wc.write({
                            'last_allergen_id': allergen.id,
                            'requires_cip': True
                        })
                        wc.message_post(body=_("Contaminated by allergen '%s' from order %s. CIP Lock engaged.") % (allergen.name, mo.name))
        return res

class CIPIntervention(models.TransientModel):
    _name = 'farm.cip.wizard'
    _description = 'Certify Clean-In-Place'

    workcenter_id = fields.Many2one('mrp.workcenter', required=True)
    iot_verification_hash = fields.Char("IoT Wash Data Hash (Optional)")
    inspector_id = fields.Many2one('res.users', default=lambda self: self.env.user, required=True)

    def action_certify_cip(self):
        self.ensure_one()
        self.workcenter_id.write({
            'requires_cip': False,
            'last_allergen_id': False,
            'last_cip_date': fields.Datetime.now()
        })
        self.workcenter_id.message_post(body=_("CIP Certified by %s. Line is safe for production.") % self.inspector_id.name)
        return {'type': 'ir.actions.act_window_close'}
