from odoo import models, fields, api, _

class StockLot(models.Model):
    _inherit = 'stock.lot'

    # 批次溯源 [US-14-03]
    parent_lot_id = fields.Many2one('stock.lot', string="Parent Lot/Origin", help="Trace back to the raw material lot")
    child_lot_ids = fields.One2many('stock.lot', 'parent_lot_id', string="Derived Products")
    
    # 性能优化：写入时预计算的全路径 [Pre-calculated Path]
    full_traceability_path = fields.Text("Full Traceability Path", readonly=True, 
                                       help="Flattened upstream lot IDs for instant lookup.")

    # 分级与元数据 [US-14-05]
    quality_grade = fields.Selection([
        ('a', 'Grade A / Premium'),
        ('b', 'Grade B / Standard'),
        ('c', 'Grade C / Processing'),
        ('loss', 'Loss/Waste')
    ], string='Quality Grade')
    
    harvest_date = fields.Date('Harvest Date')
    plot_id = fields.Many2one('farm.land', string='Origin Plot')
