from odoo import models, fields, api, _
from datetime import date

class FarmNurseryBatch(models.Model):
    _name = 'farm.nursery.batch'
    _description = 'Nursery Batch'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Batch ID", required=True, copy=False)
    product_id = fields.Many2one('product.product', string="Variety/Seed", required=True, domain=[('is_variety', '=', True)])
    sowing_date = fields.Date("Sowing Date", default=fields.Date.today)
    seedling_age = fields.Integer("Seedling Age (Days)", compute='_compute_seedling_age')
    
    survival_rate = fields.Float("Survival Rate (%)", default=100.0)
    quantity = fields.Float("Initial Quantity")
    current_count = fields.Float("Current Count", compute='_compute_current_count', store=True)
    
    state = fields.Selection([
        ('germinating', 'Germinating (催芽)'),
        ('nursery', 'Nursery (育苗中)'),
        ('ready', 'Ready (待移栽)'),
        ('transplanted', 'Transplanted (已移栽)'),
        ('failed', 'Failed (失败)')
    ], string="Status", default='germinating', tracking=True)

    @api.depends('sowing_date')
    def _compute_seedling_age(self):
        today = date.today()
        for batch in self:
            if batch.sowing_date:
                batch.seedling_age = (today - batch.sowing_date).days
            else:
                batch.seedling_age = 0

    @api.depends('quantity', 'survival_rate')
    def _compute_current_count(self):
        for batch in self:
            batch.current_count = batch.quantity * (batch.survival_rate / 100.0)

    def action_create_transplant_task(self):
        """ 一键转化为大田移栽任务 """
        self.ensure_one()
        task_vals = {
            'name': _('Transplant Task: %s') % self.name,
            'description': _('Transplanting seedlings from batch %s. Variety: %s') % (self.name, self.product_id.display_name),
            'project_id': self.env['project.project'].search([('activity_family', '=', 'planting')], limit=1).id,
        }
        task = self.env['project.task'].create(task_vals)
        self.write({'state': 'transplanted'})
        return task
