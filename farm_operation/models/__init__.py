# Order of loading is critical for model dependencies
# 1. Base Mixins & Domain Mixins
from . import agri_agricultural_campaign_mixin
from . import agri_bom_mixin
from . import agri_intervention_mixin
from . import farm_agricultural_campaign_mixin
from . import farm_agricultural_intervention_mixin
from . import farm_agricultural_bom_mixin

# 2. Domain Base Entities
from . import farm_agricultural_campaign_base

# 3. Core Extensions & Application Models
from . import agricultural_campaign
from . import agri_bom
from . import agri_intervention
from . import project_task
from . import stock_move
from . import farm_agricultural_campaign
from . import farm_agricultural_intervention
from . import farm_agricultural_bom

# 4. Auxiliary & Integrations
from . import farm_isl_redirection
# from . import wizard
from . import sale_order
