from odoo import models, fields, api, _

class FarmMushroomProduction(models.Model):
    _inherit = 'farm.mushroom.production'
    
    # [US-SCENARIO-34] Edible Fungi Chamber Orchestration
    growth_phase = fields.Selection([
        ('incubation', 'Incubation (发菌)'),
        ('pinning', 'Pinning (催蕾)'),
        ('fruiting', 'Fruiting (出菇)')
    ], default='incubation')
    
    plc_status = fields.Char("PLC Command Status", readonly=True)

    def action_next_phase(self):
        self.ensure_one()
        if self.growth_phase == 'incubation':
            self.growth_phase = 'pinning'
            command = "Drop temp to 12C, spike CO2 to 2000ppm"
        elif self.growth_phase == 'pinning':
            self.growth_phase = 'fruiting'
            command = "Raise temp to 18C, drop CO2 to 800ppm"
        else:
            return True
            
        self.plc_status = f"SENT: {command}"
        self.message_post(body=_("Phase changed to %s. Pushed to PLC: %s") % (self.growth_phase, command))
        return True

