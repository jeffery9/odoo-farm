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


class IndustryDataPackage(models.Model):
    """
    US-01-08: "One-Click Initialization" Industry Master Data Package
    - Pre-configured at least 5 industry-specific basic data packages
    - Import process supports "attribute mapping": automatically associate industry-standard physiological cycles with Odoo task templates
    """
    _name = 'farm.industry.data.package'
    _description = 'Industry Data Package for One-Click Initialization'
    _order = 'name'

    name = fields.Char(
        "Package Name",
        required=True,
        help="Name of the industry data package"
    )

    code = fields.Char(
        "Package Code",
        required=True,
        help="Unique code for the package"
    )

    industry_type = fields.Selection([
        ('citrus', 'Citrus Cultivation (柑橘种植)'),
        ('swine', 'Swine Farming (生猪养殖)'),
        ('poultry', 'Poultry Farming (家禽养殖)'),
        ('dairy', 'Dairy Farming (奶牛养殖)'),
        ('vegetables', 'Vegetable Farming (蔬菜种植)'),
        ('grains', 'Grain Cultivation (粮食种植)'),
        ('flowers', 'Floriculture (花卉种植)'),
        ('aquaculture', 'Aquaculture (水产养殖)'),
    ], string="Industry Type", required=True)

    description = fields.Text("Description")

    # Pre-configured variety data
    variety_ids = fields.One2many(
        'farm.industry.variety',
        'package_id',
        string="Varieties Data"
    )

    # Pre-configured physiological stage definitions
    physio_stage_ids = fields.One2many(
        'farm.industry.physio.stage',
        'package_id',
        string="Physiological Stages"
    )

    # Pre-configured UOM conversion table
    uom_conversion_ids = fields.One2many(
        'farm.industry.uom.conversion',
        'package_id',
        string="UOM Conversions"
    )

    # Pre-configured task templates
    task_template_ids = fields.One2many(
        'farm.industry.task.template',
        'package_id',
        string="Task Templates"
    )

    # Pre-configured product categories
    product_category_ids = fields.One2many(
        'farm.industry.product.category',
        'package_id',
        string="Product Categories"
    )

    def action_apply_package(self):
        """Apply this package to initialize industry data"""
        self.ensure_one()

        # Import varieties
        self._import_varieties()

        # Import physiological stages
        self._import_physio_stages()

        # Import UOM conversions
        self._import_uom_conversions()

        # Import task templates
        self._import_task_templates()

        # Import product categories
        self._import_product_categories()

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Success'),
                'message': _('Industry data package "%s" has been successfully applied.') % self.name,
                'type': 'success',
                'sticky': False,
            }
        }

    def _import_varieties(self):
        """Import varieties from the package"""
        for variety_data in self.variety_ids:
            # Check if variety already exists
            existing_variety = self.env['product.template'].search([
                ('agri_variety', '=', variety_data.variety_name),
                ('name', '=', variety_data.product_name)
            ], limit=1)

            if not existing_variety:
                self.env['product.template'].create({
                    'name': variety_data.product_name,
                    'agri_variety': variety_data.variety_name,
                    'type': 'product',
                    'agricultural_type': variety_data.agricultural_type,
                    'standard_dose': variety_data.standard_dose,
                    'dose_uom_id': variety_data.dose_uom_id.id if variety_data.dose_uom_id else False,
                    'n_content': variety_data.n_content,
                    'p_content': variety_data.p_content,
                    'k_content': variety_data.k_content,
                    'growth_duration': variety_data.growth_duration,
                    'maturity_age_days': variety_data.maturity_age_days,
                    'is_biological_asset': variety_data.is_biological_asset,
                })

    def _import_physio_stages(self):
        """Import physiological stages from the package"""
        # This would typically involve creating growth curve data for products
        for stage_data in self.physio_stage_ids:
            # Find the associated product(s) to update their growth curves
            products = self.env['product.template'].search([
                ('agri_variety', '=', stage_data.related_variety)
            ])

            for product in products:
                # Find if this age_days already exists, if not create it
                existing_curve = self.env['farm.growth.curve'].search([
                    ('product_id', '=', product.id),
                    ('age_days', '=', stage_data.age_days)
                ], limit=1)

                if not existing_curve:
                    self.env['farm.growth.curve'].create({
                        'product_id': product.id,
                        'age_days': stage_data.age_days,
                        'target_weight': stage_data.target_weight,
                        'daily_feed_rate': stage_data.daily_feed_rate,
                    })

    def _import_uom_conversions(self):
        """Import UOM conversions from the package"""
        # UOM conversions are handled by Odoo's built-in UOM system
        # We'll create or update UOM records as needed
        for conversion_data in self.uom_conversion_ids:
            # This would involve setting up UOM conversion factors
            # In Odoo, UOM conversions are typically handled in the UOM module itself
            pass

    def _import_task_templates(self):
        """Import task templates from the package"""
        for template_data in self.task_template_ids:
            # Check if task template already exists
            existing_template = self.env['project.task.type'].search([
                ('name', '=', template_data.name),
                ('project_id', '=', template_data.project_id.id if template_data.project_id else False)
            ], limit=1)

            if not existing_template:
                self.env['project.task.type'].create({
                    'name': template_data.name,
                    'description': template_data.description,
                    'fold': template_data.fold,
                    # Add other fields as needed
                })

    def _import_product_categories(self):
        """Import product categories from the package"""
        for category_data in self.product_category_ids:
            # Check if category already exists
            existing_category = self.env['product.category'].search([
                ('name', '=', category_data.name)
            ], limit=1)

            if not existing_category:
                self.env['product.category'].create({
                    'name': category_data.name,
                    'parent_id': category_data.parent_id.id if category_data.parent_id else False,
                    'agricultural_type': category_data.agricultural_type,
                })

    @api.model
    def create_default_packages(self):
        """Create default industry packages"""
        # Create citrus package
        citrus_package = self.create({
            'name': 'Citrus Cultivation Package',
            'code': 'CITRUS',
            'industry_type': 'citrus',
            'description': 'Standard data package for citrus cultivation including varieties, tasks, and growth stages.'
        })

        # Add varieties for citrus
        self.env['farm.industry.variety'].create({
            'package_id': citrus_package.id,
            'product_name': 'Oranges',
            'variety_name': 'Navel Orange',
            'agricultural_type': 'output',
            'standard_dose': 1.0,
            'growth_duration': 180,  # 6 months from planting to harvest
            'maturity_age_days': 90, # Trees mature in 90 days
            'is_biological_asset': False,
        })

        self.env['farm.industry.variety'].create({
            'package_id': citrus_package.id,
            'product_name': 'Lemons',
            'variety_name': 'Meyer Lemon',
            'agricultural_type': 'output',
            'standard_dose': 1.0,
            'growth_duration': 180,
            'maturity_age_days': 90,
            'is_biological_asset': False,
        })

        # Add physiological stages for citrus
        self.env['farm.industry.physio.stage'].create({
            'package_id': citrus_package.id,
            'stage_name': 'Seedling Stage',
            'age_days': 30,
            'target_weight': 0.1,
            'daily_feed_rate': 0.5,
            'related_variety': 'Navel Orange'
        })

        self.env['farm.industry.physio.stage'].create({
            'package_id': citrus_package.id,
            'stage_name': 'Growing Stage',
            'age_days': 90,
            'target_weight': 1.0,
            'daily_feed_rate': 1.0,
            'related_variety': 'Navel Orange'
        })

        # Create swine package
        swine_package = self.create({
            'name': 'Swine Farming Package',
            'code': 'SWINE',
            'industry_type': 'swine',
            'description': 'Standard data package for swine farming including breeds, tasks, and growth stages.'
        })

        # Add varieties for swine
        self.env['farm.industry.variety'].create({
            'package_id': swine_package.id,
            'product_name': 'Pigs',
            'variety_name': 'Yorkshire',
            'agricultural_type': 'animal',
            'standard_dose': 2.5,  # kg feed per day
            'growth_duration': 180,  # 6 months to market weight
            'maturity_age_days': 180,  # Maturity age for breeding
            'is_biological_asset': True,
            'n_content': 18.0,  # Protein content
            'p_content': 0.8,   # Phosphorus content
            'k_content': 0.6,   # Potassium content
        })

        # Add physiological stages for swine
        self.env['farm.industry.physio.stage'].create({
            'package_id': swine_package.id,
            'stage_name': 'Piglet Stage',
            'age_days': 21,
            'target_weight': 6.0,
            'daily_feed_rate': 5.0,
            'related_variety': 'Yorkshire'
        })

        self.env['farm.industry.physio.stage'].create({
            'package_id': swine_package.id,
            'stage_name': 'Growing Stage',
            'age_days': 90,
            'target_weight': 50.0,
            'daily_feed_rate': 2.5,
            'related_variety': 'Yorkshire'
        })

        self.env['farm.industry.physio.stage'].create({
            'package_id': swine_package.id,
            'stage_name': 'Finishing Stage',
            'age_days': 180,
            'target_weight': 110.0,
            'daily_feed_rate': 3.0,
            'related_variety': 'Yorkshire'
        })

        # Create poultry package
        poultry_package = self.create({
            'name': 'Poultry Farming Package',
            'code': 'POULTRY',
            'industry_type': 'poultry',
            'description': 'Standard data package for poultry farming including breeds, tasks, and growth stages.'
        })

        # Add varieties for poultry
        self.env['farm.industry.variety'].create({
            'package_id': poultry_package.id,
            'product_name': 'Chickens',
            'variety_name': 'Broilers',
            'agricultural_type': 'animal',
            'standard_dose': 0.15,  # kg feed per day per chicken
            'growth_duration': 42,  # 6 weeks to market weight
            'maturity_age_days': 180,  # Maturity for breeding
            'is_biological_asset': True,
        })

        # Create dairy package
        dairy_package = self.create({
            'name': 'Dairy Farming Package',
            'code': 'DAIRY',
            'industry_type': 'dairy',
            'description': 'Standard data package for dairy farming including breeds, tasks, and lactation stages.'
        })

        # Create vegetables package
        vegetables_package = self.create({
            'name': 'Vegetable Farming Package',
            'code': 'VEGETABLES',
            'industry_type': 'vegetables',
            'description': 'Standard data package for vegetable farming including varieties, tasks, and growth stages.'
        })

        _logger = __import__('logging').getLogger(__name__)
        _logger.info("Default industry packages have been created")


