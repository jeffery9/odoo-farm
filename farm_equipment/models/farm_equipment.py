from odoo import models, fields, api, _

class FarmEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    is_agri_machinery = fields.Boolean("Is Agricultural Machinery", default=False)
    
    # Technical Specs [US-05-03]
    horsepower = fields.Float("Engine Power (HP)")
    working_width = fields.Float("Working Width (m)")
    fuel_type = fields.Selection([
        ('diesel', 'Diesel'),
        ('electric', 'Electric'),
        ('gasoline', 'Gasoline'),
        ('hybrid', 'Hybrid')
    ], string="Fuel Type", default='diesel')
    
    fuel_tank_capacity = fields.Float("Fuel Tank Capacity (L)")
    
    # Usage Stats
    total_engine_hours = fields.Float("Total Engine Hours", compute='_compute_total_hours', store=True)
    fuel_log_ids = fields.One2many('farm.equipment.log', 'equipment_id', string="Usage Logs")

    @api.depends('fuel_log_ids.engine_hours')
    def _compute_total_hours(self):
        for eq in self:
            eq.total_engine_hours = sum(eq.fuel_log_ids.mapped('engine_hours'))

class FarmEquipmentLog(models.Model):
    _name = 'farm.equipment.log'
    _description = 'Machinery Usage & Fuel Log'
    _order = 'date desc'

    equipment_id = fields.Many2one('maintenance.equipment', string="Machinery", required=True)
    task_id = fields.Many2one('project.task', string="Related Task")
    date = fields.Date("Date", default=fields.Date.today, required=True)
    
    engine_hours = fields.Float("Hours Used", help="Operating hours for this task")
    fuel_consumed = fields.Float("Fuel Consumed (L)")
    
    operator_id = fields.Many2one('res.users', string="Operator", default=lambda self: self.env.user)
    
    notes = fields.Text("Notes")
