from odoo import models, fields

class ProjectTask(models.Model):
    _inherit = 'project.task'

    campaign_id = fields.Many2one(
        'agricultural.campaign', 
        string="Campaign/Season",
        help="Link this production task to a specific season."
    )
    
    # 继承 farm_core 中的地块/资产逻辑
    land_parcel_id = fields.Many2one('stock.location', string="Land Parcel/Pond", domain=[('is_land_parcel', '=', True)])
    biological_lot_id = fields.Many2one('stock.lot', string="Biological Asset/Lot", domain="[('is_animal', '=', True)]")
