from odoo import fields, models, api, _

class ResConfigSettings(models.TransientModel):
    """
    Configuration settings for different industry modules - replacing functionality from res_config_settings.py
    """
    _inherit = 'res.config.settings'

    # Industry module configuration options
    module_farm_field_crops = fields.Boolean(
        string='Field Crops Management',  # 大田作物管理
        help='Manage field crop plots, sowing/harvesting, mechanized operations, etc.',
        config_parameter='farm_core.module_farm_field_crops'
    )
    module_farm_protected_cultivation = fields.Boolean(
        string='Protected Cultivation',  # 设施农业管理
        help='Manage greenhouse environment control, water-fertilizer integration, temperature/humidity monitoring, etc.',
        config_parameter='farm_core.module_farm_protected_cultivation'
    )
    module_farm_orchard_horticulture = fields.Boolean(
        string='Orchard Horticulture',  # 果树园艺管理
        help='Manage tree pruning records, flowering period management, harvest tracking, annual cycle, etc.',
        config_parameter='farm_core.module_farm_orchard_horticulture'
    )
    module_farm_livestock = fields.Boolean(
        string='Livestock Management',  # 畜牧养殖管理
        help='Manage breeding records, health records, breeding management, individual identification, etc.',
        config_parameter='farm_core.module_farm_livestock'
    )
    module_farm_aquaculture = fields.Boolean(
        string='Aquaculture Management',  # 水产养殖管理
        help='Manage water quality monitoring, feeding management, growth tracking, dissolved oxygen/pH monitoring, etc.',
        config_parameter='farm_core.module_farm_aquaculture'
    )
    module_farm_medicinal_plants = fields.Boolean(
        string='Medicinal Plants',  # 中药材管理
        help='Manage GMP compliance for medicinal plants, active ingredient tracking, compliance certification, etc.',
        config_parameter='farm_core.module_farm_medicinal_plants'
    )
    module_farm_mushroom = fields.Boolean(
        string='Mushroom Cultivation',  # 食用菌管理
        help='Manage multi-batch cultivation, environmental control, harvest records, multi-harvest tracking, etc.',
        config_parameter='farm_core.module_farm_mushroom'
    )
    module_farm_apiculture = fields.Boolean(
        string='Apiculture Management',  # 蜂业管理
        help='Manage bee colony management, hive positioning, nectar source tracking, migration tracking, etc.',
        config_parameter='farm_core.module_farm_apiculture'
    )
    module_farm_agricultural_processing = fields.Boolean(
        string='Agricultural Processing',  # 农产品加工管理
        help='Manage product recipes, quality inspection, packaging tracking, batch inheritance, etc.',
        config_parameter='farm_core.module_farm_agricultural_processing'
    )
    module_farm_agritourism = fields.Boolean(
        string='Agritourism Management',  # 观光农业管理
        help='Manage resource booking, activity management, membership services, experience project tracking, etc.',
        config_parameter='farm_core.module_farm_agritourism'
    )

    # New Commercial SKU Gating Options
    group_enable_iot_telemetry = fields.Boolean(
        "Enable Base Farm IoT & Telemetry Center",
        implied_group='farm_core.group_iot_operator',
        config_parameter='farm_core.group_enable_iot_telemetry'
    )
    group_enable_a2a_netting = fields.Boolean(
        "Enable Cooperative-to-Farmer A2A Bilateral Netting",
        implied_group='farm_core.group_a2a_netting_auditor',
        config_parameter='farm_core.group_enable_a2a_netting'
    )
    group_enable_biological_valuation = fields.Boolean(
        "Enable SVL/AVL Biological Asset Fair Value Ledger",
        implied_group='farm_core.group_biological_asset_valuer',
        config_parameter='farm_core.group_enable_biological_valuation'
    )