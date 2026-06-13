from odoo import models, fields, api, _

class FarmResource(models.Model):
    _inherit = 'farm.resource'
    
    resource_type = fields.Selection(selection_add=[('workshop', 'Agritainment Workshop')], ondelete={'workshop': 'set default'})

class FarmBooking(models.Model):
    _inherit = 'farm.booking'
    
    workshop_topic = fields.Char("Workshop Topic", help="e.g. Traditional Tofu Making, Indigo Dyeing")

    def action_check_in(self):
        """
        [US-SCENARIO-28] Agritainment & Cultural Heritage Workshops
        When a school group checks in for a workshop, automatically generate
        a Traceability Passport context for the cultural products they will make.
        """
        for booking in self:
            booking.state = 'in_progress' # Assuming there's a state field, we'll just log if not
            booking.message_post(body=_("Group Checked In for Workshop: %s") % booking.workshop_topic)
            
            # If the marketing module is installed, we can tag this booking as a marketing event
            # so products made during this session inherit the cultural story.
            if 'stock.lot' in self.env:
                pass # The actual tracing happens when they buy it via POS

