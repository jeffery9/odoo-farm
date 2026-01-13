from odoo import models, fields

class FarmGrowthCurve(models.Model):
    _name = 'farm.growth.curve'
    _description = 'Agricultural Growth Curve'
    _order = 'age_days'

    product_id = fields.Many2one('product.template', string="Variety", ondelete='cascade')
    age_days = fields.Integer("Age (Days)", required=True)
    target_weight = fields.Float("Target Weight (kg)", required=True)
    daily_feed_rate = fields.Float("Feeding Rate (%)", help="Feed qty as % of body weight")

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    agricultural_type = fields.Selection([
        ('land_parcel', 'Land Parcel (地块)'),
        ('animal', 'Animal (个体动物)'),
        ('animal_group', 'Animal Group (群组)'),
        ('equipment', 'Equipment (设备)'),
        ('input', 'Input (投入品)'),
        ('output', 'Output (产出品)'),
    ], string="Agricultural Type")

    # 农业特有字段 [Everything is a Product]
    agri_variety = fields.Char("Variety/Species (品种)")
    born_at = fields.Datetime("Born At/Started At")
    dead_at = fields.Datetime("Dead At/Terminated At")
    identification_number = fields.Char("Identification No. (耳标/编号)")

    # Growth Curve Data [US-Livestock]
    growth_curve_ids = fields.One2many('farm.growth.curve', 'product_id', string="Growth Curve")

    def get_expected_weight(self, age_days):
        """ 根据年龄返回预期体重 """
        curve = self.growth_curve_ids.filtered(lambda c: c.age_days <= age_days).sorted('age_days', reverse=True)
        return curve[0].target_weight if curve else 0.0

    # 批次属性定义 [US-01-02]
    lot_properties_definition = fields.PropertiesDefinition('Lot Properties Definition')

    # 养分含量 [US-01-03]
    n_content = fields.Float("Nitrogen (N) %", help="Nitrogen percentage content")
    p_content = fields.Float("Phosphorus (P) %", help="Phosphorus percentage content")
    k_content = fields.Float("Potassium (K) %", help="Potassium percentage content")

    # MTO 提前期逻辑 [US-09-01]
    growth_duration = fields.Integer("Growth Duration (Days)", help="Standard growth period from planting to harvest.")
