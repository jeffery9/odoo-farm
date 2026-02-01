# Farm Management System - Model Summary

This document provides a comprehensive overview of all the models in the farm management system, organized by functional module with detailed field definitions and relationships.


## Table of Contents
1. [Core Models](#core-models)
2. [Land Management Models](#land-management-models)
3. [Planning Models](#planning-models)
4. [Operation Models](#operation-models)
5. [Equipment Models](#equipment-models)
6. [HR Models](#hr-models)
7. [MRP Models](#mrp-models)
8. [Field Crops Models](#field-crops-models)
9. [Livestock Models](#livestock-models)
10. [Aquaculture Models](#aquaculture-models)
11. [Specialized Farming Models](#specialized-farming-models)
12. [Processing Models](#processing-models)
13. [Quality Models](#quality-models)
14. [Safety Models](#safety-models)
15. [Certification Models](#certification-models)
16. [Weather Models](#weather-models)
17. [IoT Models](#iot-models)
18. [Mobile Models](#mobile-models)
19. [Supply Models](#supply-models)
20. [Logistics Models](#logistics-models)
21. [Multi-Farm Models](#multi-farm-models)
22. [Marketing Models](#marketing-models)
23. [Financial Models](#financial-models)
24. [Waste Management Models](#waste-management-models)
25. [Support Models](#support-models)
26. [Abstract and Mixin Models](#abstract-and-mixin-models)

## Core Models

The core models form the foundation of the farm management system, providing essential functionality for tracking farm locations, activities, and biological assets.

### Basic Farm Management
- **farm_core.FarmLocation** (`farm.location`): Represents farm locations and land parcels
  - Odoo Model: `class FarmLocation(models.Model)`
  - _name: `farm.location`
  - _description: "Farm Location & Land Parcel"
  - Fields:
    - `is_land_parcel` (Boolean): Is Land Parcel flag
    - `land_nature` (Selection): Classification based on land use guidelines
    - `land_area` (Float): Surface area of the parcel
    - `land_area_uom_id` (Many2one): Area unit of measure (uom.uom)
    - `gps_lat` (Float): Latitude coordinates
    - `gps_lng` (Float): Longitude coordinates
    - `boundary_geojson` (Text): GeoJSON polygon for boundaries
    - `calculated_area_ha` (Float): Area calculated from GeoJSON (computed)
    - `soil_type` (Selection): Type of soil
    - `slope` (Float): Slope gradient percentage
    - `aspect` (Selection): Aspect/orientation
    - `water_source` (Selection): Primary water source
    - `micro_climate_notes` (Text): Local climate characteristics
    - `soil_mineral_composition` (Text): Mineral composition of soil
    - `is_vertical_location` (Boolean): Is vertical/shelf location
    - `shelf_id` (Char): Shelf identifier
    - `shelf_level` (Integer): Level/row number
    - `shelf_slot` (Char): Slot/position identifier
    - `gis_map_url` (Char): Computed map URL (computed)
    - `soil_analysis_ids` (One2many): Linked soil analyses (farm.soil.analysis)
    - `latest_ph` (Float): Latest pH level from analyses (computed, stored)
    - `latest_organic_matter` (Float): Latest organic matter percentage (computed, stored)
    - `water_depth` (Float): Water depth in meters
    - `water_depth_dm` (Float): Water depth in decimeters (computed/inverse)
    - `is_vessel` (Boolean): Is vessel/tank flag
    - `vessel_capacity` (Float): Vessel capacity in liters
    - `vessel_material` (Selection): Material type of vessel
    - `farm_id` (Many2one): Belonging farm (res.company)
    - `location_properties_definition` (PropertiesDefinition): Properties definition
    - `location_properties` (Properties): Dynamic properties
    - `total_n_input` (Float): Accumulated nitrogen in kg (computed)
    - `total_p_input` (Float): Accumulated phosphorus in kg (computed)
    - `total_k_input` (Float): Accumulated potassium in kg (computed)
    - `target_n_per_mu` (Float): Target nitrogen per mu
    - `target_p_per_mu` (Float): Target phosphorus per mu
    - `target_k_per_mu` (Float): Target potassium per mu
    - `n_balance_status` (Float): Nitrogen surplus/deficit (computed)
    - `p_balance_status` (Float): Phosphorus surplus/deficit (computed)
    - `k_balance_status` (Float): Potassium surplus/deficit (computed)
  - Methods:
    - `_compute_gis_map_url()`: Computes GIS map URL from coordinates
    - `_compute_latest_soil_stats()`: Computes latest soil statistics
    - `_compute_water_depth_dm()`: Computes water depth in decimeters
    - `_inverse_water_depth_dm()`: Inverse function for water depth
    - `_compute_nutrient_balance()`: Computes accumulated nutrient balance
    - `_compute_balance_status()`: Computes nutrient surplus/deficit status
  - Relationships:
    - One2many: `soil_analysis_ids` → `farm.soil.analysis.location_id`
    - Many2one: `land_area_uom_id` → `uom.uom`
    - Many2one: `farm_id` → `res.company`
    - Inherits from: `mail.thread`, `mail.activity.mixin`, `stock.location`, `farm.core.gis.utils`

- **farm_core.SoilAnalysis** (`farm.soil.analysis`): Manages soil analysis data for farm locations
  - Odoo Model: `class SoilAnalysis(models.Model)`
  - _name: `farm.soil.analysis`
  - _description: "Soil Analysis Report"
  - _order: "analysis_date desc"
  - Fields:
    - `name` (Char): Report reference (required, default: New)
    - `location_id` (Many2one): Land parcel the analysis belongs to (required)
    - `analysis_date` (Date): Date of analysis (default: today)
    - `laboratory_id` (Many2one): Laboratory that performed the analysis
    - `ph_level` (Float): pH level with 2 decimal digits
    - `organic_matter` (Float): Organic matter percentage
    - `nitrogen_content` (Float): Nitrogen content in mg/kg
    - `phosphorus_content` (Float): Phosphorus content in mg/kg
    - `potassium_content` (Float): Potassium content in mg/kg
    - `magnesium` (Float): Magnesium content in mg/kg
    - `calcium` (Float): Calcium content in mg/kg
    - `recommendation` (Text): Fertilization recommendations
    - `state` (Selection): Status (draft, done, cancel)
  - Methods:
    - `create()`: Creates new soil analysis with sequence code
    - `action_validate()`: Validates the soil analysis
  - Relationships:
    - Many2one: `location_id` → `farm.location`
    - Many2one: `laboratory_id` → `res.partner`
    - Inherits from: `mail.thread`, `mail.activity.mixin`

- **farm_core.FarmActivity**: Represents farm activities and operations
- **farm_core.FarmTask**: Represents tasks related to farm activities

### Configuration and Setup
- **farm_core.IndustryDataPackage**: Configuration model for industry data packages
- **farm_core.IndustryVariety**: Configuration model for industry varieties
- **farm_core.IndustryPhysioStage**: Configuration model for industry physiological stages
- **farm_core.IndustryUOMConversion**: Configuration model for unit of measure conversions
- **farm_core.IndustryTaskTemplate**: Configuration model for industry task templates
- **farm_core.IndustryProductCategory**: Configuration model for industry product categories
- **farm_core.FarmGrowthCurve**: Configuration model for farm growth curves

### Biological Assets
- **farm_core.BiologicalAsset** (`farm.biological.asset`): Represents biological assets in farming operations
  - Odoo Model: `class BiologicalAsset(models.Model)`
  - _name: `farm.biological.asset`
  - _description: "Biological Asset"
  - Fields:
    - `name` (Char): Asset name (required, default: New)
    - `lot_id` (Many2one): Stock lot for the biological asset (required)
    - `agricultural_type` (Selection): Asset type (animal, plant, tree)
    - `birth_date` (Date): Birth/germination date
    - `gender` (Selection): Gender (male, female, other)
    - `father_id` (Many2one): Father biological asset
    - `mother_id` (Many2one): Mother biological asset
    - `growth_stage` (Selection): Growth stage (newborn, growing, mature, harvested)
    - `is_mature` (Boolean): Is mature flag (computed, stored)
    - `generation` (Selection): Generation (G0-G3)
    - `quality_grade` (Selection): Quality grade (A, B, C)
    - `valuation_ids` (One2many): Asset valuations (farm.biological.asset.valuation)
    - `current_valuation` (Float): Current valuation (computed, stored)
    - `maturity_date` (Date): Maturity date (computed, stored)
  - Methods:
    - `_compute_maturity_date()`: Computes maturity date based on birth date and product maturity age
    - `_compute_is_mature_from_age()`: Computes if asset is mature based on actual dates
    - `_compute_current_valuation()`: Computes current valuation from active valuation records
    - `_cron_check_maturity_and_transfer_asset()`: Cron method to check maturity and transfer asset costs
    - `_process_maturity_transfer()`: Processes cost transfer when biological asset reaches maturity
  - Relationships:
    - Many2one: `lot_id` → `stock.lot`
    - Many2one: `father_id` → `farm.biological.asset`
    - Many2one: `mother_id` → `farm.biological.asset`
    - One2many: `valuation_ids` → `farm.biological.asset.valuation.asset_id`
    - Inherits from: `mail.thread`, `mail.activity.mixin`, `farm.core.creation.method.mixin`, `farm.core.computed.field.mixin`, `farm.core.compliance.mixin`

- **farm_core.BiologicalAssetValuation** (`farm.biological.asset.valuation`): Manages valuation of biological assets
  - Odoo Model: `class BiologicalAssetValuation(models.Model)`
  - _name: `farm.biological.asset.valuation`
  - _description: "Biological Asset Valuation and Depreciation"
  - _order: "create_date desc"
  - Fields:
    - `asset_id` (Many2one): Biological asset being valued (required)
    - `original_value` (Float): Original cost/value (required)
    - `growth_stage_coefficient` (Float): Value coefficient based on growth stage
    - `depreciation_years` (Float): Number of years for depreciation
    - `annual_depreciation_rate` (Float): Annual depreciation percentage
    - `accumulated_depreciation` (Float): Total depreciation accumulated (computed, stored)
    - `net_book_value` (Float): Current book value after depreciation (computed, stored)
    - `stage_coefficient_ids` (One2many): Growth stage coefficients (farm.biological.asset.stage.coefficient)
    - `state` (Selection): Status (active, disposed, depreciated)
  - Methods:
    - `action_create_depreciation_entry()`: Creates depreciation journal entry for the biological asset
    - `_compute_accumulated_depreciation()`: Calculates accumulated depreciation based on time passed and depreciation rate
    - `_compute_net_book_value()`: Calculates net book value after depreciation
    - `_onchange_asset_id()`: Auto-populates valuation parameters based on product settings
  - Relationships:
    - Many2one: `asset_id` → `farm.biological.asset`
    - One2many: `stage_coefficient_ids` → `farm.biological.asset.stage.coefficient.valuation_id`
    - Inherits from: Ordered by create date

- **farm_core.BiologicalAssetStageCoefficient** (`farm.biological.asset.stage.coefficient`): Defines stage coefficients for biological asset valuation
  - Odoo Model: `class BiologicalAssetStageCoefficient(models.Model)`
  - _name: `farm.biological.asset.stage.coefficient`
  - _description: "Biological Asset Stage Coefficient"
  - Fields:
    - `valuation_id` (Many2one): Valuation record (required, ondelete=cascade)
    - `biological_stage` (Selection): Growth stage (newborn, growing, mature, harvested)
    - `coefficient` (Float): Value coefficient multiplier
    - `description` (Char): Description of coefficient
  - Methods:
    - `_onchange_biological_stage()`: Sets default coefficient based on growth stage
  - Relationships:
    - Many2one: `valuation_id` → `farm.biological.asset.valuation` with cascade delete

### Geographic and Spatial
- **farm_core.FarmGeofence**: Geofencing management for farm locations
- **farm_core.GISCoordinateUtils** (Abstract): Provides GIS coordinate utilities

### Common Utilities
- **farm_core.CommonAgriculturalFields** (Abstract): Provides common agricultural fields across models
- **farm_core.CreationMethodMixin** (Abstract): Provides creation method utilities
- **farm_core.ComputedFieldMixin** (Abstract): Provides computed field utilities
- **farm_core.ComplianceMixin** (Abstract): Provides compliance utilities

## Land Management Models

Land management models handle the tracking and management of farm locations and land use.

- **farm_land_mgmt.FarmLocation**: Represents farm locations and land management
- **farm_land_mgmt.FarmActivity**: Represents farm activities in land management
- **farm_land_mgmt.ProjectTask**: Project tasks for land management operations

## Planning Models

Planning models handle agricultural planning and scenario management.

- **farm_planning.AgriInterventionTemplate** (`agri.intervention.template`): Templates for agricultural interventions
  - Odoo Model: `class AgriInterventionTemplate(models.Model)`
  - _name: `agri.intervention.template`
  - _description: "Agricultural Intervention Template"
  - Fields:
    - `name` (Char): Operation name (required)
    - `intervention_type` (Selection): Category (tillage, sowing, fertilizing, protection, harvesting)
    - `input_ids` (One2many): Estimated inputs (agri.intervention.template.input)
    - `estimated_labor_hours` (Float): Estimated labor in hours (default: 1.0)
  - Relationships:
    - One2many: `input_ids` → `agri.intervention.template.input.template_id`

- **farm_planning.AgriInterventionTemplateInput** (`agri.intervention.template.input`): Input templates for interventions
  - Odoo Model: `class AgriInterventionTemplateInput(models.Model)`
  - _name: `agri.intervention.template.input`
  - _description: "Agricultural Intervention Template Input"
  - Fields:
    - `template_id` (Many2one): Template reference (ondelete=cascade)
    - `product_id` (Many2one): Product/material reference (required) (product.product)
    - `quantity` (Float): Quantity per unit area (default: 1.0) or `qty_per_unit` depending on context
  - Relationships:
    - Many2one: `template_id` → `agri.intervention.template`
    - Many2one: `product_id` → `product.product`

- **farm_planning.AgriTechnicalRoute** (`agri.technical.route`): Technical routes for agricultural operations (cultural itinerary)
  - Odoo Model: `class AgriTechnicalRoute(models.Model)`
  - _name: `agri.technical.route`
  - _description: "Agricultural Technical Route"
  - _inherit: `mail.thread`, `mail.activity.mixin`
  - Fields:
    - `name` (Char): Route name (required)
    - `activity_family` (Selection): Activity family (planting, livestock, aquaculture)
    - `line_ids` (One2many): Intervention sequence (agri.technical.route.line)
  - Relationships:
    - One2many: `line_ids` → `agri.technical.route.line.route_id`
    - Inherits from: `mail.thread`, `mail.activity.mixin`

- **farm_planning.AgriTechnicalRouteLine** (`agri.technical.route.line`): Line items for technical routes
  - Odoo Model: `class AgriTechnicalRouteLine(models.Model)`
  - _name: `agri.technical.route.line`
  - _description: "Agricultural Technical Route Line"
  - Fields:
    - `route_id` (Many2one): Technical route reference (required) (agri.technical.route)
    - `sequence` (Integer): Execution sequence order
    - `intervention_template_id` (Many2one): Template for this step (agri.intervention.template)
    - `estimated_days` (Float): Estimated days to complete this step
  - Relationships:
    - Many2one: `route_id` → `agri.technical.route`
    - Many2one: `intervention_template_id` → `agri.intervention.template`

- **farm_planning.AgriScenario**: Agricultural scenario planning
  - Odoo Model: `class AgriScenario(models.Model)`
  - _name: `agri.scenario`
  - _description: "Agricultural Scenario Planning"
  - Relationships:
    - Extends: Base models with scenario planning functionality

- **farm_planning.AgriScenarioInputForecast**: Forecast inputs for scenarios
  - Odoo Model: `class AgriScenarioInputForecast(models.Model)`
  - _name: `agri.scenario.input.forecast`
  - _description: "Agricultural Scenario Input Forecast"
  - Relationships:
    - Extends: Base models with scenario input forecast functionality

- **farm_planning.AgriTechnicalRouteLine** (`agri.technical.route.line`): Line items for technical routes
  - (This model would be found in the actual file but was not fully shown in the grep results)

- **farm_planning.AgriScenario**: Agricultural scenario planning
- **farm_planning.AgriScenarioInputForecast**: Forecast inputs for scenarios

## Operation Models

Operation models manage the planning, execution, and tracking of farming operations.

### Campaign and Intervention Management
- **farm_operation.FarmAgriculturalCampaign** (`farm.agricultural.campaign`): Manages agricultural campaigns and planning
  - Odoo Model: `class FarmAgriculturalCampaign(models.Model)`
  - _name: `farm.agricultural.campaign`
  - _description: "Agricultural Campaign (ISL Layer)"
  - Fields:
    - `isl_campaign_code` (Char): ISL-specific campaign identifier
    - `farm_location_id` (Many2one): ISL Farm location link
  - Relationships:
    - Many2one: `farm_location_id` → `farm.location`
    - Inherits from: `farm.agricultural.campaign.mixin`

- **farm_operation.AgriculturalCampaign**: Alternative campaign model for agricultural operations
  - Odoo Model: `class AgriculturalCampaign(models.Model)`
  - _name: `agricultural.campaign`
  - _inherit: `farm.agricultural.campaign.base`
  - Relationship: Extends and specializes the base agricultural campaign functionality

- **farm_operation.FarmAgriculturalIntervention** (`farm.agricultural.intervention`): Represents agricultural interventions and treatments
  - Odoo Model: `class FarmAgriculturalIntervention(models.Model)`
  - _name: `farm.agricultural.intervention`
  - _description: "Agricultural Intervention (ISL Layer)"
  - _inherits: `mrp.production`
  - _inherit: `farm.agricultural.intervention.mixin`
  - Fields:
    - `production_id` (Many2one): Base production order (required, ondelete=cascade)
  - Relationships:
    - _inherits: `mrp.production` via `production_id` field
    - _inherit: `farm.agricultural.intervention.mixin`
    - Links to base Odoo MRP production model

- **farm_operation.AgriIntervention** (`mrp.production`): Alternative intervention model for agricultural operations
  - Odoo Model: `class AgriIntervention(models.Model)`
  - _name: `mrp.production` (Extends existing model)
  - _inherit: `mrp.production` and `farm.agricultural.intervention.mixin`
  - Fields:
    - Inherits all fields from `mrp.production` (Odoo's native manufacturing order)
    - Additional functionality from `farm.agricultural.intervention.mixin`
  - Relationships:
    - _inherit: `mrp.production` and `farm.agricultural.intervention.mixin`
    - Provides agricultural-specific functionality while maintaining compatibility with Odoo MRP system

- **farm_operation.MrpProduction**: Manufacturing resource planning production orders for operations
  - Odoo Model: `class MrpProduction(models.Model)`
  - _name: `mrp.production` (Extends existing model)
  - _inherit: `mrp.production`
  - Methods:
    - `_get_isl_model()`: Returns specialized model based on industry type
    - `action_confirm()`: Processing-specific pre-confirmation checks
    - `button_mark_done()`: Processing-specific pre-done checks
  - Relationships:
    - Extends: `mrp.production` (Odoo's native manufacturing order model)

### Manufacturing Resource Planning
- **farm_operation.MrpBom**: Manufacturing resource planning bill of materials for operations
- **farm_operation.MrpBomLine**: Line items for manufacturing resource planning
- **farm_operation.MrpProduction**: Manufacturing resource planning production orders
- **farm_operation.FarmAgriculturalBom**: Bill of materials for agricultural operations
- **farm_operation.FarmAgriculturalBomLine**: Line items for agricultural bill of materials

### Project Management
- **farm_operation.ProjectTask**: Tasks associated with farming projects
- **farm_operation.StockMove**: Tracks movement of stock in operations

### Mixins
- **farm_operation.FarmAgriculturalCampaignMixin** (Abstract): Provides agricultural campaign utilities
- **farm_operation.FarmAgriculturalInterventionMixin** (Abstract): Provides agricultural intervention utilities
- **farm_operation.FarmAgriculturalBomMixin** (Abstract): Provides agricultural BOM utilities
- **farm_operation.FarmAgriculturalBomLineMixin** (Abstract): Provides agricultural BOM line utilities
- **farm_operation.FarmAgriculturalCampaignBase** (Abstract): Provides base functionality for agricultural campaigns

## Equipment Models

Equipment models manage farm machinery and equipment operations.

- **farm_equipment.FarmEquipment**: Equipment management for farming
  - Odoo Model: `class FarmEquipment(models.Model)`
  - _name: `farm.equipment`
  - _description: "Farm Equipment Management"
  - Relationships:
    - Extends: Base models with equipment management functionality

- **farm_equipment.FarmEquipmentLog**: Log of equipment usage and maintenance
  - Odoo Model: `class FarmEquipmentLog(models.Model)`
  - _name: `farm.equipment.log`
  - _description: "Farm Equipment Usage and Maintenance Log"
  - Relationships:
    - Extends: Base models with equipment log functionality

- **farm_equipment.FarmBattery**: Battery management for equipment
  - Odoo Model: `class FarmBattery(models.Model)`
  - _name: `farm.battery`
  - _description: "Farm Equipment Battery Management"
  - Relationships:
    - Extends: Base models with battery management functionality

- **farm_equipment.FarmEquipmentChecklist**: Checklists for equipment maintenance
  - Odoo Model: `class FarmEquipmentChecklist(models.Model)`
  - _name: `farm.equipment.checklist`
  - _description: "Farm Equipment Maintenance Checklists"
  - Relationships:
    - Extends: Base models with equipment checklist functionality

- **farm_equipment.FarmEquipmentChecklistLine**: Line items for equipment checklists
  - Odoo Model: `class FarmEquipmentChecklistLine(models.Model)`
  - _name: `farm.equipment.checklist.line`
  - _description: "Farm Equipment Checklist Line Items"
  - Relationships:
    - Extends: Base models with equipment checklist line functionality

## HR Models

HR models manage human resources for farming operations.

- **farm_hr.FarmWageRule**: Wage rules for farm workers
  - Odoo Model: `class FarmWageRule(models.Model)`
  - _name: `farm.wage.rule`
  - _description: "Farm Worker Wage Rules"
  - Relationships:
    - Extends: Base models with wage rule functionality

- **farm_hr.FarmLaborPayment**: Labor payment management
  - Odoo Model: `class FarmLaborPayment(models.Model)`
  - _name: `farm.labor.payment`
  - _description: "Farm Labor Payment Management"
  - Relationships:
    - Extends: Base models with labor payment functionality

- **farm_hr.FarmLaborPaymentLine**: Line items for labor payments
  - Odoo Model: `class FarmLaborPaymentLine(models.Model)`
  - _name: `farm.labor.payment.line`
  - _description: "Farm Labor Payment Line Items"
  - Relationships:
    - Extends: Base models with labor payment line functionality

- **farm_hr.FarmWorklog**: Work log tracking
  - Odoo Model: `class FarmWorklog(models.Model)`
  - _name: `farm.worklog`
  - _description: "Farm Work Log Tracking"
  - Relationships:
    - Extends: Base models with work log functionality

- **farm_hr.ProjectTask**: HR-enhanced project task management
  - Odoo Model: `class ProjectTask(models.Model)`
  - _name: `project.task`
  - _description: "HR-Enhanced Project Task Management"
  - _inherit: `project.task`
  - Relationships:
    - Extends: `project.task` (Odoo's native project task model) with HR enhancements

- **farm_hr.AgriSkill**: Agricultural skill tracking
  - Odoo Model: `class AgriSkill(models.Model)`
  - _name: `farm.agri.skill`
  - _description: "Agricultural Skill Tracking"
  - Relationships:
    - Extends: Base models with agricultural skill functionality

- **farm_hr.FarmEmployeeCertificate**: Employee certificate management
  - Odoo Model: `class FarmEmployeeCertificate(models.Model)`
  - _name: `farm.employee.certificate`
  - _description: "Farm Employee Certificate Management"
  - Relationships:
    - Extends: Base models with employee certificate functionality

- **farm_hr.HrEmployee**: Enhanced employee records for agriculture
  - Odoo Model: `class HrEmployee(models.Model)`
  - _name: `hr.employee`
  - _description: "Agricultural Employee Records Enhancement"
  - _inherit: `hr.employee`
  - Relationships:
    - Extends: `hr.employee` (Odoo's native employee model) with agricultural enhancements

## MRP Models

MRP (Manufacturing Resource Planning) models handle production planning and bill of materials management.

### Production Management
- **farm_mrp.MrpProduction** (`mrp.production`): Manufacturing resource planning production orders
  - Relationships:
    - Inherits from: `mrp.production` (Odoo's native model)
    - Method: `_get_isl_model()` - returns specialized model based on industry type
    - Method: `action_confirm()` - processing-specific pre-confirmation checks
    - Method: `button_mark_done()` - processing-specific pre-done checks

- **farm_mrp.MrpBom**: Manufacturing resource planning bill of materials
- **farm_mrp.MrpBomLine**: Line items for manufacturing bills of materials

### Stock Management
- **farm_mrp.StockLot**: Stock lots for manufacturing processes

### Mixins
- **farm_mrp.FarmAgriBomMixin** (Abstract): Provides agricultural BOM utilities for MRP
- **farm_mrp.FarmAgriProductionMixin** (Abstract): Provides agricultural production utilities for MRP

## Field Crops Models

Field crops models manage grain and field crop production operations.

### Operations
- **farm_field_crops.FieldCropOperation**: Operations for field crop management

### Production and Planning
- **farm_field_crops.MrpProduction**: Manufacturing resource planning for field crops
- **farm_field_crops.MrpBom**: Manufacturing resource planning BOM for field crops
- **farm_field_crops.FarmCropBom**: Field crop-specific BOM
- **farm_field_crops.FarmCropProduction**: Field crop production management
- **farm_field_crops.FarmCropLot**: Field crop lot management
- **farm_field_crops.FarmCropBomLine**: Line items for field crop BOM

### Stock Management
- **farm_field_crops.StockLot**: Stock lots for field crop management

## Livestock Models

Livestock models manage animal husbandry and livestock-related operations.

### Core Livestock Management
- **farm_livestock.FarmLot**: Livestock lot management
- **farm_livestock.StockLot**: Stock lots for livestock management
- **farm_livestock.FarmBreedingRecord**: Records of livestock breeding activities

### Production and Planning
- **farm_livestock.MrpProduction**: Manufacturing resource planning for livestock
- **farm_livestock.MrpBom**: Manufacturing resource planning BOM for livestock
- **farm_livestock.FarmLivestockBom**: Livestock-specific BOM
- **farm_livestock.FarmLivestockProduction**: Livestock production management
- **farm_livestock.FarmLivestockBomLine**: Line items for livestock BOM

### Health Management
- **farm_livestock.FarmAnimalHealthWizard**: Wizard for livestock health management

## Aquaculture Models

Aquaculture models manage fish and aquatic organism farming operations.

### Operations
- **farm_aquaculture.FarmAquacultureOperation**: Operations for aquaculture management
- **farm_aquaculture.FarmWaterQualityLog**: Logs for water quality in aquaculture

### Production and Planning
- **farm_aquaculture.MrpProduction**: Manufacturing resource planning for aquaculture
- **farm_aquaculture.MrpBom**: Manufacturing resource planning BOM for aquaculture
- **farm_aquaculture.FarmAquacultureBom**: Aquaculture-specific BOM
- **farm_aquaculture.FarmAquacultureProduction**: Aquaculture production management
- **farm_aquaculture.FarmAquacultureBomLine**: Line items for aquaculture BOM

### Stock Management
- **farm_aquaculture.StockLot**: Stock lots for aquaculture management

## Specialized Farming Models

### AgriTourism
- **farm_agritourism.FarmAgritourismOperation**: Operations for agritourism
- **farm_agritourism.FarmResourceUsage**: Resource usage tracking for agritourism
- **farm_agritourism.FarmResource**: Resource management for agritourism
- **farm_agritourism.FarmBooking**: Booking management for agritourism
- **farm_agritourism.SaleOrder**: Agritourism-enhanced sale orders
- **farm_agritourism.ProductTemplate**: Agritourism-enhanced product templates
- **farm_agritourism.SaleOrderLine**: Line items for agritourism sale orders

### Orchard/Horticulture
- **farm_orchard_horticulture.OrchardOperation**: Operations for orchard and horticulture
- **farm_orchard_horticulture.FruitTree**: Management of fruit trees
- **farm_orchard_horticulture.PlantYieldRecord**: Record of plant yields

### Apiculture
- **farm_apiculture.FarmApicultureOperation**: Operations for apiculture (beekeeping)
- **farm_apiculture.FarmHiveInspection**: Inspection records for beehives

### Mushroom
- **farm_mushroom.FarmMushroomOperation**: Operations for mushroom production
- **farm_mushroom.FarmMushroomHarvest**: Harvest management for mushrooms

### Medicinal Plants
- **farm_medicinal_plants.FarmMedicinalPlantsOperation**: Operations for medicinal plant production
- **farm_medicinal_plants.FarmMedicinalPlantsAnalysis**: Analysis of medicinal plants

### Protected Cultivation
- **farm_protected_cultivation.ProtectedCultivationOperation**: Operations for protected cultivation
- **farm_protected_cultivation.FarmEnvironmentalLog**: Environmental logging for protected cultivation

### Breeding
- **farm_breeding.FarmTraitValue**: Management of trait values for breeding
- **farm_breeding.FarmLotBreeding**: Breeding management for lots
- **farm_breeding.FarmNurseryBatch**: Management of nursery batches for breeding
- **farm_breeding.FarmTraitComparisonWizard**: Wizard for comparing traits
- **farm_breeding.FarmTraitComparisonLine**: Line items for trait comparisons

### Sustainability
- **farm_sustainability.AgriculturalCampaign**: Sustainability-enhanced agricultural campaigns
- **farm_sustainability.ProductTemplate**: Sustainability-enhanced product templates
- **farm_sustainability.AgriIntervention** (`mrp.production`): Sustainability-enhanced interventions (extends mrp.production)
  - Odoo Model: `class AgriIntervention(models.Model)`
  - _name: `mrp.production` (Extends existing model)
  - _inherit: `mrp.production`
  - Fields:
    - `calculated_carbon_emission` (Float): Calculated carbon emission in kg CO2e (computed, stored)
  - Methods:
    - `_compute_carbon_emission()`: Computes carbon emission based on raw material inputs and their emission factors
  - Relationships:
    - Inherits from: `mrp.production`
    - Computes emission from `move_raw_ids.product_uom_qty` and `move_raw_ids.product_id.carbon_emission_factor`

- **farm_sustainability.StockLot** (`stock.lot`): Sustainability-enhanced stock lots (extends stock.lot)
  - Odoo Model: `class StockLot(models.Model)`
  - _name: `stock.lot` (Extends existing model)
  - _inherit: `stock.lot`
  - Fields:
    - `carbon_footprint` (Float): Carbon footprint in kg CO2e (computed, stored)
  - Methods:
    - `_compute_carbon_footprint()`: Computes carbon footprint for the lot
  - Relationships:
    - Inherits from: `stock.lot`

### ESG Framework (farm_esg module)
- **esg.ESGFramework** (`esg.framework`): Core ESG framework model
  - Odoo Model: `class ESGFramework(models.Model)`
  - _name: `esg.framework`
  - _description: "ESG Framework"
  - _inherit: `mail.thread`, `mail.activity.mixin`
  - Fields:
    - `name` (Char): Framework name
    - `code` (Char): Unique framework code
    - `description` (Text): Framework description
    - `framework_type` (Selection): Type (environmental, social, governance, combined)
    - `standards_body` (Char): Standards body maintaining framework
    - `version` (Char): Framework version
    - `effective_date` (Date): Effective date
    - `expiry_date` (Date): Expiry date
    - `is_active` (Boolean): Active status
    - `compliance_level` (Selection): Compliance level (basic, intermediate, advanced, leadership)
    - `indicator_ids` (One2many): Related ESG indicators
  - Relationships:
    - One2many: `indicator_ids` → `esg.indicator.framework_id`

- **esg.ESGAssessment** (`esg.assessment`): ESG performance assessment model
  - Odoo Model: `class ESGAssessment(models.Model)`
  - _name: `esg.assessment`
  - _description: "ESG Assessment"
  - _inherit: `mail.thread`, `mail.activity.mixin`
  - Fields:
    - `name` (Char): Assessment name
    - `assessment_date` (Date): Assessment date
    - `assessment_type` (Selection): Type (environmental, social, governance, combined)
    - `framework_id` (Many2one): Associated ESG framework
    - `assessment_period` (Selection): Period (daily, weekly, monthly, quarterly, annually)
    - `year` (Integer): Assessment year
    - `assessed_entity_type` (Selection): Entity type (company, farm, operation, product, process)
    - `assessed_entity_id` (Reference): Entity being assessed
    - `overall_esg_score` (Float): Overall ESG score (0-100) (computed, stored)
    - `assessment_status` (Selection): Status (draft, in_progress, completed, validated, archived)
    - `environmental_score` (Float): Environmental score (0-100)
    - `social_score` (Float): Social score (0-100)
    - `governance_score` (Float): Governance score (0-100)
    - `assessor_id` (Many2one): Assessor user
    - `assessment_method` (Selection): Method (self_assessment, third_party, hybrid)
    - `certification_body` (Char): Certification body
    - `target_ids` (Many2many): Related ESG targets
  - Methods:
    - `_compute_overall_esg_score()`: Computes overall score as weighted average
    - `action_start_assessment()`: Start assessment process
    - `action_complete_assessment()`: Complete assessment process

- **esg.ESGIndicator** (`esg.indicator`): ESG indicator model
  - Odoo Model: `class ESGIndicator(models.Model)`
  - _name: `esg.indicator`
  - _description: "ESG Indicator"
  - _inherit: `mail.thread`, `mail.activity.mixin`
  - _order: 'category, name'
  - Fields:
    - `name` (Char): Indicator name
    - `code` (Char): Indicator code
    - `description` (Text): Indicator description
    - `category` (Selection): Category (environmental, social, governance)
    - `subcategory` (Selection): Subcategory (carbon_emissions, water_usage, waste_management, biodiversity, energy_efficiency, etc.)
    - `framework_id` (Many2one): Associated ESG framework
    - `unit_of_measurement` (Char): Unit of measurement
    - `data_collection_method` (Selection): Collection method (automated, manual_input, third_party, survey, audit)
    - `baseline_value` (Float): Baseline value
    - `target_value` (Float): Target value
    - `threshold_value` (Float): Threshold value
    - `weight` (Float): Weight in ESG score calculation
    - `min_acceptable_value` (Float): Minimum acceptable value
    - `max_acceptable_value` (Float): Maximum acceptable value
    - `is_percentage` (Boolean): Whether indicator is percentage
    - `is_active` (Boolean): Active status
    - `reporting_frequency` (Selection): Frequency (daily, weekly, monthly, quarterly, annually)
    - `assessment_line_ids` (One2many): Related assessment lines
  - Relationships:
    - Many2one: `framework_id` → `esg.framework`
    - One2many: `assessment_line_ids` → `esg.assessment.line`

- **esg.ESGAssessmentLine** (`esg.assessment.line`): Individual indicator scores within assessments
  - Odoo Model: `class ESGAssessmentLine(models.Model)`
  - _name: `esg.assessment.line`
  - _description: "ESG Assessment Line"
  - _inherit: `mail.thread`, `mail.activity.mixin`
  - Fields:
    - `assessment_id` (Many2one): Associated ESG assessment
    - `indicator_id` (Many2one): Associated ESG indicator
    - `actual_value` (Float): Actual measured value
    - `target_value` (Float): Target value (related)
    - `baseline_value` (Float): Baseline value (related)
    - `variance` (Float): Variance from target (computed, stored)
    - `performance_score` (Float): Performance score (0-100) (computed, stored)
    - `achievement_percentage` (Float): Achievement percentage (computed, stored)
    - `data_source` (Char): Data source
    - `verification_status` (Selection): Verification status (unverified, self_verified, third_party_verified, certified)
    - `collection_date` (Date): Data collection date
    - `collected_by` (Many2one): User who collected data
  - Methods:
    - `_compute_variance()`: Computes variance from target
    - `_compute_performance_score()`: Computes performance score based on achievement
    - `_compute_achievement_percentage()`: Computes achievement percentage

- **esg.ESGTarget** (`esg.target`): ESG goals and targets model
  - Odoo Model: `class ESGTarget(models.Model)`
  - _name: `esg.target`
  - _description: "ESG Target"
  - _inherit: `mail.thread`, `mail.activity.mixin`
  - Fields:
    - `name` (Char): Target name
    - `description` (Text): Target description
    - `category` (Selection): Category (environmental, social, governance)
    - `target_type` (Selection): Type (reduction, improvement, compliance, certification, benchmark)
    - `baseline_value` (Float): Baseline value
    - `target_value` (Float): Target value
    - `current_value` (Float): Current value (computed, stored)
    - `unit_of_measurement` (Char): Unit of measurement
    - `start_date` (Date): Start date
    - `target_date` (Date): Target date
    - `achieved_date` (Date): Date achieved (readonly)
    - `progress_percentage` (Float): Progress percentage (computed, stored)
    - `is_achieved` (Boolean): Whether target is achieved (computed, stored)
    - `framework_id` (Many2one): Associated ESG framework
    - `related_indicator_ids` (Many2many): Related indicators
    - `responsible_user_id` (Many2one): Responsible user
    - `priority` (Selection): Priority level (low, medium, high, critical)
    - `status` (Selection): Status (planned, in_progress, partially_achieved, achieved, deferred, cancelled)
    - `stakeholder_ids` (Many2many): Related stakeholders
    - `last_update` (Text): Last update notes
  - Methods:
    - `_compute_progress_percentage()`: Computes progress percentage
    - `_compute_is_achieved()`: Determines if target is achieved
    - `_compute_current_value()`: Computes current value
    - `action_update_current_value()`: Manual update of current value
    - `action_mark_achieved()`: Mark target as achieved
    - `action_track_progress()`: Track progress function

- **esg.ESGPerformanceReport** (`esg.performance.report`): ESG performance reporting model
  - Odoo Model: `class ESGPerformanceReport(models.Model)`
  - _name: `esg.performance.report`
  - _description: "ESG Performance Report"
  - _inherit: `mail.thread`, `mail.activity.mixin`
  - Fields:
    - `name` (Char): Report name
    - `report_date` (Date): Report date
    - `report_period` (Selection): Report period (monthly, quarterly, semi_annually, annually)
    - `year` (Integer): Report year
    - `company_id` (Many2one): Associated company
    - `environmental_score` (Float): Environmental score (0-100)
    - `social_score` (Float): Social score (0-100)
    - `governance_score` (Float): Governance score (0-100)
    - `overall_esg_score` (Float): Overall ESG score (0-100) (computed, stored)
    - `total_targets` (Integer): Total targets (computed, stored)
    - `achieved_targets` (Integer): Achieved targets (computed, stored)
    - `achievement_rate` (Float): Achievement rate percentage (computed, stored)
    - `compliance_rate` (Float): Compliance rate percentage
    - `audit_findings` (Integer): Number of audit findings
    - `corrective_actions` (Integer): Corrective actions required
    - `executive_summary` (Html): Executive summary
    - `key_achievements` (Html): Key achievements
    - `challenges` (Html): Challenges
    - `improvement_plan` (Html): Improvement plan
    - `assessment_ids` (Many2many): Related assessments
    - `target_ids` (Many2many): Related targets
  - Methods:
    - `_compute_overall_score()`: Computes overall ESG score
    - `_compute_target_metrics()`: Computes target-related metrics
    - `action_generate_report()`: Generate ESG report

### ESG Carbon Module (farm_esg_carbon)
- **farm_esg_carbon.ProductTemplateExtension**: Extends product templates with carbon emissions
  - Odoo Model: `class ProductTemplate(models.Model)` (extension)
  - _inherit: `product.template`
  - Fields:
    - `carbon_emission_factor` (Float): Carbon emission factor (kg CO2e per unit)

- **farm_esg_carbon.AgriInterventionExtension**: Extends production orders with carbon calculations
  - Odoo Model: `class AgriIntervention(models.Model)` (extension)
  - _inherit: `mrp.production`
  - Fields:
    - `calculated_carbon_emission` (Float): Calculated carbon emission (kg CO2e) (computed, stored)
  - Methods:
    - `_compute_carbon_emission()`: Computes total carbon emission from raw materials

### ESG Environmental Compliance (farm_esg_environmental)
- **agri.ESGRedLineConfig** (`agri.esg.red.line.config`): ESG red line configuration model
  - Odoo Model: `class AgriESGRedLineConfig(models.Model)`
  - _name: `agri.esg.red.line.config`
  - _description: "Agri ESG Red Line Configuration"
  - _inherit: `mail.thread`, `mail.activity.mixin`
  - Fields:
    - `name` (Char): Red line name
    - `red_line_type` (Selection): Type (deforestation, water_extraction, soil_degradation, protected_area, carbon_emission, chemical_runoff, biodiversity_loss)
    - `coordinates` (Text): Boundary coordinates for geofencing
    - `buffer_distance_km` (Float): Buffer distance in kilometers
    - `threshold_value` (Float): Threshold value
    - `threshold_unit` (Char): Threshold unit
    - `threshold_description` (Text): Threshold description
    - `active_monitoring` (Boolean): Active monitoring flag
    - `monitoring_frequency` (Selection): Frequency (real_time, hourly, daily, weekly)
    - `description` (Text): Description
    - `remediation_plan` (Text): Remediation plan

- **agri.ESGRedLineMonitoring** (`agri.esg.red.line.monitoring`): ESG compliance monitoring model
  - Odoo Model: `class AgriESGRedLineMonitoring(models.Model)`
  - _name: `agri.esg.red.line.monitoring`
  - _description: "Agri ESG Red Line Monitoring"
  - _inherit: `mail.thread`, `mail.activity.mixin`
  - _order: 'detection_date desc'
  - Fields:
    - `name` (Char): Monitoring record name
    - `red_line_config_id` (Many2one): Red line configuration
    - `batch_lot_id` (Many2one): Associated batch/lot
    - `location_id` (Many2one): Location being monitored
    - `detection_date` (Datetime): Detection date
    - `compliance_status` (Selection): Status (compliant, warning, violation, critical, resolved)
    - `current_value` (Float): Current measured value
    - `threshold_value` (Float): Threshold value (related)
    - `carbon_footprint_kg` (Float): Carbon footprint
    - `water_usage_m3` (Float): Water usage in cubic meters
    - `land_use_area` (Float): Land use area in square meters
    - `is_in_protected_area` (Boolean): Whether in protected area
    - `distance_to_boundary_km` (Float): Distance to boundary in kilometers
    - `detection_method` (Selection): Method (geofence, threshold_monitoring, manual_audit, iot_sensor, telemetry)
    - `detection_details` (Text): Detection details
    - `automated_check` (Boolean): Automated check flag
    - `alert_issued` (Boolean): Alert issued flag
    - `corrective_actions` (Text): Required corrective actions
    - `remediation_date` (Datetime): Remediation date
    - `resolution_notes` (Text): Resolution notes
  - Methods:
    - `_check_compliance_status()`: Check compliance status
    - `action_issue_red_line_alert()`: Issue red line alert
    - `action_resolve_violation()`: Resolve violation
    - `action_check_batch_compliance()`: Check batch compliance
    - `_perform_specific_check()`: Perform specific compliance check
    - `_check_deforestation_risk()`: Check deforestation risk
    - `_check_water_usage()`: Check water usage
    - `_check_carbon_footprint()`: Check carbon footprint
    - `_check_protected_area_compliance()`: Check protected area compliance
    - `_cron_check_compliance()`: Scheduled compliance check

- **agri.StockLotESGExtension** (`stock.lot`): ESG compliance extension to stock lots
  - Odoo Model: `class AgriStockLot(models.Model)` (extension)
  - _inherit: `stock.lot`
  - Fields:
    - `esg_compliance_status` (Selection): ESG compliance status (computed, stored)
    - `esg_monitoring_ids` (One2many): ESG monitoring records
    - `last_esg_check` (Datetime): Last ESG check date
    - `water_usage_m3` (Float): Water usage for this lot
    - `land_use_area_m2` (Float): Land use area in square meters
  - Methods:
    - `_compute_esg_compliance_status()`: Compute ESG compliance status
    - `action_check_esg_compliance()`: Check ESG compliance

### ESG Circular Economy (farm_esg_circular)
- **agri.CircularFlow** (`agri.sustainability.circular.flow`): Agricultural circular flow model
  - Odoo Model: `class AgriSustainabilityCircularFlow(models.Model)`
  - _name: `agri.sustainability.circular.flow`
  - _description: "Agricultural Circular Flow"
  - _inherit: `mail.thread`, `mail.activity.mixin`
  - _order: 'create_date desc'
  - Fields:
    - `name` (Char): Flow name
    - `code` (Char): Flow code (unique)
    - `flow_type` (Selection): Type (waste_to_resource, byproduct_to_sale, recycling, energy_recovery, composting, biogas_production)
    - `description` (Text): Flow description
    - `input_product_id` (Many2one): Input product/ingredient
    - `output_product_id` (Many2one): Output product/resource
    - `input_quantity` (Float): Input quantity
    - `output_quantity` (Float): Output quantity
    - `start_date` (Date): Start date
    - `end_date` (Date): End date
    - `duration_days` (Integer): Duration in days (computed, stored)
    - `economic_value` (Float): Economic value (computed, stored)
    - `environmental_impact` (Float): Environmental impact score (computed, stored)
    - `social_impact` (Float): Social impact score (computed, stored)
    - `processing_cost` (Float): Processing cost
    - `revenue` (Float): Revenue
    - `net_benefit` (Float): Net benefit (computed, stored)
    - `status` (Selection): Status (planned, active, completed, suspended, cancelled)
    - `responsible_person_id` (Many2one): Responsible person
    - `department_id` (Many2one): Responsible department
    - `related_production_id` (Many2one): Related production order
    - `related_sale_order_id` (Many2one): Related sale order
    - `related_carbon_calculation_id` (Many2one): Related carbon calculation
    - `created_by` (Many2one): Created by user
    - `create_date` (Datetime): Creation date (readonly)
    - `write_date` (Datetime): Last update date (readonly)
  - Methods:
    - `_compute_duration()`: Compute duration in days
    - `_compute_net_benefit()`: Compute net benefit
    - `_compute_economic_value()`: Compute economic value
    - `_compute_environmental_impact()`: Compute environmental impact score
    - `_compute_social_impact()`: Compute social impact score
    - `action_activate_flow()`: Activate the flow
    - `action_complete_flow()`: Complete the flow
    - `action_suspend_flow()`: Suspend the flow
    - `name_get()`: Custom display name

- **agri.CircularFlowAnalysis** (`agri.sustainability.circular.flow.analysis`): Circular flow analysis view model
  - Odoo Model: `class AgriSustainabilityCircularFlowAnalysis(models.Model)`
  - _name: `agri.sustainability.circular.flow.analysis`
  - _description: "Agricultural Circular Flow Analysis"
  - _auto: False (database view)
  - Fields:
    - `flow_id` (Many2one): Related circular flow
    - `flow_type` (Selection): Flow type (related)
    - `input_product_id` (Many2one): Input product (related)
    - `output_product_id` (Many2one): Output product (related)
    - `economic_value` (Float): Economic value (related)
    - `environmental_impact` (Float): Environmental impact (related)
    - `net_benefit` (Float): Net benefit (related)
    - `status` (Selection): Status (related)
    - `month` (Char): Month for reporting
    - `year` (Char): Year for reporting
  - Methods:
    - `init()`: Initialize database view

### ESG Sustainability Reporting (farm_esg_sustainability)
- **agri.SustainabilityMetric** (`agri.sustainability.metric`): Agricultural sustainability metric model
  - Odoo Model: `class AgriSustainabilityMetric(models.Model)`
  - _name: `agri.sustainability.metric`
  - _description: "Agricultural Sustainability Metric"
  - _inherit: `mail.thread`, `mail.activity.mixin`
  - _order: 'category, sequence'
  - Fields:
    - `name` (Char): Metric name (translatable)
    - `code` (Char): Unique metric code
    - `category` (Selection): Category (economic, environmental, social, governance)
    - `unit` (Char): Unit of measure
    - `description` (Text): Description (translatable)
    - `sequence` (Integer): Display sequence
    - `target_value` (Float): Target value
    - `current_value` (Float): Current value (computed, stored)
    - `progress_rate` (Float): Progress rate percentage (computed, stored)
    - `is_active` (Boolean): Active status
    - `calculation_method` (Selection): Method (manual, automatic, formula)
    - `formula` (Text): Calculation formula
    - `last_updated` (Datetime): Last updated (readonly)
    - `value_history_ids` (One2many): Value history
  - Methods:
    - `_compute_current_value()`: Compute current value from history
    - `_compute_progress_rate()`: Compute progress rate
    - `action_update_value()`: Update metric value action
    - `name_get()`: Custom display name

- **agri.SustainabilityMetricValue** (`agri.sustainability.metric.value`): Sustainability metric value history
  - Odoo Model: `class AgriSustainabilityMetricValue(models.Model)`
  - _name: `agri.sustainability.metric.value`
  - _description: "Agri Sustainability Metric Value"
  - _inherit: `mail.thread`, `mail.activity.mixin`
  - _order: 'date desc'
  - Fields:
    - `metric_id` (Many2one): Related metric
    - `value` (Float): Metric value
    - `date` (Datetime): Record date
    - `note` (Text): Notes
    - `recorded_by` (Many2one): Recorded by user
  - Methods:
    - `create()`: Override create to update parent metric timestamp

- **agri.SustainabilityMetricValueWizard** (`agri.sustainability.metric.value.wizard`): Wizard for updating metric values
  - Odoo Model: `class AgriSustainabilityMetricValueWizard(models.TransientModel)`
  - _name: `agri.sustainability.metric.value.wizard`
  - _description: "Agri Sustainability Metric Value Update Wizard"
  - Fields:
    - `metric_id` (Many2one): Related metric (readonly)
    - `value` (Float): New value
    - `date` (Datetime): Date
    - `note` (Text): Notes
  - Methods:
    - `action_update_value()`: Execute value update

### Carbon Asset Management
- **farm_sustainability.CarbonAsset**: Management of carbon assets (Deprecated - Use agri.carbon.asset)
  - Odoo Model: `class CarbonAsset(models.Model)` (now inherits from agri.carbon.asset)
  - _name: `farm.carbon.asset`
  - _description: "Carbon Sequestration Asset (Deprecated - Use agri.carbon.asset)"
  - Original logic preserved with deprecation warning

- **agri_sustainability.AgriCarbonAsset**: Agricultural carbon sequestration asset management
  - Odoo Model: `class AgriCarbonAsset(models.Model)`
  - _name: `agri.carbon.asset`
  - _description: "Agricultural Carbon Sequestration Asset"
  - Relationships:
    - location_id (Many2one to farm.location)
    - Contains original logic for carbon asset tracking

- **farm_sustainability.FarmEcologicalActivity**: Ecological activity management (Deprecated - Use agri.ecological.activity)
  - Odoo Model: `class FarmEcologicalActivity(models.Model)` (now inherits from agri.ecological.activity)
  - _name: `farm.ecological.activity`
  - _description: "Ecological Maintenance Activity (Deprecated - Use agri.ecological.activity)"
  - Original logic preserved with deprecation warning

- **agri_sustainability.AgriEcologicalActivity**: Agricultural ecological activity management
  - Odoo Model: `class AgriEcologicalActivity(models.Model)`
  - _name: `agri.ecological.activity`
  - _description: "Agricultural Ecological Activity"
  - Relationships:
    - location_id (Many2one to farm.location)

### CSA (Community Supported Agriculture)
- **farm_csa.FarmCSAPlan**: Community Supported Agriculture plans
- **farm_csa.FarmCSASubscription**: CSA subscription management
- **farm_csa.FarmSharedTool**: Shared tool management for CSA

### Subsidy Management
- **farm_subsidy.FarmSubsidyProgram**: Management of subsidy programs
- **farm_subsidy.FarmSubsidyApplication**: Application management for subsidies

## Processing Models

Processing models handle post-harvest activities, manufacturing, and value-added processing operations.

### Production and BOM
- **farm_processing.MrpProduction** (`mrp.production`): Processing production orders
  - Odoo Model: `class MrpProduction(models.Model)`
  - _name: `mrp.production` (Extends existing model)
  - _inherit: `mrp.production`
  - Methods:
    - `_get_isl_model()`: Returns 'farm.processing.production' for food_processing industry type
    - `action_confirm()`: Processing-specific pre-confirmation checks
    - `button_mark_done()`: Processing-specific pre-done checks
  - Relationships:
    - Inherits from: `mrp.production` (Odoo's native model)

- **farm_processing.MrpBom**: Manufacturing resource planning bill of materials for processing
  - Odoo Model: `class MrpBom(models.Model)`
  - _name: `mrp.bom` (Extends existing model)
  - _inherit: `mrp.bom`
  - Relationships:
    - Extends: `mrp.bom` (Odoo's native BOM model)

- **farm_processing.FarmProcessingBom**: Processing bills of materials
  - Odoo Model: `class FarmProcessingBom(models.Model)`
  - _name: `farm.processing.bom`
  - _description: "Processing Bill of Materials (ISL Layer)"
  - _inherits: `mrp.bom`
  - Relationships:
    - _inherits: `mrp.bom` via inherited field
    - Links to base Odoo MRP BOM model

- **farm_processing.FarmProcessingProduction**: Processing production orders
  - Odoo Model: `class FarmProcessingProduction(models.Model)`
  - _name: `farm.processing.production`
  - _description: "Processing Production Order (ISL Layer)"
  - _inherits: `mrp.production`
  - Relationships:
    - _inherits: `mrp.production` via inherited field
    - Links to base Odoo MRP production model

- **farm_processing.FarmProcessingBomLine**: Processing BOM line items
  - Odoo Model: `class FarmProcessingBomLine(models.Model)`
  - _name: `farm.processing.bom.line`
  - _description: "Processing BOM Line (ISL Layer)"
  - _inherits: `mrp.bom.line`
  - Relationships:
    - _inherits: `mrp.bom.line` via inherited field
    - Links to base Odoo MRP BOM line model

### Work Centers and Operations
- **farm_processing.MrpWorkcenter**: Work centers for processing operations
  - Odoo Model: `class MrpWorkcenter(models.Model)`
  - _name: `mrp.workcenter` (Extends existing model)
  - _inherit: `mrp.workcenter`
  - Relationships:
    - Extends: `mrp.workcenter` (Odoo's native work center model)

- **farm_processing.MrpRoutingWorkcenter**: Routing for work centers in processing
  - Odoo Model: `class MrpRoutingWorkcenter(models.Model)`
  - _name: `mrp.routing.workcenter` (Extends existing model)
  - _inherit: `mrp.routing.workcenter`
  - Relationships:
    - Extends: `mrp.routing.workcenter` (Odoo's native routing work center model)

- **farm_processing.MrpWorkorder**: Work orders for processing operations
  - Odoo Model: `class MrpWorkorder(models.Model)`
  - _name: `mrp.workorder` (Extends existing model)
  - _inherit: `mrp.workorder`
  - Relationships:
    - Extends: `mrp.workorder` (Odoo's native work order model)

- **farm_processing.FarmIndustryWorkcenter**: Industry-specific work centers for processing
  - Odoo Model: `class FarmIndustryWorkcenter(models.Model)`
  - _name: `farm.industry.workcenter`
  - _description: "Industry-Specific Work Center for Processing"
  - Relationships:
    - Extends: `mrp.workcenter` with industry-specific features

- **farm_processing.FarmIndustryOperation**: Industry-specific operations for processing
  - Odoo Model: `class FarmIndustryOperation(models.Model)`
  - _name: `farm.industry.operation`
  - _description: "Industry-Specific Operation for Processing"
  - Relationships:
    - Extends: `mrp.routing.workcenter` with industry-specific features

### Stock and Logistics
- **farm_processing.StockLot**: Stock lots for processing operations
  - Odoo Model: `class StockLot(models.Model)`
  - _name: `stock.lot` (Extends existing model)
  - _inherit: `stock.lot`
  - Relationships:
    - Extends: `stock.lot` (Odoo's native stock lot model)

- **farm_processing.StockMove**: Stock movement in processing operations
  - Odoo Model: `class StockMove(models.Model)`
  - _name: `stock.move` (Extends existing model)
  - _inherit: `stock.move`
  - Relationships:
    - Extends: `stock.move` (Odoo's native stock move model)

- **farm_processing.StockPicking**: Stock picking for processing operations
  - Odoo Model: `class StockPicking(models.Model)`
  - _name: `stock.picking` (Extends existing model)
  - _inherit: `stock.picking`
  - Relationships:
    - Extends: `stock.picking` (Odoo's native stock picking model)

- **farm_processing.FarmIndustryPicking**: Industry-specific picking for processing
  - Odoo Model: `class FarmIndustryPicking(models.Model)`
  - _name: `farm.industry.picking`
  - _description: "Industry-Specific Picking for Processing"
  - Relationships:
    - Extends: `stock.picking` with industry-specific features

### Product and Packaging
- **farm_processing.ProductTemplate**: Product templates for processing
  - Odoo Model: `class ProductTemplate(models.Model)`
  - _name: `product.template` (Extends existing model)
  - _inherit: `product.template`
  - Relationships:
    - Extends: `product.template` (Odoo's native product template model)

- **farm_processing.FarmPackage**: Packaging management for processing
  - Odoo Model: `class FarmPackage(models.Model)`
  - _name: `farm.package`
  - _description: "Packaging Management for Processing"
  - Relationships:
    - Extends: `product.template` with packaging-specific features

- **farm_processing.FarmPackageLevel**: Package level management for processing
  - Odoo Model: `class FarmPackageLevel(models.Model)`
  - _name: `farm.package.level`
  - _description: "Package Level Management for Processing"
  - Relationships:
    - Extends: `product.product` with packaging level features

### Health and Safety
- **farm_processing.FarmHealthSchedule**: Health scheduling for biological assets
  - Odoo Model: `class FarmHealthSchedule(models.Model)`
  - _name: `farm.health.schedule`
  - _description: "Health Schedule for Biological Assets"
  - Relationships:
    - Extends: Base models with health scheduling functionality

- **farm_processing.StockLotHealth**: Health tracking for stock lots
  - Odoo Model: `class StockLotHealth(models.Model)`
  - _name: `stock.lot.health`
  - _description: "Health Tracking for Stock Lots"
  - _inherit: `stock.lot`
  - Relationships:
    - Extends: `stock.lot` with health tracking features

### Lot Variants
- **farm_processing.FarmLotHarvest**: Harvest lot tracking for processing
  - Odoo Model: `class FarmLotHarvest(models.Model)`
  - _name: `farm.lot.harvest`
  - _description: "Harvest Lot Tracking"
  - Relationships:
    - Extends: `stock.lot` with harvest-specific features

- **farm_processing.FarmLotLivestock**: Livestock lot tracking for processing
  - Odoo Model: `class FarmLotLivestock(models.Model)`
  - _name: `farm.lot.livestock`
  - _description: "Livestock Lot Tracking"
  - Relationships:
    - Extends: `stock.lot` with livestock-specific features

- **farm_processing.FarmLotAquaculture**: Aquaculture lot tracking for processing
  - Odoo Model: `class FarmLotAquaculture(models.Model)`
  - _name: `farm.lot.aquaculture`
  - _description: "Aquaculture Lot Tracking"
  - Relationships:
    - Extends: `stock.lot` with aquaculture-specific features

### Specialized Functionality
- **farm_processing.FarmAllergen**: Allergen management for processing
  - Odoo Model: `class FarmAllergen(models.Model)`
  - _name: `farm.allergen`
  - _description: "Allergen Management"
  - Relationships:
    - Extends: Product and manufacturing models with allergen tracking

- **farm_processing.FarmScLicense**: SC license management for processing
  - Odoo Model: `class FarmScLicense(models.Model)`
  - _name: `farm.sc.license`
  - _description: "SC License Management"
  - Relationships:
    - Extends: Company and product models with license tracking

- **farm_processing.FarmScCategory**: SC category management for processing
  - Odoo Model: `class FarmScCategory(models.Model)`
  - _name: `farm.sc.category`
  - _description: "SC Category Management"
  - Relationships:
    - Extends: Product models with category management

### Wizards
- **farm_processing.FarmRecallWizard**: Wizard for product recall operations
  - Odoo Model: `class FarmRecallWizard(models.TransientModel)`
  - _name: `farm.recall.wizard`
  - _description: "Product Recall Wizard"
  - Relationships:
    - Extends: Transient model for recall operations

- **farm_processing.FarmRecallLine**: Recall line items
  - Odoo Model: `class FarmRecallLine(models.TransientModel)`
  - _name: `farm.recall.line`
  - _description: "Product Recall Line Items"
  - Relationships:
    - Extends: Transient model for recall line items

- **farm_processing.FarmSubstituteWizard**: Wizard for material substitution
  - Odoo Model: `class FarmSubstituteWizard(models.TransientModel)`
  - _name: `farm.substitute.wizard`
  - _description: "Material Substitute Wizard"
  - Relationships:
    - Extends: Transient model for substitution operations

- **farm_processing.FarmSubstituteLine**: Substitute line items
  - Odoo Model: `class FarmSubstituteLine(models.TransientModel)`
  - _name: `farm.substitute.line`
  - _description: "Substitute Line Items"
  - Relationships:
    - Extends: Transient model for substitution line items

- **farm_processing.FarmWasteTransformationWizard**: Wizard for waste transformation
  - Odoo Model: `class FarmWasteTransformationWizard(models.TransientModel)`
  - _name: `farm.waste.transformation.wizard`
  - _description: "Waste Transformation Wizard"
  - Relationships:
    - Extends: Transient model for waste transformation operations

## Quality Models

Quality models ensure product quality and compliance throughout the farming process.

- **farm_quality.FarmQualityPoint** (`farm.quality.point`): Quality control points for farming operations
  - Odoo Model: `class FarmQualityPoint(models.Model)`
  - _name: `farm.quality.point`
  - _description: "Quality Control Point"
  - Fields:
    - `name` (Char): Title of the quality point (required)
    - `product_id` (Many2one): Associated product/variety (product.product)
    - `test_type` (Selection): Test type (pass_fail, measure)
    - `norm` (Float): Measurement norm
    - `tolerance_min` (Float): Minimum tolerance
    - `tolerance_max` (Float): Maximum tolerance
    - `active` (Boolean): Active status
  - Relationships:
    - Many2one: `product_id` → `product.product`

- **farm_quality.FarmQualityCheck** (`farm.quality.check`): Quality checks for farming operations
  - Odoo Model: `class FarmQualityCheck(models.Model)`
  - _name: `farm.quality.check`
  - _description: "Quality Check"
  - _inherit: `mail.thread`, `mail.activity.mixin`
  - Fields:
    - `name` (Char): Reference (required, default: New)
    - `point_id` (Many2one): Control point (farm.quality.point)
    - `lot_id` (Many2one): Lot/Batch (required) (stock.lot)
    - `sample_id` (Many2one): Linked sample (farm.quality.sample)
    - `task_id` (Many2one): Production task (project.task)
    - `test_type` (Selection): Test type (related to point_id.test_type)
    - `measure` (Float): Actual measure
    - `quality_state` (Selection): Status (none, pass, fail)
    - `user_id` (Many2one): Responsible user (res.users)
    - `is_blind_view` (Boolean): Whether to show masked information (computed)
  - Properties:
    - `display_lot_name`: Returns lot name to display (with masking if blind view)
    - `display_product_name`: Returns product name to display (with masking if blind view)
  - Methods:
    - `_compute_blind_view()`: Computes whether the current user should see masked information
    - `create()`: Creates new quality check with sequence number
    - `action_pass()`: Marks the check as passed
    - `action_fail()`: Marks the check as failed
    - `action_done()`: Processes measure-type checks based on tolerance range
    - `action_open_quality_alert()`: Creates and returns quality alert record
  - Relationships:
    - Many2one: `point_id` → `farm.quality.point`
    - Many2one: `lot_id` → `stock.lot`
    - Many2one: `sample_id` → `farm.quality.sample`
    - Many2one: `task_id` → `project.task`
    - Many2one: `user_id` → `res.users`
    - Inherits from: `mail.thread`, `mail.activity.mixin`

- **farm_quality.FarmQualityAlert** (`farm.quality.alert`): Quality alerts for farming operations
  - Odoo Model: `class FarmQualityAlert(models.Model)`
  - _name: `farm.quality.alert`
  - _description: "Quality Alert"
  - _inherit: `mail.thread`, `mail.activity.mixin`
  - Fields:
    - `name` (Char): Title (required)
    - `check_id` (Many2one): Source check (farm.quality.check)
    - `lot_id` (Many2one): Lot/Batch (required) (stock.lot)
    - `product_id` (Many2one): Product (product.product)
    - `user_id` (Many2one): Responsible user (res.users)
    - `priority` (Selection): Priority (low, normal, high)
    - `description` (Text): Description
    - `cause` (Text): Root cause
    - `action_taken` (Text): Action taken
    - `state` (Selection): Status (new, confirmed, action_proposed, closed)
  - Methods:
    - `action_confirm()`: Confirms the quality alert
    - `action_close_scrapped()`: Closes alert and marks asset for scrapping
  - Relationships:
    - Many2one: `check_id` → `farm.quality.check`
    - Many2one: `lot_id` → `stock.lot`
    - Many2one: `product_id` → `product.product`
    - Many2one: `user_id` → `res.users`
    - Inherits from: `mail.thread`, `mail.activity.mixin`

- **farm_quality.FarmLotQuality** (`stock.lot`): Quality tracking for lots (extends stock.lot)
  - Odoo Model: `class FarmLotQuality(models.Model)`
  - _name: `stock.lot` (Extends existing model)
  - _inherit: `stock.lot`
  - Fields:
    - `quality_status` (Selection): Quality status (none, passed, failed)
    - `qc_release_state` (Selection): QC release status (locked, released)
    - `quality_check_ids` (One2many): Quality checks (farm.quality.check)
  - Methods:
    - `action_qc_release()`: Manually releases the lot
    - `action_lock()`: Manually locks the lot
  - Relationships:
    - One2many: `quality_check_ids` → `farm.quality.check.lot_id`
    - Inherits from: `stock.lot`

- **farm_quality.FarmQualitySample**: Quality samples for testing
  - Odoo Model: `class FarmQualitySample(models.Model)`
  - _name: `farm.quality.sample`
  - _description: "Quality Sample"
  - Relationships:
    - Extends: Base models with quality sample functionality

- **farm_quality.StockPicking**: Quality-enhanced stock picking (extends stock.picking)
  - Odoo Model: `class StockPicking(models.Model)`
  - _name: `stock.picking` (Extends existing model)
  - _inherit: `stock.picking`
  - Methods:
    - `button_validate()`: Quality and release interception logic
  - Relationships:
    - Inherits from: `stock.picking`

## Safety Models

Safety models handle biosafety and prevention management.

- **farm_safety.FarmPreventionTemplate**: Prevention templates for safety
  - Odoo Model: `class FarmPreventionTemplate(models.Model)`
  - _name: `farm.prevention.template`
  - _description: "Agri-Prevention Template"
  - Fields:
    - `name` (Char): Template Name (required)
    - `active` (Boolean): Active status (default: True)
    - `line_ids` (One2many): Operations (farm.prevention.line)
    - `company_id` (Many2one): Company (res.company)
  - Relationships:
    - One2many: `line_ids` → `farm.prevention.line.template_id`
    - Many2one: `company_id` → `res.company` (default: current company)

- **farm_safety.FarmPreventionLine**: Line items for prevention measures
  - Odoo Model: `class FarmPreventionLine(models.Model)`
  - _name: `farm.prevention.line`
  - _description: "Prevention Operation Line"
  - _order: "delay_days asc"
  - Fields:
    - `template_id` (Many2one): Template (farm.prevention.template, ondelete=cascade)
    - `name` (Char): Operation Name (required)
    - `delay_days` (Integer): Delay Days (T+N) (default: 0)
    - `product_id` (Many2one): Vaccine/Medicine (product.product)
    - `qty` (Float): Quantity (default: 1.0)
  - Relationships:
    - Many2one: `template_id` → `farm.prevention.template` with cascade delete
    - Many2one: `product_id` → `product.product`

- **farm_safety.FarmLotQuarantine**: Quarantine management for lots
  - Odoo Model: `class FarmLotQuarantine(models.Model)`
  - _name: `stock.lot`
  - _inherit: `stock.lot`
  - Fields:
    - `is_quarantined` (Boolean): In Quarantine (default: False, tracking=True)
    - `quarantine_reason` (Text): Quarantine Reason
    - `quarantine_start_date` (Date): Quarantine Start
    - `withdrawal_end_datetime` (Datetime): Withdrawal End (tracking=True)
    - `withdrawal_status` (Selection): Safety Status (safe, warning) (computed, stored)
    - `withdrawal_remaining_days` (Integer): Safe Harvest Countdown (computed)
  - Methods:
    - `_compute_withdrawal_status()`: Computes withdrawal safety status
    - `_compute_withdrawal_remaining()`: Computes withdrawal remaining days
    - `action_quarantine(reason, is_epidemic)`: Quarantines asset and generates buffer fence
    - `action_release_quarantine()`: Releases asset from quarantine
  - Relationships:
    - Inherits: `stock.lot` (Odoo's stock lot model) with quarantine functionality

- **farm_safety.StockPickingQuarantine**: Quarantine management for stock picking
  - Odoo Model: `class StockPickingQuarantine(models.Model)`
  - _name: `stock.picking`
  - _inherit: `stock.picking`
  - Methods:
    - `button_validate()`: Quarantine and withdrawal period interception logic
  - Relationships:
    - Inherits: `stock.picking` (Odoo's stock picking model) with safety validation

- **farm_safety.ProjectTask**: Safety-enhanced project task management
  - Odoo Model: `class ProjectTask(models.Model)`
  - _name: `project.task`
  - _inherit: `project.task`
  - Fields:
    - `prevention_template_id` (Many2one): Prevention Plan (farm.prevention.template)
  - Methods:
    - `action_confirm_intervention_safety(product_ids)`: Updates withdrawal period for medication interventions
    - `action_apply_prevention_template()`: Generates subtasks from prevention template
  - Relationships:
    - Many2one: `prevention_template_id` → `farm.prevention.template`
    - Inherits: `project.task` (Odoo's project task model) with safety features

- **farm_safety.FarmBiosafetyAccessLog**: Biosafety access logging
  - Odoo Model: `class FarmBiosafetyAccessLog(models.Model)`
  - _name: `farm.biosafety.access.log`
  - _description: "Bio-safety Access Log"
  - _inherit: `mail.thread`, `mail.activity.mixin`
  - _order: "access_time desc"
  - Fields:
    - `location_id` (Many2one): Restricted Area (stock.location, usage=internal, required)
    - `person_id` (Many2one): Person/Visitor (res.partner)
    - `employee_id` (Many2one): Employee (hr.employee)
    - `access_time` (Datetime): Access Time (default: now)
    - `access_type` (Selection): Type (entry, exit) (required, default: entry)
    - `sanitization_confirmed` (Boolean): Sanitization Performed (default: False)
    - `quarantine_period_passed` (Boolean): Quarantine Period Passed (default: True)
    - `vehicle_plate` (Char): Vehicle Plate
    - `purpose` (Text): Purpose of Entry
  - Methods:
    - `create()`: Creates access log and warns on missing sanitization
  - Relationships:
    - Many2one: `location_id` → `stock.location`
    - Many2one: `person_id` → `res.partner`
    - Many2one: `employee_id` → `hr.employee`

## Certification Models

Certification models handle compliance and certification requirements.

- **farm_certification.FarmLocationCert**: Certification for farm locations
  - Odoo Model: `class FarmLocationCert(models.Model)`
  - _name: `farm.location.cert`
  - _description: "Farm Location Certification"
  - Relationships:
    - Extends: Base models with location certification functionality

- **farm_certification.FarmLotCert**: Certification for lots
  - Odoo Model: `class FarmLotCert(models.Model)`
  - _name: `farm.lot.cert`
  - _description: "Farm Lot Certification"
  - Relationships:
    - Extends: Base models with lot certification functionality

- **farm_certification.FarmGAPCertification**: Good Agricultural Practices certification
  - Odoo Model: `class FarmGAPCertification(models.Model)`
  - _name: `farm.gap.certification`
  - _description: "Good Agricultural Practices Certification"
  - Fields:
    - `name` (Char): Certification reference
    - `location_id` (Many2one): Associated farm location (farm.location)
    - `certifying_body_id` (Many2one): Certifying organization (res.partner)
    - `certification_date` (Date): Date of certification
    - `valid_from` (Date): Start date of validity
    - `valid_to` (Date): End date of validity
    - `status` (Selection): Certification status (active, suspended, expired)
    - `scope` (Text): Scope of certification
    - `standards` (Text): Standards applied
  - Methods:
    - `action_renew()`: Renew the certification
    - `action_suspend()`: Suspend the certification
    - `action_cancel()`: Cancel the certification
  - Relationships:
    - Many2one: `location_id` → `farm.location`
    - Many2one: `certifying_body_id` → `res.partner`

- **farm_certification.FarmGAPAudit**: GAP audit management
  - Odoo Model: `class FarmGAPAudit(models.Model)`
  - _name: `farm.gap.audit`
  - _description: "GAP Audit Management"
  - Fields:
    - `name` (Char): Audit reference
    - `certification_id` (Many2one): Associated certification (farm.gap.certification)
    - `audit_date` (Date): Date of audit
    - `auditor_id` (Many2one): Assigned auditor (res.partner)
    - `audit_type` (Selection): Type of audit (initial, surveillance, recertification)
    - `findings` (Text): Audit findings
    - `status` (Selection): Audit status (planned, in_progress, completed, failed)
    - `recommendations` (Text): Recommendations
  - Methods:
    - `action_start_audit()`: Start the audit
    - `action_complete_audit()`: Complete the audit
  - Relationships:
    - Many2one: `certification_id` → `farm.gap.certification`
    - Many2one: `auditor_id` → `res.partner`

- **farm_certification.FarmGAPRequirement**: GAP requirements management
  - Odoo Model: `class FarmGAPRequirement(models.Model)`
  - _name: `farm.gap.requirement`
  - _description: "GAP Requirements Management"
  - Relationships:
    - Extends: Base models with GAP requirement functionality

- **farm_certification.FarmGAPComplianceCheck**: GAP compliance checks
  - Odoo Model: `class FarmGAPComplianceCheck(models.Model)`
  - _name: `farm.gap.compliance.check`
  - _description: "GAP Compliance Checks"
  - Relationships:
    - Extends: Base models with compliance check functionality

- **farm_certification.FarmCertificationDashboard**: Dashboard for certification management
  - Odoo Model: `class FarmCertificationDashboard(models.Model)`
  - _name: `farm.certification.dashboard`
  - _description: "Certification Management Dashboard"
  - Relationships:
    - Extends: Base models with dashboard functionality

- **farm_certification.ResPartner**: Certification-enhanced partner records
  - Odoo Model: `class ResPartner(models.Model)`
  - _name: `res.partner`
  - _description: "Certification-Enhanced Partner Records"
  - _inherit: `res.partner`
  - Relationships:
    - Extends: `res.partner` (Odoo's native partner model) with certification enhancements

- **farm_certification.FarmPartnerCertification**: Partner certification management
  - Odoo Model: `class FarmPartnerCertification(models.Model)`
  - _name: `farm.partner.certification`
  - _description: "Partner Certification Management"
  - Relationships:
    - Extends: Base models with partner certification functionality

- **farm_certification.PurchaseOrder**: Certification-enhanced purchase orders
  - Odoo Model: `class PurchaseOrder(models.Model)`
  - _name: `purchase.order`
  - _description: "Certification-Enhanced Purchase Orders"
  - _inherit: `purchase.order`
  - Relationships:
    - Extends: `purchase.order` (Odoo's native purchase order model) with certification enhancements

## Weather Models

Weather models provide environmental data and forecasting capabilities.

- **farm_weather.FarmWeatherForecast**: Weather forecasting for farming operations
- **farm_weather.ResConfigSettings**: Configuration settings for weather features

## IoT Models

IoT models handle telemetry, automation, and device management for smart farming.

- **farm_iot.FarmTelemetry**: Telemetry data collection for farming
- **farm_iot.FarmLocation**: IoT-enhanced farm location tracking
- **farm_iot.FarmAutomationRule**: Automation rules for IoT devices
- **farm_iot.FarmCommandLog**: Logging of commands sent to IoT devices
- **farm_iot.IotDeviceMapping**: Mapping of IoT devices to farm assets
- **farm_iot.IotTelemetryBuffer**: Buffer for incoming telemetry data
- **farm_iot.FarmDeviceCommand**: Commands for IoT devices

## Mobile Models

Mobile models handle mobile app functionality for field operations.

- **farm_mobile.FarmEvidence**: Evidence collection for mobile operations
  - Odoo Model: `class FarmEvidence(models.Model)`
  - _name: `farm.evidence`
  - _description: "Mobile Evidence Collection"
  - Relationships:
    - Extends: Base models with mobile evidence functionality

- **farm_mobile.FarmSyncQueue**: Synchronization queue for mobile operations
  - Odoo Model: `class FarmSyncQueue(models.Model)`
  - _name: `farm.sync.queue`
  - _description: "Mobile Synchronization Queue"
  - Relationships:
    - Extends: Base models with sync queue functionality

- **farm_mobile.FarmCheckIn**: Check-in functionality for mobile operations
  - Odoo Model: `class FarmCheckIn(models.Model)`
  - _name: `farm.checkin`
  - _description: "Mobile Check-in Functionality"
  - Relationships:
    - Extends: Base models with check-in functionality

- **farm_mobile.FarmChecklistSubmission**: Checklist submissions from mobile
  - Odoo Model: `class FarmChecklistSubmission(models.Model)`
  - _name: `farm.checklist.submission`
  - _description: "Mobile Checklist Submission"
  - Relationships:
    - Extends: Base models with checklist submission functionality

- **farm_mobile.FarmChecklistSubmissionLine**: Line items for checklist submissions
  - Odoo Model: `class FarmChecklistSubmissionLine(models.Model)`
  - _name: `farm.checklist.submission.line`
  - _description: "Mobile Checklist Submission Line Items"
  - Relationships:
    - Extends: Base models with checklist submission line functionality

- **farm_mobile.FarmExpertCall**: Expert call functionality for mobile
  - Odoo Model: `class FarmExpertCall(models.Model)`
  - _name: `farm.expert.call`
  - _description: "Mobile Expert Call Functionality"
  - Relationships:
    - Extends: Base models with expert call functionality

- **farm_mobile.AgriIntervention** (`mrp.production`): Mobile-enhanced agricultural interventions (extends mrp.production)
  - Odoo Model: `class AgriIntervention(models.Model)`
  - _name: `mrp.production` (Extends existing model)
  - _inherit: `mrp.production`
  - Fields:
    - `check_in_ids` (One2many): Check-in history (farm.checkin)
    - `evidence_ids` (One2many): Site evidence records (farm.evidence)
    - `current_check_in_id` (Many2one): Active check-in (computed) (farm.checkin)
  - Methods:
    - `action_mobile_capture_evidence(lat, lng, photo_base64, note)`: Mobile-specific evidence capture
  - Relationships:
    - Inherits from: `mrp.production`
    - One2many: `check_in_ids` → `farm.checkin.intervention_id`
    - One2many: `evidence_ids` → `farm.evidence` with domain filter
    - Many2one: `current_check_in_id` → `farm.checkin`

## Supply Models

Supply models handle inventory, procurement, and supply chain management.

### Basic Supply Management
- **farm_supply.FarmSeasonalStockRule**: Seasonal stock rules for supply management
- **farm_supply.ProductTemplate**: Supply-specific product templates
- **farm_supply.SaleOrder**: Supply-specific sale orders
- **farm_supply.PurchaseOrder**: Supply-specific purchase orders
- **farm_supply.PurchaseOrderLine**: Line items for purchase orders

### Risk and Planning
- **farm_supply.SupplyRiskRadar**: Risk radar for supply management

### Advanced Supply Features
- **farm_supply.InputVMIConfiguration**: Vendor-managed inventory configuration
- **farm_supply.VMISensorReading**: Sensor readings for VMI
- **farm_supply.QualityBasedPricing**: Quality-based pricing models
- **farm_supply.JointProcurementConfiguration**: Configuration for joint procurement
- **farm_supply.JointProcurementOrder**: Joint procurement orders
- **farm_supply.CircularAssetTracking**: Tracking of circular assets
- **farm_supply.AssetRentalAgreement**: Rental agreements for assets

### Storage Management
- **farm_supply.StockLocationExtension**: Extensions to stock locations for supply
- **farm_supply.ColdStorageReading**: Cold storage monitoring
- **farm_supply.StockMoveExtension**: Extensions to stock moves for supply
- **farm_supply.ProductTemplateExtension**: Extensions to product templates for supply

### Logistics and Compliance
- **farm_supply.SafePODConfiguration**: POD configuration for safe delivery
- **farm_supply.DeliveryTrackingRecord**: Records of delivery tracking
- **farm_supply.ExportDocumentHub**: Export documentation hub
- **farm_supply.ExportGeneratedDocument**: Generated export documents

### Temperature Management
- **farm_supply.ShelfLifePrediction**: Shelf life prediction models
- **farm_supply.TemperatureReading**: Temperature readings for supply chain
- **farm_supply.PrecoolingProcess**: Precooling process management
- **farm_supply.PrecoolingTemperature**: Temperature management for precooling

### Abstract Utilities
- **farm_supply.CommonFieldMixin** (Abstract): Provides common fields
- **farm_supply.CreationMethodMixin** (Abstract): Provides creation method utilities
- **farm_supply.ComputedFieldMixin** (Abstract): Provides computed field utilities
- **farm_supply.ComplianceMixin** (Abstract): Provides compliance utilities
- **farm_supply.StorageManagementMixin** (Abstract): Provides storage management utilities
- **farm_supply.QualityManagementMixin** (Abstract): Provides quality management utilities

## Logistics Models

Logistics models handle transportation and logistics.

- **farm_logistics.ProductTemplate**: Logistics-enhanced product templates
- **farm_logistics.StockPicking**: Logistics-enhanced stock picking
- **farm_logistics.FarmVehicle**: Vehicle management for logistics
- **farm_logistics.FarmTransportTemperature**: Temperature management for transport

## Multi-Farm Models

Multi-farm models handle cooperative farming, shared resources, and multi-farm operations.

### Cooperative Management
- **farm_multi_farm.CooperativeMember**: Members of farming cooperatives
  - Odoo Model: `class CooperativeMember(models.Model)`
  - _name: `farm.cooperative.member`
  - _description: "Cooperative Member Management"
  - Relationships:
    - Extends: Base models with cooperative member functionality

- **farm_multi_farm.CooperativeEntity**: Cooperative entity management
  - Odoo Model: `class CooperativeEntity(models.Model)`
  - _name: `farm.cooperative.entity`
  - _description: "Cooperative Entity Management"
  - Relationships:
    - Extends: Base models with cooperative entity functionality

- **farm_multi_farm.FarmEntity**: Farm entity management
  - Odoo Model: `class FarmEntity(models.Model)`
  - _name: `farm.entity`
  - _description: "Farm Entity Management"
  - Relationships:
    - Extends: Base models with farm entity functionality

- **farm_multi_farm.FranchiseFarm**: Franchise farm management
  - Odoo Model: `class FranchiseFarm(models.Model)`
  - _name: `farm.franchise.farm`
  - _description: "Franchise Farm Management"
  - Relationships:
    - Extends: Base models with franchise farm functionality

### Financial Management
- **farm_multi_farm.ShareTransaction**: Share transaction management
  - Odoo Model: `class ShareTransaction(models.Model)`
  - _name: `farm.share.transaction`
  - _description: "Share Transaction Management"
  - Relationships:
    - Extends: Base models with share transaction functionality

- **farm_multi_farm.DividendDistribution**: Dividend distribution for cooperatives
  - Odoo Model: `class DividendDistribution(models.Model)`
  - _name: `farm.dividend.distribution`
  - _description: "Dividend Distribution for Cooperatives"
  - Relationships:
    - Extends: Base models with dividend distribution functionality

- **farm_multi_farm.DividendLine**: Line items for dividend distributions
  - Odoo Model: `class DividendLine(models.Model)`
  - _name: `farm.dividend.line`
  - _description: "Dividend Distribution Line Items"
  - Relationships:
    - Extends: Base models with dividend line functionality

- **farm_multi_farm.InternalCredit**: Internal credit management
  - Odoo Model: `class InternalCredit(models.Model)`
  - _name: `farm.internal.credit`
  - _description: "Internal Credit Management"
  - Relationships:
    - Extends: Base models with internal credit functionality

- **farm_multi_farm.CreditTransaction**: Credit transaction management
  - Odoo Model: `class CreditTransaction(models.Model)`
  - _name: `farm.credit.transaction`
  - _description: "Credit Transaction Management"
  - Relationships:
    - Extends: Base models with credit transaction functionality

- **farm_multi_farm.CooperativeTreasury**: Treasury management for cooperatives
  - Odoo Model: `class CooperativeTreasury(models.Model)`
  - _name: `farm.cooperative.treasury`
  - _description: "Treasury Management for Cooperatives"
  - Relationships:
    - Extends: Base models with treasury functionality

- **farm_multi_farm.InternalLoan**: Internal loan management
  - Odoo Model: `class InternalLoan(models.Model)`
  - _name: `farm.internal.loan`
  - _description: "Internal Loan Management"
  - Relationships:
    - Extends: Base models with internal loan functionality

### Subsidy and Governance
- **farm_multi_farm.SubsidyDisbursement**: Subsidy disbursement management
  - Odoo Model: `class SubsidyDisbursement(models.Model)`
  - _name: `farm.subsidy.disbursement`
  - _description: "Subsidy Disbursement Management"
  - Relationships:
    - Extends: Base models with subsidy disbursement functionality

- **farm_multi_farm.SubsidyDisbursementLine**: Line items for subsidy disbursements
  - Odoo Model: `class SubsidyDisbursementLine(models.Model)`
  - _name: `farm.subsidy.disbursement.line`
  - _description: "Subsidy Disbursement Line Items"
  - Relationships:
    - Extends: Base models with subsidy disbursement line functionality

- **farm_multi_farm.CooperativeDecision**: Cooperative decision management
  - Odoo Model: `class CooperativeDecision(models.Model)`
  - _name: `farm.cooperative.decision`
  - _description: "Cooperative Decision Management"
  - Relationships:
    - Extends: Base models with cooperative decision functionality

### Machinery and Resource Sharing
- **farm_multi_farm.SharedMachineryPool**: Shared machinery pool management
  - Odoo Model: `class SharedMachineryPool(models.Model)`
  - _name: `farm.shared.machinery.pool`
  - _description: "Shared Machinery Pool Management"
  - Relationships:
    - Extends: Base models with shared machinery functionality

- **farm_multi_farm.MachineryRental**: Machinery rental management
  - Odoo Model: `class MachineryRental(models.Model)`
  - _name: `farm.machinery.rental`
  - _description: "Machinery Rental Management"
  - Relationships:
    - Extends: Base models with machinery rental functionality

- **farm_multi_farm.ResourceSharing**: Resource sharing management
  - Odoo Model: `class ResourceSharing(models.Model)`
  - _name: `farm.resource.sharing`
  - _description: "Resource Sharing Management"
  - Relationships:
    - Extends: Base models with resource sharing functionality

### Procurement and Distribution
- **farm_multi_farm.JointProcurementPO**: Joint procurement purchase orders
  - Odoo Model: `class JointProcurementPO(models.Model)`
  - _name: `farm.joint.procurement.po`
  - _description: "Joint Procurement Purchase Orders"
  - Relationships:
    - Extends: `purchase.order` with joint procurement functionality

- **farm_multi_farm.JointProcurementPOMember**: Member relationships for joint procurement
  - Odoo Model: `class JointProcurementPOMember(models.Model)`
  - _name: `farm.joint.procurement.po.member`
  - _description: "Joint Procurement PO Member Relationships"
  - Relationships:
    - Extends: Base models with joint procurement member functionality

- **farm_multi_farm.HubSpokeDistribution**: Hub-and-spoke distribution model
  - Odoo Model: `class HubSpokeDistribution(models.Model)`
  - _name: `farm.hub.spoke.distribution`
  - _description: "Hub-and-Spoke Distribution Model"
  - Relationships:
    - Extends: Base models with hub-and-spoke distribution functionality

- **farm_multi_farm.HubSpokeDistributionLine**: Line items for hub-and-spoke distribution
  - Odoo Model: `class HubSpokeDistributionLine(models.Model)`
  - _name: `farm.hub.spoke.distribution.line`
  - _description: "Hub-and-Spoke Distribution Line Items"
  - Relationships:
    - Extends: Base models with hub-and-spoke distribution line functionality

- **farm_multi_farm.JointProcurement**: Joint procurement management
  - Odoo Model: `class JointProcurement(models.Model)`
  - _name: `farm.joint.procurement`
  - _description: "Joint Procurement Management"
  - Relationships:
    - Extends: Base models with joint procurement functionality

- **farm_multi_farm.JointProcurementLine**: Line items for joint procurement
  - Odoo Model: `class JointProcurementLine(models.Model)`
  - _name: `farm.joint.procurement.line`
  - _description: "Joint Procurement Line Items"
  - Relationships:
    - Extends: Base models with joint procurement line functionality

### Settlement and Transactions
- **farm_multi_farm.NettingSettlement**: Netting settlement for transactions
  - Odoo Model: `class NettingSettlement(models.Model)`
  - _name: `farm.netting.settlement`
  - _description: "Netting Settlement for Transactions"
  - Relationships:
    - Extends: Base models with netting settlement functionality

- **farm_multi_farm.NettingReceivableLine**: Receivable line items for netting
  - Odoo Model: `class NettingReceivableLine(models.Model)`
  - _name: `farm.netting.receivable.line`
  - _description: "Netting Receivable Line Items"
  - Relationships:
    - Extends: Base models with netting receivable functionality

- **farm_multi_farm.NettingPayableLine**: Payable line items for netting
  - Odoo Model: `class NettingPayableLine(models.Model)`
  - _name: `farm.netting.payable.line`
  - _description: "Netting Payable Line Items"
  - Relationships:
    - Extends: Base models with netting payable functionality

### Marketplace and Services
- **farm_multi_farm.InternalMarketplace**: Internal marketplace management
  - Odoo Model: `class InternalMarketplace(models.Model)`
  - _name: `farm.internal.marketplace`
  - _description: "Internal Marketplace Management"
  - Relationships:
    - Extends: Base models with internal marketplace functionality

- **farm_multi_farm.MarketplaceDemandMatch**: Demand matching for marketplace
  - Odoo Model: `class MarketplaceDemandMatch(models.Model)`
  - _name: `farm.marketplace.demand.match`
  - _description: "Marketplace Demand Matching"
  - Relationships:
    - Extends: Base models with marketplace demand matching functionality

- **farm_multi_farm.InternalMarketplaceTransaction**: Transactions in internal marketplace
  - Odoo Model: `class InternalMarketplaceTransaction(models.Model)`
  - _name: `farm.internal.marketplace.transaction`
  - _description: "Internal Marketplace Transactions"
  - Relationships:
    - Extends: Base models with internal marketplace transaction functionality

- **farm_multi_farm.AgriService**: Agricultural service management
  - Odoo Model: `class AgriService(models.Model)`
  - _name: `farm.agri.service`
  - _description: "Agricultural Service Management"
  - Relationships:
    - Extends: Base models with agricultural service functionality

- **farm_multi_farm.ServiceOrder**: Service order management
  - Odoo Model: `class ServiceOrder(models.Model)`
  - _name: `farm.service.order`
  - _description: "Service Order Management"
  - Relationships:
    - Extends: `sale.order` with service order functionality

### Quality and Certification
- **farm_multi_farm.QualityControlStandard**: Quality control standards
  - Odoo Model: `class QualityControlStandard(models.Model)`
  - _name: `farm.quality.control.standard`
  - _description: "Quality Control Standards"
  - Relationships:
    - Extends: Base models with quality control standard functionality

- **farm_multi_farm.ProductCertification**: Product certification management
  - Odoo Model: `class ProductCertification(models.Model)`
  - _name: `farm.product.certification`
  - _description: "Product Certification Management"
  - Relationships:
    - Extends: Base models with product certification functionality

### Procurement Planning
- **farm_multi_farm.ProcurementPlanning**: Procurement planning management
  - Odoo Model: `class ProcurementPlanning(models.Model)`
  - _name: `farm.procurement.planning`
  - _description: "Procurement Planning Management"
  - Relationships:
    - Extends: Base models with procurement planning functionality

- **farm_multi_farm.ProcurementPlanningLine**: Line items for procurement planning
  - Odoo Model: `class ProcurementPlanningLine(models.Model)`
  - _name: `farm.procurement.planning.line`
  - _description: "Procurement Planning Line Items"
  - Relationships:
    - Extends: Base models with procurement planning line functionality

- **farm_multi_farm.ProcurementAllocationLine**: Allocation line items for procurement
  - Odoo Model: `class ProcurementAllocationLine(models.Model)`
  - _name: `farm.procurement.allocation.line`
  - _description: "Procurement Allocation Line Items"
  - Relationships:
    - Extends: Base models with procurement allocation line functionality

### Governance and Audit
- **farm_multi_farm.MultiSignProcess**: Multi-signature process management
  - Odoo Model: `class MultiSignProcess(models.Model)`
  - _name: `farm.multi.sign.process`
  - _description: "Multi-Signature Process Management"
  - Relationships:
    - Extends: Base models with multi-signature process functionality

- **farm_multi_farm.MultiSignLine**: Line items for multi-signature processes
  - Odoo Model: `class MultiSignLine(models.Model)`
  - _name: `farm.multi.sign.line`
  - _description: "Multi-Signature Process Line Items"
  - Relationships:
    - Extends: Base models with multi-signature line functionality

- **farm_multi_farm.DecisionAudit**: Audit trail for decisions
  - Odoo Model: `class DecisionAudit(models.Model)`
  - _name: `farm.decision.audit`
  - _description: "Decision Audit Trail"
  - Relationships:
    - Extends: Base models with decision audit functionality

### Extensions
- **farm_multi_farm.CooperativeMemberExtension**: Extensions to cooperative members
  - Odoo Model: `class CooperativeMemberExtension(models.Model)`
  - _name: `farm.cooperative.member.extension`
  - _description: "Cooperative Member Extensions"
  - Relationships:
    - Extends: `farm.cooperative.member` with additional functionality

- **farm_multi_farm.InternalSettlementExtension**: Extensions to internal settlements
  - Odoo Model: `class InternalSettlementExtension(models.Model)`
  - _name: `farm.internal.settlement.extension`
  - _description: "Internal Settlement Extensions"
  - Relationships:
    - Extends: Base models with internal settlement extensions

- **farm_multi_farm.CooperativeEntityExtension**: Extensions to cooperative entities
  - Odoo Model: `class CooperativeEntityExtension(models.Model)`
  - _name: `farm.cooperative.entity.extension`
  - _description: "Cooperative Entity Extensions"
  - Relationships:
    - Extends: `farm.cooperative.entity` with additional functionality

- **farm_multi_farm.FarmEntityExtension**: Extensions to farm entities
  - Odoo Model: `class FarmEntityExtension(models.Model)`
  - _name: `farm.entity.extension`
  - _description: "Farm Entity Extensions"
  - Relationships:
    - Extends: `farm.entity` with additional functionality

### Finance and Management Utilities (Abstract)
- **farm_multi_farm.BaseSequenceMixin** (Abstract): Provides sequence utilities for multi-farm
  - Odoo Model: `class BaseSequenceMixin(models.AbstractModel)`
  - _name: `farm.multi.farm.base.sequence.mixin`
  - _description: "Base Sequence Mixin for Multi-Farm"
  - Relationships:
    - Inherits: `models.AbstractModel`

- **farm_multi_farm.BaseCodeMixin** (Abstract): Provides code utilities for multi-farm
  - Odoo Model: `class BaseCodeMixin(models.AbstractModel)`
  - _name: `farm.multi.farm.base.code.mixin`
  - _description: "Base Code Mixin for Multi-Farm"
  - Relationships:
    - Inherits: `models.AbstractModel`

- **farm_multi_farm.BaseTotalAmountMixin** (Abstract): Provides total amount utilities for multi-farm
  - Odoo Model: `class BaseTotalAmountMixin(models.AbstractModel)`
  - _name: `farm.multi.farm.base.total.amount.mixin`
  - _description: "Base Total Amount Mixin for Multi-Farm"
  - Relationships:
    - Inherits: `models.AbstractModel`

- **farm_multi_farm.BaseInvestmentAmountMixin** (Abstract): Provides investment amount utilities for multi-farm
  - Odoo Model: `class BaseInvestmentAmountMixin(models.AbstractModel)`
  - _name: `farm.multi.farm.base.investment.amount.mixin`
  - _description: "Base Investment Amount Mixin for Multi-Farm"
  - Relationships:
    - Inherits: `models.AbstractModel`

- **farm_multi_farm.BaseServiceAmountMixin** (Abstract): Provides service amount utilities for multi-farm
  - Odoo Model: `class BaseServiceAmountMixin(models.AbstractModel)`
  - _name: `farm.multi.farm.base.service.amount.mixin`
  - _description: "Base Service Amount Mixin for Multi-Farm"
  - Relationships:
    - Inherits: `models.AbstractModel`

- **farm_multi_farm.BaseActionConfirmMixin** (Abstract): Provides action confirmation utilities for multi-farm
  - Odoo Model: `class BaseActionConfirmMixin(models.AbstractModel)`
  - _name: `farm.multi.farm.base.action.confirm.mixin`
  - _description: "Base Action Confirmation Mixin for Multi-Farm"
  - Relationships:
    - Inherits: `models.AbstractModel`

- **farm_multi_farm.BaseActionApproveMixin** (Abstract): Provides action approval utilities for multi-farm
  - Odoo Model: `class BaseActionApproveMixin(models.AbstractModel)`
  - _name: `farm.multi.farm.base.action.approve.mixin`
  - _description: "Base Action Approval Mixin for Multi-Farm"
  - Relationships:
    - Inherits: `models.AbstractModel`

- **farm_multi_farm.BaseActionRejectMixin** (Abstract): Provides action rejection utilities for multi-farm
  - Odoo Model: `class BaseActionRejectMixin(models.AbstractModel)`
  - _name: `farm.multi.farm.base.action.reject.mixin`
  - _description: "Base Action Rejection Mixin for Multi-Farm"
  - Relationships:
    - Inherits: `models.AbstractModel`

- **farm_multi_farm.BaseActionCancelMixin** (Abstract): Provides action cancellation utilities for multi-farm
  - Odoo Model: `class BaseActionCancelMixin(models.AbstractModel)`
  - _name: `farm.multi.farm.base.action.cancel.mixin`
  - _description: "Base Action Cancellation Mixin for Multi-Farm"
  - Relationships:
    - Inherits: `models.AbstractModel`

- **farm_multi_farm.BaseCreditLimitMixin** (Abstract): Provides credit limit utilities for multi-farm
  - Odoo Model: `class BaseCreditLimitMixin(models.AbstractModel)`
  - _name: `farm.multi.farm.base.credit.limit.mixin`
  - _description: "Base Credit Limit Mixin for Multi-Farm"
  - Relationships:
    - Inherits: `models.AbstractModel`

- **farm_multi_farm.BaseLoanAmountMixin** (Abstract): Provides loan amount utilities for multi-farm
  - Odoo Model: `class BaseLoanAmountMixin(models.AbstractModel)`
  - _name: `farm.multi.farm.base.loan.amount.mixin`
  - _description: "Base Loan Amount Mixin for Multi-Farm"
  - Relationships:
    - Inherits: `models.AbstractModel`

- **farm_multi_farm.BaseAvailableAmountMixin** (Abstract): Provides available amount utilities for multi-farm
  - Odoo Model: `class BaseAvailableAmountMixin(models.AbstractModel)`
  - _name: `farm.multi.farm.base.available.amount.mixin`
  - _description: "Base Available Amount Mixin for Multi-Farm"
  - Relationships:
    - Inherits: `models.AbstractModel`

- **farm_multi_farm.BaseShareValueMixin** (Abstract): Provides share value utilities for multi-farm
  - Odoo Model: `class BaseShareValueMixin(models.AbstractModel)`
  - _name: `farm.multi.farm.base.share.value.mixin`
  - _description: "Base Share Value Mixin for Multi-Farm"
  - Relationships:
    - Inherits: `models.AbstractModel`

- **farm_multi_farm.BaseTotalInvestmentMixin** (Abstract): Provides total investment utilities for multi-farm
  - Odoo Model: `class BaseTotalInvestmentMixin(models.AbstractModel)`
  - _name: `farm.multi.farm.base.total.investment.mixin`
  - _description: "Base Total Investment Mixin for Multi-Farm"
  - Relationships:
    - Inherits: `models.AbstractModel`

- **farm_multi_farm.BaseAvailableCreditMixin** (Abstract): Provides available credit utilities for multi-farm
  - Odoo Model: `class BaseAvailableCreditMixin(models.AbstractModel)`
  - _name: `farm.multi.farm.base.available.credit.mixin`
  - _description: "Base Available Credit Mixin for Multi-Farm"
  - Relationships:
    - Inherits: `models.AbstractModel`

- **farm_multi_farm.BaseComplianceStatusMixin** (Abstract): Provides compliance status utilities for multi-farm
  - Odoo Model: `class BaseComplianceStatusMixin(models.AbstractModel)`
  - _name: `farm.multi.farm.base.compliance.status.mixin`
  - _description: "Base Compliance Status Mixin for Multi-Farm"
  - Relationships:
    - Inherits: `models.AbstractModel`

- **farm_multi_farm.BaseCertifiedStatusMixin** (Abstract): Provides certified status utilities for multi-farm
  - Odoo Model: `class BaseCertifiedStatusMixin(models.AbstractModel)`
  - _name: `farm.multi.farm.base.certified.status.mixin`
  - _description: "Base Certified Status Mixin for Multi-Farm"
  - Relationships:
    - Inherits: `models.AbstractModel`

- **farm_multi_farm.BaseNetAmountMixin** (Abstract): Provides net amount utilities for multi-farm
  - Odoo Model: `class BaseNetAmountMixin(models.AbstractModel)`
  - _name: `farm.multi.farm.base.net.amount.mixin`
  - _description: "Base Net Amount Mixin for Multi-Farm"
  - Relationships:
    - Inherits: `models.AbstractModel`

- **farm_multi_farm.BaseSettlementDirectionMixin** (Abstract): Provides settlement direction utilities for multi-farm
  - Odoo Model: `class BaseSettlementDirectionMixin(models.AbstractModel)`
  - _name: `farm.multi.farm.base.settlement.direction.mixin`
  - _description: "Base Settlement Direction Mixin for Multi-Farm"
  - Relationships:
    - Inherits: `models.AbstractModel`

- **farm_multi_farm.BaseAmountCalculationMixin** (Abstract): Provides amount calculation utilities for multi-farm
  - Odoo Model: `class BaseAmountCalculationMixin(models.AbstractModel)`
  - _name: `farm.multi.farm.base.amount.calculation.mixin`
  - _description: "Base Amount Calculation Mixin for Multi-Farm"
  - Relationships:
    - Inherits: `models.AbstractModel`

## Marketing Models

Marketing models handle sales and customer relationships.

- **farm_marketing.FarmPartner**: Partners for marketing operations
- **farm_marketing.FarmSaleOrder**: Sale orders for marketing operations
- **farm_marketing.FarmSaleOrderLine**: Line items for marketing sale orders
- **farm_marketing.FarmLotMarketing**: Marketing-specific lot management
- **farm_marketing.AgriGIRegistry**: Geographic indication registry for marketing
- **farm_marketing.StockLot**: Marketing-enhanced stock lot management

## Financial Models

Financial models handle accounting and financial operations for farms.

- **farm_financial.AccountMove**: Financial accounting entries
  - Odoo Model: `class AccountMove(models.Model)`
  - _name: `account.move`
  - _description: "Financial Accounting Entries"
  - _inherit: `account.move`
  - Relationships:
    - Extends: `account.move` (Odoo's native accounting entry model)

- **farm_financial.AccountMoveLine**: Line items for accounting entries
  - Odoo Model: `class AccountMoveLine(models.Model)`
  - _name: `account.move.line`
  - _description: "Financial Accounting Entry Line Items"
  - _inherit: `account.move.line`
  - Relationships:
    - Extends: `account.move.line` (Odoo's native accounting line model)

- **farm_financial.ProcessingCostAllocation**: Allocation of processing costs
  - Odoo Model: `class ProcessingCostAllocation(models.Model)`
  - _name: `farm.processing.cost.allocation`
  - _description: "Processing Cost Allocation"
  - Relationships:
    - Extends: Base models with processing cost allocation functionality

- **farm_financial.AgriCostWIPTransfer** (Abstract): Work-in-progress cost transfers for agriculture
  - Odoo Model: `class AgriCostWIPTransfer(models.AbstractModel)`
  - _name: `farm.agri.cost.wip.transfer`
  - _description: "Work-in-Progress Cost Transfer for Agriculture"
  - _inherit: `models.AbstractModel`
  - Relationships:
    - Inherits: `models.AbstractModel`

- **farm_financial.AgriMortalityAmortization** (Abstract): Amortization of mortality costs
  - Odoo Model: `class AgriMortalityAmortization(models.AbstractModel)`
  - _name: `farm.agri.mortality.amortization`
  - _description: "Mortality Cost Amortization for Agriculture"
  - _inherit: `models.AbstractModel`
  - Relationships:
    - Inherits: `models.AbstractModel`

- **farm_financial.ProjectTask**: Financial aspects of project tasks
  - Odoo Model: `class ProjectTask(models.Model)`
  - _name: `project.task`
  - _description: "Financial Project Task Aspects"
  - _inherit: `project.task`
  - Relationships:
    - Extends: `project.task` (Odoo's native project task model)

## Waste Management Models

Waste management models handle waste processing and manure management.

- **farm_waste_mgmt.FarmManureBatch**: Management of manure batches
- **farm_waste_mgmt.FarmManureLedger**: Ledger of manure transactions
- **farm_waste_mgmt.StorageEnvironment**: Environment monitoring for storage
- **farm_waste_mgmt.ProcessingWaste**: Management of processing waste

## Support Models

### Training and Education
- **farm_training.FarmCertificateType**: Types of farm certificates
  - Odoo Model: `class FarmCertificateType(models.Model)`
  - _name: `farm.certificate.type`
  - _description: "Agricultural Certificate Type"
  - Fields:
    - `name` (Char): Certificate Name (required, translatable)
    - `code` (Char): Code (required)
    - `required_for_intervention_types` (Selection): Mandatory for Task Type (crop protection, aerial spraying, medical, harvesting)
  - Relationships:
    - Used by: `farm.certificate.certificate_type_id` → `farm.certificate.type`

- **farm_training.FarmCertificate**: Management of farm certificates
  - Odoo Model: `class FarmCertificate(models.Model)`
  - _name: `farm.certificate`
  - _description: "Farmer Certificate"
  - _inherit: `mail.thread`, `mail.activity.mixin`
  - Fields:
    - `name` (Char): Certificate No. (required)
    - `employee_id` (Many2one): Employee (hr.employee, required)
    - `certificate_type_id` (Many2one): Type (farm.certificate.type, required)
    - `issue_date` (Date): Issue Date
    - `expiry_date` (Date): Expiry Date
    - `is_valid` (Boolean): Is Valid (computed, stored)
    - `attachment_ids` (Many2many): Certificate Photos (ir.attachment)
  - Methods:
    - `_compute_is_valid()`: Computes whether the certificate is valid based on expiry date
  - Relationships:
    - Many2one: `employee_id` → `hr.employee`
    - Many2one: `certificate_type_id` → `farm.certificate.type`
    - Many2many: `attachment_ids` → `ir.attachment`

- **farm_training.FarmTrainingSession**: Training session management
  - Odoo Model: `class FarmTrainingSession(models.Model)`
  - _name: `farm.training.session`
  - _description: "Farmer Training Session"
  - _inherit: `mail.thread`, `mail.activity.mixin`
  - Fields:
    - `name` (Char): Topic (required)
    - `date` (Date): Date (default: today)
    - `hours` (Float): Duration (Hours)
    - `trainer_id` (Many2one): Trainer/Expert (res.partner)
    - `trainee_ids` (Many2many): Trainees (hr.employee)
    - `content` (Html): Training Content
    - `state` (Selection): State (draft, done)
  - Methods:
    - `action_complete()`: Marks the session as completed
    - `_cron_check_certificate_expiry()`: Automatic scan for expiring certificates
    - `get_qualified_worker_domain(intervention_type)`: Returns domain for qualified workers
  - Relationships:
    - Many2one: `trainer_id` → `res.partner`
    - Many2many: `trainee_ids` → `hr.employee`

- **farm_training.HrEmployee**: Training-enhanced employee records
  - Odoo Model: `class HrEmployee(models.Model)`
  - _name: `hr.employee`
  - _inherit: `hr.employee`
  - Fields:
    - `certificate_ids` (One2many): Certificates (farm.certificate)
    - `training_session_ids` (Many2many): Training History (farm.training.session)
    - `total_training_hours` (Float): Total Training Hours (computed)
  - Methods:
    - `_compute_training_hours()`: Computes total training hours from completed sessions
  - Relationships:
    - One2many: `certificate_ids` → `farm.certificate.employee_id`
    - Many2many: `training_session_ids` → `farm.training.session`
    - Inherits: `hr.employee` (Odoo's employee model)

- **farm_training.AgriIntervention**: Training-enhanced interventions
  - Odoo Model: `class AgriIntervention(models.Model)`
  - _name: `mrp.production`
  - _inherit: `mrp.production`
  - Methods:
    - `_onchange_intervention_type_filter_workers()`: Filters workers by certificate requirements
    - `action_confirm()`: Certification compliance check logic
  - Relationships:
    - Inherits: `mrp.production` (Odoo's manufacturing order model) with certification checks

- **farm_training.FarmTrainingSkill**: Skills management for training
  - Odoo Model: `class FarmTrainingSkill(models.Model)`
  - _name: `farm.training.skill`
  - _description: "Farm Training Skill"
  - Fields:
    - `name` (Char): Skill Name (required)
    - `description` (Text): Description
  - Relationships:
    - Used by: `farm.training.certification.required_skills_ids` → `farm.training.skill`

- **farm_training.FarmTrainingCertification**: Training certification management
  - Odoo Model: `class FarmTrainingCertification(models.Model)`
  - _name: `farm.training.certification`
  - _description: "Farm Training Certification"
  - Fields:
    - `name` (Char): Certification Name (required)
    - `description` (Text): Description
    - `validity_period` (Integer): Validity Period in Years
    - `required_skills_ids` (Many2many): Required Skills (farm.training.skill)
  - Relationships:
    - Many2many: `required_skills_ids` → `farm.training.skill`

- **farm_training.FarmTrainingTrainingRecord**: Training record management
  - Odoo Model: `class FarmTrainingTrainingRecord(models.Model)`
  - _name: `farm.training.training_record`
  - _description: "Farm Training Record"
  - _rec_name: "display_name"
  - Fields:
    - `employee_id` (Many2one): Employee (hr.employee, required)
    - `certification_id` (Many2one): Certification (farm.training.certification, required)
    - `training_date` (Date): Training Date (default: today)
    - `expiration_date` (Date): Expiration Date (computed, stored)
    - `status` (Selection): Status (valid, expired, upcoming_expire, pending, revoked)
    - `trainer_id` (Many2one): Trainer/Issued By (res.partner)
    - `notes` (Text): Notes
    - `display_name` (Char): Display Name (computed, stored)
  - Methods:
    - `_compute_display_name()`: Computes display name
    - `_compute_expiration_date()`: Computes expiration date from validity period
    - `_compute_status()`: Computes status based on expiration date
    - `_check_dates()`: Validates that training date is not after expiration date
  - Relationships:
    - Many2one: `employee_id` → `hr.employee`
    - Many2one: `certification_id` → `farm.training.certification`
    - Many2one: `trainer_id` → `res.partner`

### Financial Support
- **farm_finance_loan.FarmLoan**: Management of farm loans
  - Odoo Model: `class FarmLoan(models.Model)`
  - _name: `farm.loan`
  - _description: "Agricultural Loan"
  - _inherit: `mail.thread`, `mail.activity.mixin`
  - Fields:
    - `name` (Char): Loan Reference (default: "New")
    - `partner_id` (Many2one): Lender (Bank/Co-op) (res.partner, required)
    - `loan_type` (Selection): Loan Type (operational, equipment, biological)
    - `amount_principal` (Monetary): Principal Amount (currency_field: currency_id)
    - `amount_interest` (Monetary): Projected Interest (currency_field: currency_id)
    - `currency_id` (Many2one): Currency (res.currency)
    - `date_start` (Date): Start Date
    - `date_maturity` (Date): Maturity Date
    - `collateral_lot_ids` (Many2many): Collateral Assets (stock.lot)
    - `collateral_value` (Monetary): Collateral Valuation (computed)
    - `state` (Selection): State (draft, submitted, active, paid, defaulted)
  - Methods:
    - `_compute_collateral_value()`: Computes collateral valuation
    - `create()`: Creates loan with sequence code
  - Relationships:
    - Many2one: `partner_id` → `res.partner`
    - Many2many: `collateral_lot_ids` → `stock.lot`

- **farm_finance_gov.FarmRuralRevitalizationProject**: Management of rural revitalization projects
  - Odoo Model: `class FarmRuralRevitalizationProject(models.Model)`
  - _name: `farm.rural.revitalization.project`
  - _description: "Rural Revitalization Project"
  - _inherit: `mail.thread`, `mail.activity.mixin`
  - Fields:
    - `name` (Char): Project Name (required)
    - `code` (Char): Project Code (required)
    - `fund_source` (Char): Fund Source
    - `budget_amount` (Monetary): Budget Amount (currency_field: currency_id)
    - `currency_id` (Many2one): Currency (res.currency)
    - `date_start` (Date): Start Date
    - `date_end` (Date): End Date
    - `state` (Selection): State (draft, approved, in_progress, completed, cancelled)
    - `account_move_ids` (One2many): Related Account Moves (account.move)
    - `total_expenditure` (Monetary): Total Expenditure (computed)
  - Methods:
    - `_compute_total_expenditure()`: Computes total expenditure from related moves
  - Relationships:
    - One2many: `account_move_ids` → `account.move.rural_project_id`

- **farm_finance_gov.AccountMove**: Government finance-enhanced accounting entries
  - Odoo Model: `class AccountMove(models.Model)`
  - _name: `account.move`
  - _inherit: `account.move`
  - Fields:
    - `rural_project_id` (Many2one): Rural Revitalization Project (farm.rural.revitalization.project)
  - Methods:
    - `_check_rural_project_funds()`: Validates project fund compliance
  - Relationships:
    - Many2one: `rural_project_id` → `farm.rural.revitalization.project`
    - Inherits: `account.move` (Odoo's accounting entry model)

### Crisis and Risk Management
- **farm_crisis.FarmEmergencyProtocol**: Emergency protocols for crisis management
  - Odoo Model: `class FarmEmergencyProtocol(models.Model)`
  - _name: `farm.emergency.protocol`
  - _description: "Emergency Response Protocol (SOP)"
  - Fields:
    - `name` (Char): Protocol Name (required)
    - `crisis_type` (Selection): Crisis Type (disease, pest, contamination, disaster, security)
    - `steps` (Html): Action Steps (SOP)
    - `required_asset_lockdown` (Boolean): Requires Asset Lockdown
    - `notify_authorities` (Boolean): Notify Authorities
  - Relationships:
    - Used by: `farm.crisis.incident.protocol_id` → `farm.emergency.protocol`

- **farm_crisis.FarmCrisisIncident**: Management of crisis incidents
  - Odoo Model: `class FarmCrisisIncident(models.Model)`
  - _name: `farm.crisis.incident`
  - _description: "Crisis Incident Record"
  - _inherit: `mail.thread`, `mail.activity.mixin`
  - Fields:
    - `name` (Char): Incident Ref (default: "New")
    - `protocol_id` (Many2one): Active Protocol (farm.emergency.protocol, required)
    - `date_start` (Datetime): Detected At (default: now)
    - `date_end` (Datetime): Resolved At
    - `affected_location_ids` (Many2many): Affected Zones (stock.location)
    - `affected_lot_ids` (Many2many): Affected Assets/Batches (stock.lot)
    - `state` (Selection): State (draft, active, contained, resolved)
  - Methods:
    - `create()`: Creates incident with sequence code
    - `action_activate_crisis()`: Activates crisis mode and locks assets
    - `action_resolve()`: Resolves the crisis incident
  - Relationships:
    - Many2one: `protocol_id` → `farm.emergency.protocol`
    - Many2many: `affected_location_ids` → `stock.location`
    - Many2many: `affected_lot_ids` → `stock.lot`

- **farm_crisis.StockLot**: Crisis-enhanced stock lot management
  - Odoo Model: `class StockLot(models.Model)`
  - _name: `stock.lot`
  - _inherit: `stock.lot`
  - Fields:
    - `is_crisis_locked` (Boolean): Locked by Crisis (computed, searchable)
  - Methods:
    - `_compute_crisis_lock()`: Computes if the lot is locked by active crisis
    - `_search_crisis_locked()`: Search method for locked status
  - Relationships:
    - Inherits: `stock.lot` (Odoo's stock lot model) with crisis lock functionality

- **farm_crisis.SaleOrder**: Crisis-enhanced sale orders
  - Odoo Model: `class SaleOrder(models.Model)`
  - _name: `sale.order`
  - _inherit: `sale.order`
  - Methods:
    - `action_confirm()`: Validates sale orders against crisis-locked lots
  - Relationships:
    - Inherits: `sale.order` (Odoo's sale order model) with crisis validation

- **farm_disaster_risk.FarmDisasterIncident**: Management of disaster incidents
  - Odoo Model: `class FarmDisasterIncident(models.Model)`
  - _name: `farm.disaster.incident`
  - _description: "Meteorological Disaster Incident"
  - _inherit: `mail.thread`, `mail.activity.mixin`
  - Fields:
    - `name` (Char): Incident Ref (default: "New")
    - `disaster_type` (Selection): Disaster Type (hail, frost, flood, drought, gale, high_temp, other)
    - `date_start` (Date): Start Date (default: today)
    - `date_end` (Date): End Date
    - `affected_location_ids` (Many2many): Affected Land Parcels (stock.location)
    - `intensity` (Selection): Intensity (minor, moderate, severe)
    - `description` (Text): Description of Damage
    - `crisis_incident_id` (Many2one): Linked Crisis Incident (farm.crisis.incident)
    - `loss_assessment_ids` (One2many): Loss Assessments (farm.loss.assessment)
    - `total_estimated_loss` (Monetary): Total Estimated Loss (computed)
    - `currency_id` (Many2one): Currency (res.currency)
  - Methods:
    - `_compute_total_estimated_loss()`: Computes total estimated loss
    - `create()`: Creates incident with sequence code
    - `action_create_crisis_incident()`: Creates linked crisis incident
  - Relationships:
    - Many2many: `affected_location_ids` → `stock.location`
    - Many2one: `crisis_incident_id` → `farm.crisis.incident`
    - One2many: `loss_assessment_ids` → `farm.loss.assessment`

- **farm_disaster_risk.FarmLossAssessment**: Assessment of losses from disasters
  - Odoo Model: `class FarmLossAssessment(models.Model)`
  - _name: `farm.loss.assessment`
  - _description: "Disaster Loss Assessment"
  - _inherit: `mail.thread`, `mail.activity.mixin`
  - Fields:
    - `name` (Char): Assessment Ref (default: "New")
    - `disaster_incident_id` (Many2one): Disaster Incident (farm.disaster.incident, required)
    - `assessment_date` (Date): Assessment Date (default: today)
    - `assessor_id` (Many2one): Assessor (res.partner)
    - `affected_parcel_id` (Many2one): Affected Land Parcel (stock.location, required)
    - `crop_id` (Many2one): Affected Crop (product.product)
    - `estimated_loss_amount` (Monetary): Estimated Loss Amount (currency_field: currency_id)
    - `currency_id` (Many2one): Currency (res.currency)
    - `loss_description` (Text): Detailed Loss Description
    - `insurance_claim_id` (Many2one): Linked Insurance Claim (account.move)
    - `state` (Selection): State (draft, submitted, approved, rejected)
  - Methods:
    - `create()`: Creates assessment with sequence code
  - Relationships:
    - Many2one: `disaster_incident_id` → `farm.disaster.incident`
    - Many2one: `assessor_id` → `res.partner`
    - Many2one: `affected_parcel_id` → `stock.location`
    - Many2one: `crop_id` → `product.product`
    - Many2one: `insurance_claim_id` → `account.move`

### Registration and Knowledge
- **farm_entity_reg.ResCompany**: Company registration for farming entities
  - Odoo Model: `class ResCompany(models.Model)`
  - _name: `res.company`
  - _inherit: `res.company`
  - Fields:
    - `unified_social_credit_code` (Char): Unified Social Credit Code
    - `registration_no` (Char): Registration No.
    - `entity_type` (Selection): Entity Type (family_farm, cooperative, enterprise)
    - `license_attachment_ids` (Many2many): Electronic Licenses (ir.attachment)
    - `license_expiry_date` (Date): License Expiry Date
    - `is_license_expired` (Boolean): License Expired (computed)
  - Methods:
    - `_compute_license_status()`: Computes license expiry status
  - Relationships:
    - Many2many: `license_attachment_ids` → `ir.attachment`
    - Inherits: `res.company` (Odoo's company model)

- **farm_entity_reg.FarmCooperativeMember**: Cooperative member registration
  - Odoo Model: `class FarmCooperativeMember(models.Model)`
  - _name: `farm.cooperative.member`
  - _description: "Cooperative Member"
  - Fields:
    - `company_id` (Many2one): Cooperative (res.company, required)
    - `partner_id` (Many2one): Member Name (res.partner, required)
    - `membership_date` (Date): Membership Date (default: today)
    - `share_capital` (Float): Share Capital
    - `is_chairman` (Boolean): Is Chairman
  - Relationships:
    - Many2one: `company_id` → `res.company`
    - Many2one: `partner_id` → `res.partner`

- **farm_input_reg.ProductTemplate**: Input registration-enhanced product templates
  - Odoo Model: `class ProductTemplate(models.Model)`
  - _name: `product.template`
  - _inherit: `product.template`
  - Relationships:
    - Inherits: `product.template` (Odoo's product template model) with input registration enhancements

- **farm_input_reg.MrpProduction**: Input registration-enhanced production orders
  - Odoo Model: `class MrpProduction(models.Model)`
  - _name: `mrp.production`
  - _inherit: `mrp.production`
  - Relationships:
    - Inherits: `mrp.production` (Odoo's manufacturing order model) with input registration enhancements

- **farm_knowledge.FarmPestDisease**: Management of pest and disease information
  - Odoo Model: `class FarmPestDisease(models.Model)`
  - _name: `farm.pest.disease`
  - _description: "Pest & Disease Database"
  - _inherit: `mail.thread`, `mail.activity.mixin`
  - Fields:
    - `name` (Char): Name (required, translatable)
    - `scientific_name` (Char): Scientific Name
    - `category` (Selection): Category (pest, disease, weed)
    - `symptoms` (Html): Symptoms Description (translatable)
    - `cause` (Text): Cause/Etiology (translatable)
    - `prevention` (Html): Prevention Measures (translatable)
    - `photo` (Binary): Reference Photo
    - `image_name` (Char): Image Name
    - `recommended_intervention_id` (Many2one): Recommended Treatment (agri.intervention.template)
    - `description` (Text): Detailed Description (translatable)
    - `active` (Boolean): Active status
  - Methods:
    - `action_view_treatment()`: Opens treatment view for the pest/disease
  - Relationships:
    - Many2one: `recommended_intervention_id` → `agri.intervention.template`

- **farm_knowledge.FAQEntry**: FAQ entries for agricultural knowledge
  - Odoo Model: `class FAQEntry(models.Model)`
  - _name: `faq.entry`
  - _description: "Frequently Asked Questions"
  - _order: "sequence, id"
  - Fields:
    - `sequence` (Integer): Sequence (default: 10)
    - `question` (Char): Question (required, translatable)
    - `answer` (Html): Answer (required, translatable)
    - `category` (Selection): Category (general, planting, livestock, equipment, quality, safety)
    - `active` (Boolean): Active status
    - `tags` (Char): Tags
    - `target_model` (Char): Target Model
    - `knowledge_id` (Many2one): Detailed Article (agricultural.knowledge)
  - Relationships:
    - Many2one: `knowledge_id` → `agricultural.knowledge`

- **farm_knowledge.AgriculturalKnowledge**: General agricultural knowledge management
  - Odoo Model: `class AgriculturalKnowledge(models.Model)`
  - _name: `agricultural.knowledge`
  - _description: "Agricultural Knowledge Base"
  - _inherit: `mail.thread`, `mail.activity.mixin`
  - Fields:
    - `name` (Char): Title (required, translatable)
    - `content` (Html): Content (translatable)
    - `category` (Selection): Category (crop_varieties, cultivation, pest_disease, fertilization, irrigation, harvesting, processing, marketing, regulations, best_practices)
    - `knowledge_type` (Selection): Knowledge Type (article, case_study, standard)
    - `tags` (Char): Tags
    - `active` (Boolean): Active status
    - `author_id` (Many2one): Author (res.users)
    - `difficulty_level` (Selection): Difficulty Level (beginner, intermediate, expert)
    - `industry_specific` (Selection): Industry Specific (general, planting, livestock, aquaculture, winemaking, bakery, dairy, processing)
    - `seasonality` (Selection): Seasonality (spring, summer, autumn, winter, year_round)
    - `video_url` (Char): Video URL
    - `attachment_ids` (Many2many): Attachments (ir.attachment)
    - `view_count` (Integer): View Count (default: 0, readonly)
    - `helpful_count` (Integer): Helpful Count (default: 0, readonly)
    - `pest_disease_id` (Many2one): Related Pest/Disease (farm.pest.disease)
  - Methods:
    - `smart_search(keywords)`: Intelligent search for knowledge articles
    - `action_mark_helpful()`: Marks article as helpful
  - Relationships:
    - Many2one: `author_id` → `res.users`
    - Many2one: `pest_disease_id` → `farm.pest.disease`
    - Many2many: `attachment_ids` → `ir.attachment`

### Label and UX
- **farm_label.ProductTemplate**: Label-enhanced product templates
  - Odoo Model: `class ProductTemplate(models.Model)`
  - _name: `product.template`
  - _inherit: `product.template`
  - Fields:
    - `ingredient_list` (Text): Ingredients (translatable)
    - `storage_condition` (Char): Storage Condition (translatable, default: "Store in cool and dry place")
    - `shelf_life_days` (Integer): Shelf Life (Days)
    - `food_standard_code` (Char): Executive Standard Code (default: "GB/T ...")
    - `production_license_no` (Char): Production License No (SC)
  - Relationships:
    - Inherits: `product.template` (Odoo's product template model) with label compliance fields

- **farm_label.StockLot**: Label-enhanced stock lot management
  - Odoo Model: `class StockLot(models.Model)`
  - _name: `stock.lot`
  - _inherit: `stock.lot`
  - Fields:
    - `producer_id` (Many2one): Producer (res.partner, default: company partner)
    - `net_content` (Char): Net Content (e.g. 500g, 1L)
  - Methods:
    - `get_qr_quoted_traceability_url()`: Gets URL-encoded traceability URL
  - Relationships:
    - Many2one: `producer_id` → `res.partner`
    - Inherits: `stock.lot` (Odoo's stock lot model) with label fields

- **farm_label.StockLocation**: Label-enhanced stock location management
  - Odoo Model: `class StockLocation(models.Model)`
  - _name: `stock.location`
  - _inherit: `stock.location`
  - Methods:
    - `get_qr_quoted_name()`: Gets URL-encoded location name
  - Relationships:
    - Inherits: `stock.location` (Odoo's stock location model) with label utilities

- **farm_label.ResCompany**: Label-enhanced company records
  - Odoo Model: `class ResCompany(models.Model)`
  - _name: `res.company`
  - _inherit: `res.company`
  - Relationships:
    - Inherits: `res.company` (Odoo's company model) with label enhancements

- **farm_label.ResConfigSettings**: Label configuration settings
  - Odoo Model: `class ResConfigSettings(models.TransientModel)`
  - _name: `res.config.settings`
  - _inherit: `res.config.settings`
  - Relationships:
    - Inherits: `res.config.settings` (Odoo's configuration settings model) with label settings

- **farm_ux.VoiceRecognitionAlias**: Voice recognition aliases for UX
  - Odoo Model: `class VoiceRecognitionAlias(models.Model)`
  - _name: `farm.voice.recognition.alias`
  - _description: "Voice Recognition Alias for Agricultural Terms"
  - _order: "alias"
  - Fields:
    - `alias` (Char): Spoken Alias / Phonetic (required)
    - `target_term` (Char): Standard Term (required)
  - Methods:
    - `normalize_voice_text(text)`: Normalizes voice-to-text output using registered aliases
  - Relationships:
    - Provides voice recognition functionality for agricultural terms

- **farm_ux.FormLayoutTemplate**: Form layout templates for UX
  - Odoo Model: `class FormLayoutTemplate(models.Model)`
  - _name: `form.layout.template`
  - _description: "Form Layout Template for Industry-Specific Views"
  - Fields:
    - `name` (Char): Template Name (required, translatable)
    - `model_name` (Char): Model Name (required)
    - `industry_type` (Selection): Industry Type (planting, livestock, aquaculture, winemaking, bakery, dairy, processing, general)
    - `layout_definition` (Text): Layout Definition (JSON)
    - `is_active` (Boolean): Is Active (default: True)
    - `description` (Text): Description (translatable)
    - `user_role` (Selection): User Role (farmer, technician, worker, manager)
    - `version` (Char): Version (default: "1.0")
    - `created_by` (Many2one): Created By (res.users)
    - `created_date` (Datetime): Created Date (default: now)
  - Methods:
    - `apply_layout_to_view(view_id)`: Applies layout template to view
  - Relationships:
    - Many2one: `created_by` → `res.users`

- **farm_ux.ContextualHelp**: Contextual help for UX
  - Odoo Model: `class ContextualHelp(models.Model)`
  - _name: `contextual.help`
  - _description: "Smart Contextual Help for Agricultural Operations"
  - Fields:
    - `name` (Char): Help Topic (required, translatable)
    - `model_name` (Char): Model Name (required)
    - `field_name` (Char): Field Name
    - `view_type` (Selection): View Type (form, list, kanban, calendar, graph, pivot)
    - `help_content` (Html): Help Content (translatable)
    - `help_video_url` (Char): Video Tutorial URL
    - `help_image` (Binary): Help Image
    - `image_name` (Char): Image Name
    - `is_active` (Boolean): Is Active (default: True)
    - `priority` (Integer): Priority (default: 10)
    - `target_roles` (Many2many): Target Roles (res.groups)
    - `industry_context` (Selection): Industry Context (general, planting, livestock, etc.)
    - `difficulty_level` (Selection): Difficulty Level (beginner, intermediate, advanced)
  - Methods:
    - `get_contextual_help(model_name, field_name, view_type)`: Gets contextual help for specific context
  - Relationships:
    - Many2many: `target_roles` → `res.groups`

- **farm_ux.VisualStatusIndicator**: Visual status indicators for UX
  - Odoo Model: `class VisualStatusIndicator(models.Model)`
  - _name: `visual.status.indicator`
  - _description: "Visual Status Indicator Configuration"
  - Fields:
    - `name` (Char): Indicator Name (required, translate=True)
    - `model_name` (Char): Model Name (required, help="The model this indicator applies to (e.g. mrp.production)")
    - `field_name` (Char): Field Name (required, help="The field to monitor for status changes")
    - `evaluation_logic` (Text): Evaluation Logic (help="Python lambda function to evaluate status (e.g. lambda record: record.state == "done" and "green" or "red")")
    - `status_type` (Selection): Status Type (task, quality, safety, compliance, weather, equipment) (required)
    - `status_value` (Char): Status Value (required, help="Value to match (e.g. "pending", "in_progress", "done")")
    - `color_code` (Char): Color Code (default="#000000", help="CSS color code for the indicator")
    - `icon` (Char): Icon (help="Font Awesome icon (e.g. fa-check, fa-warning)")
    - `badge_style` (Selection): Badge Style (primary, secondary, success, danger, warning, info) (default="secondary")
    - `notification_sound` (Char): Notification Sound (help="Sound file for audio notifications")
    - `vibration_pattern` (Char): Vibration Pattern (help="Pattern for mobile vibration feedback")
    - `animation_effect` (Char): Animation Effect (help="CSS animation for status transitions")
    - `is_active` (Boolean): Is Active (default=True)
    - `display_on_mobile` (Boolean): Display on Mobile (default=True)
    - `description` (Text): Description (translate=True)
  - Methods:
    - `evaluate_status(self, record)`: Dynamically evaluates record status
  - Relationships: Inherits mail.thread, mail.activity.mixin

- **farm_ux.FarmSocialNetwork**: Social network functionality for farming
  - Odoo Model: `class FarmSocialNetwork(models.Model)`
  - _name: `farm.social.network`
  - _description: "Farm Social Network & Collaboration Platform"
  - Fields:
    - `name` (Char): Network Name (required, translate=True)
    - `network_type` (Selection): Network Type (coop_members, regional_farmers, specialty_crops, knowledge_sharing, resource_sharing) (required)
    - `member_ids` (Many2many): Members (res.partner)
    - `admin_ids` (Many2many): Administrators (res.users)
    - `description` (Text): Description (translate=True)
    - `is_active` (Boolean): Is Active (default=True)
    - `created_by` (Many2one): Created By (res.users, default=lambda self: self.env.user)
    - `created_date` (Datetime): Created Date (default=fields.Datetime.now)
    - `privacy_level` (Selection): Privacy Level (public, private, invite_only) (default="private")
    - `message_board` (Text): Message Board (help="Public message board content")
    - `shared_resources` (Text): Shared Resources (help="Shared resources and experiences")
  - Relationships: Inherits mail.thread, mail.activity.mixin

- **farm_ux.AccessibilitySettings**: Accessibility settings for UX
  - Odoo Model: `class AccessibilitySettings(models.Model)`
  - _name: `accessibility.settings`
  - _description: "Accessibility & Inclusive Design Settings"
  - Fields:
    - `name` (Char): Setting Name (required, translate=True)
    - `user_id` (Many2one): User (res.users, required, default=lambda self: self.env.user)
    - `screen_reader_enabled` (Boolean): Screen Reader Enabled (help="Enable screen reader compatibility")
    - `keyboard_navigation` (Boolean): Keyboard Navigation (help="Enable keyboard-only navigation")
    - `font_scaling` (Float): Font Scaling Factor (default=1.0, help="Scale factor for all fonts (1.0 = normal)")
    - `high_contrast_mode` (Boolean): High Contrast Mode (help="Enable high contrast color scheme")
    - `large_touch_targets` (Boolean): Large Touch Targets (help="Enable larger touch targets for easier interaction")
    - `reduced_motion` (Boolean): Reduced Motion (help="Reduce animations and motion effects")
    - `color_blind_mode` (Boolean): Color Blind Mode (help="Adjust colors for color blindness")
    - `voice_navigation` (Boolean): Voice Navigation (help="Enable voice-based navigation")
    - `font_family_preference` (Char): Font Family Preference (help="Preferred font family for accessibility")
    - `alternative_input_method` (Selection): Alternative Input Method (none, voice, switch, eye_tracking) (default="none")
    - `voice_control_enabled` (Boolean): Voice Control Enabled (help="Enable voice commands")
    - `custom_color_scheme` (Char): Custom Color Scheme (help="Custom CSS for color adjustments")
    - `is_active` (Boolean): Is Active (default=True)
    - `last_updated` (Datetime): Last Updated (default=fields.Datetime.now)
  - Methods:
    - `_check_font_scaling_range(self)`: Checks font scaling range constraint (0.5-3.0)
  - Relationships: Inherits mail.thread, mail.activity.mixin

- **farm_ux.WorkspaceCustomization**: Workspace customization for UX
  - Odoo Model: `class WorkspaceCustomization(models.Model)`
  - _name: `workspace.customization`
  - _description: "Personalized Workspace Customization"
  - Fields:
    - `name` (Char): Customization Name (required, translate=True)
    - `user_id` (Many2one): User (res.users, required, default=lambda self: self.env.user)
    - `dashboard_widgets` (Text): Dashboard Widgets (help="JSON configuration of dashboard widgets")
    - `theme_preference` (Selection): Theme Preference (light, dark, eye_care, high_contrast) (default="light")
    - `quick_actions` (Text): Quick Actions (help="JSON configuration of quick action bar")
    - `language_preference` (Char): Language Preference (default="zh_CN")
    - `timezone_preference` (Char): Timezone Preference (default="Asia/Shanghai")
    - `font_size` (Selection): Font Size (small, normal, large, extra_large) (default="normal")
    - `layout_preference` (Text): Layout Preferences (help="JSON configuration of UI layouts")
    - `is_active` (Boolean): Is Active (default=True)
    - `last_updated` (Datetime): Last Updated (default=fields.Datetime.now)
  - Methods:
    - `save_customization(self)`: Saves user customization settings
    - `get_user_customization(self, user_id=None)`: Gets user customization settings
  - Relationships: Inherits mail.thread, mail.activity.mixin

- **farm_ux.TermMapping**: Term mapping for UX
  - Odoo Model: `class TermMapping(models.Model)`
  - _name: `term.mapping`
  - _description: "Term Mapping for Agricultural Terminology"
  - _order: `source_term asc`
  - Fields:
    - `name` (Char): Mapping Name (required, translate=True)
    - `source_term` (Char): Source Term (Industrial) (required, help="Original industrial term (e.g. Manufacturing Order)")
    - `target_term` (Char): Target Term (Agricultural) (required, help="Agricultural equivalent term (e.g. Intervention)")
    - `language_code` (Char): Language Code (default="zh_CN", help="Language code for localization")
    - `industry_context` (Selection): Industry Context (general, planting, livestock, aquaculture, winemaking, bakery, dairy, processing) (default="general")
    - `region_specific` (Boolean): Region Specific (help="Is this term specific to certain regions?")
    - `region_code` (Char): Region Code (help="Specific region code if region-specific")
    - `is_active` (Boolean): Is Active (default=True)
    - `description` (Text): Description (translate=True)
    - `example_usage` (Text): Example Usage (translate=True)
  - Methods:
    - `_check_unique_mapping(self)`: Ensures term mapping uniqueness constraint
    - `apply_term_mapping_to_text(self, text)`: Applies term mapping to text
    - `apply_term_mapping(self, text)`: Compatibility method for term mapping
  - Relationships: Inherits mail.thread, mail.activity.mixin

- **farm_ux.MultiSensoryInteraction**: Multi-sensory interaction for UX
  - Odoo Model: `class MultiSensoryInteraction(models.Model)`
  - _name: `multi.sensory.interaction`
  - _description: "Multi-Sensory Interaction Configuration"
  - Fields:
    - `name` (Char): Feature Name (required, translate=True)
    - `interaction_type` (Selection): Interaction Type (voice_input, gesture_control, audio_feedback, haptic_feedback, visual_enhancement, large_touch_target) (required)
    - `model_name` (Char): Model Name (help="Model this feature applies to")
    - `field_name` (Char): Field Name (help="Field this feature applies to")
    - `is_enabled` (Boolean): Is Enabled (default=True)
    - `voice_commands` (Text): Voice Commands (help="JSON configuration of voice commands")
    - `gesture_mappings` (Text): Gesture Mappings (help="JSON configuration of gesture mappings")
    - `audio_notification` (Boolean): Audio Notification (help="Enable audio feedback")
    - `haptic_feedback` (Boolean): Haptic Feedback (help="Enable vibration feedback")
    - `visual_enhancement` (Boolean): Visual Enhancement (help="Enable visual enhancements")
    - `large_font_support` (Boolean): Large Font Support (help="Support large font mode")
    - `high_contrast_mode` (Boolean): High Contrast Mode (help="Support high contrast mode")
    - `screen_reader_compatible` (Boolean): Screen Reader Compatible (help="Compatible with screen readers")
    - `keyboard_shortcuts` (Text): Keyboard Shortcuts (help="JSON configuration of keyboard shortcuts")
    - `description` (Text): Description (translate=True)
  - Relationships: Inherits mail.thread, mail.activity.mixin

- **farm_ux.IrUiView**: Customized views for UX
  - Odoo Model: `class IrUiView(models.Model)`
  - _name: `ir.ui.view`
  - _inherit: `ir.ui.view`
  - Methods:
    - `get_view(self, view_id=None, view_type='form', **options)`: Unified view customization handling (term mapping + layout templates)
  - Relationships: Inherits ir.ui.view

- **farm_ux.IrHttp**: HTTP handling for UX
  - Odoo Model: `class IrHttp(models.AbstractModel)`
  - _name: `ir.http`
  - _inherit: `ir.http`
  - Methods:
    - `session_info(self)`: Injects accessibility features and UX customization into session_info
  - Relationships: Inherits ir.http

- **farm_ux.AccessibilityIntegration**: Accessibility integration for UX
  - Odoo Model: `class AccessibilityIntegration(models.AbstractModel)`
  - _name: `accessibility.integration`
  - _description: "Accessibility Integration RPC"
  - Methods:
    - `get_accessibility_features(self, user_id=None)`: Gets user accessibility features
    - `get_contextual_help_data(self, model_name, view_type='form', field_name=None)`: Gets contextual help data
  - Relationships: Abstract model for frontend RPC interfaces

- **farm_ux.MailThread**: Mail thread handling for UX
  - Odoo Model: `class MailThread(models.AbstractModel)`
  - _name: `mail.thread`
  - _inherit: `mail.thread`
  - Methods:
    - `message_post(self, **kwargs)`: Overridden message_post to support social networking
  - Relationships: Inherits mail.thread

- **farm_ux.FarmSocialNetworkIntegration**: Social network integration for farming
  - Odoo Model: `class FarmSocialNetworkIntegration(models.AbstractModel)`
  - _name: `farm.social.network.integration`
  - _description: "Farm Social Network Integration"
  - Methods:
    - `post_message_to_network(self, record, message)`: Implements specific posting logic
  - Relationships: Abstract model for social network integration

### Live Streaming and E-commerce
- **farm_live_streaming.LiveStreamingSession**: Management of live streaming sessions
  - Odoo Model: `class LiveStreamingSession(models.Model)`
  - _name: `live.streaming.session`
  - _description: "Live Streaming Session"
  - _inherit: `mail.thread`, `mail.activity.mixin`
  - Fields:
    - `name` (Char): Session Title (required)
    - `account_id` (Many2one): Douyin Account (douyin.account, required)
    - `start_time` (Datetime): Scheduled Start
    - `end_time` (Datetime): Actual End
    - `state` (Selection): State (planned, live, ended, archived) (default="planned", tracking=True)
    - `product_ids` (Many2many): Featured Products (product.product)
    - `view_count` (Integer): View Count (readonly=True)
    - `like_count` (Integer): Likes (readonly=True)
    - `comment_count` (Integer): Comments (readonly=True)
    - `total_sales` (Float): Sales Generated (readonly=True)
    - `archive_url` (Char): Replay Link
    - `video_binary` (Binary): Clip Archive
    - `dy_room_id` (Char): Douyin Room ID (help="Actual ID of the live room on Douyin")
  - Methods:
    - `action_start_live()`: Starts live session
    - `action_end_live()`: Ends live session and fetches final stats/replay
    - `action_refresh_stats()`: Refreshes live streaming statistics
    - `action_fetch_replay_link()`: Fetches and stores replay link
  - Relationships: Inherits mail.thread, mail.activity.mixin

- **farm_live_streaming.LiveOrder**: Management of live streaming orders
  - Odoo Model: `class LiveOrder(models.Model)`
  - _name: `live.order`
  - _description: "Live Stream Sales Order"
  - _inherit: `mail.thread`, `mail.activity.mixin`
  - Fields:
    - `name` (Char): Order Reference (required)
    - `dy_order_id` (Char): Douyin Order ID (required, index=True)
    - `account_id` (Many2one): Account (douyin.account, required)
    - `session_id` (Many2one): Live Session (live.streaming.session)
    - `raw_data` (Text): Raw Data JSON
    - `odoo_so_id` (Many2one): Odoo Sales Order (sale.order, readonly=True)
    - `buyer_nick` (Char): Buyer Name
    - `amount_total` (Float): Order Amount
    - `state` (Selection): State (draft, imported, failed, shipped) (default="draft", tracking=True)
  - Methods:
    - `action_view_odoo_so()`: Views associated Odoo sales order
    - `action_download_from_douyin(self, account_id)`: Downloads orders from Douyin
    - `action_import_to_odoo(self)`: Imports downloaded orders to Odoo
    - `_create_sale_order(self, dy_order, product)`: Creates sales order from Douyin order
    - `action_sync_shipping_to_douyin(self, carrier_name, tracking_ref)`: Syncs shipping status to Douyin
  - Relationships: Inherits mail.thread, mail.activity.mixin

- **farm_live_streaming.StockPicking**: Live streaming-enhanced stock picking
  - Odoo Model: `class StockPicking(models.Model)`
  - _name: `stock.picking`
  - _inherit: `stock.picking`
  - Methods:
    - `button_validate(self)`: Enhanced to sync shipping to Douyin on validation
  - Relationships: Inherits stock.picking

- **farm_live_streaming.DouyinAccount**: Douyin account management
  - Odoo Model: `class DouyinAccount(models.Model)`
  - _name: `douyin.account`
  - _description: "Douyin Enterprise Account"
  - _inherit: `mail.thread`, `mail.activity.mixin`
  - Fields:
    - `name` (Char): Account Nickname (required)
    - `client_key` (Char): Client Key (App ID) (required)
    - `client_secret` (Char): Client Secret (required, password=True)
    - `shop_id` (Char): Shop ID (抖音小店ID)
    - `access_token` (Char): Access Token (readonly=True)
    - `refresh_token` (Char): Refresh Token (readonly=True)
    - `token_expiry` (Datetime): Token Expiry (readonly=True)
    - `state` (Selection): State (draft, authorized, expired) (default="draft", tracking=True)
    - `health_status` (Selection): Health Status (healthy, warning, error) (computed, store=True)
    - `last_health_check` (Datetime): Last Check
    - `responsible_user_id` (Many2one): Responsible (res.users, default=lambda self: self.env.user)
  - Methods:
    - `_compute_health_status(self)`: Computes health status based on token expiry
    - `action_verify_connection(self)`: Verifies API connection
    - `_cron_monitor_accounts(self)`: Cron job to monitor account health
    - `_create_expiry_activity(self, note=False)`: Creates expiry activity notification
    - `action_authorize(self)`: Generates Douyin OAuth authorization link
    - `_exchange_code_for_token(self, code)`: Exchanges code for access token
    - `_refresh_access_token(self)`: Refreshes access token
    - `_process_token_response(self, response)`: Processes token response
    - `_execute_request(self, endpoint, params=None, method='POST')`: Executes HTTP request
    - `_do_douyin_request(self, endpoint, params=None, method='POST')`: Handles request orchestration
    - `action_confirm_shipping(self, dy_order_id, logistics_code, tracking_no)`: Confirms shipping on Douyin
    - `action_get_live_stats(self, room_id)`: Gets live streaming statistics
    - `action_get_live_replay(self, room_id)`: Gets live streaming replay
    - `action_sync_orders(self)`: Syncs orders from Douyin
  - Relationships: Inherits mail.thread, mail.activity.mixin

- **farm_live_streaming.DouyinQualification**: Douyin qualification management
  - Odoo Model: `class DouyinQualification(models.Model)`
  - _name: `douyin.qualification`
  - _description: "Douyin Onboarding Qualification"
  - _inherit: `mail.thread`, `mail.activity.mixin`
  - Fields:
    - `name` (Char): Application Title (required, default="New Douyin Application")
    - `company_id` (Many2one): Farm Company (res.company, default=lambda self: self.env.company)
    - `business_license` (Binary): Business License (required)
    - `uscc` (Char): Unified Social Credit Code (required)
    - `legal_person_name` (Char): Legal Representative (required)
    - `id_card_front` (Binary): ID Card Front
    - `id_card_back` (Binary): ID Card Back
    - `food_license` (Binary): Food Business License
    - `cert_expiry_date` (Date): License Expiry Date
    - `state` (Selection): State (draft, validating, passed, rejected) (default="draft", tracking=True)
  - Methods:
    - `_check_uscc_format(self)`: Validates USCC format (18 characters)
    - `action_perform_pre_audit(self)`: Performs system automation pre-audit logic
    - `action_go_to_douyin_register(self)`: Guides to Douyin enterprise account opening website
  - Relationships: Inherits mail.thread, mail.activity.mixin

- **farm_live_streaming.DouyinProduct**: Douyin product management
  - Odoo Model: `class DouyinProduct(models.Model)`
  - _name: `douyin.product`
  - _description: "Douyin Shop Product Sync"
  - Fields:
    - `account_id` (Many2one): Douyin Account (douyin.account, required)
    - `product_id` (Many2one): Odoo Product (product.product, required)
    - `douyin_item_id` (Char): Douyin Item ID (help="ID in Douyin Shop")
    - `sync_state` (Selection): Sync State (pending, synced, error) (default="pending", tracking=True)
    - `last_sync_time` (Datetime): Last Sync
  - Methods:
    - `action_sync_to_douyin(self)`: Syncs product information and traceability story to Douyin
    - `action_sync_stock_only(self)`: Syncs only stock quantity to Douyin
  - Relationships: Links Odoo products to Douyin shop items

- **farm_live_streaming.StockQuant**: Live streaming-enhanced stock quant management
  - Odoo Model: `class StockQuant(models.Model)`
  - _name: `stock.quant`
  - _inherit: `stock.quant`
  - Methods:
    - `create(self, vals_list)`: Creates quant and triggers Douyin stock sync
    - `write(self, vals)`: Updates quant and triggers Douyin stock sync if changes affect stock
    - `_trigger_douyin_stock_sync(self)`: Triggers Douyin stock sync for related products
  - Relationships: Inherits stock.quant

### Monitoring and Specialized Services
- **farm_green_monitor.StockLocation**: Green monitoring-enhanced stock locations
  - Odoo Model: `class StockLocation(models.Model)`
  - _name: `stock.location` (inherited)
  - _inherit: `stock.location`
  - Fields:
    - `fertilizer_reduction_target` (Float): Fertilizer Reduction Target (%) (default=0.0)
    - `pesticide_reduction_target` (Float): Pesticide Reduction Target (%) (default=0.0)
  - Relationships: Inherits stock.location

- **farm_green_monitor.ProjectTask**: Green monitoring-enhanced project tasks
  - Odoo Model: `class ProjectTask(models.Model)`
  - _name: `project.task` (inherited)
  - _inherit: `project.task`
  - Fields:
    - `total_fertilizer_used` (Float): Total Fertilizer Used (kg) (computed, store=True)
    - `total_pesticide_used` (Float): Total Pesticide Used (kg) (computed, store=True)
    - `fertilizer_per_mu` (Float): Fertilizer (kg/mu) (computed, store=True)
    - `pesticide_per_mu` (Float): Pesticide (kg/mu) (computed, store=True)
  - Methods:
    - `_compute_green_monitor_stats(self)`: Computes green monitoring statistics
  - Relationships: Inherits project.task

- **farm_green_monitor.FarmGreenMonitorReport** (Abstract): Reports for green monitoring
  - Odoo Model: `class FarmGreenMonitorReport(models.AbstractModel)`
  - _name: `report.farm_green_monitor.reduction_trend_report`
  - _description: "Fertilizer/Pesticide Reduction Trend Report"
  - Methods:
    - `_get_report_values(self, docids, data=None)`: Gets report values
    - `_get_reduction_data(self, campaign)`: Gets reduction data for report
  - Relationships: Abstract report model

- **farm_data_security.ResConfigSettings**: Data security configuration settings
  - Odoo Model: `class ResConfigSettings(models.TransientModel)`
  - _name: `res.config.settings`
  - _inherit: `res.config.settings`
  - Fields:
    - `data_storage_region` (Selection): Data Storage Region (china_mainland, overseas) (config_parameter="farm_data_security.data_storage_region")
    - `is_dengbao_level3_compliant` (Boolean): Dengbao Level 3 Compliant (config_parameter="farm_data_security.is_dengbao_level3_compliant")
  - Methods:
    - `action_check_data_localization(self)`: Checks data localization compliance
  - Relationships: Inherits res.config.settings

- **farm_data_security.FarmLocation**: Data security-enhanced farm location management
  - Odoo Model: `class FarmLocation(models.Model)`
  - _name: `stock.location` (inherited)
  - _inherit: `stock.location`
  - Methods:
    - `unlink(self)`: Audit logging for location deletion
  - Relationships: Inherits stock.location

- **farm_data_security.ResPartner**: Data security-enhanced partner records
  - Odoo Model: `class ResPartner(models.Model)`
  - _name: `res.partner` (inherited)
  - _inherit: `res.partner`
  - Methods:
    - `write(self, vals)`: Audit logging for partner modifications
  - Relationships: Inherits res.partner

- **farm_exchange.FarmDataExchanger**: Data exchange management
  - Odoo Model: `class FarmDataExchanger(models.Model)`
  - _name: `farm.data.exchanger`
  - _description: "Agricultural Data Exchanger"
  - _inherit: `mail.thread`, `mail.activity.mixin`
  - Fields:
    - `name` (Char): Exchange Reference (required)
    - `format_type` (Selection): Data Format (daplos, telepac, edi) (default="daplos", required)
    - `exchange_type` (Selection): Exchange Type (export, import) (default="export", required)
    - `date` (Datetime): Exchange Date (default=fields.Datetime.now)
    - `data_file` (Binary): Data File
    - `file_name` (Char): File Name
    - `state` (Selection): State (draft, done, error) (default="draft", tracking=True)
  - Methods:
    - `action_perform_exchange(self)`: Performs standardized data exchange
    - `_export_daplos_xml(self)`: Exports DAPLOS (ISO 11783-10) XML format
    - `_export_telepac_csv(self)`: Exports TELEPAC CSV format
  - Relationships: Inherits mail.thread, mail.activity.mixin

### Sales and Certification Compliance
- **farm_pos.PosOrder**: Point of sale order management
  - Odoo Model: `class PosOrder(models.Model)`
  - _name: `pos.order` (inherited)
  - _inherit: `pos.order`
  - Fields:
    - `picking_location_id` (Many2one): Picking Source Plot (stock.location, domain=[('is_land_parcel', '=', True)], help="The specific land parcel where these products were picked.")
  - Methods:
    - `_prepare_invoice_vals(self)`: Prepares invoice values with location information
  - Relationships: Inherits pos.order

- **farm_pos.PosOrderLine**: Line items for POS orders
  - Odoo Model: `class PosOrderLine(models.Model)`
  - _name: `pos.order.line` (inherited)
  - _inherit: `pos.order.line`
  - Fields:
    - `lot_id` (Many2one): Production Lot (stock.lot)
  - Relationships: Inherits pos.order.line

- **farm_sale_ch.ExportCountryStandard**: Export country standards management
  - Odoo Model: `class ExportCountryStandard(models.Model)`
  - _name: `export.country.standard`
  - _description: "Export Country Standard"
  - Fields:
    - `name` (Char): Country Name (required)
    - `code` (Char): Country Code (required, help="ISO国家代码")
    - `prohibited_products` (Many2many): Prohibited Products/Pesticides (product.template, help="该国家禁止使用的农药或其他产品清单")
    - `compliance_requirements` (Text): Compliance Requirements (help="其他合规要求")
    - `active` (Boolean): Active (default=True)
    - `import_date` (Datetime): Import Date (help="Date when this standard was imported")
    - `imported_by` (Many2one): Imported By (res.users, help="User who imported this standard")
    - `custom_rules` (Text): Custom Rules (help="Custom compliance rules for this country")
    - `last_updated` (Datetime): Last Updated (help="Last time this standard was updated")
    - `update_frequency` (Selection): Update Frequency (daily, weekly, monthly, quarterly, annually) (default="annually", help="How often this standard should be reviewed")
    - `contact_person` (Char): Contact Person (help="Contact person for this country's regulations")
    - `official_source` (Char): Official Source (help="Official source for this country's regulations")
    - `next_review_date` (Date): Next Review Date (help="When to next review this standard")
  - Methods:
    - `batch_import_standards(self, standards_data)`: Batch imports standards
    - `update_standard(self)`: Updates standard
    - `schedule_next_review(self)`: Schedules next review
  - Relationships: Base export country standard model that can be inherited

- **farm_sale_ch.StockLot**: Sale CH-enhanced stock lot management
  - Odoo Model: `class StockLot(models.Model)`
  - _name: `stock.lot` (inherited)
  - _inherit: `stock.lot`
  - Fields:
    - `input_history_ids` (Many2many): Input History (product.template, computed, help="该批次产品生产过程中使用的所有投入品")
  - Methods:
    - `_compute_input_history(self)`: Computes input history for the lot
    - `check_export_compliance(self, country_code)`: Checks export compliance against country standards
    - `_get_input_history(self)`: Gets input history for the lot
    - `_get_related_inputs_for_product(self, product)`: Gets related inputs for a product
  - Relationships: Inherits stock.lot

- **farm_sale_ch.SaleOrder**: Sale CH-enhanced sale orders
  - Odoo Model: `class SaleOrder(models.Model)`
  - _name: `sale.order` (inherited)
  - _inherit: `sale.order`
  - Fields:
    - `export_country_code` (Char): Export Country Code (help="如果此订单是出口订单，请输入目标国家代码")
    - `export_compliance_status` (Selection): Export Compliance Status (unknown, compliant, non_compliant) (default="unknown", readonly=True)
  - Methods:
    - `generate_compliance_report(self, country_code)`: Generates compliance report for export
    - `_get_compliance_recommendations(self, standard, violations)`: Gets compliance recommendations
    - `auto_check_compliance_before_sale(self)`: Auto-checks compliance before sale
    - `generate_certificate_of_compliance(self)`: Generates compliance certificate
    - `_generate_certificate_number(self)`: Generates certificate number
    - `action_confirm(self)`: Confirms sale with export compliance checks
    - `_onchange_product_export_compliance(self)`: Onchange for product export compliance
  - Relationships: Inherits sale.order

- **farm_sale_ch.SaleOrderLine**: Line items for sale CH orders
  - Odoo Model: `class SaleOrderLine(models.Model)`
  - _name: `sale.order.line` (inherited)
  - _inherit: `sale.order.line`
  - Methods:
    - `_onchange_product_export_compliance(self)`: Onchange for export compliance checking
  - Relationships: Inherits sale.order.line

- **farm_sale_ch.ExportComplianceLog**: Export compliance logging
  - Odoo Model: `class ExportComplianceLog(models.Model)`
  - _name: `export.compliance.log`
  - _description: "Export Compliance Check Log"
  - _order: `checked_on desc`
  - Fields:
    - `order_id` (Many2one): Sale Order (sale.order, required)
    - `country_code` (Char): Country Code (required)
    - `violations` (Char): Violations (help="Compliance violations found")
    - `checked_on` (Datetime): Checked On (required, default=fields.Datetime.now)
    - `result` (Selection): Result (passed, failed) (required)
    - `notes` (Text): Notes (help="Additional notes about the compliance check")
    - `checked_by` (Many2one): Checked By (res.users, default=lambda self: self.env.user)
  - Relationships: Links sale orders to compliance check logs

- **farm_sale_ch.ExportCertificate**: Export certificate management
  - Odoo Model: `class ExportCertificate(models.Model)`
  - _name: `export.certificate`
  - _description: "Export Compliance Certificate"
  - _rec_name: `certificate_number`
  - Fields:
    - `order_id` (Many2one): Sale Order (sale.order, required)
    - `product_name` (Char): Product Name (required)
    - `destination_country` (Char): Destination Country (required)
    - `certificate_number` (Char): Certificate Number (required, copy=False)
    - `issue_date` (Date): Issue Date (required, default=fields.Date.today)
    - `valid_until` (Date): Valid Until (required)
    - `inspector` (Char): Inspector (required)
    - `compliance_details` (Text): Compliance Details (help="Detailed compliance information")
    - `is_active` (Boolean): Is Active (default=True)
    - `attachment` (Binary): Certificate Attachment (help="Certificate file")
    - `attachment_name` (Char): Attachment Name
  - Methods:
    - `_check_valid_until(self)`: Checks valid until date constraint
    - `action_generate_certificate_document(self)`: Generates certificate document
    - `_create_certificate_document(self, certificate)`: Creates certificate document content
    - `check_certificate_validity(self, certificate_number)`: Checks certificate validity
  - Relationships: Links sale orders to export certificates

- **farm_cert_ch.FarmProductCertificate**: Product certification for CH
  - Odoo Model: `class FarmProductCertificate(models.Model)`
  - _name: `farm.product.certificate`
  - _description: "Edible Agri-Product Certificate"
  - _inherit: `mail.thread`, `mail.activity.mixin`
  - _rec_name: `certificate_no`
  - Fields:
    - `certificate_no` (Char): Certificate No. (default=lambda self: _('New'))
    - `picking_id` (Many2one): Source Dispatch (stock.picking, required)
    - `lot_id` (Many2one): Product Lot (stock.lot, required)
    - `product_id` (Many2one): Product (product.product, related='lot_id.product_id', store=True)
    - `producer_name` (Char): Producer Name (default=lambda self: self.env.company.name)
    - `origin_location_id` (Many2one): Origin/Farm (stock.location, domain=[('is_land_parcel', '=', True)])
    - `production_date` (Date): Production Date (related='lot_id.create_date', store=True)
    - `commitment_statement` (Html): Commitment Statement (default HTML content)
    - `quality_check_ids` (Many2many): Related Quality Checks (farm.quality.check)
    - `certificate_qr_code` (Char): Certificate QR Code (computed, store=True)
  - Methods:
    - `_compute_qr_code(self)`: Computes certificate QR code
    - `create(self, vals_list)`: Creates certificate with sequence number
  - Relationships: Inherits mail.thread, mail.activity.mixin

- **farm_cert_ch.StockPicking**: Certification CH-enhanced stock picking
  - Odoo Model: `class StockPicking(models.Model)`
  - _name: `stock.picking` (inherited)
  - _inherit: `stock.picking`
  - Fields:
    - `requires_cert_ch` (Boolean): Requires Cert. (China) (computed, store=True)
    - `certificate_ch_ids` (One2many): Certificates (China) (farm.product.certificate, 'picking_id')
  - Methods:
    - `_compute_requires_cert_ch(self)`: Computes if certification is required
    - `action_generate_cert_ch(self)`: Generates edible agricultural product certificate
  - Relationships: Inherits stock.picking

### Machinery and Subsidy Support
- **farm_machinery_ch.FarmEquipment**: Machinery CH-enhanced equipment management
  - Odoo Model: `class FarmEquipment(models.Model)`
  - _name: `maintenance.equipment` (inherited)
  - _inherit: `maintenance.equipment`
  - Fields:
    - `is_subsidized_machinery` (Boolean): Eligible for Subsidy (default=False)
    - `subsidy_category` (Char): Subsidy Category (e.g. "耕整地机械-拖拉机")
    - `subsidy_model_no` (Char): Subsidy Model No.
    - `subsidy_grade_params` (Char): Subsidy Grading Parameters
    - `estimated_subsidy_amount` (Monetary): Estimated Subsidy Amount (currency_field='currency_id')
    - `currency_id` (Many2one): Currency (res.currency, default=lambda self: self.env.company.currency_id)
    - `invoice_attachment_ids` (Many2many): Invoice Attachments (ir.attachment, 'machinery_invoice_rel', 'equipment_id', 'attachment_id')
    - `photo_attachment_ids` (Many2many): Machinery Photos (ir.attachment, 'machinery_photo_rel', 'equipment_id', 'attachment_id')
  - Methods:
    - `action_match_subsidy_catalog(self)`: Matches national machinery subsidy catalog
  - Relationships: Inherits maintenance.equipment

- **farm_machinery_ch.FarmMachinerySubsidyApplication**: Machinery subsidy application management
  - Odoo Model: `class FarmMachinerySubsidyApplication(models.Model)`
  - _name: `farm.machinery.subsidy.application`
  - _description: "Agricultural Machinery Subsidy Application"
  - _inherit: `mail.thread`, `mail.activity.mixin`
  - Fields:
    - `name` (Char): Application Ref (default=lambda self: _('New'))
    - `equipment_id` (Many2one): Machinery (maintenance.equipment, required)
    - `applicant_id` (Many2one): Applicant (res.partner, default=lambda self: self.env.company.partner_id)
    - `application_date` (Date): Application Date (default=fields.Date.today)
    - `estimated_subsidy` (Monetary): Estimated Subsidy (related='equipment_id.estimated_subsidy_amount')
    - `currency_id` (Many2one): Currency (res.currency, related='equipment_id.currency_id')
    - `state` (Selection): State (draft, submitted, approved, paid, rejected) (default="draft", tracking=True)
  - Methods:
    - `create(self, vals_list)`: Creates application with sequence number
  - Relationships: Inherits mail.thread, mail.activity.mixin

- **farm_subsidy_ch.FarmSubsidyApplication**: Subsidy CH-enhanced subsidy application management
  - Odoo Model: `class FarmSubsidyApplication(models.Model)`
  - _name: `farm.subsidy.application` (inherited)
  - _inherit: `farm.subsidy.application`
  - Fields:
    - `crop_type_china` (Selection): Crop Type (China) (early_rice, wheat, corn, soybean, other) (required)
    - `declared_area_mu` (Float): Declared Area (mu) (computed, store=True)
  - Methods:
    - `_compute_declared_area_mu(self)`: Computes declared area in mu (1 mu = 666.67 sqm)
    - `action_generate_moara_report(self)`: Generates MOARA subsidy report
  - Relationships: Inherits farm.subsidy.application

### Industrial IoT
- **industrial_iot.IiotDevice**: Industrial IoT device management
  - Odoo Model: `class IiotDevice(models.Model)`
  - _name: `iiot.device`
  - _description: "Industrial IoT Device"
  - _order: "serial_number"
  - Fields:
    - `name` (Char): Name (computed field based on serial_number and device_id, store=True)
    - `serial_number` (Char): Serial Number (required, unique, copy=False, help: "Physical serial number (unique)")
    - `device_id` (Char): Device ID (required, unique, copy=False, help: "Logical ID for Topics")
    - `profile_id` (Many2one): Communication Profile (iiot.device.profile, required, help: "Associated communication profile")
    - `business_ref` (Reference): Business Reference (dynamic selection of business entities, help: "Associated business entity (equipment/workcenter/location)")
    - `config_token` (Char): Config Token (copy=False, help: "One-time configuration download token")
    - `firmware_version` (Char): Firmware Version (help: "Current firmware version")
    - `is_camera` (Boolean): Is Camera (video stream integration [US-16-01], default: False)
    - `live_stream_url` (Char): Live Stream URL (help: "HLS/HTTP/RTSP stream URL for the camera")
    - `is_active` (Boolean): Active (default: True)
    - `last_telemetry` (Datetime): Last Telemetry
    - `last_command` (Datetime): Last Command
    - `connection_status` (Selection): Connection Status (selection: offline/online/error, default: 'offline')
    - `created_date` (Datetime): Created Date (default: fields.Datetime.now)
    - `last_update` (Datetime): Last Update (default: fields.Datetime.now)
  - SQL Constraints:
    - serial_number_uniq: Serial number must be unique
    - device_id_uniq: Device ID must be unique
  - Methods:
    - `_get_business_models()`: Returns list of models that can be referenced in business_ref field
    - `_compute_name()`: Computes device name as "{serial_number} ({device_id})"
    - `_check_device_id_format()`: Validates device_id format (letters, numbers, underscores, hyphens)
    - `action_generate_config_token()`: Generates pairing token
    - `get_topic_map()`: Generates complete topic list with SaaS isolation (company_id prefix)
    - `send_command(action, **params)`: Sends command with SaaS isolation via HTTP-to-MQTT bridge
    - `process_telemetry_data(telemetry_data)`: Processes incoming telemetry data based on rules
    - `create(vals)`: Handles device creation with default device_id and config_token generation
    - `write(vals)`: Updates last_update timestamp

- **industrial_iot.IiotTelemetryRule**: Telemetry rules for industrial IoT
  - Odoo Model: `class IiotTelemetryRule(models.Model)`
  - _name: `iiot.telemetry.rule`
  - _description: "Industrial IoT Telemetry Rule"
  - _order: "profile_id, sequence"
  - Fields:
    - `name` (Char): Name (required)
    - `sequence` (Integer): Sequence (default: 10)
    - `active` (Boolean): Active (default: True)
    - `profile_id` (Many2one): Profile (iiot.device.profile, required, help: "Associated device profile")
    - `json_path` (Char): JSON Path (required, help: "Path to extract value from telemetry payload, e.g. $.temperature", default: "$.value")
    - `target_model` (Char): Target Model (required, help: "Target model, e.g. maintenance.equipment")
    - `target_domain` (Char): Target Domain (required, help: "Domain to find target records, e.g. [('iot_device_id', '=', '{{ device_id }}')]", default: "[('id', '!=', 0)]")
    - `target_field` (Char): Target Field (required, help: "Target field to write to, e.g. x_temperature")
  - Methods:
    - `_check_json_path()`: Validates JSON Path format
    - `_check_target_domain()`: Validates target domain format
    - `evaluate_domain(device_id)`: Evaluates the target domain with device_id context

- **industrial_iot.IiotFirmware**: Firmware management for industrial IoT devices
  - Odoo Model: `class IiotFirmware(models.Model)`
  - _name: `iiot.firmware`
  - _description: "Industrial IoT Firmware"
  - _order: "version DESC"
  - Fields:
    - `name` (Char): Name (computed field based on version and profile_code, store=True)
    - `version` (Char): Version (required, help: "Firmware version number")
    - `profile_code` (Char): Device Type (required, help: "Applicable device type code")
    - `url` (Char): Download URL (required, help: "Firmware download URL")
    - `checksum` (Char): Checksum (help: "Firmware file checksum")
    - `description` (Text): Description
    - `is_active` (Boolean): Active (default: True, help: "Is this an active version?")
    - `created_date` (Datetime): Created Date (default: fields.Datetime.now)
  - SQL Constraints:
    - version_profile_uniq: Firmware version must be unique for each device type
  - Methods:
    - `_compute_name()`: Computes firmware name as "{profile_code} v{version}"
    - `_check_version_format()`: Validates version format (letters, numbers, dots, underscores, hyphens)
    - `_check_url_format()`: Validates URL format (requires http://, https:// or ftp:// prefix)
    - `action_deactivate()`: Deactivates firmware version
    - `action_activate()`: Activates firmware version

- **industrial_iot.IiotUpdate**: Update management for industrial IoT devices
  - Odoo Model: `class IiotUpdate(models.Model)`
  - _name: `iiot.update`
  - _description: "Industrial IoT Firmware Update"
  - _order: "create_date DESC"
  - Fields:
    - `name` (Char): Update Name (computed field based on device_id and firmware_id, store=True)
    - `device_id` (Many2one): Target Device (iiot.device, required)
    - `firmware_id` (Many2one): Firmware Version (iiot.firmware, required)
    - `update_id` (Char): Update ID (default: auto-generated UUID, readonly)
    - `status` (Selection): Status (selection: pending/sent/downloading/installing/success/failed/cancelled, default: 'pending')
    - `start_time` (Datetime): Start Time
    - `end_time` (Datetime): End Time
    - `error_message` (Text): Error Message
    - `progress` (Float): Progress (default: 0.0, help: "Update progress percentage (0.0-100.0)")
    - `description` (Text): Description
  - Methods:
    - `_compute_name()`: Computes update name as "{device_id.device_id} -> {firmware_id.version}"
    - `_generate_update_id()`: Generates UUID for update ID
    - `action_send_ota()`: Sends OTA update command to device
    - `update_status_from_device(new_status, progress, error_message)`: Updates status from device
    - `action_cancel_update()`: Cancels update task

- **industrial_iot.IiotDeviceProfile**: Device profiles for industrial IoT
  - Odoo Model: `class IiotDeviceProfile(models.Model)`
  - _name: `iiot.device.profile`
  - _description: "Industrial IoT Device Profile"
  - _order: "code"
  - Fields:
    - `name` (Char): Name (required)
    - `code` (Char): Code (required, help: "Device type code, e.g. cnc_v1")
    - `telemetry_topic_template` (Char): Telemetry Topic Template (default: "telemetry/{device}/data", help: "Telemetry topic template, e.g. telemetry/{device}/data")
    - `command_topic_template` (Char): Command Topic Template (default: "cmd/{device}/request", help: "Command topic template, e.g. cmd/{device}/request")
    - `ota_notify_topic_template` (Char): OTA Notify Topic Template (default: "ota/{device}/notify", help: "OTA notify topic template, e.g. ota/{device}/notify")
    - `ota_status_topic_template` (Char): OTA Status Topic Template (default: "ota/{device}/status", help: "OTA status topic template, e.g. ota/{device}/status")
    - `command_template` (Text): Command Template (default: '{"action": "{{ action }}", "params": {{ params | tojson }}}', help: "Command message template (Jinja2)")
  - Methods:
    - `_check_topic_templates()`: Validates that topic templates contain {device} placeholder
    - `_check_code()`: Validates code format (letters, numbers, underscores, hyphens)

### Agricultural Processing
- **farm_agricultural_processing.SeasonalBom**: Seasonal bills of materials for processing
  - Odoo Model: `class SeasonalBom(models.Model)`
  - _name: `farm.seasonal.bom`
  - _description: "Seasonal Versioned Recipe Management"
  - _order: "product_tmpl_id, season_start_date"
  - Fields:
    - `name` (Char): Seasonal Recipe Name (required, default from _default_name)
    - `product_tmpl_id` (Many2one): Product (product.template)
    - `bom_id` (Many2one): Base BOM (mrp.bom)
    - `season_name` (Char): Season Name (required)
    - `season_description` (Text): Season Description
    - `season_start_date` (Date): Season Start Date (required)
    - `season_end_date` (Date): Season End Date (required)
    - `seasonal_material_ids` (One2many): Seasonal Material Adjustments (farm.seasonal.bom.material)
    - `seasonal_parameter_ids` (One2many): Seasonal Parameter Adjustments (farm.seasonal.bom.parameter)
    - `version_number` (Integer): Version (default: 1)
    - `version_name` (Char): Version Name
    - `state` (Selection): Status (draft, active, inactive)
    - `is_seasonal_adjustment` (Boolean): Has Seasonal Adjustment (computed, stored)
    - `base_yield_factor` (Float): Base Yield Factor (default: 1.0)
    - `seasonal_yield_factor` (Float): Seasonal Yield Factor (computed, stored)
  - Methods:
    - `_default_name()`: Default name for seasonal recipe
    - `_check_season_dates()`: Ensures season end date is after start date
    - `_check_overlapping_seasons()`: Ensures no overlapping seasons for the same product
    - `_compute_has_seasonal_adjustment()`: Computes if has seasonal adjustment
    - `_compute_seasonal_yield_factor()`: Computes seasonal yield factor
    - `action_activate()`: Activate this seasonal recipe
    - `action_deactivate()`: Deactivate this seasonal recipe
    - `get_applicable_seasonal_bom(product_id, date)`: Get applicable seasonal BOM for product on date
    - `apply_seasonal_adjustments(base_bom)`: Apply seasonal adjustments to base BOM
    - `action_view_seasonal_materials()`: Open view to see seasonal material adjustments
    - `action_view_seasonal_parameters()`: Open view to see seasonal parameter adjustments
  - Relationships:
    - Many2one: `product_tmpl_id` → `product.template`
    - Many2one: `bom_id` → `mrp.bom`
    - One2many: `seasonal_material_ids` → `farm.seasonal.bom.material.seasonal_bom_id`
    - One2many: `seasonal_parameter_ids` → `farm.seasonal.bom.parameter.seasonal_bom_id`

- **farm_agricultural_processing.SeasonalBomMaterial**: Materials for seasonal BOMs
  - Odoo Model: `class SeasonalBomMaterial(models.Model)`
  - _name: `farm.seasonal.bom.material`
  - _description: "Seasonal BOM Material Adjustment"
  - Fields:
    - `seasonal_bom_id` (Many2one): Seasonal BOM (farm.seasonal.bom, ondelete=cascade)
    - `product_id` (Many2one): Material (product.product, required)
    - `base_qty` (Float): Base Quantity (required)
    - `seasonal_qty` (Float): Seasonal Quantity (required)
    - `qty_difference` (Float): Quantity Difference (computed, stored)
    - `adjustment_reason` (Text): Adjustment Reason
  - Methods:
    - `_compute_qty_difference()`: Computes quantity difference
    - `_onchange_product_id()`: Sets base quantity from original BOM
  - Relationships:
    - Many2one: `seasonal_bom_id` → `farm.seasonal.bom` with cascade delete
    - Many2one: `product_id` → `product.product`

- **farm_agricultural_processing.SeasonalBomParameter**: Parameters for seasonal BOMs
  - Odoo Model: `class SeasonalBomParameter(models.Model)`
  - _name: `farm.seasonal.bom.parameter`
  - _description: "Seasonal BOM Parameter Adjustment"
  - Fields:
    - `seasonal_bom_id` (Many2one): Seasonal BOM (farm.seasonal.bom, ondelete=cascade)
    - `parameter_name` (Char): Parameter Name (required)
    - `base_value` (Float): Base Value (required)
    - `seasonal_value` (Float): Seasonal Value (required)
    - `value_difference` (Float): Value Difference (computed, stored)
    - `unit_of_measure` (Char): Unit of Measure
    - `adjustment_reason` (Text): Adjustment Reason
  - Methods:
    - `_compute_value_difference()`: Computes value difference
  - Relationships:
    - Many2one: `seasonal_bom_id` → `farm.seasonal.bom` with cascade delete

- **farm_agricultural_processing.FarmProcessingProductionAnalyticsExtension**: Analytics extensions for processing production
  - Odoo Model: `class FarmProcessingProductionAnalyticsExtension(models.Model)`
  - _name: `farm.processing.production.analytics.extension`
  - _description: "Analytics Extensions for Processing Production"
  - Relationships:
    - Extends: Base models with analytics extension functionality

- **farm_agricultural_processing.AgriProcessingYieldRateAnalytics**: Yield rate analytics for agriculture processing
  - Odoo Model: `class AgriProcessingYieldRateAnalytics(models.Model)`
  - _name: `agri.processing.yield.rate.analytics`
  - _description: "Yield Rate Analytics for Agriculture Processing"
  - Relationships:
    - Extends: Base models with yield rate analytics functionality

- **farm_agricultural_processing.AgriProcessingRecallSimulation**: Recall simulation for agriculture processing
  - Odoo Model: `class AgriProcessingRecallSimulation(models.Model)`
  - _name: `agri.processing.recall.simulation`
  - _description: "Recall Simulation for Agriculture Processing"
  - Relationships:
    - Extends: Base models with recall simulation functionality

- **farm_agricultural_processing.AgriProcessingPerformanceAnalytics**: Performance analytics for agriculture processing
  - Odoo Model: `class AgriProcessingPerformanceAnalytics(models.Model)`
  - _name: `agri.processing.performance.analytics`
  - _description: "Performance Analytics for Agriculture Processing"
  - Relationships:
    - Extends: Base models with performance analytics functionality

- **farm_agricultural_processing.FarmProcessingProductionNetVegetablesExtension**: Net vegetables extensions for processing production
  - Odoo Model: `class FarmProcessingProductionNetVegetablesExtension(models.Model)`
  - _name: `farm.processing.production.net.vegetables.extension`
  - _description: "Net Vegetables Extensions for Processing Production"
  - Relationships:
    - Extends: Base models with net vegetables extension functionality

- **farm_agricultural_processing.FarmProcessingBomNetVegetablesExtension**: Net vegetables extensions for processing BOM
  - Odoo Model: `class FarmProcessingBomNetVegetablesExtension(models.Model)`
  - _name: `farm.processing.bom.net.vegetables.extension`
  - _description: "Net Vegetables Extensions for Processing BOM"
  - Relationships:
    - Extends: Base models with net vegetables BOM extension functionality

- **farm_agricultural_processing.FarmProcessingStepNetVegetables**: Net vegetables processing steps
  - Odoo Model: `class FarmProcessingStepNetVegetables(models.Model)`
  - _name: `farm.processing.step.net.vegetables`
  - _description: "Net Vegetables Processing Steps"
  - Relationships:
    - Extends: Base models with net vegetables processing steps

- **farm_agricultural_processing.FarmProcessingBomExtension**: Extensions for processing BOMs
  - Odoo Model: `class FarmProcessingBomExtension(models.Model)`
  - _name: `farm.processing.bom.extension`
  - _description: "Extensions for Processing BOMs"
  - Relationships:
    - Extends: Base models with processing BOM extension functionality

- **farm_agricultural_processing.FarmProcessingBomLineExtension**: Extensions for processing BOM lines
  - Odoo Model: `class FarmProcessingBomLineExtension(models.Model)`
  - _name: `farm.processing.bom.line.extension`
  - _description: "Extensions for Processing BOM Lines"
  - Relationships:
    - Extends: Base models with processing BOM line extension functionality

- **farm_agricultural_processing.FarmBomGradeDistribution**: Grade distribution for BOMs
  - Odoo Model: `class FarmBomGradeDistribution(models.Model)`
  - _name: `farm.bom.grade.distribution`
  - _description: "Grade Distribution for BOMs"
  - Relationships:
    - Extends: Base models with grade distribution functionality

- **farm_agricultural_processing.FarmProcessingProductionExtension**: Extensions for processing production
  - Odoo Model: `class FarmProcessingProductionExtension(models.Model)`
  - _name: `farm.processing.production.extension`
  - _description: "Extensions for Processing Production"
  - Relationships:
    - Extends: Base models with processing production extension functionality

- **farm_agricultural_processing.FarmProcessingProductionMassBalanceExtension**: Mass balance extensions for processing production
  - Odoo Model: `class FarmProcessingProductionMassBalanceExtension(models.Model)`
  - _name: `farm.processing.production.mass.balance.extension`
  - _description: "Mass Balance Extensions for Processing Production"
  - Relationships:
    - Extends: Base models with mass balance extension functionality

- **farm_agricultural_processing.FarmProcessingProductionMultiOutputExtension**: Multi-output extensions for processing production
  - Odoo Model: `class FarmProcessingProductionMultiOutputExtension(models.Model)`
  - _name: `farm.processing.production.multi.output.extension`
  - _description: "Multi-Output Extensions for Processing Production"
  - Relationships:
    - Extends: Base models with multi-output extension functionality

- **farm_agricultural_processing.AgriProcessingMultiOutputLine**: Multi-output line items for agriculture processing
  - Odoo Model: `class AgriProcessingMultiOutputLine(models.Model)`
  - _name: `agri.processing.multi.output.line`
  - _description: "Multi-Output Line Items for Agriculture Processing"
  - Relationships:
    - Extends: Base models with multi-output line functionality

- **farm_agricultural_processing.FarmProcessingProductionAttributeInheritanceExtension**: Attribute inheritance extensions for processing production
  - Odoo Model: `class FarmProcessingProductionAttributeInheritanceExtension(models.Model)`
  - _name: `farm.processing.production.attribute.inheritance.extension`
  - _description: "Attribute Inheritance Extensions for Processing Production"
  - Relationships:
    - Extends: Base models with attribute inheritance extension functionality

- **farm_agricultural_processing.FarmProcessingProductionActiveIngredientExtension**: Active ingredient extensions for processing production
  - Odoo Model: `class FarmProcessingProductionActiveIngredientExtension(models.Model)`
  - _name: `farm.processing.production.active.ingredient.extension`
  - _description: "Active Ingredient Extensions for Processing Production"
  - Relationships:
    - Extends: Base models with active ingredient extension functionality

- **farm_agricultural_processing.FarmProcessingProductionAllergenExtension**: Allergen extensions for processing production
  - Odoo Model: `class FarmProcessingProductionAllergenExtension(models.Model)`
  - _name: `farm.processing.production.allergen.extension`
  - _description: "Allergen Extensions for Processing Production"
  - Relationships:
    - Extends: Base models with allergen extension functionality

- **farm_agricultural_processing.FarmProcessingProductionGmpExtension**: GMP extensions for processing production
  - Odoo Model: `class FarmProcessingProductionGmpExtension(models.Model)`
  - _name: `farm.processing.production.gmp.extension`
  - _description: "GMP Extensions for Processing Production"
  - Relationships:
    - Extends: Base models with GMP extension functionality

- **farm_agricultural_processing.AgriProcessingEnvironmentalMonitoringLine**: Environmental monitoring line items for agriculture processing
  - Odoo Model: `class AgriProcessingEnvironmentalMonitoringLine(models.Model)`
  - _name: `agri.processing.environmental.monitoring.line`
  - _description: "Environmental Monitoring Line Items for Agriculture Processing"
  - Relationships:
    - Extends: Base models with environmental monitoring line functionality

- **farm_agricultural_processing.FarmProcessingProductionLabelComplianceExtension**: Label compliance extensions for processing production
  - Odoo Model: `class FarmProcessingProductionLabelComplianceExtension(models.Model)`
  - _name: `farm.processing.production.label.compliance.extension`
  - _description: "Label Compliance Extensions for Processing Production"
  - Relationships:
    - Extends: Base models with label compliance extension functionality

- **farm_agricultural_processing.FarmProcessingProductionHaccpExtension**: HACCP extensions for processing production
  - Odoo Model: `class FarmProcessingProductionHaccpExtension(models.Model)`
  - _name: `farm.processing.production.haccp.extension`
  - _description: "HACCP Extensions for Processing Production"
  - Relationships:
    - Extends: Base models with HACCP extension functionality

- **farm_agricultural_processing.AgriProcessingHaccpMonitoringLine**: HACCP monitoring line items for agriculture processing
  - Odoo Model: `class AgriProcessingHaccpMonitoringLine(models.Model)`
  - _name: `agri.processing.haccp.monitoring.line`
  - _description: "HACCP Monitoring Line Items for Agriculture Processing"
  - Relationships:
    - Extends: Base models with HACCP monitoring line functionality

- **farm_agricultural_processing.AgriProcessingHaccpVerificationLine**: HACCP verification line items for agriculture processing
  - Odoo Model: `class AgriProcessingHaccpVerificationLine(models.Model)`
  - _name: `agri.processing.haccp.verification.line`
  - _description: "HACCP Verification Line Items for Agriculture Processing"
  - Relationships:
    - Extends: Base models with HACCP verification line functionality

- **farm_agricultural_processing.FarmProcessingProductionSCExtension**: SC extensions for processing production
  - Odoo Model: `class FarmProcessingProductionSCExtension(models.Model)`
  - _name: `farm.processing.production.sc.extension`
  - _description: "SC Extensions for Processing Production"
  - Relationships:
    - Extends: Base models with SC extension functionality

- **farm_agricultural_processing.FarmProcessingBomSCExtension**: SC extensions for processing BOM
  - Odoo Model: `class FarmProcessingBomSCExtension(models.Model)`
  - _name: `farm.processing.bom.sc.extension`
  - _description: "SC Extensions for Processing BOM"
  - Relationships:
    - Extends: Base models with SC BOM extension functionality

- **farm_agricultural_processing.AgriProcessingLicenseCheck**: License checks for agriculture processing
  - Odoo Model: `class AgriProcessingLicenseCheck(models.Model)`
  - _name: `agri.processing.license.check`
  - _description: "License Checks for Agriculture Processing"
  - Relationships:
    - Extends: Base models with license check functionality

- **farm_agricultural_processing.FarmProcessingProductionPackagingExtension**: Packaging extensions for processing production
  - Odoo Model: `class FarmProcessingProductionPackagingExtension(models.Model)`
  - _name: `farm.processing.production.packaging.extension`
  - _description: "Packaging Extensions for Processing Production"
  - Relationships:
    - Extends: Base models with packaging extension functionality

- **farm_agricultural_processing.AgriProcessingPackaging**: Packaging management for agriculture processing
  - Odoo Model: `class AgriProcessingPackaging(models.Model)`
  - _name: `agri.processing.packaging`
  - _description: "Packaging Management for Agriculture Processing"
  - Relationships:
    - Extends: Base models with packaging management functionality

- **farm_agricultural_processing.FarmProcessingBomFormulaVersionExtension**: Formula version extensions for processing BOM
  - Odoo Model: `class FarmProcessingBomFormulaVersionExtension(models.Model)`
  - _name: `farm.processing.bom.formula.version.extension`
  - _description: "Formula Version Extensions for Processing BOM"
  - Relationships:
    - Extends: Base models with formula version extension functionality

- **farm_agricultural_processing.FarmProcessingBlindMaterial**: Blind material management for processing
  - Odoo Model: `class FarmProcessingBlindMaterial(models.Model)`
  - _name: `farm.processing.blind.material`
  - _description: "Blind Material Management for Processing"
  - Relationships:
    - Extends: Base models with blind material management functionality

- **farm_agricultural_processing.FarmProcessingFormulaAutoCorrection**: Formula auto-correction for processing
  - Odoo Model: `class FarmProcessingFormulaAutoCorrection(models.Model)`
  - _name: `farm.processing.formula.auto.correction`
  - _description: "Formula Auto-Correction for Processing"
  - Relationships:
    - Extends: Base models with formula auto-correction functionality

- **farm_agricultural_processing.StockLotTraceabilityExtension**: Traceability extensions for stock lots
  - Odoo Model: `class StockLotTraceabilityExtension(models.Model)`
  - _name: `stock.lot.traceability.extension`
  - _description: "Traceability Extensions for Stock Lots"
  - _inherit: `stock.lot`
  - Relationships:
    - Extends: `stock.lot` with traceability extension functionality

- **farm_agricultural_processing.AgriProcessingLotTracking**: Lot tracking for agriculture processing
  - Odoo Model: `class AgriProcessingLotTracking(models.Model)`
  - _name: `agri.processing.lot.tracking`
  - _description: "Lot Tracking for Agriculture Processing"
  - Relationships:
    - Extends: Base models with lot tracking functionality

- **farm_agricultural_processing.FarmWorkcenterExtension**: Extensions for work centers in processing
  - Odoo Model: `class FarmWorkcenterExtension(models.Model)`
  - _name: `farm.workcenter.extension`
  - _description: "Extensions for Work Centers in Processing"
  - _inherit: `mrp.workcenter`
  - Relationships:
    - Extends: `mrp.workcenter` with processing extension functionality

- **farm_agricultural_processing.FarmWorkorderEnergyExtension**: Energy extensions for work orders in processing
  - Odoo Model: `class FarmWorkorderEnergyExtension(models.Model)`
  - _name: `farm.workorder.energy.extension`
  - _description: "Energy Extensions for Work Orders in Processing"
  - _inherit: `mrp.workorder`
  - Relationships:
    - Extends: `mrp.workorder` with energy extension functionality

### Ecology
- **farm_ecology.FarmBiodiversityIndicator**: Biodiversity indicators for ecological management
- **farm_ecology.FarmEcologicalZone**: Ecological zone management

## Abstract and Mixin Models

Abstract and mixin models provide reusable functionality across the system:

### System Utilities
- **CommonValidationsMixin** (Abstract): Provides common validation utilities
  - Odoo Model: `class CommonValidationsMixin(models.AbstractModel)`
  - _name: `farm.core.common.validations.mixin`
  - _description: "Common Validation Utilities Mixin"
  - _inherit: `models.AbstractModel`
  - Relationships:
    - Inherits: `models.AbstractModel`

- **CommonComputeMethodsMixin** (Abstract): Provides common compute method utilities
  - Odoo Model: `class CommonComputeMethodsMixin(models.AbstractModel)`
  - _name: `farm.core.common.compute.methods.mixin`
  - _description: "Common Compute Method Utilities Mixin"
  - _inherit: `models.AbstractModel`
  - Relationships:
    - Inherits: `models.AbstractModel`

- **ByproductCostShareMixin** (Abstract): Provides byproduct cost sharing utilities
  - Odoo Model: `class ByproductCostShareMixin(models.AbstractModel)`
  - _name: `farm.core.byproduct.cost.share.mixin`
  - _description: "Byproduct Cost Share Mixin"
  - _inherit: `models.AbstractModel`
  - Relationships:
    - Inherits: `models.AbstractModel`

### Core Reusable Functionality
- **CommonAgriculturalFields** (Abstract): Provides common agricultural fields across models
  - Odoo Model: `class CommonAgriculturalFields(models.AbstractModel)`
  - _name: `farm.core.common.agricultural.fields`
  - _description: "Common Agricultural Fields Mixin"
  - _inherit: `models.AbstractModel`
  - Relationships:
    - Inherits: `models.AbstractModel`

- **CreationMethodMixin** (Abstract): Provides creation method utilities
  - Odoo Model: `class CreationMethodMixin(models.AbstractModel)`
  - _name: `farm.core.creation.method.mixin`
  - _description: "Creation Method Utilities Mixin"
  - _inherit: `models.AbstractModel`
  - Relationships:
    - Inherits: `models.AbstractModel`

- **ComputedFieldMixin** (Abstract): Provides computed field utilities
  - Odoo Model: `class ComputedFieldMixin(models.AbstractModel)`
  - _name: `farm.core.computed.field.mixin`
  - _description: "Computed Field Utilities Mixin"
  - _inherit: `models.AbstractModel`
  - Relationships:
    - Inherits: `models.AbstractModel`

- **ComplianceMixin** (Abstract): Provides compliance utilities
  - Odoo Model: `class ComplianceMixin(models.AbstractModel)`
  - _name: `farm.core.compliance.mixin`
  - _description: "Compliance Utilities Mixin"
  - _inherit: `models.AbstractModel`
  - Relationships:
    - Inherits: `models.AbstractModel`

- **GISCoordinateUtils** (Abstract): Provides GIS coordinate utilities
  - Odoo Model: `class GISCoordinateUtils(models.AbstractModel)`
  - _name: `farm.core.gis.utils`
  - _description: "GIS Coordinate Utilities Mixin"
  - _inherit: `models.AbstractModel`
  - Relationships:
    - Inherits: `models.AbstractModel`

### Operation Utilities
- **FarmAgriculturalCampaignMixin** (Abstract): Provides agricultural campaign utilities
  - Odoo Model: `class FarmAgriculturalCampaignMixin(models.AbstractModel)`
  - _name: `farm.agricultural.campaign.mixin`
  - _description: "Agricultural Campaign Utilities Mixin"
  - _inherit: `models.AbstractModel`
  - Relationships:
    - Inherits: `models.AbstractModel`

- **FarmAgriculturalInterventionMixin** (Abstract): Provides agricultural intervention utilities
  - Odoo Model: `class FarmAgriculturalInterventionMixin(models.AbstractModel)`
  - _name: `farm.agricultural.intervention.mixin`
  - _description: "Agricultural Intervention Utilities Mixin"
  - _inherit: `models.AbstractModel`
  - Relationships:
    - Inherits: `models.AbstractModel`

- **FarmAgriculturalBomMixin** (Abstract): Provides agricultural BOM utilities
  - Odoo Model: `class FarmAgriculturalBomMixin(models.AbstractModel)`
  - _name: `farm.agricultural.bom.mixin`
  - _description: "Agricultural BOM Utilities Mixin"
  - _inherit: `models.AbstractModel`
  - Relationships:
    - Inherits: `models.AbstractModel`

- **FarmAgriculturalBomLineMixin** (Abstract): Provides agricultural BOM line utilities
  - Odoo Model: `class FarmAgriculturalBomLineMixin(models.AbstractModel)`
  - _name: `farm.agricultural.bom.line.mixin`
  - _description: "Agricultural BOM Line Utilities Mixin"
  - _inherit: `models.AbstractModel`
  - Relationships:
    - Inherits: `models.AbstractModel`

- **FarmAgriculturalCampaignBase** (Abstract): Provides base functionality for agricultural campaigns
  - Odoo Model: `class FarmAgriculturalCampaignBase(models.AbstractModel)`
  - _name: `farm.agricultural.campaign.base`
  - _description: "Agricultural Campaign Base Functionality"
  - _inherit: `models.AbstractModel`
  - Relationships:
    - Inherits: `models.AbstractModel`

### MRP Utilities
- **FarmAgriBomMixin** (Abstract): Provides agricultural BOM utilities for MRP
  - Odoo Model: `class FarmAgriBomMixin(models.AbstractModel)`
  - _name: `farm.agri.bom.mixin`
  - _description: "Agricultural BOM Utilities for MRP"
  - _inherit: `models.AbstractModel`
  - Relationships:
    - Inherits: `models.AbstractModel`

- **FarmAgriProductionMixin** (Abstract): Provides agricultural production utilities for MRP
  - Odoo Model: `class FarmAgriProductionMixin(models.AbstractModel)`
  - _name: `farm.agri.production.mixin`
  - _description: "Agricultural Production Utilities for MRP"
  - _inherit: `models.AbstractModel`
  - Relationships:
    - Inherits: `models.AbstractModel`

- **MrpBomLineIslAbstract** (Abstract): Abstract base for MRP BOM line ISL models
  - Odoo Model: `class MrpBomLineIslAbstract(models.AbstractModel)`
  - _name: `mrp.bom.line.isl.abstract`
  - _description: "Abstract Base for MRP BOM Line ISL Models"
  - _inherit: `models.AbstractModel`
  - Relationships:
    - Inherits: `models.AbstractModel`

### Supply Chain Utilities
- **StorageManagementMixin** (Abstract): Provides storage management utilities
  - Odoo Model: `class StorageManagementMixin(models.AbstractModel)`
  - _name: `farm.storage.management.mixin`
  - _description: "Storage Management Utilities Mixin"
  - _inherit: `models.AbstractModel`
  - Relationships:
    - Inherits: `models.AbstractModel`

- **QualityManagementMixin** (Abstract): Provides quality management utilities
  - Odoo Model: `class QualityManagementMixin(models.AbstractModel)`
  - _name: `farm.quality.management.mixin`
  - _description: "Quality Management Utilities Mixin"
  - _inherit: `models.AbstractModel`
  - Relationships:
    - Inherits: `models.AbstractModel`

This comprehensive model summary represents the full scope of the farm management system, covering all aspects of agricultural operations from planning and production to processing, marketing, and financial management.