class IndustryVariety(models.Model):
    """Variety data for industry packages"""
    _name = 'farm.industry.variety'
    _description = 'Industry Package Variety Data'

    package_id = fields.Many2one(
        'farm.industry.data.package',
        string="Industry Package",
        required=True,
        ondelete='cascade'
    )

    product_name = fields.Char("Product Name", required=True)
    variety_name = fields.Char("Variety Name", required=True)
    agricultural_type = fields.Selection([
        ('land_parcel', 'Land Parcel'),
        ('animal', 'Animal'),
        ('animal_group', 'Animal Group'),
        ('equipment', 'Equipment'),
        ('input', 'Input'),
        ('output', 'Output'),
    ], string="Agricultural Type", default='output')

    # Standard agricultural properties
    standard_dose = fields.Float("Standard Dose")
    dose_uom_id = fields.Many2one('uom.uom', string="Dose Unit")
    n_content = fields.Float("Nitrogen (N) %")
    p_content = fields.Float("Phosphorus (P) %")
    k_content = fields.Float("Potassium (K) %")
    growth_duration = fields.Integer("Growth Duration (Days)")
    maturity_age_days = fields.Integer("Maturity Age (Days)")
    is_biological_asset = fields.Boolean("Is Biological Asset")


class IndustryPhysioStage(models.Model):
    """Physiological stage data for industry packages"""
    _name = 'farm.industry.physio.stage'
    _description = 'Industry Package Physiological Stage Data'

    package_id = fields.Many2one(
        'farm.industry.data.package',
        string="Industry Package",
        required=True,
        ondelete='cascade'
    )

    stage_name = fields.Char("Stage Name", required=True)
    age_days = fields.Integer("Age (Days)", required=True)
    target_weight = fields.Float("Target Weight (kg)")
    daily_feed_rate = fields.Float("Daily Feed Rate (%)")
    related_variety = fields.Char("Related Variety")

    description = fields.Text("Description")


