from odoo import models, fields, api, _

class FarmEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    is_agri_machinery = fields.Boolean("Is Agricultural Machinery", default=False)
    is_drone = fields.Boolean("Is Drone (无人机)", default=False)
    
    # Technical Specs [US-05-03, US-22-01]
    horsepower = fields.Float("Engine Power (HP)")
    working_width = fields.Float("Working Width (m)", help="Spraying/Working width")
    payload_capacity = fields.Float("Max Payload (kg/L)", help="Tank or hopper capacity")
    max_flight_time = fields.Integer("Max Flight Time (min)")
    
    # 电池管理
    battery_ids = fields.One2many('farm.battery', 'drone_id', string="Associated Batteries")
    
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

class FarmBattery(models.Model):
    """
    US-22-01: 农用无人机电池资产管理
    """
    _name = 'farm.battery'
    _description = 'Agri-Drone Battery'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Serial Number", required=True)
    drone_id = fields.Many2one('maintenance.equipment', string="Assigned Drone", domain="[('is_drone', '=', True)]")
    
    cycle_count = fields.Integer("Cycle Count (循环次数)", default=0, tracking=True)
    max_cycles = fields.Integer("Design Life (Cycles)", default=200)
    current_capacity_health = fields.Float("Health (%)", default=100.0, tracking=True)
    
    state = fields.Selection([
        ('healthy', 'Good'),
        ('aging', 'Aging (建议更换)'),
        ('retired', 'Retired'),
        ('damaged', 'Damaged')
    ], string="Status", compute='_compute_state', store=True)

    @api.depends('cycle_count', 'max_cycles', 'current_capacity_health')
    def _compute_state(self):
        for rec in self:
            if rec.cycle_count > rec.max_cycles or rec.current_capacity_health < 70:
                rec.state = 'aging'
            else:
                rec.state = 'healthy'

    def action_log_cycle(self):
        """ 手动记录一次充放电循环 """
        for rec in self:
            rec.cycle_count += 1
            rec.message_post(body=_("Battery cycle recorded. New count: %s") % rec.cycle_count)
