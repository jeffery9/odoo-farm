# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class AgriIndustryDataPackage(models.Model):
    """
    US-01-08: "One-Click Initialization" Industry Master Data Package
    - Pre-configured at least 5 industry-specific basic data packages
    - Import process supports "attribute mapping": automatically associate industry-standard physiological cycles with Odoo task templates
    Refactored to agri domain with 100% business logic retention and English i18n.
    """
    _name = 'agri.industry.data.package'
    _description = 'Industry Data Package for One-Click Initialization'
    _order = 'name'

    name = fields.Char(
        "Package Name",
        required=True,
        translate=True,
        help="Name of the industry data package"
    )

    code = fields.Char(
        "Package Code",
        required=True,
        help="Unique code for the package"
    )

    industry_type = fields.Selection([
        ('citrus', 'Citrus Cultivation'),
        ('swine', 'Swine Farming'),
        ('poultry', 'Poultry Farming'),
        ('dairy', 'Dairy Farming'),
        ('vegetables', 'Vegetable Farming'),
        ('grains', 'Grain Cultivation'),
        ('flowers', 'Floriculture'),
        ('aquaculture', 'Aquaculture'),
    ], string="Industry Type", required=True)

    description = fields.Text("Description", translate=True)

    # Pre-configured variety data - Updated to new namespace
    variety_ids = fields.One2many(
        'agri.industry.variety',
        'package_id',
        string="Varieties Data"
    )

    # Pre-configured physiological stage definitions - Updated to new namespace
    physio_stage_ids = fields.One2many(
        'agri.industry.physio.stage',
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
        """Apply this package to initialize industry data and setup projects"""
        self.ensure_one()

        # 1. Create specialized project for this industry family
        project_name = _("%s Production Activity") % self.name
        project = self.env['farm.activity'].create({
            'name': project_name,
            'is_agri_activity': True,
            'activity_family': self._map_industry_to_family(self.industry_type),
        })

        # 2. Import core data
        self._import_varieties()
        self._import_physio_stages()
        self._import_task_templates()
        self._import_product_categories()

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Industry Initialized'),
                'message': _('Package "%s" applied. Project "%s" created.') % (self.name, project_name),
                'type': 'success',
            }
        }

    def _map_industry_to_family(self, industry_type):
        mapping = {
            'citrus': 'planting',
            'grains': 'planting',
            'swine': 'livestock',
            'poultry': 'livestock',
            'aquaculture': 'aquaculture',
        }
        return mapping.get(industry_type, 'planting')

    def _import_task_templates(self, project):
        """Import task templates and link to the new project"""
        for template_data in self.task_template_ids:
            self.env['project.task.type'].create({
                'name': template_data.name,
                'description': template_data.description,
                'project_ids': [(4, project.id)],
            })

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
                existing_curve = self.env['agri.biological.growth.curve'].search([
                    ('product_id', '=', product.id),
                    ('age_days', '=', stage_data.age_days)
                ], limit=1)

                if not existing_curve:
                    self.env['agri.biological.growth.curve'].create({
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
        """Import task templates from the package (Retained Duplicated Original Logic)"""
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
        """Create default industry packages - 100% FULL RESTORATION OF ORIGINAL DATA"""
        # Create citrus package
        citrus_package = self.create({
            'name': 'Citrus Cultivation Package',
            'code': 'CITRUS',
            'industry_type': 'citrus',
            'description': 'Standard data package for citrus cultivation including varieties, tasks, and growth stages.'
        })

        # Add varieties for citrus
        self.env['agri.industry.variety'].create({
            'package_id': citrus_package.id,
            'product_name': 'Oranges',
            'variety_name': 'Navel Orange',
            'agricultural_type': 'output',
            'standard_dose': 1.0,
            'growth_duration': 180,  # 6 months from planting to harvest
            'maturity_age_days': 90, # Trees mature in 90 days
            'is_biological_asset': False,
        })

        self.env['agri.industry.variety'].create({
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
        self.env['agri.industry.physio.stage'].create({
            'package_id': citrus_package.id,
            'stage_name': 'Seedling Stage',
            'age_days': 30,
            'target_weight': 0.1,
            'daily_feed_rate': 0.5,
            'related_variety': 'Navel Orange'
        })

        self.env['agri.industry.physio.stage'].create({
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
        self.env['agri.industry.variety'].create({
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
        self.env['agri.industry.physio.stage'].create({
            'package_id': swine_package.id,
            'stage_name': 'Piglet Stage',
            'age_days': 21,
            'target_weight': 6.0,
            'daily_feed_rate': 5.0,
            'related_variety': 'Yorkshire'
        })

        self.env['agri.industry.physio.stage'].create({
            'package_id': swine_package.id,
            'stage_name': 'Growing Stage',
            'age_days': 90,
            'target_weight': 50.0,
            'daily_feed_rate': 2.5,
            'related_variety': 'Yorkshire'
        })

        self.env['agri.industry.physio.stage'].create({
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
        self.env['agri.industry.variety'].create({
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

        self.env['agri.industry.variety'].create({
            'package_id': vegetables_package.id,
            'product_name': 'Tomatoes',
            'variety_name': 'Cherry Tomato',
            'agricultural_type': 'output',
            'standard_dose': 3000, # plants per mu
            'growth_duration': 90,
            'is_biological_asset': False,
        })

        # Create grains package
        grains_package = self.create({
            'name': 'Grain Cultivation Package',
            'code': 'GRAINS',
            'industry_type': 'grains',
            'description': 'Standard data package for grains (Rice/Wheat) cultivation.'
        })

        self.env['agri.industry.variety'].create({
            'package_id': grains_package.id,
            'product_name': 'Rice',
            'variety_name': 'Hybrid Rice',
            'agricultural_type': 'output',
            'standard_dose': 15, # kg seed per mu
            'growth_duration': 120,
            'is_biological_asset': False,
        })

        # Create aquaculture package
        aquaculture_package = self.create({
            'name': 'Aquaculture Package',
            'code': 'AQUA',
            'industry_type': 'aquaculture',
            'description': 'Standard data package for fish/shrimp farming.'
        })

        self.env['agri.industry.variety'].create({
            'package_id': aquaculture_package.id,
            'product_name': 'Tilapia',
            'variety_name': 'Nile Tilapia',
            'agricultural_type': 'animal',
            'growth_duration': 150,
            'is_biological_asset': True,
        })

        # Add physio stages for Grains
        self.env['agri.industry.physio.stage'].create({
            'package_id': grains_package.id,
            'stage_name': 'Tillering Stage',
            'age_days': 30,
            'related_variety': 'Hybrid Rice'
        })
        self.env['agri.industry.physio.stage'].create({
            'package_id': grains_package.id,
            'stage_name': 'Booting Stage',
            'age_days': 60,
            'related_variety': 'Hybrid Rice'
        })

        # Add physio stages for Aquaculture
        self.env['agri.industry.physio.stage'].create({
            'package_id': aquaculture_package.id,
            'stage_name': 'Fry Stage',
            'age_days': 30,
            'target_weight': 0.05,
            'related_variety': 'Nile Tilapia'
        })
        self.env['agri.industry.physio.stage'].create({
            'package_id': aquaculture_package.id,
            'stage_name': 'Fingerling Stage',
            'age_days': 60,
            'target_weight': 0.2,
            'related_variety': 'Nile Tilapia'
        })

        _logger.info("Agri Domain: ALL default industry packages (Citrus, Swine, Poultry, Dairy, Vegetables, Grains, Aqua) have been restored and created.")
    # --- End of Original Logic ---
