from odoo import models, fields, api, _

class ResPartner(models.Model):
    """
    Agricultural Community Identity.
    Injects Sustainability Mixin to track ESG reputation and credit score.
    """
    _name = 'res.partner'
    _inherit = ['res.partner', 'agri.sustainability.mixin']
    
    # GS1 Global Identifiers [EPCIS Alignment]
    gs1_gln = fields.Char('GS1 GLN', help='Global Location Number (13 digits)', size=13)
    
    # We use credit_score defined in SustainabilityMixin
    
    def action_view_reputation_history(self):
        """Action to view credit slashing and bonus history."""
        self.ensure_one()
        # To be implemented with specific history logs
        return True
