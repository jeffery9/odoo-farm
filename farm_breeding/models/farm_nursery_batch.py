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
    
    # Transition Math [US-31]
    target_land_area = fields.Float("Target Area (mu/sqm)")
    target_density = fields.Float("Target Density (Plants/unit)")
    estimated_loss_rate = fields.Float("Nursery Loss Rate (%)", default=10.0)
    
    plants_needed = fields.Float("Total Plants Needed", compute='_compute_plants_needed')
    
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

    @api.depends('target_land_area', 'target_density', 'estimated_loss_rate')
    def _compute_plants_needed(self):
        for batch in self:
            if 100.0 - batch.estimated_loss_rate > 0:
                batch.plants_needed = (batch.target_land_area * batch.target_density) / (1 - batch.estimated_loss_rate / 100.0)
            else:
                batch.plants_needed = 0.0

    @api.depends('quantity', 'survival_rate')
    def _compute_current_count(self):
        for batch in self:
            batch.current_count = batch.quantity * (batch.survival_rate / 100.0)

    def action_create_transplant_task(self):
        """ 一键转化为大田移栽任务并生成移库单 """
        self.ensure_one()
        
        # 1. 创建任务
        task_vals = {
            'name': _('Transplant Task: %s') % self.name,
            'description': _('Transplanting %s seedlings. Variety: %s') % (self.current_count, self.product_id.display_name),
            'project_id': self.env['project.project'].search([('activity_family', '=', 'planting')], limit=1).id,
            'size_value': self.target_land_area,
        }
        task = self.env['project.task'].create(task_vals)
        
        # 2. 生成内部调拨 (从育苗室到生产区)
        picking_type = self.env['stock.picking.type'].search([('code', '=', 'internal')], limit=1)
        if picking_type:
            self.env['stock.picking'].create({
                'picking_type_id': picking_type.id,
                'origin': self.name,
                'move_ids': [(0, 0, {
                    'name': self.name,
                    'product_id': self.product_id.id,
                    'product_uom_qty': self.current_count,
                    'product_uom': self.product_id.uom_id.id,
                    'location_id': self.env.ref('stock.stock_location_stock').id, # 简化示例
                    'location_dest_id': self.env.ref('stock.stock_location_stock').id,
                })]
            })

        self.write({'state': 'transplanted'})
        return task
