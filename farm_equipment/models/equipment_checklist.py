from odoo import models, fields, api, _

class FarmEquipmentChecklist(models.Model):
    """
    US-26-03: 机械启动前安全点检模版
    """
    _name = 'farm.equipment.checklist'
    _description = 'Equipment Pre-op Checklist'

    name = fields.Char("Checklist Name", required=True)
    equipment_type = fields.Selection([
        ('machinery', 'General Machinery'),
        ('drone', 'Drone (UAV)'),
        ('vehicle', 'Vehicle')
    ], string="Applies To", default='machinery')
    
    line_ids = fields.One2many('farm.equipment.checklist.line', 'checklist_id', string="Check Items")
    active = fields.Boolean(default=True)

class FarmEquipmentChecklistLine(models.Model):
    _name = 'farm.equipment.checklist.line'
    _description = 'Checklist Item'

    checklist_id = fields.Many2one('farm.equipment.checklist', ondelete='cascade')
    name = fields.Char("Requirement", required=True) # e.g. "Check Oil Level"
    is_mandatory = fields.Boolean("Mandatory", default=True)
    requires_photo = fields.Boolean("Require Photo Evidence", default=False)

class FarmEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    checklist_id = fields.Many2one('farm.equipment.checklist', string="Pre-op Checklist")