class IndustryUOMConversion(models.Model):
    """UOM conversion data for industry packages"""
    _name = 'farm.industry.uom.conversion'
    _description = 'Industry Package UOM Conversion Data'

    package_id = fields.Many2one(
        'farm.industry.data.package',
        string="Industry Package",
        required=True,
        ondelete='cascade'
    )

    from_uom_id = fields.Many2one('uom.uom', string="From UOM", required=True)
    to_uom_id = fields.Many2one('uom.uom', string="To UOM", required=True)
    factor = fields.Float("Conversion Factor", required=True, default=1.0)

    description = fields.Text("Description")


class IndustryTaskTemplate(models.Model):
    """Task template data for industry packages"""
    _name = 'farm.industry.task.template'
    _description = 'Industry Package Task Template Data'

    package_id = fields.Many2one(
        'farm.industry.data.package',
        string="Industry Package",
        required=True,
        ondelete='cascade'
    )

    name = fields.Char("Template Name", required=True)
    description = fields.Text("Description")
    fold = fields.Boolean("Folded in Kanban", default=False)
    project_id = fields.Many2one('project.project', string="Project")

    # Additional fields for agricultural task templates
    expected_duration = fields.Integer("Expected Duration (Days)")
    required_equipment = fields.Char("Required Equipment")
    required_inputs = fields.Char("Required Inputs")


