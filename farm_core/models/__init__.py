# Order of loading is critical for model dependencies in Odoo 19
from . import lxml_patch
from . import quality_point_mock
# 1. Base Mixins & Protocols
from . import base_mixins
from . import agri_mixins
from . import agri_evidence_mixin
from . import agri_view_mixin
from . import agri_odoo19_performance_security_mixin

# 2. Domain Entities (Level 2/3)
from . import agri_location
from . import agri_neighborhood
from . import agri_task_mixin
from . import agri_biological_asset
from . import agri_soil_analysis
from . import agri_industry_planting_mixin

# 3. Core Foundation Models
from . import common_fields
from . import product_category_extension
from . import res_partner
from . import res_company
from . import performance_monitor

# 4. Standard Extensions & Auxiliary Models
from . import agri_stock_lot
from . import agri_lot_kinship
from . import agri_stock_move
from . import agri_treatment_batch
from . import stock_matter_tracking
from . import stock_matter_tracking_link
from . import stock_matter_link
from . import stock_quant_consolidation
from . import farm_growth_curve  # Must be before product_template_extension

# 5. Application/Business Models (Level 4)
from . import product_template_extension
from . import land_location
from . import farm_location_3d
from . import biological_asset
from . import activity_operation

# 6. Industry Specialized Data (Level 1/2)
from . import industry_data_package
from . import industry_variety
from . import industry_physio_stage
from . import industry_product_category
from . import industry_task_template
from . import industry_uom_conversion
from . import industry_package_wizard

# 7. Financial & Clearing Engine
from . import agri_value_bridge
from . import agri_clearing_ledger
from . import agri_clearing_engine

# 8. System Logic
from . import config_settings
from . import geofencing
from . import gis_utils
