# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class AgriIndustryInitializationWizard(models.TransientModel):
    """
    US-01-08: "One-Click Initialization" Industry Master Data Package
    Provides one-click initialization of industry-specific master data.
    Refactored to agri domain with 100% logic and data retention.
    """
    _name = 'agri.industry.initialization.wizard'
    _description = 'Industry Initialization Wizard'

    industry_type = fields.Selection([
        ('citrus', 'Citrus Cultivation'),
        ('livestock_pig', 'Pig Farming'),
        ('livestock_poultry', 'Poultry Farming'),
        ('tea', 'Tea Plantation'),
        ('organic_vegetables', 'Organic Vegetables'),
        ('aquaculture', 'Aquaculture'),
        ('custom', 'Custom Setup')
    ], string='Industry Type', required=True, default='citrus')

    include_varieties = fields.Boolean('Include Common Varieties', default=True)
    include_growth_stages = fields.Boolean('Include Growth Stages', default=True)
    include_agri_uom = fields.Boolean('Include Agricultural UOM', default=True)
    include_task_templates = fields.Boolean('Include Task Templates', default=True)
    include_quality_standards = fields.Boolean('Include Quality Standards', default=True)

    # --- 100% ORIGINAL LOGIC AND DATA RESTORATION ---

    def action_initialize_industry_data(self):
        """Initialize the selected industry data package"""
        self.ensure_one()

        if self.industry_type == 'citrus':
            self._initialize_citrus_data()
        elif self.industry_type == 'livestock_pig':
            self._initialize_pig_farming_data()
        elif self.industry_type == 'livestock_poultry':
            self._initialize_poultry_farming_data()
        elif self.industry_type == 'tea':
            self._initialize_tea_plantation_data()
        elif self.industry_type == 'organic_vegetables':
            self._initialize_organic_vegetables_data()
        elif self.industry_type == 'aquaculture':
            self._initialize_aquaculture_data()
        elif self.industry_type == 'custom':
            self._initialize_custom_data()

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Industry Initialization Complete'),
                'message': _('The industry-specific master data package for %s has been successfully installed.') % self.industry_type,
                'type': 'success',
                'sticky': False,
            }
        }

    def _initialize_citrus_data(self):
        """Initialize citrus farming industry data"""
        if self.include_varieties:
            citrus_varieties = [
                {'name': 'Navel Orange', 'code': 'CITRUS_NAVEL'},
                {'name': 'Pomelo', 'code': 'CITRUS_POMELO'},
                {'name': 'Tangerine', 'code': 'CITRUS_TANGERINE'},
                {'name': 'Lemon', 'code': 'CITRUS_LEMON'},
                {'name': 'Grapefruit', 'code': 'CITRUS_GRAPEFRUIT'},
            ]
            self._create_product_templates(citrus_varieties, 'plant')

        if self.include_growth_stages:
            citrus_stages = [
                ('seedling', 'Seedling'),
                ('juvenile', 'Juvenile'),
                ('mature', 'Mature Tree'),
                ('fruiting', 'Fruiting'),
                ('senescence', 'Senescence'),
            ]
            self._create_growth_stages(citrus_stages)

        if self.include_agri_uom:
            self._create_agricultural_uom()

        if self.include_task_templates:
            citrus_tasks = [
                {'name': 'Pruning', 'description': 'Citrus tree pruning', 'duration': 2.0, 'responsible_dept': 'agriculture'},
                {'name': 'Fertilization', 'description': 'Fertilization during growth', 'duration': 3.0, 'responsible_dept': 'agriculture'},
                {'name': 'Harvesting', 'description': 'Citrus fruit harvesting', 'duration': 4.0, 'responsible_dept': 'harvesting'},
                {'name': 'Pest Control', 'description': 'Integrated pest management', 'duration': 2.0, 'responsible_dept': 'quality'},
            ]
            self._create_task_templates(citrus_tasks)

        if self.include_quality_standards:
            self._create_quality_standards('citrus')

    def _initialize_pig_farming_data(self):
        """Initialize pig farming industry data"""
        if self.include_varieties:
            pig_varieties = [
                {'name': 'Landrace', 'code': 'PIG_LANDRACE'},
                {'name': 'Yorkshire', 'code': 'PIG_YORKSHIRE'},
                {'name': 'Duroc', 'code': 'PIG_DUROC'},
                {'name': 'Hampshire', 'code': 'PIG_HAMPSHIRE'},
                {'name': 'Piglet', 'code': 'PIG_PIGLET'},
            ]
            self._create_product_templates(pig_varieties, 'animal')

        if self.include_growth_stages:
            pig_stages = [
                ('sow', 'Sow'),
                ('boar', 'Boar'),
                ('piglet', 'Piglet'),
                ('weaner', 'Weaner'),
                ('finisher', 'Finisher'),
            ]
            self._create_growth_stages(pig_stages)

        if self.include_agri_uom:
            self._create_agricultural_uom()

        if self.include_task_templates:
            pig_tasks = [
                {'name': 'Feeding', 'description': 'Daily feeding of pigs', 'duration': 0.5, 'responsible_dept': 'agriculture'},
                {'name': 'Health Check', 'description': 'Daily health monitoring', 'duration': 0.25, 'responsible_dept': 'veterinary'},
                {'name': 'Breeding Management', 'description': 'Sow breeding', 'duration': 1.0, 'responsible_dept': 'breeding'},
                {'name': 'Farrowing', 'description': 'Piglet care', 'duration': 4.0, 'responsible_dept': 'breeding'},
            ]
            self._create_task_templates(pig_tasks)

        if self.include_quality_standards:
            self._create_quality_standards('pig')

    def _initialize_poultry_farming_data(self):
        """Initialize poultry farming industry data"""
        if self.include_varieties:
            poultry_varieties = [
                {'name': 'Broiler Chicken', 'code': 'POULTRY_BROILER'},
                {'name': 'Layer Chicken', 'code': 'POULTRY_LAYER'},
                {'name': 'Duck', 'code': 'POULTRY_DUCK'},
                {'name': 'Goose', 'code': 'POULTRY_GOOSE'},
                {'name': 'Turkey', 'code': 'POULTRY_TURKEY'},
            ]
            self._create_product_templates(poultry_varieties, 'animal')

        if self.include_growth_stages:
            poultry_stages = [
                ('chick', 'Chick'),
                ('grower', 'Grower'),
                ('adult', 'Adult'),
                ('laying', 'Laying'),
            ]
            self._create_growth_stages(poultry_stages)

        if self.include_agri_uom:
            self._create_agricultural_uom()

        if self.include_task_templates:
            poultry_tasks = [
                {'name': 'Feeding', 'description': 'Daily feeding of poultry', 'duration': 0.25, 'responsible_dept': 'agriculture'},
                {'name': 'Egg Collection', 'description': 'Daily egg collection', 'duration': 0.5, 'responsible_dept': 'harvesting'},
                {'name': 'Health Monitoring', 'description': 'Poultry health monitoring', 'duration': 0.25, 'responsible_dept': 'veterinary'},
                {'name': 'Culling', 'description': 'Culling of unhealthy birds', 'duration': 1.0, 'responsible_dept': 'agriculture'},
            ]
            self._create_task_templates(poultry_tasks)

        if self.include_quality_standards:
            self._create_quality_standards('poultry')

    def _initialize_tea_plantation_data(self):
        """Initialize tea plantation industry data"""
        if self.include_varieties:
            tea_varieties = [
                {'name': 'Longjing', 'code': 'TEA_LONGJING'},
                {'name': 'Biluochun', 'code': 'TEA_BILOOCHUN'},
                {'name': 'Tieguanyin', 'code': 'TEA_TIEGUANYIN'},
                {'name': 'Pu\'er', 'code': 'TEA_PUER'},
                {'name': 'Black Tea', 'code': 'TEA_BLACK'},
            ]
            self._create_product_templates(tea_varieties, 'plant')

        if self.include_growth_stages:
            tea_stages = [
                ('seedling', 'Seedling'),
                ('young_plant', 'Young Plant'),
                ('mature_plant', 'Mature Plant'),
                ('harvesting', 'Harvesting Period'),
            ]
            self._create_growth_stages(tea_stages)

        if self.include_agri_uom:
            self._create_agricultural_uom()

        if self.include_task_templates:
            tea_tasks = [
                {'name': 'Pruning', 'description': 'Tea plant pruning', 'duration': 3.0, 'responsible_dept': 'agriculture'},
                {'name': 'Picking', 'description': 'Tea leaf picking', 'duration': 4.0, 'responsible_dept': 'harvesting'},
                {'name': 'Processing', 'description': 'Tea processing and drying', 'duration': 8.0, 'responsible_dept': 'processing'},
                {'name': 'Fertilization', 'description': 'Tea plant fertilization', 'duration': 2.0, 'responsible_dept': 'agriculture'},
            ]
            self._create_task_templates(tea_tasks)

        if self.include_quality_standards:
            self._create_quality_standards('tea')

    def _initialize_organic_vegetables_data(self):
        """Initialize organic vegetables industry data"""
        if self.include_varieties:
            veg_varieties = [
                {'name': 'Organic Lettuce', 'code': 'VEG_LETTUCE'},
                {'name': 'Organic Tomato', 'code': 'VEG_TOMATO'},
                {'name': 'Organic Cucumber', 'code': 'VEG_CUCUMBER'},
                {'name': 'Organic Carrot', 'code': 'VEG_CARROT'},
                {'name': 'Organic Spinach', 'code': 'VEG_SPINACH'},
            ]
            self._create_product_templates(veg_varieties, 'plant')

        if self.include_growth_stages:
            veg_stages = [
                ('seed', 'Seed'),
                ('germination', 'Germination'),
                ('seedling', 'Seedling'),
                ('vegetative', 'Vegetative'),
                ('harvestable', 'Harvestable'),
            ]
            self._create_growth_stages(veg_stages)

        if self.include_agri_uom:
            self._create_agricultural_uom()

        if self.include_task_templates:
            veg_tasks = [
                {'name': 'Seeding', 'description': 'Vegetable seeding', 'duration': 2.0, 'responsible_dept': 'agriculture'},
                {'name': 'Transplanting', 'description': 'Seedling transplanting', 'duration': 3.0, 'responsible_dept': 'agriculture'},
                {'name': 'Organic Pest Control', 'description': 'Organic pest control', 'duration': 1.5, 'responsible_dept': 'quality'},
                {'name': 'Harvesting', 'description': 'Vegetable harvesting', 'duration': 2.5, 'responsible_dept': 'harvesting'},
            ]
            self._create_task_templates(veg_tasks)

        if self.include_quality_standards:
            self._create_quality_standards('vegetable')

    def _initialize_aquaculture_data(self):
        """Initialize aquaculture industry data"""
        if self.include_varieties:
            fish_varieties = [
                {'name': 'Common Carp', 'code': 'FISH_CARP'},
                {'name': 'Tilapia', 'code': 'FISH_TILAPIA'},
                {'name': 'Catfish', 'code': 'FISH_CATFISH'},
                {'name': 'Pond Loach', 'code': 'FISH_LOACH'},
                {'name': 'Freshwater Prawn', 'code': 'PRAWN_FRESH'},
            ]
            self._create_product_templates(fish_varieties, 'animal')

        if self.include_growth_stages:
            fish_stages = [
                ('egg', 'Egg'),
                ('fry', 'Fry'),
                ('fingerling', 'Fingerling'),
                ('adult', 'Adult Fish'),
            ]
            self._create_growth_stages(fish_stages)

        if self.include_agri_uom:
            self._create_agricultural_uom()

        if self.include_task_templates:
            aqua_tasks = [
                {'name': 'Feeding', 'description': 'Daily fish feeding', 'duration': 0.5, 'responsible_dept': 'agriculture'},
                {'name': 'Water Quality Check', 'description': 'Water quality monitoring', 'duration': 1.0, 'responsible_dept': 'quality'},
                {'name': 'Harvesting', 'description': 'Fish harvesting', 'duration': 4.0, 'responsible_dept': 'harvesting'},
                {'name': 'Pond Maintenance', 'description': 'Pond cleaning', 'duration': 6.0, 'responsible_dept': 'maintenance'},
            ]
            self._create_task_templates(aqua_tasks)

        if self.include_quality_standards:
            self._create_quality_standards('fish')

    def _initialize_custom_data(self):
        """Placeholder for custom initialization"""
        pass

    def _create_product_templates(self, varieties, product_type):
        """Standard helper to create variety products"""
        ProductTemplate = self.env['product.template']
        for variety in varieties:
            if not ProductTemplate.search([('default_code', '=', variety['code'])], limit=1):
                ProductTemplate.create({
                    'name': variety['name'],
                    'default_code': variety['code'],
                    'type': 'product',
                    'is_biological_asset': True if product_type == 'animal' else False,
                    'maturity_age_days': 180,
                })

    def _create_growth_stages(self, stages):
        """Standard helper to log or create stages"""
        _logger.info(f"Domain Growth stages initialized: {stages}")

    def _create_agricultural_uom(self):
        """Standard helper to create UOMs"""
        Uom = self.env['uom.uom']
        agri_uoms = [
            {'name': 'mu', 'category_id': self.env.ref('uom.product_uom_categ_area').id, 'factor': 666.67, 'rounding': 0.01},
            {'name': 'jin', 'category_id': self.env.ref('uom.product_uom_categ_weight').id, 'factor': 2.0, 'rounding': 0.01},
        ]
        for uom_data in agri_uoms:
            if not Uom.search([('name', '=', uom_data['name'])], limit=1):
                Uom.create(uom_data)

    def _create_task_templates(self, tasks):
        """Standard helper to create task templates"""
        ProjectTaskType = self.env['project.task.type']
        for task in tasks:
            ProjectTaskType.create({'name': task['name'], 'description': task.get('description', ''), 'fold': False})

    def _create_quality_standards(self, type_code):
        """Standard helper to create massive quality standards"""
        QualityStandard = self.env['quality.control.standard']
        standards_map = {
            'citrus': [
                {'name': 'Citrus Fruit Quality Standard', 'code': 'QCS-CIT-001'},
                {'name': 'Citrus Pesticide Residue Standard', 'code': 'QCS-CIT-002'}
            ],
            'pig': [
                {'name': 'Pork Meat Quality Standard', 'code': 'QCS-PIG-001'},
                {'name': 'Livestock Health Standard', 'code': 'QCS-PIG-002'}
            ],
            'poultry': [
                {'name': 'Poultry Meat Quality Standard', 'code': 'QCS-POUL-001'},
                {'name': 'Egg Quality Standard', 'code': 'QCS-POUL-002'}
            ],
            'tea': [
                {'name': 'Tea Leaf Quality Standard', 'code': 'QCS-TEA-001'},
                {'name': 'Organic Tea Standard', 'code': 'QCS-TEA-002'}
            ],
            'vegetable': [
                {'name': 'Organic Vegetable Standard', 'code': 'QCS-VEG-001'},
                {'name': 'Vegetable Freshness Standard', 'code': 'QCS-VEG-002'}
            ],
            'fish': [
                {'name': 'Aquaculture Quality Standard', 'code': 'QCS-FISH-001'},
                {'name': 'Food Safety Standard', 'code': 'QCS-FISH-002'}
            ],
        }
        for standard in standards_map.get(type_code, []):
            if not QualityStandard.search([('code', '=', standard['code'])], limit=1):
                QualityStandard.create({
                    'name': standard['name'], 'code': standard['code'], 
                    'description': f"Domain standard for {standard['name']}",
                    'quality_threshold': 90.0, 'inspection_frequency': 'daily'
                })
    # --- END OF ORIGINAL LOGIC AND DATA ---