class IndustryProductCategory(models.Model):
    """Product category data for industry packages"""
    _name = 'farm.industry.product.category'
    _description = 'Industry Package Product Category Data'

    package_id = fields.Many2one(
        'farm.industry.data.package',
        string="Industry Package",
        required=True,
        ondelete='cascade'
    )

    name = fields.Char("Category Name", required=True)
    parent_id = fields.Many2one('product.category', string="Parent Category")
    agricultural_type = fields.Selection([
        ('land_parcel', 'Land Parcel'),
        ('animal', 'Animal'),
        ('animal_group', 'Animal Group'),
        ('equipment', 'Equipment'),
        ('input', 'Input'),
        ('output', 'Output'),
    ], string="Agricultural Type")


class IndustryPackageWizard(models.TransientModel):
    """
    Wizard for applying industry data packages
    """
    _name = 'farm.industry.package.wizard'
    _description = 'Industry Package Application Wizard'

    package_id = fields.Many2one(
        'farm.industry.data.package',
        string="Industry Package",
        required=True
    )

    confirmation_message = fields.Char(
        string="Confirmation Message",
        compute='_compute_confirmation_message'
    )

    @api.depends('package_id')
    def _compute_confirmation_message(self):
        for record in self:
            if record.package_id:
                record.confirmation_message = _("Apply the '%s' package? This will initialize your system with industry-specific data.") % record.package_id.name
            else:
                record.confirmation_message = ""

    def action_apply_selected_package(self):
        """Apply the selected package"""
        self.ensure_one()
        if not self.package_id:
            raise Exception(_("Please select an industry package to apply."))

        # Call the apply method on the selected package
        return self.package_id.action_apply_package()


class FarmGrowthCurve(models.Model):
    """
    Growth curve management for agricultural products
    """
    _name = 'farm.growth.curve'
    _description = 'Agricultural Growth Curve'
    _order = 'age_days'

    product_id = fields.Many2one('product.template', string="Variety", ondelete='cascade')
    age_days = fields.Integer("Age (Days)", required=True)
    target_weight = fields.Float("Target Weight (kg)", required=True)
    daily_feed_rate = fields.Float("Feeding Rate (%)", help="Feed qty as % of body weight")

    def get_expected_weight(self, product, age_days):
        """Get expected weight based on age"""
        curve = self.search([('product_id', '=', product.id), ('age_days', '<=', age_days)], order='age_days DESC', limit=1)
        return curve.target_weight if curve else 0.0


class ProductTemplate(models.Model):
    """
    Product template extensions for agricultural products - replacing functionality from product_template.py
    """
    _inherit = 'product.template'

    # Agricultural-specific fields
    agricultural_type = fields.Selection([
        ('land_parcel', 'Land Parcel'),
        ('animal', 'Animal'),
        ('animal_group', 'Animal Group'),
        ('equipment', 'Equipment'),
        ('input', 'Input'),
        ('output', 'Output'),
    ], string="Agricultural Type")

    # Agricultural-specific fields
    agri_variety = fields.Char("Variety/Species")
    born_at = fields.Datetime("Born At/Started At")
    dead_at = fields.Datetime("Dead At/Terminated At")
    identification_number = fields.Char("Identification No.")

    # Growth curve data
    growth_curve_ids = fields.One2many('farm.growth.curve', 'product_id', string="Growth Curve")

    def get_expected_weight(self, age_days):
        """Get expected weight based on age"""
        curve = self.growth_curve_ids.filtered(lambda c: c.age_days <= age_days).sorted('age_days', reverse=True)
        return curve[0].target_weight if curve else 0.0

    # Lot property definitions
    lot_properties_definition = fields.PropertiesDefinition('Lot Properties Definition')

    # Nutrient content
    n_content = fields.Float("Nitrogen (N) %", help="Nitrogen percentage content")
    p_content = fields.Float("Phosphorus (P) %", help="Phosphorus percentage content")
    k_content = fields.Float("Potassium (K) %", help="Potassium percentage content")

    # MTO lead time logic
    growth_duration = fields.Integer("Growth Duration (Days)", help="Standard growth period from planting to harvest.")

    # Generation tracking (G0-G3)
    agri_generation = fields.Selection([
        ('g0', 'G0 (Breeder Seed/Original)'),
        ('g1', 'G1 (Foundation Seed)'),
        ('g2', 'G2 (Registered Seed)'),
        ('g3', 'G3 (Certified/Commercial Seed)')
    ], string="Agri Generation", help="Generation tracking for seeds or livestock.")

    # Biological asset accounting
    is_biological_asset = fields.Boolean("Is Biological Asset", default=False)
    maturity_age_days = fields.Integer("Maturity Age (Days)", help="Age at which the asset is considered mature (e.g. starts producing fruit/milk).")

    # Agricultural UOM flexible conversion
    standard_dose = fields.Float("Standard Dose", help="Recommended quantity per unit of area.")
    dose_uom_id = fields.Many2one('uom.uom', string="Dose Unit", help="Unit for the dose (e.g., kg/mu, L/ha).")