from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # Industry module configuration options
    module_farm_field_crops = fields.Boolean(
        string='Field Crops Management',  # 大田作物管理
        help='Manage field crop plots, sowing/harvesting, mechanized operations, etc.'
    )
    module_farm_protected_cultivation = fields.Boolean(
        string='Protected Cultivation',  # 设施农业管理
        help='Manage greenhouse environment control, water-fertilizer integration, temperature/humidity monitoring, etc.'
    )
    module_farm_orchard_horticulture = fields.Boolean(
        string='Orchard Horticulture',  # 果树园艺管理
        help='Manage tree pruning records, flowering period management, harvest tracking, annual cycle, etc.'
    )
    module_farm_livestock = fields.Boolean(
        string='Livestock Management',  # 畜牧养殖管理
        help='Manage breeding records, health records, breeding management, individual identification, etc.'
    )
    module_farm_aquaculture = fields.Boolean(
        string='Aquaculture Management',  # 水产养殖管理
        help='Manage water quality monitoring, feeding management, growth tracking, dissolved oxygen/pH monitoring, etc.'
    )
    module_farm_medicinal_plants = fields.Boolean(
        string='Medicinal Plants',  # 中药材管理
        help='Manage GMP compliance for medicinal plants, active ingredient tracking, compliance certification, etc.'
    )
    module_farm_mushroom = fields.Boolean(
        string='Mushroom Cultivation',  # 食用菌管理
        help='Manage multi-batch cultivation, environmental control, harvest records, multi-harvest tracking, etc.'
    )
    module_farm_apiculture = fields.Boolean(
        string='Apiculture Management',  # 蜂业管理
        help='Manage bee colony management, hive positioning, nectar source tracking, migration tracking, etc.'
    )
    module_farm_agricultural_processing = fields.Boolean(
        string='Agricultural Processing',  # 农产品加工管理
        help='Manage product recipes, quality inspection, packaging tracking, batch inheritance, etc.'
    )
    module_farm_agritourism = fields.Boolean(
        string='Agritourism Management',  # 观光农业管理
        help='Manage resource booking, activity management, membership services, experience project tracking, etc.'
    )