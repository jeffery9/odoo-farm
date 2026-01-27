from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class IndustryInitializationWizard(models.TransientModel):
    """
    US-01-08: "One-Click Initialization" Industry Master Data Package
    Provides one-click initialization of industry-specific master data
    """
    _name = 'farm.industry.initialization.wizard'
    _description = 'Industry Initialization Wizard'

    industry_type = fields.Selection([
        ('citrus', 'Citrus Fruits (柑橘类)'),
        ('livestock_pig', 'Pig Farming (生猪养殖)'),
        ('livestock_poultry', 'Poultry Farming (家禽养殖)'),
        ('tea', 'Tea Plantation (茶叶种植)'),
        ('organic_vegetables', 'Organic Vegetables (有机蔬菜)'),
        ('aquaculture', 'Aquaculture (水产养殖)'),
        ('custom', 'Custom Setup')
    ], string='Industry Type', required=True, default='citrus')

    include_varieties = fields.Boolean('Include Common Varieties', default=True)
    include_growth_stages = fields.Boolean('Include Growth Stages', default=True)
    include_agri_uom = fields.Boolean('Include Agricultural UOM', default=True)
    include_task_templates = fields.Boolean('Include Task Templates', default=True)
    include_quality_standards = fields.Boolean('Include Quality Standards', default=True)

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
                'message': _('The industry-specific master data package for %s has been successfully installed.') % dict(self.fields_get(allfields=['industry_type'])['industry_type']['selection'])[self.industry_type],
                'type': 'success',
                'sticky': False,
            }
        }

    def _initialize_citrus_data(self):
        """Initialize citrus farming industry data"""
        if self.include_varieties:
            citrus_varieties = [
                {'name': 'Navel Orange (脐橙)', 'code': 'CITRUS_NAVEL'},
                {'name': 'Pomelo (柚子)', 'code': 'CITRUS_POMELO'},
                {'name': 'Tangerine (橘子)', 'code': 'CITRUS_TANGERINE'},
                {'name': 'Lemon (柠檬)', 'code': 'CITRUS_LEMON'},
                {'name': 'Grapefruit (葡萄柚)', 'code': 'CITRUS_GRAPEFRUIT'},
            ]
            self._create_product_templates(citrus_varieties, 'plant')

        if self.include_growth_stages:
            citrus_stages = [
                ('seedling', 'Seedling (幼苗期)'),
                ('juvenile', 'Juvenile (幼树期)'),
                ('mature', 'Mature Tree (成年树)'),
                ('fruiting', 'Fruiting (结果期)'),
                ('senescence', 'Senescence (衰老期)'),
            ]
            self._create_growth_stages(citrus_stages)

        if self.include_agri_uom:
            self._create_agricultural_uom()

        if self.include_task_templates:
            citrus_tasks = [
                {
                    'name': 'Pruning (修剪)',
                    'description': 'Citrus tree pruning to maintain health and productivity',
                    'duration': 2.0,  # hours
                    'responsible_dept': 'agriculture'
                },
                {
                    'name': 'Fertilization (施肥)',
                    'description': 'Fertilization during growth period',
                    'duration': 3.0,
                    'responsible_dept': 'agriculture'
                },
                {
                    'name': 'Harvesting (采摘)',
                    'description': 'Citrus fruit harvesting',
                    'duration': 4.0,
                    'responsible_dept': 'harvesting'
                },
                {
                    'name': 'Pest Control (病虫害防治)',
                    'description': 'Integrated pest management for citrus',
                    'duration': 2.0,
                    'responsible_dept': 'quality'
                },
            ]
            self._create_task_templates(citrus_tasks)

        if self.include_quality_standards:
            self._create_quality_standards('citrus')

    def _initialize_pig_farming_data(self):
        """Initialize pig farming industry data"""
        if self.include_varieties:
            pig_varieties = [
                {'name': 'Landrace (长白猪)', 'code': 'PIG_LANDRACE'},
                {'name': 'Yorkshire (大约克夏)', 'code': 'PIG_YORKSHIRE'},
                {'name': 'Duroc (杜洛克)', 'code': 'PIG_DUROC'},
                {'name': 'Hampshire (汉普夏)', 'code': 'PIG_HAMPSHIRE'},
                {'name': 'Piglet (仔猪)', 'code': 'PIG_PIGLET'},
            ]
            self._create_product_templates(pig_varieties, 'animal')

        if self.include_growth_stages:
            pig_stages = [
                ('sow', 'Sow (母猪)'),
                ('boar', 'Boar (公猪)'),
                ('piglet', 'Piglet (仔猪)'),
                ('weaner', 'Weaner (保育猪)'),
                ('finisher', 'Finisher (育肥猪)'),
            ]
            self._create_growth_stages(pig_stages)

        if self.include_agri_uom:
            self._create_agricultural_uom()

        if self.include_task_templates:
            pig_tasks = [
                {
                    'name': 'Feeding (喂料)',
                    'description': 'Daily feeding of pigs',
                    'duration': 0.5,
                    'responsible_dept': 'agriculture'
                },
                {
                    'name': 'Health Check (健康检查)',
                    'description': 'Daily health monitoring',
                    'duration': 0.25,
                    'responsible_dept': 'veterinary'
                },
                {
                    'name': 'Breeding Management (配种管理)',
                    'description': 'Sow breeding and pregnancy monitoring',
                    'duration': 1.0,
                    'responsible_dept': 'breeding'
                },
                {
                    'name': 'Farrowing (分娩)',
                    'description': 'Farrowing assistance and piglet care',
                    'duration': 4.0,
                    'responsible_dept': 'breeding'
                },
            ]
            self._create_task_templates(pig_tasks)

        if self.include_quality_standards:
            self._create_quality_standards('pig')

    def _initialize_poultry_farming_data(self):
        """Initialize poultry farming industry data"""
        if self.include_varieties:
            poultry_varieties = [
                {'name': 'Broiler Chicken (肉鸡)', 'code': 'POULTRY_BROILER'},
                {'name': 'Layer Chicken (蛋鸡)', 'code': 'POULTRY_LAYER'},
                {'name': 'Duck (鸭)', 'code': 'POULTRY_DUCK'},
                {'name': 'Goose (鹅)', 'code': 'POULTRY_GOOSE'},
                {'name': 'Turkey (火鸡)', 'code': 'POULTRY_TURKEY'},
            ]
            self._create_product_templates(poultry_varieties, 'animal')

        if self.include_growth_stages:
            poultry_stages = [
                ('chick', 'Chick (雏禽)'),
                ('grower', 'Grower (中禽)'),
                ('adult', 'Adult (成禽)'),
                ('laying', 'Laying (产蛋期)'),
            ]
            self._create_growth_stages(poultry_stages)

        if self.include_agri_uom:
            self._create_agricultural_uom()

        if self.include_task_templates:
            poultry_tasks = [
                {
                    'name': 'Feeding (喂料)',
                    'description': 'Daily feeding of poultry',
                    'duration': 0.25,
                    'responsible_dept': 'agriculture'
                },
                {
                    'name': 'Egg Collection (捡蛋)',
                    'description': 'Daily egg collection',
                    'duration': 0.5,
                    'responsible_dept': 'harvesting'
                },
                {
                    'name': 'Health Monitoring (健康监测)',
                    'description': 'Poultry health monitoring',
                    'duration': 0.25,
                    'responsible_dept': 'veterinary'
                },
                {
                    'name': 'Culling (淘汰)',
                    'description': 'Culling of unhealthy birds',
                    'duration': 1.0,
                    'responsible_dept': 'agriculture'
                },
            ]
            self._create_task_templates(poultry_tasks)

        if self.include_quality_standards:
            self._create_quality_standards('poultry')

    def _initialize_tea_plantation_data(self):
        """Initialize tea plantation industry data"""
        if self.include_varieties:
            tea_varieties = [
                {'name': 'Longjing (龙井)', 'code': 'TEA_LONGJING'},
                {'name': 'Biluochun (碧螺春)', 'code': 'TEA_BILOOCHUN'},
                {'name': 'Tieguanyin (铁观音)', 'code': 'TEA_TIEGUANYIN'},
                {'name': 'Pu\'er (普洱)', 'code': 'TEA_PUER'},
                {'name': 'Black Tea (红茶)', 'code': 'TEA_BLACK'},
            ]
            self._create_product_templates(tea_varieties, 'plant')

        if self.include_growth_stages:
            tea_stages = [
                ('seedling', 'Seedling (茶苗)'),
                ('young_plant', 'Young Plant (幼龄期)'),
                ('mature_plant', 'Mature Plant (成龄期)'),
                ('harvesting', 'Harvesting Period (采摘期)'),
            ]
            self._create_growth_stages(tea_stages)

        if self.include_agri_uom:
            self._create_agricultural_uom()

        if self.include_task_templates:
            tea_tasks = [
                {
                    'name': 'Pruning (修剪)',
                    'description': 'Tea plant pruning for growth',
                    'duration': 3.0,
                    'responsible_dept': 'agriculture'
                },
                {
                    'name': 'Picking (采摘)',
                    'description': 'Tea leaf picking',
                    'duration': 4.0,
                    'responsible_dept': 'harvesting'
                },
                {
                    'name': 'Processing (加工)',
                    'description': 'Tea processing and drying',
                    'duration': 8.0,
                    'responsible_dept': 'processing'
                },
                {
                    'name': 'Fertilization (施肥)',
                    'description': 'Tea plant fertilization',
                    'duration': 2.0,
                    'responsible_dept': 'agriculture'
                },
            ]
            self._create_task_templates(tea_tasks)

        if self.include_quality_standards:
            self._create_quality_standards('tea')

    def _initialize_organic_vegetables_data(self):
        """Initialize organic vegetables industry data"""
        if self.include_varieties:
            veg_varieties = [
                {'name': 'Organic Lettuce (有机生菜)', 'code': 'VEG_LETTUCE'},
                {'name': 'Organic Tomato (有机番茄)', 'code': 'VEG_TOMATO'},
                {'name': 'Organic Cucumber (有机黄瓜)', 'code': 'VEG_CUCUMBER'},
                {'name': 'Organic Carrot (有机胡萝卜)', 'code': 'VEG_CARROT'},
                {'name': 'Organic Spinach (有机菠菜)', 'code': 'VEG_SPINACH'},
            ]
            self._create_product_templates(veg_varieties, 'plant')

        if self.include_growth_stages:
            veg_stages = [
                ('seed', 'Seed (播种期)'),
                ('germination', 'Germination (发芽期)'),
                ('seedling', 'Seedling (幼苗期)'),
                ('vegetative', 'Vegetative (生长期)'),
                ('harvestable', 'Harvestable (采收期)'),
            ]
            self._create_growth_stages(veg_stages)

        if self.include_agri_uom:
            self._create_agricultural_uom()

        if self.include_task_templates:
            veg_tasks = [
                {
                    'name': 'Seeding (播种)',
                    'description': 'Vegetable seeding',
                    'duration': 2.0,
                    'responsible_dept': 'agriculture'
                },
                {
                    'name': 'Transplanting (移栽)',
                    'description': 'Seedling transplanting',
                    'duration': 3.0,
                    'responsible_dept': 'agriculture'
                },
                {
                    'name': 'Organic Pest Control (有机虫害防治)',
                    'description': 'Organic pest control methods',
                    'duration': 1.5,
                    'responsible_dept': 'quality'
                },
                {
                    'name': 'Harvesting (采收)',
                    'description': 'Vegetable harvesting',
                    'duration': 2.5,
                    'responsible_dept': 'harvesting'
                },
            ]
            self._create_task_templates(veg_tasks)

        if self.include_quality_standards:
            self._create_quality_standards('vegetable')

    def _initialize_aquaculture_data(self):
        """Initialize aquaculture industry data"""
        if self.include_varieties:
            fish_varieties = [
                {'name': 'Common Carp (鲤鱼)', 'code': 'FISH_CARP'},
                {'name': 'Tilapia (罗非鱼)', 'code': 'FISH_TILAPIA'},
                {'name': 'Catfish (鲶鱼)', 'code': 'FISH_CATFISH'},
                {'name': 'Pond Loach (泥鳅)', 'code': 'FISH_LOACH'},
                {'name': 'Freshwater Prawn (淡水虾)', 'code': 'PRAWN_FRESH'},
            ]
            self._create_product_templates(fish_varieties, 'animal')

        if self.include_growth_stages:
            fish_stages = [
                ('egg', 'Egg (鱼卵)'),
                ('fry', 'Fry (鱼苗)'),
                ('fingerling', 'Fingerling (鱼种)'),
                ('adult', 'Adult Fish (成鱼)'),
            ]
            self._create_growth_stages(fish_stages)

        if self.include_agri_uom:
            self._create_agricultural_uom()

        if self.include_task_templates:
            aqua_tasks = [
                {
                    'name': 'Feeding (喂食)',
                    'description': 'Daily fish feeding',
                    'duration': 0.5,
                    'responsible_dept': 'agriculture'
                },
                {
                    'name': 'Water Quality Check (水质检测)',
                    'description': 'Water quality monitoring',
                    'duration': 1.0,
                    'responsible_dept': 'quality'
                },
                {
                    'name': 'Harvesting (捕捞)',
                    'description': 'Fish harvesting',
                    'duration': 4.0,
                    'responsible_dept': 'harvesting'
                },
                {
                    'name': 'Pond Maintenance (池塘维护)',
                    'description': 'Pond cleaning and maintenance',
                    'duration': 6.0,
                    'responsible_dept': 'maintenance'
                },
            ]
            self._create_task_templates(aqua_tasks)

        if self.include_quality_standards:
            self._create_quality_standards('fish')

    def _initialize_custom_data(self):
        """Initialize custom industry data (placeholder)"""
        # This would typically trigger a custom setup process
        pass

    def _create_product_templates(self, varieties, product_type):
        """Create product templates for the specified varieties"""
        ProductTemplate = self.env['product.template']

        for variety in varieties:
            product_template = ProductTemplate.search([('code', '=', variety['code'])], limit=1)
            if not product_template:
                ProductTemplate.create({
                    'name': variety['name'],
                    'default_code': variety['code'],
                    'type': 'product',
                    'categ_id': self.env.ref('product.product_category_1').id,
                    'list_price': 10.0,
                    'standard_price': 5.0,
                    # Add agricultural specific fields if they exist
                    'is_biological_asset': True if product_type == 'animal' else False,
                    'maturity_age_days': 180,  # Default maturity age
                })

    def _create_growth_stages(self, stages):
        """Create growth stage records"""
        # This would typically add stages to a specific growth stage model
        # For now, we'll log the creation of stages
        _logger.info(f"Growth stages initialized: {stages}")

    def _create_agricultural_uom(self):
        """Create common agricultural UOMs and conversion factors"""
        Uom = self.env['uom.uom']

        # Add some common agricultural UOMs if they don't exist
        agri_uoms = [
            {
                'name': 'mu (亩)',
                'category_id': self.env.ref('uom.product_uom_categ_area').id,
                'factor': 666.67,  # 1 mu = 666.67 m2
                'rounding': 0.01,
            },
            {
                'name': 'jin (斤)',
                'category_id': self.env.ref('uom.product_uom_categ_weight').id,
                'factor': 2.0,  # 1 kg = 2 jin
                'rounding': 0.01,
            },
        ]

        for uom_data in agri_uoms:
            existing = Uom.search([('name', '=', uom_data['name'])], limit=1)
            if not existing:
                Uom.create(uom_data)

    def _create_task_templates(self, tasks):
        """Create project task templates"""
        ProjectTaskType = self.env['project.task.type']

        for task in tasks:
            ProjectTaskType.create({
                'name': task['name'],
                'description': task['description'],
                'fold': False  # Not folded by default
            })

    def _create_quality_standards(self, type_code):
        """Create quality standards based on product type"""
        QualityStandard = self.env['quality.control.standard']

        standards = []
        if type_code == 'citrus':
            standards = [
                {'name': 'Citrus Fruit Quality Standard', 'code': 'QCS-CIT-001', 'description': 'Citrus fruit grading and quality metrics'},
                {'name': 'Citrus Pesticide Residue Standard', 'code': 'QCS-CIT-002', 'description': 'Maximum residue limits for pesticides in citrus'},
            ]
        elif type_code == 'pig':
            standards = [
                {'name': 'Pork Meat Quality Standard', 'code': 'QCS-PIG-001', 'description': 'Meat quality and safety standards'},
                {'name': 'Livestock Health Standard', 'code': 'QCS-PIG-002', 'description': 'Animal health and welfare standards'},
            ]
        elif type_code == 'poultry':
            standards = [
                {'name': 'Poultry Meat Quality Standard', 'code': 'QCS-POUL-001', 'description': 'Poultry meat quality metrics'},
                {'name': 'Egg Quality Standard', 'code': 'QCS-POUL-002', 'description': 'Egg grading and quality standards'},
            ]
        elif type_code == 'tea':
            standards = [
                {'name': 'Tea Leaf Quality Standard', 'code': 'QCS-TEA-001', 'description': 'Tea leaf grading standards'},
                {'name': 'Organic Tea Standard', 'code': 'QCS-TEA-002', 'description': 'Organic certification requirements for tea'},
            ]
        elif type_code == 'vegetable':
            standards = [
                {'name': 'Organic Vegetable Standard', 'code': 'QCS-VEG-001', 'description': 'Organic certification requirements'},
                {'name': 'Vegetable Freshness Standard', 'code': 'QCS-VEG-002', 'description': 'Freshness and shelf-life standards'},
            ]
        elif type_code == 'fish':
            standards = [
                {'name': 'Aquaculture Quality Standard', 'code': 'QCS-FISH-001', 'description': 'Aquaculture product quality standards'},
                {'name': 'Food Safety Standard', 'code': 'QCS-FISH-002', 'description': 'Food safety and hygiene standards'},
            ]

        for standard in standards:
            existing = QualityStandard.search([('code', '=', standard['code'])], limit=1)
            if not existing:
                QualityStandard.create({
                    'name': standard['name'],
                    'code': standard['code'],
                    'description': standard['description'],
                    'inspection_criteria': 'Standard inspection criteria for ' + standard['name'],
                    'quality_threshold': 90.0,  # Default quality threshold
                    'inspection_frequency': 'daily',
                })