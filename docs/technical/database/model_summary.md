# 农场管理系统：领域模型全局字典 (Global Domain Model Dictionary - V8.0)
> **自动生成**: 基于 Python 抽象语法树 (AST) 静态解析。
> **涵盖范围**: 全量 101 个微服务模块中的物理表定义与继承关系。

## 1. 核心与主数据域 (Core & Master Data)
### `agri.audit.log` (Defined in `farm_core`)
  - **Class**: `AgriAuditLog`
  - **描述**: Agricultural Audit Log

  - **核心字段**:
    - `model_name` (Char): model_name
    - `record_id` (Integer): record_id
    - `operation` (Char): operation
    - `user_id` (Many2one): res.users
    - `timestamp` (Datetime): timestamp
    - `details` (Text): details
    - `severity` (Selection): severity
    - `ip_address` (Char): ip_address
    - `session_id` (Char): session_id

### `agri.biological.asset` (Defined in `farm_core`)
  - **Class**: `AgriBiologicalAsset`
  - **描述**: Agricultural Biological Asset Standard
  - _inherit_: `agri.biological.asset.mixin, agri.sustainability.mixin, agri.evidence.mixin, mail.thread`
  - **核心字段**:
    - `name` (Char): Standard Identity
    - `active` (Boolean): active
    - `parent_asset_id` (Many2one): agri.biological.asset
    - `sub_asset_ids` (One2many): agri.biological.asset

### `agri.biological.asset` (Defined in `farm_valuation`)
  - **Class**: `BiologicalAssetExtension`
  - **描述**: 
  - _inherit_: `agri.biological.asset`
  - **核心字段**:
    - `current_fair_value` (Float): Current Fair Value
    - `fair_value_date` (Date): Fair Value Date
    - `fair_valuation_ids` (One2many): agri.biological.asset.fair.valuation
    - `ope_integration` (Float): OPE Integration Score

### `agri.biological.growth.curve` (Defined in `farm_core`)
  - **Class**: `AgriBiologicalGrowthCurve`
  - **描述**: Agricultural Biological Growth Curve

  - **核心字段**:
    - `product_id` (Many2one): product.template
    - `age_days` (Integer): Physiological Age (Days)
    - `target_weight` (Float): Target Weight (kg)
    - `daily_feed_rate` (Float): Daily Feeding Rate (%)

### `agri.geospatial.geofence` (Defined in `farm_core`)
  - **Class**: `AgriGeospatialGeofence`
  - **描述**: Agricultural Geofence Standard
  - _inherit_: `mail.thread, mail.activity.mixin, farm.core.gis.utils`
  - **核心字段**:
    - `name` (Char): Fence Name
    - `fence_type` (Selection): fence_type
    - `coordinates` (Text): Polygon Coordinates
    - `active` (Boolean): active
    - `company_id` (Many2one): res.company
    - `target_category` (Selection): target_category
    - `alert_level` (Selection): alert_level

### `agri.industry.data.package` (Defined in `farm_core`)
  - **Class**: `AgriIndustryDataPackage`
  - **描述**: Industry Data Package for One-Click Initialization

  - **核心字段**:
    - `name` (Char): Package Name
    - `code` (Char): Package Code
    - `industry_type` (Selection): industry_type
    - `description` (Text): Description
    - `variety_ids` (One2many): agri.industry.variety
    - `physio_stage_ids` (One2many): agri.industry.physio.stage
    - `uom_conversion_ids` (One2many): farm.industry.uom.conversion
    - `task_template_ids` (One2many): farm.industry.task.template
    - `product_category_ids` (One2many): farm.industry.product.category

### `agri.industry.physio.stage` (Defined in `farm_core`)
  - **Class**: `AgriIndustryPhysioStage`
  - **描述**: Agricultural Physiological Stage

  - **核心字段**:
    - `package_id` (Many2one): agri.industry.data.package
    - `stage_name` (Char): Stage Name
    - `age_days` (Integer): Age (Days)
    - `target_weight` (Float): Target Weight (kg)
    - `daily_feed_rate` (Float): Daily Feed Rate (%)
    - `related_variety` (Char): Related Variety
    - `sequence` (Integer): Sequence
    - `is_harvest_stage` (Boolean): Is Harvest Stage
    - `accumulated_temp_threshold` (Float): Target Accumulated Temp (°C)
    - `description` (Text): Standard Description
    - `active` (Boolean): active

### `agri.industry.variety` (Defined in `farm_core`)
  - **Class**: `AgriIndustryVariety`
  - **描述**: Agricultural Variety Standard
  - _inherit_: `agri.industry.variety.mixin, mail.thread`
  - **核心字段**:
    - `package_id` (Many2one): agri.industry.data.package
    - `product_name` (Char): Product Name
    - `variety_name` (Char): Variety Name
    - `agricultural_type` (Selection): agricultural_type
    - `standard_dose` (Float): Standard Dose
    - `dose_uom_id` (Many2one): uom.uom
    - `n_content` (Float): Nitrogen (N) %
    - `p_content` (Float): Phosphorus (P) %
    - `k_content` (Float): Potassium (K) %
    - `growth_duration` (Integer): Growth Duration (Days)
    - `maturity_age_days` (Integer): Maturity Age (Days)
    - `is_biological_asset` (Boolean): Is Biological Asset
    - `active` (Boolean): active

### `agri.location` (Defined in `farm_core`)
  - **Class**: `AgriLocation`
  - **描述**: Agricultural Physical Location
  - _inherit_: `agri.geospatial.mixin, agri.sustainability.mixin, agri.embedding.mixin, mail.thread`
  - **核心字段**:
    - `name` (Char): Location ID/Name
    - `location_type` (Selection): location_type
    - `parent_id` (Many2one): agri.location
    - `child_ids` (One2many): agri.location
    - `active` (Boolean): active

### `agri.neighborhood.registry` (Defined in `farm_core`)
  - **Class**: `AgriNeighborhoodRegistry`
  - **描述**: Agricultural Neighborhood Registry

  - **核心字段**:
    - `spatial_grid_id` (Char): Grid ID
    - `res_model` (Char): Entity Model
    - `res_id` (Integer): Entity ID
    - `agent_id` (Char): Agent identifier
    - `last_seen` (Datetime): Last Seen
    - `is_active` (Boolean): Is Active

### `agri.soil.analysis` (Defined in `farm_core`)
  - **Class**: `AgriSoilAnalysis`
  - **描述**: Agricultural Soil Analysis Standard
  - _inherit_: `agri.soil.analysis.mixin, agri.sustainability.mixin, agri.evidence.mixin, mail.thread`
  - **核心字段**:
    - `name` (Char): Analysis Identity
    - `analysis_date` (Date): Analysis Date
    - `spatial_grid_id` (Char): Target Grid ID

### `farm.activity` (Defined in `farm_core`)
  - **Class**: `FarmActivity`
  - **描述**: Agricultural Activity
  - _inherit_: `farm.core.creation.method.mixin`
  - **核心字段**:
    - `project_id` (Many2one): project.project
    - `is_agri_activity` (Boolean): is_agri_activity
    - `activity_family` (Selection): activity_family
    - `production_cycle` (Selection): production_cycle
    - `task_sequence_id` (Many2one): ir.sequence

### `farm.biological.asset` (Defined in `farm_core`)
  - **Class**: `BiologicalAsset`
  - **描述**: Biological Asset (Deprecated - Use agri.biological.asset)
  - _inherit_: `agri.biological.asset, mail.thread, mail.activity.mixin, farm.core.creation.method.mixin, farm.core.computed.field.mixin, farm.core.compliance.mixin`
  - **核心字段**:
    - `lot_id` (Many2one): stock.lot
    - `father_id` (Many2one): farm.biological.asset
    - `mother_id` (Many2one): farm.biological.asset
    - `growth_stage` (Selection): growth_stage
    - `is_mature` (Boolean): Is Mature (Operational)
    - `generation` (Selection): generation
    - `quality_grade` (Selection): quality_grade
    - `current_valuation` (Float): Current Valuation
    - `maturity_date` (Date): Maturity Date

### `farm.industry.package.wizard` (Defined in `farm_core`)
  - **Class**: `IndustryPackageWizard`
  - **描述**: Industry Package Application Wizard

  - **核心字段**:
    - `package_id` (Many2one): agri.industry.data.package
    - `confirmation_message` (Char): confirmation_message

### `farm.industry.product.category` (Defined in `farm_core`)
  - **Class**: `IndustryProductCategory`
  - **描述**: Industry Package Product Category Data

  - **核心字段**:
    - `package_id` (Many2one): agri.industry.data.package
    - `name` (Char): Category Name
    - `parent_id` (Many2one): product.category
    - `agricultural_type` (Selection): agricultural_type

### `farm.industry.task.template` (Defined in `farm_core`)
  - **Class**: `IndustryTaskTemplate`
  - **描述**: Industry Package Task Template Data

  - **核心字段**:
    - `package_id` (Many2one): agri.industry.data.package
    - `name` (Char): Template Name
    - `description` (Text): Description
    - `fold` (Boolean): Folded in Kanban
    - `project_id` (Many2one): project.project
    - `expected_duration` (Integer): Expected Duration (Days)
    - `required_equipment` (Char): Required Equipment
    - `required_inputs` (Char): Required Inputs

### `farm.industry.uom.conversion` (Defined in `farm_core`)
  - **Class**: `IndustryUOMConversion`
  - **描述**: Industry Package UOM Conversion Data

  - **核心字段**:
    - `package_id` (Many2one): agri.industry.data.package
    - `from_uom_id` (Many2one): uom.uom
    - `to_uom_id` (Many2one): uom.uom
    - `factor` (Float): Conversion Factor
    - `description` (Text): Description

### `farm.location` (Defined in `farm_agri_science`)
  - **Class**: `FarmLocation`
  - **描述**: 
  - _inherit_: `farm.location`
  - **核心字段**:
    - `grid_resolution` (Selection): grid_resolution
    - `grid_cell_ids` (One2many): agri.geospatial.grid.cell
    - `grid_generated` (Boolean): Grid Layout Generated

### `farm.location` (Defined in `farm_core`)
  - **Class**: `FarmLocation`
  - **描述**: Farm Location & Land Parcel
  - _inherit_: `mail.thread, mail.activity.mixin, stock.location, farm.core.gis.utils, agri.industry.planting.mixin, agri.certification.status.mixin`
  - **核心字段**:
    - `agri_location_id` (Many2one): agri.location
    - `is_land_parcel` (Boolean): Is Land Parcel
    - `land_nature` (Selection): land_nature
    - `land_area` (Float): Area (sqm/mu)
    - `land_area_uom_id` (Many2one): uom.uom
    - `gps_lat` (Float): Latitude
    - `gps_lng` (Float): Longitude
    - `boundary_geojson` (Text): Boundary Coordinates (GeoJSON)
    - `calculated_area_ha` (Float): Calculated Area (Ha)
    - `gis_map_url` (Char): Map Link
    - `soil_type` (Selection): soil_type
    - `slope` (Float): Slope Gradient (%)
    - `aspect` (Selection): aspect
    - `water_source` (Selection): water_source
    - `micro_climate_notes` (Text): Micro-climate Characteristics
    - *... 以及其他 13 个业务字段*

### `farm.location` (Defined in `farm_greenhouse`)
  - **Class**: `FarmLocation`
  - **描述**: 
  - _inherit_: `farm.location`
  - **核心字段**:
    - `is_greenhouse` (Boolean): Is Greenhouse
    - `greenhouse_type` (Selection): greenhouse_type
    - `current_temp` (Float): Internal Temp (°C)
    - `current_humidity` (Float): Humidity (%)
    - `current_co2` (Float): CO2 (ppm)
    - `current_light` (Float): Light Intensity (Lux)
    - `current_ec` (Float): Nutrient EC (mS/cm)
    - `current_ph` (Float): Nutrient pH

### `farm.location` (Defined in `farm_iot`)
  - **Class**: `FarmLocation`
  - **描述**: 
  - _inherit_: `farm.location`
  - **核心字段**:
    - `digital_twin_enabled` (Boolean): Digital Twin Enabled
    - `digital_twin_scene_id` (Many2one): agri.digital.twin.scene

### `farm.task` (Defined in `farm_core`)
  - **Class**: `FarmTask`
  - **描述**: Agricultural Task
  - _inherit_: `farm.core.creation.method.mixin, agri.task.mixin`
  - **核心字段**:
    - `task_id` (Many2one): project.task
    - `land_parcel_id` (Many2one): farm.location
    - `activity_family` (Selection): activity_family
    - `product_id` (Many2one): product.product
    - `variety_id` (Many2one): product.template
    - `planned_start_date` (Date): Planned Start Date
    - `planned_end_date` (Date): Planned End Date
    - `actual_start_date` (Date): Actual Start Date
    - `actual_end_date` (Date): Actual End Date
    - `required_equipment_ids` (Many2many): product.product
    - `required_material_ids` (Many2many): product.product
    - `required_labor_hours` (Float): Required Labor Hours
    - `estimated_cost` (Float): Estimated Cost
    - `actual_cost` (Float): Actual Cost
    - `safety_protocol_followed` (Boolean): Safety Protocol Followed
    - *... 以及其他 2 个业务字段*

### `procurement.allocation.line` (Defined in `farm_multi_farm_procurement`)
  - **Class**: `ProcurementAllocationLine`
  - **描述**: Procurement Allocation Line

  - **核心字段**:
    - `planning_line_id` (Many2one): procurement.planning.line
    - `member_id` (Many2one): cooperative.member
    - `quantity` (Float): Quantity
    - `priority_score` (Float): Priority Score
    - `allocation_date` (Date): Allocation Date

### `product.template` (Defined in `farm_core`)
  - **Class**: `ProductTemplate`
  - **描述**: 
  - _inherit_: `product.template`
  - **核心字段**:
    - `agricultural_type` (Selection): agricultural_type
    - `agri_variety` (Char): Variety/Species
    - `breed_certificate_no` (Char): Breed Registration/Certificate No.
    - `breeder_id` (Many2one): res.partner
    - `genetic_traits` (Text): Genetic Traits
    - `is_transgenic` (Boolean): GMO / Transgenic
    - `best_sowing_month_start` (Selection): best_sowing_month_start
    - `best_sowing_month_end` (Selection): best_sowing_month_end
    - `harvest_season_notes` (Char): Harvest Season Description
    - `born_at` (Datetime): Born At/Started At
    - `dead_at` (Datetime): Dead At/Terminated At
    - `identification_number` (Char): Identification No.
    - `growth_curve_ids` (One2many): agri.biological.growth.curve
    - `lot_properties_definition` (PropertiesDefinition): Lot Properties Definition
    - `n_content` (Float): Nitrogen (N) %
    - *... 以及其他 8 个业务字段*

### `res.company` (Defined in `farm_core`)
  - **Class**: `ResCompany`
  - **描述**: 
  - _inherit_: `res.company`
  - **核心字段**:
    - `properties_definition` (PropertiesDefinition): Farm Properties Definition

### `res.config.settings` (Defined in `farm_core`)
  - **Class**: `ResConfigSettings`
  - **描述**: 
  - _inherit_: `res.config.settings`
  - **核心字段**:
    - `module_farm_field_crops` (Boolean): module_farm_field_crops
    - `module_farm_protected_cultivation` (Boolean): module_farm_protected_cultivation
    - `module_farm_orchard_horticulture` (Boolean): module_farm_orchard_horticulture
    - `module_farm_livestock` (Boolean): module_farm_livestock
    - `module_farm_aquaculture` (Boolean): module_farm_aquaculture
    - `module_farm_medicinal_plants` (Boolean): module_farm_medicinal_plants
    - `module_farm_mushroom` (Boolean): module_farm_mushroom
    - `module_farm_apiculture` (Boolean): module_farm_apiculture
    - `module_farm_agricultural_processing` (Boolean): module_farm_agricultural_processing
    - `module_farm_agritourism` (Boolean): module_farm_agritourism

### `res.partner` (Defined in `farm_core`)
  - **Class**: `ResPartner`
  - **描述**: 
  - _inherit_: `res.partner, agri.sustainability.mixin`


### `stock.location` (Defined in `farm_certification`)
  - **Class**: `FarmLocationCert`
  - **描述**: 
  - _inherit_: `stock.location`
  - **核心字段**:
    - `certification_level` (Selection): certification_level
    - `conversion_start_date` (Date): Conversion Start Date
    - `last_prohibited_substance_date` (Date): Last Prohibited Substance Date
    - `conversion_target_days` (Integer): Target Conversion Days
    - `conversion_progress` (Float): Conversion Progress (%)

### `stock.location` (Defined in `farm_green_monitor`)
  - **Class**: `StockLocation`
  - **描述**: 
  - _inherit_: `stock.location`
  - **核心字段**:
    - `fertilizer_reduction_target` (Float): Fertilizer Reduction Target (%)
    - `pesticide_reduction_target` (Float): Pesticide Reduction Target (%)

### `stock.location` (Defined in `farm_iot`)
  - **Class**: `FarmLocation`
  - **描述**: 
  - _inherit_: `stock.location`
  - **核心字段**:
    - `camera_device_id` (Many2one): iiot.device

### `stock.location` (Defined in `farm_label`)
  - **Class**: `StockLocation`
  - **描述**: 
  - _inherit_: `stock.location`


### `stock.lot` (Defined in `farm_core`)
  - **Class**: `StockLot`
  - **描述**: 
  - _inherit_: `stock.lot, agri.view.mixin, agri.sustainability.mixin, agri.traceability.mixin, agri.geospatial.mixin, agri.nutrient.mixin, agri.certification.status.mixin, agri.evidence.mixin, agri.clearing.mixin`


### `stock.move.line` (Defined in `farm_core`)
  - **Class**: `AgriStockMoveLine`
  - **描述**: 
  - _inherit_: `stock.move.line, agri.nutrient.mixin`


### `stock.move` (Defined in `farm_core`)
  - **Class**: `AgriStockMove`
  - **描述**: 
  - _inherit_: `stock.move, agri.nutrient.mixin, agri.sustainability.mixin`


## 2. 生产与作业流域 (Operations & Interventions)
### `agri.intervention.template.input` (Defined in `farm_planning`)
  - **Class**: `AgriInterventionTemplateInput`
  - **描述**: Intervention Template Input

  - **核心字段**:
    - `template_id` (Many2one): agri.intervention.template
    - `product_id` (Many2one): product.product
    - `qty_per_unit` (Float): Qty per Area/Unit

### `agri.intervention.template.input` (Defined in `farm_planning`)
  - **Class**: `AgriInterventionTemplateInput`
  - **描述**: Template Input Requirement

  - **核心字段**:
    - `template_id` (Many2one): agri.intervention.template
    - `product_id` (Many2one): product.product
    - `quantity` (Float): Quantity per Unit Area

### `agri.intervention.template` (Defined in `farm_planning`)
  - **Class**: `AgriInterventionTemplate`
  - **描述**: Agricultural Intervention Template

  - **核心字段**:
    - `name` (Char): Operation Name
    - `intervention_type` (Selection): intervention_type
    - `input_ids` (One2many): agri.intervention.template.input
    - `estimated_labor_hours` (Float): Estimated Labor (Hours)

### `agri.intervention.template` (Defined in `farm_planning`)
  - **Class**: `AgriInterventionTemplate`
  - **描述**: Intervention Template

  - **核心字段**:
    - `name` (Char): Operation Name
    - `intervention_type` (Selection): intervention_type
    - `labor_hours_per_unit` (Float): Labor Hours per Hectare/Group
    - `input_ids` (One2many): agri.intervention.template.input

### `agri.intervention` (Defined in `farm_operation`)
  - **Class**: `AgriIntervention`
  - **描述**: Agricultural Intervention (ISL Layer)
  - _inherit_: `mail.thread, mail.activity.mixin, agri.intervention.mixin`
  - **核心字段**:
    - `production_id` (Many2one): mrp.production

### `agricultural.campaign` (Defined in `farm_operation`)
  - **Class**: `AgriculturalCampaign`
  - **描述**: 
  - _inherit_: `agricultural.campaign`


### `agricultural.campaign` (Defined in `farm_operation`)
  - **Class**: `AgriculturalCampaign`
  - **描述**: Agricultural Production Season
  - _inherit_: `farm.agricultural.campaign.base`
  - **核心字段**:
    - `project_task_ids` (One2many): project.task

### `farm.agricultural.bom.line` (Defined in `farm_operation`)
  - **Class**: `FarmAgricultulturalBomLine`
  - **描述**: Agricultural BOM Line (ISL Layer)
  - _inherit_: `agri.bom.line.mixin`
  - **核心字段**:
    - `bom_line_id` (Many2one): mrp.bom.line

### `farm.agricultural.bom` (Defined in `farm_operation`)
  - **Class**: `FarmAgriculturalBom`
  - **描述**: Agricultural BOM (ISL Layer)
  - _inherit_: `agri.bom.mixin`
  - **核心字段**:
    - `bom_id` (Many2one): mrp.bom

### `farm.agricultural.campaign` (Defined in `farm_esg_sustainability`)
  - **Class**: `AgriculturalCampaign`
  - **描述**: 
  - _inherit_: `farm.agricultural.campaign`
  - **核心字段**:
    - `task_ids` (One2many): project.task
    - `total_n` (Float): Total Nitrogen (kg)
    - `total_p` (Float): Total Phosphorus (kg)
    - `total_k` (Float): Total Potassium (kg)
    - `n_reduction_rate` (Float): N Reduction %
    - `p_reduction_rate` (Float): P Reduction %
    - `k_reduction_rate` (Float): K Reduction %

### `farm.agricultural.campaign` (Defined in `farm_operation`)
  - **Class**: `FarmAgriculturalCampaign`
  - **描述**: Agricultural Campaign (ISL Layer)
  - _inherit_: `farm.agricultural.campaign.mixin`
  - **核心字段**:
    - `isl_campaign_code` (Char): ISL Campaign Code
    - `farm_location_id` (Many2one): farm.location

### `farm.agritourism.operation` (Defined in `farm_agritourism`)
  - **Class**: `FarmAgritourismOperation`
  - **描述**: Farm Agritourism Operation
  - _inherit_: `project.task`
  - **核心字段**:
    - `activity_type` (Selection): activity_type
    - `activity_code` (Char): Activity Code
    - `visitor_count` (Integer): Planned Visitor Count
    - `actual_visitor_count` (Integer): Actual Visitor Count
    - `visitor_age_distribution` (Text): Visitor Age Distribution
    - `visitor_special_needs` (Text): Special Needs/Requirements
    - `resource_usage_ids` (One2many): farm.resource.usage
    - `activity_date` (Date): Activity Date
    - `activity_start_time` (Float): Start Time
    - `activity_end_time` (Float): End Time
    - `requires_reservation` (Boolean): Requires Reservation
    - `safety_measures` (Text): Safety Measures
    - `emergency_contact` (Char): Emergency Contact
    - `insurance_coverage` (Char): Insurance Coverage Information
    - `risk_assessment_completed` (Boolean): Risk Assessment Completed
    - *... 以及其他 14 个业务字段*

### `farm.industry.operation` (Defined in `farm_processing`)
  - **Class**: `FarmIndustryOperation`
  - **描述**: Industry-Specific Process Operation (ISL Layer)

  - **核心字段**:
    - `operation_id` (Many2one): mrp.routing.workcenter
    - `technical_manual` (Html): Technical SOP
    - `param_monitoring_required` (Boolean): Monitor Critical Parameters
    - `target_value` (Float): Target Value
    - `tolerance_range` (Float): Tolerance (+/-)

### `farm.orchard.operation` (Defined in `farm_orchard_horticulture`)
  - **Class**: `OrchardOperation`
  - **描述**: Orchard Manual Operation
  - _inherit_: `mail.thread, mail.activity.mixin, agri.quality.gate.mixin`
  - **核心字段**:
    - `operation_id` (Many2one): project.task
    - `tree_id` (Many2one): stock.lot
    - `pruning_type` (Selection): pruning_type

### `mrp.bom.line` (Defined in `farm_operation`)
  - **Class**: `MrpBomLine`
  - **描述**: 
  - _inherit_: `mrp.bom.line, agri.bom.line.mixin, agri.nutrient.mixin`


### `mrp.bom` (Defined in `farm_operation`)
  - **Class**: `MrpBom`
  - **描述**: 
  - _inherit_: `mrp.bom, agri.bom.mixin, agri.view.mixin, agri.nutrient.mixin, agri.sustainability.mixin`


### `mrp.bom` (Defined in `farm_operation`)
  - **Class**: `MrpBom`
  - **描述**: 
  - _inherit_: `mrp.bom`


### `mrp.production` (Defined in `farm_operation`)
  - **Class**: `AgriIntervention`
  - **描述**: Agricultural Intervention (De-industrialized View)
  - _inherit_: `mrp.production, agri.intervention.mixin, agri.sustainability.mixin, agri.geospatial.mixin, farm.agri.science.mixin, agri.nutrient.mixin, agri.actuator.mixin, agri.evidence.mixin, agri.clearing.mixin`
  - **核心字段**:
    - `daily_temp_max` (Float): Daily Max Temperature
    - `daily_temp_min` (Float): Daily Min Temperature

### `mrp.production` (Defined in `farm_operation`)
  - **Class**: `MrpProduction`
  - **描述**: 
  - _inherit_: `mrp.production, agri.sustainability.mixin, agri.weather.sensitive.mixin, agri.agent.instruction.mixin`


### `mrp.production` (Defined in `farm_operation`)
  - **Class**: `MrpProduction`
  - **描述**: 
  - _inherit_: `mrp.production`


### `project.task` (Defined in `farm_operation`)
  - **Class**: `ProjectTask`
  - **描述**: Multi-Industry Activity Production
  - _inherit_: `project.task`
  - **核心字段**:
    - `industry_type` (Selection): industry_type
    - `campaign_id` (Many2one): farm.agricultural.campaign
    - `land_parcel_id` (Many2one): farm.location
    - `gps_lat` (Float): gps_lat
    - `gps_lng` (Float): gps_lng
    - `biological_lot_id` (Many2one): stock.lot
    - `support_id` (Many2one): product.product
    - `size_value` (Float): Production Size
    - `sale_order_id` (Many2one): sale.order
    - `intervention_ids` (One2many): mrp.production
    - `total_n` (Float): Total Nitrogen (kg)
    - `total_p` (Float): Total Phosphorus (kg)
    - `total_k` (Float): Total Potassium (kg)
    - `n_density` (Float): N Density (kg/mu)
    - `p_density` (Float): P Density (kg/mu)
    - *... 以及其他 3 个业务字段*

### `sale.order` (Defined in `farm_operation`)
  - **Class**: `SaleOrder`
  - **描述**: 
  - _inherit_: `sale.order`


### `stock.move` (Defined in `farm_operation`)
  - **Class**: `StockMove`
  - **描述**: 
  - _inherit_: `stock.move`
  - **核心字段**:
    - `quality_grade` (Selection): quality_grade
    - `agri_loss_reason` (Selection): agri_loss_reason

## 3. 行业标准代理层 (Industry Standard Layer - ISL)
### `agri.isl.extension` (Defined in `farm_isl`)
  - **Class**: `AgriISLIndustryExtension`
  - **描述**: Agri ISL Extension

  - **核心字段**:
    - `name` (Char): Extension Name
    - `industry_type` (Selection): industry_type
    - `model_name` (Char): Model Name
    - `extension_fields` (Text): Extension Fields (JSON)
    - `extension_methods` (Text): Extension Methods
    - `active` (Boolean): Active
    - `description` (Text): Description

### `agri.isl.industry.planting` (Defined in `farm_isl`)
  - **Class**: `ISLIndustryPlanting`
  - **描述**: ISL Planting Specification
  - _inherit_: `agri.industry.planting.mixin`
  - **核心字段**:
    - `name` (Char): Spec Name
    - `standard_id` (Char): Global Standard ID
    - `is_organic_compatible` (Boolean): Organic Compatible
    - `min_buffer_zone_meters` (Float): Min Buffer Zone (m)

### `agri.isl.migration.utility` (Defined in `farm_isl`)
  - **Class**: `AgriISLMigrationUtility`
  - **描述**: Agri ISL Data Migration Utility

  - **核心字段**:
    - `industry_type` (Selection): industry_type
    - `model_to_migrate` (Selection): model_to_migrate
    - `confirmation` (Boolean): Confirm Migration

### `agri.mrp.bom` (Defined in `farm_isl`)
  - **Class**: `AgriMRPBom`
  - **描述**: Agri ISL MRP Bill of Materials
  - _inherit_: `agri.manufacturing.mixin`
  - **核心字段**:
    - `mrp_bom_id` (Many2one): mrp.bom
    - `allergen_control` (Boolean): Allergen Control
    - `active_ingredient` (Char): Active Ingredient
    - `safety_coefficient` (Float): Safety Coefficient
    - `recipe_validation` (Html): Recipe Validation
    - `ingredient_compliance` (Text): Ingredient Compliance

### `agri.mrp.production` (Defined in `farm_isl`)
  - **Class**: `AgriMRPProduction`
  - **描述**: Agri ISL MRP Production Order
  - _inherit_: `agri.manufacturing.mixin`
  - **核心字段**:
    - `mrp_production_id` (Many2one): mrp.production
    - `haccp_plan` (Html): HACCP Plan
    - `gmp_compliance` (Boolean): GMP Compliance
    - `safety_procedures` (Html): Safety Procedures
    - `quality_gate_checks` (Text): Quality Gate Checks

### `agri.mrp.workcenter` (Defined in `farm_isl`)
  - **Class**: `AgriMRPWorkcenter`
  - **描述**: Agri ISL MRP Work Center
  - _inherit_: `agri.manufacturing.mixin`
  - **核心字段**:
    - `workcenter_id` (Many2one): mrp.workcenter
    - `cip_required` (Boolean): CIP Required
    - `explosion_proof` (Boolean): Explosion Proof
    - `clean_room_class` (Char): Clean Room Class
    - `capacity_uom` (Char): Capacity Unit of Measure
    - `efficiency_factor` (Float): Efficiency Factor

### `agri.mrp.workorder` (Defined in `farm_isl`)
  - **Class**: `AgriMRPWorkorder`
  - **描述**: Agri ISL MRP Work Order
  - _inherit_: `agri.manufacturing.mixin`
  - **核心字段**:
    - `workorder_id` (Many2one): mrp.workorder
    - `operator_certification` (Html): Operator Certification
    - `equipment_validation` (Html): Equipment Validation
    - `in_process_inspection` (Html): In-Process Inspection
    - `batch_record` (Html): Batch Record

### `agri.product.template` (Defined in `farm_isl`)
  - **Class**: `AgriProductTemplate`
  - **描述**: Agri ISL Product Template
  - _inherit_: `agri.product.mixin`
  - **核心字段**:
    - `product_template_id` (Many2one): product.template
    - `allergen_information` (Html): Allergen Information
    - `pharmacological_class` (Char): Pharmacological Class
    - `safety_data_sheet` (Binary): Safety Data Sheet
    - `safety_data_sheet_name` (Char): SDS Name
    - `hazard_class` (Char): Hazard Class
    - `regulatory_class` (Char): Regulatory Class

### `agri.purchase.order` (Defined in `farm_isl`)
  - **Class**: `AgriPurchaseOrder`
  - **描述**: Agri ISL Purchase Order
  - _inherit_: `agri.sales.purchase.mixin`
  - **核心字段**:
    - `purchase_order_id` (Many2one): purchase.order
    - `supplier_certification` (Char): Supplier Certification
    - `incoming_inspection` (Html): Incoming Inspection
    - `certificate_verification` (Html): Certificate Verification
    - `quality_agreement` (Html): Quality Agreement

### `agri.sale.order` (Defined in `farm_isl`)
  - **Class**: `AgriSaleOrder`
  - **描述**: Agri ISL Sale Order
  - _inherit_: `agri.sales.purchase.mixin`
  - **核心字段**:
    - `sale_order_id` (Many2one): sale.order
    - `delivery_compliance` (Html): Delivery Compliance
    - `traceability_requirements` (Html): Traceability Requirements
    - `shipping_conditions` (Html): Shipping Conditions
    - `certificate_requirements` (Html): Certificate Requirements
    - `temperature_monitoring` (Boolean): Temperature Monitoring

### `agri.stock.lot` (Defined in `farm_isl`)
  - **Class**: `AgriStockLot`
  - **描述**: Agri ISL Stock Lot
  - _inherit_: `agri.inventory.mixin`
  - **核心字段**:
    - `stock_lot_id` (Many2one): stock.lot
    - `harvest_date` (Date): Harvest Date
    - `kill_date` (Date): Kill Date
    - `sterility_date` (Date): Sterility Date
    - `certificate_of_analysis` (Binary): Certificate of Analysis
    - `certificate_of_analysis_name` (Char): COA Name
    - `stability_data` (Html): Stability Data
    - `storage_conditions` (Html): Storage Conditions

### `agri.stock.picking` (Defined in `farm_isl`)
  - **Class**: `AgriStockPicking`
  - **描述**: Agri ISL Stock Picking
  - _inherit_: `agri.inventory.mixin`
  - **核心字段**:
    - `picking_id` (Many2one): stock.picking
    - `chain_of_custody` (Html): Chain of Custody
    - `temperature_log` (Html): Temperature Log
    - `humidity_log` (Html): Humidity Log
    - `security_seal` (Char): Security Seal
    - `compliance_verification` (Html): Compliance Verification

### `farm.isl.extension` (Defined in `farm_isl`)
  - **Class**: `ISLIndustryExtension`
  - **描述**: Farm ISL Extension (Deprecated - Use agri.isl.extension)
  - _inherit_: `agri.isl.extension`


### `agri.isl.mrp.bom` (Defined in `farm_isl`)
  - **Class**: `AgriMRPBom`
  - **描述**: Farm ISL MRP Bill of Materials
  - _inherit_: `farm.manufacturing.mixin`
  - **核心字段**:
    - `mrp_bom_id` (Many2one): mrp.bom
    - `allergen_control` (Boolean): Allergen Control
    - `active_ingredient` (Char): Active Ingredient
    - `safety_coefficient` (Float): Safety Coefficient
    - `recipe_validation` (Html): Recipe Validation
    - `ingredient_compliance` (Text): Ingredient Compliance

### `agri.isl.mrp.production` (Defined in `farm_isl`)
  - **Class**: `AgriMRPProduction`
  - **描述**: Farm ISL MRP Production Order
  - _inherit_: `farm.manufacturing.mixin`
  - **核心字段**:
    - `mrp_production_id` (Many2one): mrp.production
    - `haccp_plan` (Html): HACCP Plan
    - `gmp_compliance` (Boolean): GMP Compliance
    - `safety_procedures` (Html): Safety Procedures
    - `quality_gate_checks` (Text): Quality Gate Checks

### `agri.isl.mrp.workcenter` (Defined in `farm_isl`)
  - **Class**: `AgriMRPWorkcenter`
  - **描述**: Farm ISL MRP Work Center
  - _inherit_: `farm.manufacturing.mixin`
  - **核心字段**:
    - `workcenter_id` (Many2one): mrp.workcenter
    - `cip_required` (Boolean): CIP Required
    - `explosion_proof` (Boolean): Explosion Proof
    - `clean_room_class` (Char): Clean Room Class
    - `capacity_uom` (Char): Capacity Unit of Measure
    - `efficiency_factor` (Float): Efficiency Factor

### `agri.isl.mrp.workorder` (Defined in `farm_isl`)
  - **Class**: `AgriMRPWorkorder`
  - **描述**: Farm ISL MRP Work Order
  - _inherit_: `farm.manufacturing.mixin`
  - **核心字段**:
    - `workorder_id` (Many2one): mrp.workorder
    - `operator_certification` (Html): Operator Certification
    - `equipment_validation` (Html): Equipment Validation
    - `in_process_inspection` (Html): In-Process Inspection
    - `batch_record` (Html): Batch Record

### `agri.isl.product.template` (Defined in `farm_isl`)
  - **Class**: `AgriProductTemplate`
  - **描述**: Farm ISL Product Template
  - _inherit_: `farm.product.mixin`
  - **核心字段**:
    - `product_template_id` (Many2one): product.template
    - `allergen_information` (Html): Allergen Information
    - `pharmacological_class` (Char): Pharmacological Class
    - `safety_data_sheet` (Binary): Safety Data Sheet
    - `safety_data_sheet_name` (Char): SDS Name
    - `hazard_class` (Char): Hazard Class
    - `regulatory_class` (Char): Regulatory Class

### `agri.isl.purchase.order` (Defined in `farm_isl`)
  - **Class**: `FarmPurchaseOrder`
  - **描述**: Farm ISL Purchase Order
  - _inherit_: `farm.sales.purchase.mixin`
  - **核心字段**:
    - `purchase_order_id` (Many2one): purchase.order
    - `supplier_certification` (Char): Supplier Certification
    - `incoming_inspection` (Html): Incoming Inspection
    - `certificate_verification` (Html): Certificate Verification
    - `quality_agreement` (Html): Quality Agreement

### `agri.isl.sale.order` (Defined in `farm_isl`)
  - **Class**: `FarmSaleOrder`
  - **描述**: Farm ISL Sale Order
  - _inherit_: `farm.sales.purchase.mixin`
  - **核心字段**:
    - `sale_order_id` (Many2one): sale.order
    - `delivery_compliance` (Html): Delivery Compliance
    - `traceability_requirements` (Html): Traceability Requirements
    - `shipping_conditions` (Html): Shipping Conditions
    - `certificate_requirements` (Html): Certificate Requirements
    - `temperature_monitoring` (Boolean): Temperature Monitoring

### `agri.isl.stock.lot` (Defined in `farm_isl`)
  - **Class**: `FarmStockLot`
  - **描述**: Farm ISL Stock Lot
  - _inherit_: `farm.inventory.mixin`
  - **核心字段**:
    - `stock_lot_id` (Many2one): stock.lot
    - `harvest_date` (Date): Harvest Date
    - `kill_date` (Date): Kill Date
    - `sterility_date` (Date): Sterility Date
    - `certificate_of_analysis` (Binary): Certificate of Analysis
    - `certificate_of_analysis_name` (Char): COA Name
    - `stability_data` (Html): Stability Data
    - `storage_conditions` (Html): Storage Conditions

### `agri.isl.stock.picking` (Defined in `farm_isl`)
  - **Class**: `FarmStockPicking`
  - **描述**: Farm ISL Stock Picking
  - _inherit_: `farm.inventory.mixin`
  - **核心字段**:
    - `picking_id` (Many2one): stock.picking
    - `chain_of_custody` (Html): Chain of Custody
    - `temperature_log` (Html): Temperature Log
    - `humidity_log` (Html): Humidity Log
    - `security_seal` (Char): Security Seal
    - `compliance_verification` (Html): Compliance Verification

### `isl.migration.utility` (Defined in `farm_isl`)
  - **Class**: `ISLMigrationUtility`
  - **描述**: ISL Data Migration Utility (Deprecated - Use agri.isl.migration.utility)
  - _inherit_: `agri.isl.migration.utility`


### `stock.lot` (Defined in `farm_isl`)
  - **Class**: `StockLot`
  - **描述**: 
  - _inherit_: `stock.lot`


### `stock.move` (Defined in `farm_isl`)
  - **Class**: `StockMove`
  - **描述**: 
  - _inherit_: `stock.move`


## 4. 智能决策与视觉感知域 (AI & Perception)
### `agri.a2a.negotiation` (Defined in `farm_ai_robotics_bridge`)
  - **Class**: `A2ANegotiationMessageExtension`
  - **描述**: 
  - _inherit_: `agri.a2a.negotiation`


### `agri.ai.agent.workflow.step` (Defined in `farm_ai_agent`)
  - **Class**: `AgriAiAgentWorkflowStep`
  - **描述**: AI Agent Workflow Step

  - **核心字段**:
    - `name` (Char): Step Name
    - `workflow_id` (Many2one): agri.ai.agent.workflow
    - `sequence` (Integer): Sequence
    - `step_type` (Selection): step_type
    - `coordination_layer_id` (Many2one): agri.ai.coordination.layer
    - `ai_agent_id` (Many2one): agri.ai.agent
    - `ai_vision_service_id` (Many2one): agri.ai.pest.disease.detection
    - `ai_financial_service_id` (Many2one): farm.crop.yield.insurance
    - `step_config` (Text): Step Configuration (JSON)
    - `condition` (Text): Execution Condition (Python Expression)
    - `action_code` (Text): Action Code (Python) for Custom Steps

### `agri.ai.agent.workflow` (Defined in `farm_ai_agent`)
  - **Class**: `AgriAiAgentWorkflow`
  - **描述**: AI Agent Workflow for Complex Decision Processes
  - _inherit_: `mail.thread, mail.activity.mixin`
  - **核心字段**:
    - `name` (Char): Workflow Name
    - `description` (Text): Workflow Description
    - `active` (Boolean): Active
    - `workflow_definition` (Text): Workflow Definition (JSON)
    - `coordination_layer_id` (Many2one): agri.ai.coordination.layer
    - `trigger_conditions` (Text): Trigger Conditions (JSON)
    - `step_ids` (One2many): agri.ai.agent.workflow.step
    - `execution_count` (Integer): Execution Count
    - `last_execution` (Datetime): Last Execution
    - `success_rate` (Float): Success Rate

### `agri.ai.agent` (Defined in `farm_ai_decision`)
  - **Class**: `AgriAiAgent`
  - **描述**: AI Agent for Intelligent Decision Support
  - _inherit_: `mail.thread, mail.activity.mixin, agri.ai.base.mixin`
  - **核心字段**:
    - `base_id` (Many2one): agri.ai.decision.base
    - `agent_type` (Selection): agent_type
    - `industry_id` (Char): industry_id
    - `model_architecture` (Selection): model_architecture
    - `training_data_source` (Char): Training Data Source
    - `training_accuracy` (Float): Training Accuracy
    - `last_trained` (Datetime): Last Trained
    - `training_samples` (Integer): Training Samples Count
    - `parameters` (Text): Model Parameters
    - `precision_score` (Float): Precision Score
    - `recall_score` (Float): Recall Score
    - `f1_score` (Float): F1 Score
    - `mse_score` (Float): MSE Score
    - `input_schema` (Text): Input Schema
    - `output_schema` (Text): Output Schema
    - *... 以及其他 6 个业务字段*

### `agri.ai.coordination.layer` (Defined in `farm_ai_agent`)
  - **Class**: `AgriAiCoordinationLayer`
  - **描述**: AI Coordination Layer for Agricultural Intelligence
  - _inherit_: `mail.thread, mail.activity.mixin`
  - **核心字段**:
    - `name` (Char): Coordination Name
    - `description` (Text): Description
    - `active` (Boolean): Active
    - `coordination_type` (Selection): coordination_type
    - `ai_decision_ids` (Many2many): agri.ai.agent
    - `ai_vision_ids` (Many2many): agri.ai.pest.disease.detection
    - `ai_financial_ids` (Many2many): farm.crop.yield.insurance
    - `coordination_config` (Text): Coordination Configuration (JSON)
    - `execution_context` (Text): Execution Context (JSON)
    - `result_aggregation_method` (Selection): result_aggregation_method
    - `last_execution` (Datetime): Last Execution
    - `execution_count` (Integer): Execution Count
    - `performance_metrics` (Text): Performance Metrics (JSON)
    - `industry_type` (Selection): industry_type
    - `uses_isl_data` (Boolean): Uses ISL Data
    - *... 以及其他 1 个业务字段*

### `agri.ai.crop.growth.prediction` (Defined in `farm_ai_decision`)
  - **Class**: `AgriAiCropGrowthPrediction`
  - **描述**: AI Crop Growth Prediction
  - _inherit_: `agri.ai.decision.base`
  - **核心字段**:
    - `product_id` (Many2one): product.template
    - `land_location_id` (Many2one): farm.location
    - `planting_date` (Date): Planting Date
    - `expected_harvest_date` (Date): Expected Harvest Date
    - `current_growth_stage` (Char): Current Growth Stage
    - `predicted_yield` (Float): Predicted Yield
    - `growth_deviation` (Float): Growth Deviation
    - `environmental_factors` (Text): Environmental Factors Analysis
    - `growth_curve_data` (Text): Growth Curve Data
    - `growth_recommendation` (Html): Growth Optimization Recommendation

### `agri.ai.decision.context` (Defined in `farm_ai_agent`)
  - **Class**: `AgriAIDecisionContext`
  - **描述**: AI Decision Context for Agricultural Intelligence
  - _inherit_: `mail.thread, mail.activity.mixin`
  - **核心字段**:
    - `name` (Char): Context Name
    - `description` (Text): Context Description
    - `context_data` (Text): Context Data (JSON)
    - `decision_engine_id` (Many2one): agri.ai.decision.engine
    - `coordination_layer_id` (Many2one): agri.ai.coordination.layer
    - `location_id` (Many2one): res.partner
    - `crop_type` (Many2one): product.template
    - `season` (Char): Season
    - `date_from` (Date): From Date
    - `date_to` (Date): To Date
    - `weather_conditions` (Text): Weather Conditions (JSON)
    - `soil_conditions` (Text): Soil Conditions (JSON)
    - `pest_conditions` (Text): Pest/Disease Conditions (JSON)
    - `industry_type` (Selection): industry_type
    - `uses_isl_data` (Boolean): Uses ISL Data

### `agri.ai.decision.engine` (Defined in `farm_ai_agent`)
  - **Class**: `AgriAIDecisionEngine`
  - **描述**: AI Decision Engine for Agricultural Intelligence
  - _inherit_: `mail.thread, mail.activity.mixin, agri.ai.base.mixin`
  - **核心字段**:
    - `name` (Char): Engine Name
    - `description` (Text): Description
    - `active` (Boolean): Active
    - `decision_type` (Selection): decision_type
    - `vision_service_ids` (Many2many): agri.ai.pest.disease.detection
    - `decision_service_ids` (Many2many): agri.ai.agent
    - `financial_service_ids` (Many2many): farm.crop.yield.insurance
    - `decision_config` (Text): Decision Configuration (JSON)
    - `decision_weights` (Text): Model Weights Configuration (JSON)
    - `decision_logic` (Text): Decision Logic (Python Code)
    - `execution_context` (Text): Execution Context (JSON)
    - `input_data` (Text): Input Data (JSON)
    - `output_format` (Selection): output_format
    - `workflow_enabled` (Boolean): Enable Workflow
    - `coordination_layer_id` (Many2one): agri.ai.coordination.layer
    - *... 以及其他 11 个业务字段*

### `agri.ai.decision.rule` (Defined in `farm_ai_agent`)
  - **Class**: `AgriAIDecisionRule`
  - **描述**: AI Decision Rule for Agricultural Intelligence
  - _inherit_: `mail.thread, mail.activity.mixin`
  - **核心字段**:
    - `name` (Char): Rule Name
    - `description` (Text): Rule Description
    - `active` (Boolean): Active
    - `decision_type` (Selection): decision_type
    - `condition_expression` (Text): Condition Expression (Python)
    - `action_code` (Text): Action Code (Python)
    - `priority` (Integer): Priority
    - `sequence` (Integer): Sequence
    - `industry_type` (Selection): industry_type
    - `applicable_to_all_industries` (Boolean): Applicable to All Industries

### `agri.ai.decision.workflow.step` (Defined in `farm_ai_agent`)
  - **Class**: `AgriAIDecisionWorkflowStep`
  - **描述**: AI Decision Workflow Step

  - **核心字段**:
    - `name` (Char): Step Name
    - `workflow_id` (Many2one): agri.ai.decision.workflow
    - `sequence` (Integer): Sequence
    - `step_type` (Selection): step_type
    - `decision_engine_id` (Many2one): agri.ai.decision.engine
    - `coordination_layer_id` (Many2one): agri.ai.coordination.layer
    - `step_config` (Text): Step Configuration (JSON)
    - `condition` (Text): Execution Condition (Python Expression)
    - `action_code` (Text): Action Code (Python) for Custom Steps

### `agri.ai.decision.workflow` (Defined in `farm_ai_agent`)
  - **Class**: `AgriAIDecisionWorkflow`
  - **描述**: AI Decision Workflow for Agricultural Intelligence
  - _inherit_: `mail.thread, mail.activity.mixin`
  - **核心字段**:
    - `name` (Char): Workflow Name
    - `description` (Text): Workflow Description
    - `active` (Boolean): Active
    - `workflow_definition` (Text): Workflow Definition (JSON)
    - `decision_engine_id` (Many2one): agri.ai.decision.engine
    - `trigger_conditions` (Text): Trigger Conditions (JSON)
    - `step_ids` (One2many): agri.ai.decision.workflow.step
    - `execution_count` (Integer): Execution Count
    - `last_execution` (Datetime): Last Execution
    - `success_rate` (Float): Success Rate

### `agri.ai.fertilization.decision` (Defined in `farm_ai_decision`)
  - **Class**: `AgriAiFertilizationDecision`
  - **描述**: AI Fertilization Decision
  - _inherit_: `agri.ai.decision.base`
  - **核心字段**:
    - `land_location_id` (Many2one): farm.location
    - `product_id` (Many2one): product.template
    - `soil_nitrogen` (Float): Soil Nitrogen (ppm)
    - `soil_phosphorus` (Float): Soil Phosphorus (ppm)
    - `soil_potassium` (Float): Soil Potassium (ppm)
    - `soil_ph` (Float): Soil pH
    - `crop_growth_stage` (Char): Crop Growth Stage
    - `recommended_n` (Float): Recommended N (kg/ha)
    - `recommended_p` (Float): Recommended P (kg/ha)
    - `recommended_k` (Float): Recommended K (kg/ha)
    - `fertilizer_recommendation` (Html): Fertilizer Recommendation
    - `application_timing` (Char): Application Timing
    - `nutrient_deficiency_analysis` (Html): Nutrient Deficiency Analysis

### `agri.ai.harvest.timing` (Defined in `farm_ai_decision`)
  - **Class**: `AgriAiHarvestTiming`
  - **描述**: AI Harvest Timing
  - _inherit_: `agri.ai.decision.base`
  - **核心字段**:
    - `product_id` (Many2one): product.template
    - `land_location_id` (Many2one): farm.location
    - `planting_date` (Date): Planting Date
    - `expected_harvest_date` (Date): Expected Harvest Date
    - `optimal_harvest_date` (Date): Optimal Harvest Date
    - `quality_metrics` (Text): Quality Metrics
    - `weather_impact` (Text): Weather Impact Assessment
    - `market_price_factor` (Float): Market Price Factor
    - `harvest_recommendation` (Html): Harvest Recommendation
    - `quality_score` (Float): Quality Score
    - `yield_impact` (Float): Yield Impact (%)

### `agri.ai.health.monitoring` (Defined in `farm_ai_decision`)
  - **Class**: `AgriAiHealthMonitoring`
  - **描述**: AI Health and Welfare Monitoring
  - _inherit_: `agri.ai.decision.base`
  - **核心字段**:
    - `animal_id` (Char): Animal ID
    - `species_type` (Selection): species_type
    - `behavioral_metrics` (Text): Behavioral Metrics
    - `health_indicators` (Text): Health Indicators
    - `welfare_score` (Float): Welfare Score (0-100)
    - `health_risk_level` (Selection): health_risk_level
    - `monitoring_alert` (Html): Monitoring Alert
    - `health_recommendation` (Html): Health Recommendation
    - `welfare_improvements` (Html): Welfare Improvements

### `agri.ai.irrigation.decision` (Defined in `farm_ai_decision`)
  - **Class**: `AgriAiIrrigationDecision`
  - **描述**: AI Irrigation Decision
  - _inherit_: `agri.ai.decision.base`
  - **核心字段**:
    - `land_location_id` (Many2one): farm.location
    - `product_id` (Many2one): product.template
    - `current_soil_moisture` (Float): Current Soil Moisture (%)
    - `weather_forecast` (Text): Weather Forecast Data
    - `irrigation_system` (Char): Irrigation System Type
    - `irrigation_method` (Selection): irrigation_method
    - `recommended_water_amount` (Float): Recommended Water Amount (mm)
    - `recommended_irrigation_time` (Datetime): Recommended Time
    - `evapotranspiration_rate` (Float): Evapotranspiration Rate (mm/day)
    - `irrigation_efficiency` (Float): Irrigation Efficiency (%)
    - `irrigation_advice` (Html): Irrigation Advice
    - `soil_analysis` (Text): Soil Analysis

### `agri.ai.llm.configuration` (Defined in `farm_ai_llm_integration`)
  - **Class**: `AgriAiLlmConfiguration`
  - **描述**: LLM Provider Configuration
  - _inherit_: `mail.thread, mail.activity.mixin`
  - **核心字段**:
    - `ai_config_id` (Many2one): agri.ai.configuration
    - `provider` (Selection): provider
    - `rate_limit_requests` (Integer): Rate Limit (requests/min)
    - `rate_limit_period` (Integer): Rate Limit Period (seconds)
    - `use_agricultural_context` (Boolean): Use Agricultural Context
    - `temperature` (Float): Temperature
    - `max_tokens` (Integer): Max Tokens
    - `timeout` (Integer): Timeout (seconds)
    - `application_type` (Selection): application_type

### `agri.ai.llm.service` (Defined in `farm_ai_llm_integration`)
  - **Class**: `AgriAiLlmService`
  - **描述**: LLM Service Interface
  - _inherit_: `mail.thread, mail.activity.mixin`
  - **核心字段**:
    - `name` (Char): Service Name
    - `config_id` (Many2one): agri.ai.llm.configuration
    - `last_call_time` (Datetime): Last Call Time
    - `call_count` (Integer): Call Count
    - `error_count` (Integer): Error Count

### `agri.ai.market.prediction` (Defined in `farm_ai_decision`)
  - **Class**: `AgriAiMarketPrediction`
  - **描述**: AI Market Prediction
  - _inherit_: `agri.ai.decision.base`
  - **核心字段**:
    - `prediction_type` (Selection): prediction_type
    - `product_id` (Many2one): product.template
    - `current_price` (Float): Current Market Price
    - `predicted_price_7d` (Float): Predicted Price (7 days)
    - `predicted_price_30d` (Float): Predicted Price (30 days)
    - `predicted_price_90d` (Float): Predicted Price (90 days)
    - `price_trend` (Selection): price_trend
    - `futures_price` (Float): Futures Price (Target Month)
    - `basis_value` (Float): Basis (Spot - Futures)
    - `hedging_recommendation` (Html): Hedging Strategy
    - `optimal_sales_ratio` (Float): Recommended Sales Ratio (%)
    - `procurement_action` (Selection): procurement_action
    - `market_factors` (Text): Market Factors Analysis
    - `decision_summary` (Html): AI Decision Summary

### `agri.ai.operation.path.optimization` (Defined in `farm_ai_decision`)
  - **Class**: `AgriAiOperationPathOptimization`
  - **描述**: AI Operation Path Optimization
  - _inherit_: `agri.ai.decision.base`
  - **核心字段**:
    - `operation_type` (Selection): operation_type
    - `land_location_ids` (Many2many): farm.location
    - `vehicle_type` (Char): Vehicle Type
    - `fuel_consumption_rate` (Float): Fuel Consumption (L/ha)
    - `estimated_duration` (Float): Estimated Duration (hours)
    - `total_distance` (Float): Total Distance (km)
    - `optimized_path` (Text): Optimized Path
    - `efficiency_gains` (Html): Efficiency Gains
    - `path_recommendation` (Html): Path Recommendation

### `agri.ai.pest.disease.decision` (Defined in `farm_ai_decision`)
  - **Class**: `AgriAiPestDiseaseDecision`
  - **描述**: AI Pest and Disease Decision Support
  - _inherit_: `agri.ai.decision.base`
  - **核心字段**:
    - `pest_disease_detection_id` (Many2one): agri.ai.pest.disease.detection
    - `product_id` (Many2one): product.template
    - `land_location_id` (Many2one): farm.location
    - `detection_date` (Datetime): Detection Date
    - `image_attachment` (Binary): Image Evidence
    - `image_name` (Char): Image Name
    - `pest_disease_name` (Char): Pest/Disease Name
    - `severity_level` (Selection): severity_level
    - `affected_area_percentage` (Float): Affected Area (%)
    - `detection_method` (Selection): detection_method
    - `prevention_advice` (Html): Prevention Advice
    - `treatment_options` (Html): Treatment Options
    - `risk_assessment` (Html): Risk Assessment
    - `economic_impact` (Float): Economic Impact ($)
    - `treatment_cost` (Float): Treatment Cost ($)
    - *... 以及其他 1 个业务字段*

### `agri.ai.quality.grading` (Defined in `farm_ai_decision`)
  - **Class**: `AgriAiQualityGrading`
  - **描述**: AI Quality Grading
  - _inherit_: `agri.ai.decision.base`
  - **核心字段**:
    - `product_id` (Many2one): product.template
    - `batch_lot_id` (Many2one): stock.lot
    - `sample_size` (Integer): Sample Size
    - `quality_attributes` (Text): Quality Attributes
    - `predicted_grade` (Selection): predicted_grade
    - `quality_score` (Float): Quality Score (0-100)
    - `grading_criteria` (Html): Grading Criteria Applied
    - `sorting_recommendation` (Html): Sorting Recommendation
    - `market_suggestion` (Html): Market Suggestion

### `agri.ai.resource.optimization` (Defined in `farm_ai_decision`)
  - **Class**: `AgriAiResourceOptimization`
  - **描述**: AI Resource Optimization
  - _inherit_: `agri.ai.decision.base`
  - **核心字段**:
    - `resource_type` (Selection): resource_type
    - `required_quantity` (Float): Required Quantity
    - `available_quantity` (Float): Available Quantity
    - `optimized_allocation` (Float): Optimized Allocation
    - `allocation_efficiency` (Float): Allocation Efficiency (%)
    - `resource_conflicts` (Html): Resource Conflicts
    - `optimization_recommendation` (Html): Optimization Recommendation
    - `cost_impact` (Float): Cost Impact

### `agri.ai.risk.assessment` (Defined in `farm_ai_decision`)
  - **Class**: `AgriAiRiskAssessment`
  - **描述**: AI Risk Assessment
  - _inherit_: `agri.ai.decision.base`
  - **核心字段**:
    - `risk_category` (Selection): risk_category
    - `risk_location_id` (Many2one): farm.location
    - `risk_probability` (Float): Risk Probability (%)
    - `risk_impact` (Float): Risk Impact (%)
    - `risk_score` (Float): Risk Score
    - `risk_level` (Selection): risk_level
    - `risk_factors` (Text): Risk Factors
    - `mitigation_strategies` (Html): Mitigation Strategies
    - `contingency_plans` (Html): Contingency Plans
    - `monitoring_frequency` (Selection): monitoring_frequency

### `ai.autonomous.mission.log` (Defined in `farm_ai_robotics_bridge`)
  - **Class**: `AIAutonomousMissionLogExtension`
  - **描述**: 
  - _inherit_: `ai.autonomous.mission.log`
  - **核心字段**:
    - `mission_id` (Many2one): farm.robot.mission

### `ai.autonomous.orchestrator` (Defined in `farm_ai_robotics_bridge`)
  - **Class**: `AIAutonomousOrchestratorExtension`
  - **描述**: 
  - _inherit_: `ai.autonomous.orchestrator`


### `ai.decision.engine` (Defined in `farm_ai_decision`)
  - **Class**: `AiDecisionEngine`
  - **描述**: AI Decision Engine
  - _inherit_: `mail.thread, mail.activity.mixin`
  - **核心字段**:
    - `name` (Char): Decision Ref
    - `intervention_id` (Many2one): mrp.production
    - `stress_index` (Float): stress_index
    - `growth_stage_id` (Many2one): growth_stage_id
    - `recovery_plan` (Text): Suggested Recovery Plan (AI)
    - `active_skill_json` (Text): Active Skill Directive (JSON)
    - `predicted_harvest_date` (Date): Predicted Harvest Date
    - `confidence_score` (Float): Confidence Score (%)

### `mrp.production` (Defined in `farm_ai_decision`)
  - **Class**: `AgriIntervention`
  - **描述**: 
  - _inherit_: `mrp.production`
  - **核心字段**:
    - `ai_recommendation_count` (Integer): AI Recommendations
    - `has_critical_stress` (Boolean): Critical Stress Alert

## 5. 工业物联与边缘控制域 (IIoT & Edge)
### `iiot.device.profile` (Defined in `agri_iot`)
  - **Class**: `IiotDeviceProfile`
  - **描述**: Industrial IoT Device Profile

  - **核心字段**:
    - `name` (Char): Name
    - `code` (Char): Code
    - `telemetry_topic_template` (Char): Telemetry Topic Template
    - `iiot_telemetry_rule_ids` (One2many): iiot.telemetry.rule
    - `command_topic_template` (Char): Command Topic Template
    - `ota_notify_topic_template` (Char): OTA Notify Topic Template
    - `ota_status_topic_template` (Char): OTA Status Topic Template
    - `command_template` (Text): Command Template

### `iiot.device` (Defined in `farm_iot`)
  - **Class**: `IiotDevice`
  - **描述**: 
  - _inherit_: `iiot.device`
  - **核心字段**:
    - `digital_twin_model_url` (Char): 3D Model URL
    - `last_telemetry_json` (Text): Last Telemetry JSON

### `iiot.device` (Defined in `farm_iot`)
  - **Class**: `IiotDevice`
  - **描述**: 
  - _inherit_: `iiot.device`
  - **核心字段**:
    - `geofence_id` (Many2one): agri.geospatial.geofence
    - `command_log_ids` (One2many): farm.command.log
    - `active_alert_ids` (One2many): mail.activity

### `iiot.telemetry.rule` (Defined in `agri_iot`)
  - **Class**: `IiotTelemetryRule`
  - **描述**: Industrial IoT Telemetry Rule

  - **核心字段**:
    - `name` (Char): Name
    - `sequence` (Integer): Sequence
    - `active` (Boolean): Active
    - `profile_id` (Many2one): iiot.device.profile
    - `json_path` (Char): JSON Path
    - `target_model` (Char): Target Model
    - `target_domain` (Char): Target Domain
    - `target_field` (Char): Target Field

### `iiot.telemetry` (Defined in `agri_iot`)
  - **Class**: `IiotTelemetry`
  - **描述**: IIoT Telemetry Data

  - **核心字段**:
    - `name` (Char): Sensor Name
    - `sensor_type` (Selection): sensor_type
    - `value` (Float): Value
    - `timestamp` (Datetime): Timestamp
    - `device_id` (Many2one): iiot.device
    - `gps_lat` (Float): Latitude
    - `gps_lng` (Float): Longitude

### `iiot.telemetry` (Defined in `farm_iot`)
  - **Class**: `FarmIotTelemetry`
  - **描述**: 
  - _inherit_: `iiot.telemetry`
  - **核心字段**:
    - `production_id` (Many2one): project.task
    - `drone_id` (Many2one): maintenance.equipment
    - `land_parcel_id` (Many2one): farm.location
    - `adopted_lot_id` (Many2one): stock.lot

## 6. 数字孪生与遥测域 (Digital Twin & Telemetry)
### `agri.telemetry` (Defined in `farm_iot`)
  - **Class**: `AgriTelemetry`
  - **描述**: Agricultural Telemetry Data

  - **核心字段**:
    - `name` (Char): Sensor Name
    - `sensor_type` (Selection): sensor_type
    - `value` (Float): Value
    - `timestamp` (Datetime): Timestamp
    - `production_id` (Many2one): project.task
    - `drone_id` (Many2one): maintenance.equipment
    - `device_id` (Many2one): iiot.device
    - `land_parcel_id` (Many2one): farm.location
    - `adopted_lot_id` (Many2one): stock.lot
    - `gps_lat` (Float): Latitude
    - `gps_lng` (Float): Longitude

### `farm.automation.rule` (Defined in `farm_iot`)
  - **Class**: `FarmAutomationRule`
  - **描述**: Farm IOT Automation Rule

  - **核心字段**:
    - `name` (Char): Rule Name
    - `active` (Boolean): active
    - `sensor_type` (Selection): sensor_type
    - `operator` (Selection): operator
    - `threshold` (Float): Threshold
    - `target_device_id` (Many2one): iiot.device
    - `command_to_send` (Char): Command/Action
    - `command_params` (Char): Params (JSON)

### `farm.digital.twin.marker` (Defined in `farm_iot`)
  - **Class**: `FarmDigitalTwinMarker`
  - **描述**: Digital Twin Device Marker (Deprecated - Use agri.digital.twin.marker)
  - _inherit_: `agri.digital.twin.marker`


### `farm.digital.twin.scene` (Defined in `farm_iot`)
  - **Class**: `FarmDigitalTwinScene`
  - **描述**: Digital Twin 3D Scene (Deprecated - Use agri.digital.twin.scene)
  - _inherit_: `agri.digital.twin.scene`


### `farm.telemetry` (Defined in `farm_iot`)
  - **Class**: `FarmTelemetry`
  - **描述**: Agricultural Telemetry Data (Deprecated - Use agri.telemetry)
  - _inherit_: `agri.telemetry`


### `iot.device.mapping` (Defined in `farm_iot`)
  - **Class**: `IotDeviceMapping`
  - **描述**: IoT Device to Business Field Mapper

  - **核心字段**:
    - `name` (Char): name
    - `device_id` (Many2one): iiot.device
    - `mqtt_topic` (Char): mqtt_topic
    - `direction` (Selection): direction
    - `mapping_type` (Selection): mapping_type
    - `target_model_id` (Many2one): ir.model
    - `target_field_id` (Many2one): ir.model.fields
    - `method_name` (Char): method_name
    - `match_record_by` (Selection): match_record_by
    - `match_field_id` (Many2one): ir.model.fields
    - `payload_template` (Text): Payload Template (JSON)
    - `active` (Boolean): active

### `iot.telemetry.buffer` (Defined in `farm_iot`)
  - **Class**: `IotTelemetryBuffer`
  - **描述**: IoT Raw Telemetry Buffer

  - **核心字段**:
    - `mqtt_topic` (Char): mqtt_topic
    - `raw_value` (Char): raw_value
    - `processed` (Boolean): processed
    - `processed_date` (Datetime): processed_date
    - `mapping_id` (Many2one): iot.device.mapping

## 7. ESG合规与碳账本域 (ESG & Carbon Ledger)
### `agri.carbon.factor` (Defined in `farm_esg_environmental`)
  - **Class**: `AgriCarbonFactor`
  - **描述**: Agricultural Carbon Emission Factors

  - **核心字段**:
    - `name` (Char): Factor Name
    - `product_id` (Many2one): product.template
    - `category` (Selection): category
    - `emission_factor` (Float): Emission Factor (kg CO2e / unit)
    - `uom_id` (Many2one): uom.uom
    - `source` (Char): Data Source

### `agri.carbon.ledger` (Defined in `farm_esg_environmental`)
  - **Class**: `AgriCarbonLedger`
  - **描述**: Agricultural Carbon Transaction Ledger
  - _inherit_: `mail.thread, mail.activity.mixin, agri.evidence.mixin`
  - **核心字段**:
    - `name` (Char): Transaction Ref
    - `date` (Date): Transaction Date
    - `location_id` (Many2one): farm.location
    - `lot_id` (Many2one): stock.lot
    - `operation_id` (Many2one): mrp.workorder
    - `factor_id` (Many2one): agri.carbon.factor
    - `quantity` (Float): Quantity Used
    - `uom_id` (Many2one): uom.uom
    - `total_co2e` (Float): Total CO2e (kg)
    - `impact_type` (Selection): impact_type

### `agri.esg.compliance.monitoring` (Defined in `farm_esg_risk`)
  - **Class**: `AgriESGComplianceMonitoring`
  - **描述**: Agricultural ESG Compliance Monitoring
  - _inherit_: `mail.thread, mail.activity.mixin`
  - **核心字段**:
    - `name` (Char): Compliance Check Name
    - `compliance_type` (Selection): compliance_type
    - `regulation_reference` (Char): Regulation Reference
    - `threshold_value` (Float): Threshold Value
    - `current_value` (Float): Current Value
    - `compliance_status` (Selection): compliance_status
    - `last_check_date` (Date): Last Check Date
    - `next_check_date` (Date): Next Check Date
    - `compliance_owner` (Many2one): res.users
    - `alert_issued` (Boolean): Alert Issued
    - `last_alert_date` (Date): Last Alert Date
    - `corrective_actions` (Text): Corrective Actions Required
    - `implementation_status` (Selection): implementation_status
    - `notes` (Text): Notes

### `agri.esg.kpi` (Defined in `farm_esg_risk`)
  - **Class**: `AgriESGKPI`
  - **描述**: Agricultural ESG KPI
  - _inherit_: `mail.thread, mail.activity.mixin`
  - **核心字段**:
    - `name` (Char): KPI Name
    - `kpi_category` (Selection): kpi_category
    - `kpi_type` (Selection): kpi_type
    - `reporting_period` (Selection): reporting_period
    - `target_value` (Float): Target Value
    - `current_value` (Float): Current Value
    - `unit_of_measurement` (Char): Unit of Measurement
    - `baseline_value` (Float): Baseline Value
    - `achievement_percentage` (Float): Achievement %
    - `trend_indicator` (Selection): trend_indicator
    - `year` (Integer): Year
    - `responsible_department` (Many2one): hr.department
    - `data_source` (Char): Data Source
    - `calculation_method` (Text): Calculation Method
    - `benchmark_value` (Float): Benchmark Value
    - *... 以及其他 4 个业务字段*

### `agri.sustainability.carbon.model` (Defined in `farm_esg_circular`)
  - **Class**: `AgriSustainabilityCarbonModel`
  - **描述**: Agricultural Industry Specific Carbon Model
  - _inherit_: `mail.thread, mail.activity.mixin`
  - **核心字段**:
    - `name` (Char): Model Name
    - `industry_type` (Selection): industry_type
    - `description` (Text): Description
    - `model_version` (Char): Model Version
    - `active` (Boolean): Active
    - `calculation_method` (Selection): calculation_method
    - `scope_1_supported` (Boolean): Scope 1 Supported
    - `scope_2_supported` (Boolean): Scope 2 Supported
    - `scope_3_supported` (Boolean): Scope 3 Supported
    - `emission_factors` (Text): Emission Factors JSON
    - `carbon_intensity_threshold` (Float): Carbon Intensity Threshold (kgCO2e/unit)
    - `reporting_standard` (Selection): reporting_standard
    - `compliance_requirements` (Text): Compliance Requirements
    - `audit_frequency` (Selection): audit_frequency
    - `direct_emission_coefficient` (Float): Direct Emission Coefficient
    - *... 以及其他 4 个业务字段*

### `agri.sustainability.metric.value.wizard` (Defined in `farm_esg_sustainability`)
  - **Class**: `AgriSustainabilityMetricValueWizard`
  - **描述**: Agri Sustainability Metric Value Update Wizard

  - **核心字段**:
    - `metric_id` (Many2one): agri.sustainability.metric
    - `value` (Float): New Value
    - `date` (Datetime): Date
    - `note` (Text): Note

### `agri.sustainability.metric.value` (Defined in `farm_esg_sustainability`)
  - **Class**: `AgriSustainabilityMetricValue`
  - **描述**: Agri Sustainability Metric Value
  - _inherit_: `mail.thread, mail.activity.mixin`
  - **核心字段**:
    - `metric_id` (Many2one): agri.sustainability.metric
    - `value` (Float): Value
    - `date` (Datetime): Record Date
    - `note` (Text): Note
    - `recorded_by` (Many2one): res.users

### `agri.sustainability.metric` (Defined in `farm_esg_sustainability`)
  - **Class**: `AgriSustainabilityMetric`
  - **描述**: Agricultural Sustainability Metric
  - _inherit_: `mail.thread, mail.activity.mixin`
  - **核心字段**:
    - `name` (Char): Metric Name
    - `code` (Char): Metric Code
    - `category` (Selection): category
    - `unit` (Char): Unit of Measure
    - `description` (Text): Description
    - `sequence` (Integer): Sequence
    - `target_value` (Float): Target Value
    - `current_value` (Float): Current Value
    - `progress_rate` (Float): Progress Rate (%)
    - `is_active` (Boolean): Active
    - `calculation_method` (Selection): calculation_method
    - `formula` (Text): Calculation Formula
    - `last_updated` (Datetime): Last Updated
    - `value_history_ids` (One2many): agri.sustainability.metric.value

### `agri.triple.bottom.line.metrics` (Defined in `farm_esg_compliance`)
  - **Class**: `AgriTripleBottomLineMetrics`
  - **描述**: Agricultural Triple Bottom Line Metrics
  - _inherit_: `mail.thread, mail.activity.mixin, agri.sustainability.mixin`
  - **核心字段**:
    - `name` (Char): Metric Set Name
    - `date` (Date): Date
    - `revenue` (Float): Revenue
    - `profit` (Float): Profit
    - `profit_margin` (Float): Profit Margin (%)
    - `roi` (Float): Return on Investment (%)
    - `carbon_footprint_tco2e` (Float): Carbon Footprint (tCO2e)
    - `water_usage_m3` (Float): Water Usage (m3)
    - `land_use_efficiency` (Float): Land Use Efficiency
    - `resource_efficiency` (Float): Resource Efficiency (%)
    - `jobs_created` (Integer): Jobs Created
    - `community_investment` (Float): Community Investment
    - `safety_incidents` (Integer): Safety Incidents
    - `employee_satisfaction` (Float): Employee Satisfaction (0-10)
    - `economic_score` (Float): Economic Score (0-100)
    - *... 以及其他 5 个业务字段*

### `agri.vra.soil.health.monitor` (Defined in `farm_esg_environmental`)
  - **Class**: `AgriVRASoilHealthMonitor`
  - **描述**: VRA Soil Health Monitoring and Analytics
  - _inherit_: `mail.thread, mail.activity.mixin`
  - **核心字段**:
    - `name` (Char): Soil Health Assessment
    - `assessment_date` (Date): Assessment Date
    - `location_id` (Many2one): farm.location
    - `sampling_method` (Selection): sampling_method
    - `organic_matter_content` (Float): Organic Matter Content (%)
    - `ph_level` (Float): pH Level
    - `nitrogen_level` (Float): Nitrogen Level (ppm)
    - `phosphorus_level` (Float): Phosphorus Level (ppm)
    - `potassium_level` (Float): Potassium Level (ppm)
    - `cation_exchange_capacity` (Float): CEC (cmol/kg)
    - `base_saturation_calcium` (Float): Base Saturation - Calcium (%)
    - `base_saturation_magnesium` (Float): Base Saturation - Magnesium (%)
    - `base_saturation_potassium` (Float): Base Saturation - Potassium (%)
    - `base_saturation_sodium` (Float): Base Saturation - Sodium (%)
    - `total_salinity` (Float): Total Salinity (dS/m)
    - *... 以及其他 21 个业务字段*

### `esg.environmental.report` (Defined in `farm_esg_environmental`)
  - **Class**: `ESGEnvironmentalReport`
  - **描述**: ESG Environmental Report
  - _inherit_: `esg.performance.report`
  - **核心字段**:
    - `carbon_footprint_tco2e` (Float): Carbon Footprint (tCO2e)
    - `water_stress_score` (Float): Water Stress Score (0-100)
    - `biodiversity_risk_score` (Float): Biodiversity Risk Score (0-100)

### `export.compliance.log` (Defined in `farm_sale_ch`)
  - **Class**: `ExportComplianceLog`
  - **描述**: Export Compliance Check Log

  - **核心字段**:
    - `order_id` (Many2one): sale.order
    - `country_code` (Char): Country Code
    - `violations` (Char): Violations
    - `checked_on` (Datetime): Checked On
    - `result` (Selection): result
    - `notes` (Text): Notes
    - `checked_by` (Many2one): res.users

### `farm.compliance.audit.standard` (Defined in `farm_esg_compliance`)
  - **Class**: `FarmComplianceAuditStandard`
  - **描述**: Compliance Audit Standard

  - **核心字段**:
    - `name` (Char): Standard Name
    - `country_id` (Many2one): res.country
    - `code` (Char): Standard Code
    - `active` (Boolean): active

### `farm.esg.community.investment` (Defined in `farm_esg_fair_trade`)
  - **Class**: `CommunityInvestment`
  - **描述**: Community Investment
  - _inherit_: `mail.thread, mail.activity.mixin`
  - **核心字段**:
    - `name` (Char): Investment Name
    - `investment_type` (Selection): investment_type
    - `amount` (Float): Amount
    - `beneficiaries_count` (Integer): Number of Beneficiaries
    - `location` (Char): Location
    - `investment_date` (Date): Investment Date
    - `description` (Text): Description
    - `impact_assessment` (Text): Impact Assessment
    - `evidence_attachments` (Binary): Evidence Attachments
    - `reported_by` (Many2one): res.users
    - `project_status` (Selection): project_status
    - `start_date` (Date): Start Date
    - `end_date` (Date): End Date
    - `annual_recurring` (Boolean): Annual Recurring

### `farm.esg.compliance.monitoring` (Defined in `farm_esg_risk`)
  - **Class**: `ESGComplianceMonitoring`
  - **描述**: ESG Compliance Monitoring (Deprecated - Use agri.esg.compliance.monitoring)
  - _inherit_: `agri.esg.compliance.monitoring`


### `farm.esg.dashboard` (Defined in `farm_esg_report`)
  - **Class**: `ESGDashboard`
  - **描述**: ESG Dashboard

  - **核心字段**:
    - `name` (Char): Dashboard Name
    - `dashboard_type` (Selection): dashboard_type
    - `display_period` (Selection): display_period
    - `start_date` (Date): Start Date
    - `end_date` (Date): End Date
    - `environmental_score` (Float): Environmental Score
    - `social_score` (Float): Social Score
    - `governance_score` (Float): Governance Score
    - `overall_esg_score` (Float): Overall ESG Score
    - `key_metrics` (Text): Key Metrics
    - `trend_analysis` (Text): Trend Analysis
    - `risk_indicators` (Text): Risk Indicators
    - `compliance_status` (Text): Compliance Status
    - `last_updated` (Datetime): Last Updated
    - `refresh_frequency` (Selection): refresh_frequency
    - *... 以及其他 1 个业务字段*

### `farm.esg.fair.trade.certificate` (Defined in `farm_esg_fair_trade`)
  - **Class**: `FairTradeCertificate`
  - **描述**: Fair Trade Certificate
  - _inherit_: `mail.thread, mail.activity.mixin`
  - **核心字段**:
    - `name` (Char): Certificate Name
    - `certificate_number` (Char): Certificate Number
    - `issuing_body` (Char): Issuing Body
    - `issue_date` (Date): Issue Date
    - `expiry_date` (Date): Expiry Date
    - `is_active` (Boolean): Is Active
    - `fair_trade_premium` (Float): Fair Trade Premium (%)
    - `covered_products` (Many2many): product.product
    - `covered_farms` (Many2many): res.partner
    - `certificate_type` (Selection): certificate_type
    - `status` (Selection): status
    - `annual_audit_date` (Date): Annual Audit Date
    - `next_audit_date` (Date): Next Audit Date
    - `compliance_score` (Float): Compliance Score
    - `assigned_to_user_id` (Many2one): res.users

### `farm.esg.fair.trade.premium.allocation` (Defined in `farm_esg_fair_trade`)
  - **Class**: `FairTradePremiumAllocation`
  - **描述**: Fair Trade Premium Allocation
  - _inherit_: `mail.thread, mail.activity.mixin`
  - **核心字段**:
    - `certificate_id` (Many2one): farm.esg.fair.trade.certificate
    - `allocation_date` (Date): Allocation Date
    - `amount` (Float): Amount
    - `allocation_type` (Selection): allocation_type
    - `description` (Text): Description
    - `beneficiaries` (Text): Beneficiaries
    - `impact_measure` (Text): Impact Measure
    - `allocated_by` (Many2one): res.users
    - `approved_by` (Many2one): res.users
    - `approval_date` (Date): Approval Date
    - `state` (Selection): state
    - `allocation_reference` (Char): Allocation Reference

### `farm.esg.kpi` (Defined in `farm_esg_risk`)
  - **Class**: `ESGKPI`
  - **描述**: ESG KPI (Deprecated - Use agri.esg.kpi)
  - _inherit_: `agri.esg.kpi`


### `farm.esg.labor.condition` (Defined in `farm_esg_fair_trade`)
  - **Class**: `LaborCondition`
  - **描述**: Labor Condition
  - _inherit_: `mail.thread, mail.activity.mixin`
  - **核心字段**:
    - `name` (Char): Condition Name
    - `employee_id` (Many2one): hr.employee
    - `condition_type` (Selection): condition_type
    - `issue_date` (Date): Issue Date
    - `expiry_date` (Date): Expiry Date
    - `is_valid` (Boolean): Is Valid
    - `compliance_status` (Selection): compliance_status
    - `training_record` (Many2one): hr.training
    - `certification` (Char): Certification Number
    - `issuing_body` (Char): Issuing Body
    - `notes` (Text): Notes
    - `last_inspection_date` (Date): Last Inspection Date
    - `next_inspection_date` (Date): Next Inspection Date
    - `safety_score` (Float): Safety Score

### `farm.esg.red.line.config` (Defined in `farm_esg_environmental`)
  - **Class**: `ESGRedLineConfig`
  - **描述**: ESG Red Line Configuration (Deprecated - Use agri.esg.red.line.config)
  - _inherit_: `agri.esg.red.line.config`


### `farm.esg.red.line.monitoring` (Defined in `farm_esg_environmental`)
  - **Class**: `ESGRedLineMonitoring`
  - **描述**: ESG Red Line Monitoring (Deprecated - Use agri.esg.red.line.monitoring)
  - _inherit_: `agri.esg.red.line.monitoring`


### `farm.esg.report.customization` (Defined in `farm_esg_risk`)
  - **Class**: `ESGReportCustomization`
  - **描述**: ESG Report Customization for Stakeholders
  - _inherit_: `mail.thread, mail.activity.mixin`
  - **核心字段**:
    - `name` (Char): Report Template Name
    - `report_type` (Selection): report_type
    - `stakeholder_group` (Selection): stakeholder_group
    - `report_format` (Selection): report_format
    - `report_language` (Selection): report_language
    - `report_sections` (Text): Included Sections
    - `custom_metrics` (Text): Custom Metrics
    - `data_filters` (Text): Data Filters
    - `report_logo` (Binary): Custom Logo
    - `brand_colors` (Char): Brand Colors
    - `report_recipients` (Many2many): res.partner
    - `auto_generation` (Boolean): Auto Generation
    - `generation_frequency` (Selection): generation_frequency
    - `last_generated` (Datetime): Last Generated
    - `next_scheduled_generation` (Datetime): Next Scheduled Generation
    - *... 以及其他 12 个业务字段*

### `farm.esg.report` (Defined in `farm_esg_report`)
  - **Class**: `ESGReport`
  - **描述**: ESG Report
  - _inherit_: `mail.thread, mail.activity.mixin`
  - **核心字段**:
    - `name` (Char): Report Name
    - `report_type` (Selection): report_type
    - `report_period` (Selection): report_period
    - `report_year` (Integer): Report Year
    - `language` (Selection): language
    - `environmental_section` (Text): Environmental Section
    - `social_section` (Text): Social Section
    - `governance_section` (Text): Governance Section
    - `executive_summary` (Text): Executive Summary
    - `carbon_footprint_data` (Text): Carbon Footprint Data
    - `biodiversity_data` (Text): Biodiversity Data
    - `community_impact_data` (Text): Community Impact Data
    - `governance_metrics` (Text): Governance Metrics
    - `compliance_status` (Text): Compliance Status
    - `risk_assessment_summary` (Text): Risk Assessment Summary
    - *... 以及其他 15 个业务字段*

### `farm.esg.risk.assessment` (Defined in `farm_esg_risk`)
  - **Class**: `ESGRiskAssessment`
  - **描述**: ESG Risk Assessment (Deprecated - Use agri.esg.risk.assessment)
  - _inherit_: `agri.esg.risk.assessment`


### `farm.esg.social.diversity.metric` (Defined in `farm_esg_social`)
  - **Class**: `SocialDiversityMetric`
  - **描述**: Social and Diversity Metrics
  - _inherit_: `mail.thread, mail.activity.mixin`
  - **核心字段**:
    - `name` (Char): Metric Name
    - `reporting_period` (Date): Reporting Period
    - `gender_male_count` (Integer): Male Count
    - `gender_female_count` (Integer): Female Count
    - `gender_other_count` (Integer): Other Gender Count
    - `age_under_30` (Integer): Under 30 Years
    - `age_30_to_50` (Integer): 30-50 Years
    - `age_over_50` (Integer): Over 50 Years
    - `disability_employment` (Integer): Disability Employment Count
    - `local_community_employment` (Integer): Local Community Employment
    - `temporary_contract_count` (Integer): Temporary Contract Count
    - `full_time_count` (Integer): Full Time Count
    - `total_employees` (Integer): Total Employees
    - `gender_balance_ratio` (Float): Gender Balance Ratio
    - `local_employment_ratio` (Float): Local Employment Ratio

### `farm.esg.stakeholder.engagement` (Defined in `farm_esg_risk`)
  - **Class**: `StakeholderEngagement`
  - **描述**: Stakeholder Engagement
  - _inherit_: `mail.thread, mail.activity.mixin`
  - **核心字段**:
    - `name` (Char): Engagement Activity
    - `stakeholder_id` (Many2one): res.partner
    - `stakeholder_type` (Selection): stakeholder_type
    - `engagement_date` (Date): Engagement Date
    - `engagement_type` (Selection): engagement_type
    - `engagement_topic` (Selection): engagement_topic
    - `communication_channel` (Selection): communication_channel
    - `participants_count` (Integer): Participants Count
    - `outcome_summary` (Text): Outcome Summary
    - `feedback_received` (Text): Feedback Received
    - `action_items` (Text): Action Items
    - `action_owner` (Many2one): res.users
    - `action_deadline` (Date): Action Deadline
    - `action_status` (Selection): action_status
    - `satisfaction_rating` (Selection): satisfaction_rating
    - *... 以及其他 4 个业务字段*

### `farm.esg.sustainability.goal` (Defined in `farm_esg_report`)
  - **Class**: `SustainabilityGoal`
  - **描述**: Sustainability Goal
  - _inherit_: `mail.thread, mail.activity.mixin`
  - **核心字段**:
    - `name` (Char): Goal Name
    - `goal_type` (Selection): goal_type
    - `description` (Text): Description
    - `target_year` (Integer): Target Year
    - `baseline_year` (Integer): Baseline Year
    - `baseline_value` (Float): Baseline Value
    - `target_value` (Float): Target Value
    - `current_value` (Float): Current Value
    - `progress_percentage` (Float): Progress %
    - `goal_status` (Selection): goal_status
    - `responsible_team` (Many2one): hr.department
    - `key_performance_indicators` (Text): Key Performance Indicators
    - `action_plan` (Text): Action Plan
    - `monitoring_frequency` (Selection): monitoring_frequency
    - `last_review_date` (Date): Last Review Date
    - *... 以及其他 8 个业务字段*

### `farm.export.compliance` (Defined in `farm_esg_compliance`)
  - **Class**: `FarmExportCompliance`
  - **描述**: 
  - _inherit_: `farm.export.compliance`
  - **核心字段**:
    - `standard_id` (Many2one): farm.compliance.audit.standard
    - `last_audit_run` (Datetime): Last Audit Run
    - `audit_log` (Text): Audit Log Details
    - `missing_records` (Boolean): Missing Required Records
    - `withdrawal_violation` (Boolean): Withdrawal Period Violation

### `farm.sustainability.circular.flow.analysis` (Defined in `farm_esg_circular`)
  - **Class**: `CircularFlowAnalysis`
  - **描述**: Farm Circular Flow Analysis (Deprecated - Use agri.sustainability.circular.flow.analysis)
  - _inherit_: `agri.sustainability.circular.flow.analysis`


### `farm.sustainability.circular.flow` (Defined in `farm_esg_circular`)
  - **Class**: `CircularFlow`
  - **描述**: Farm Circular Flow (Deprecated - Use agri.sustainability.circular.flow)
  - _inherit_: `agri.sustainability.circular.flow`


### `farm.sustainability.dashboard` (Defined in `farm_esg_sustainability`)
  - **Class**: `FarmSustainabilityDashboard`
  - **描述**: Sustainability Dashboard (Deprecated - Use agri.sustainability.dashboard)
  - _inherit_: `agri.sustainability.dashboard`


### `farm.sustainability.dashboard` (Defined in `farm_esg_sustainability`)
  - **Class**: `SustainabilityDashboard`
  - **描述**: Sustainability Dashboard (Deprecated - Use agri.sustainability.dashboard)
  - _inherit_: `agri.sustainability.dashboard`


### `farm.sustainability.industry.carbon.model` (Defined in `farm_esg_circular`)
  - **Class**: `IndustryCarbonModel`
  - **描述**: Industry Specific Carbon Model (Deprecated - Use agri.sustainability.carbon.model)
  - _inherit_: `agri.sustainability.carbon.model`


### `farm.sustainability.metric.value.wizard` (Defined in `farm_esg_sustainability`)
  - **Class**: `FarmSustainabilityMetricValueWizard`
  - **描述**: Sustainability Metric Value Update Wizard (Deprecated - Use agri.sustainability.metric.value.wizard)
  - _inherit_: `agri.sustainability.metric.value.wizard`


### `farm.sustainability.metric.value` (Defined in `farm_esg_sustainability`)
  - **Class**: `FarmSustainabilityMetricValue`
  - **描述**: Sustainability Metric Value (Deprecated - Use agri.sustainability.metric.value)
  - _inherit_: `agri.sustainability.metric.value`


### `farm.sustainability.metric` (Defined in `farm_esg_sustainability`)
  - **Class**: `FarmSustainabilityMetric`
  - **描述**: Sustainability Metric (Deprecated - Use agri.sustainability.metric)
  - _inherit_: `agri.sustainability.metric`


### `farm.sustainability.report` (Defined in `farm_esg_sustainability`)
  - **Class**: `FarmSustainabilityReport`
  - **描述**: Sustainability Report (Deprecated - Use agri.sustainability.report)
  - _inherit_: `agri.sustainability.report`


### `farm.sustainability.report` (Defined in `farm_esg_sustainability`)
  - **Class**: `SustainabilityReport`
  - **描述**: Sustainability Report (Deprecated - Use agri.sustainability.report)
  - _inherit_: `agri.sustainability.report`


### `mrp.production` (Defined in `farm_esg_carbon`)
  - **Class**: `AgriIntervention`
  - **描述**: 
  - _inherit_: `mrp.production`
  - **核心字段**:
    - `calculated_carbon_emission` (Float): Calculated Carbon Emission (kg CO2e)

### `mrp.workorder` (Defined in `farm_esg_environmental`)
  - **Class**: `MrpWorkorder`
  - **描述**: 
  - _inherit_: `mrp.workorder`


### `product.template` (Defined in `farm_esg_carbon`)
  - **Class**: `ProductTemplate`
  - **描述**: 
  - _inherit_: `product.template`
  - **核心字段**:
    - `carbon_emission_factor` (Float): Carbon Emission Factor (kg CO2e / unit)

### `res.config.settings` (Defined in `farm_esg`)
  - **Class**: `ResConfigSettings`
  - **描述**: 
  - _inherit_: `res.config.settings`
  - **核心字段**:
    - `is_esg_sustainability_active` (Boolean): Activate ESG Sustainability DNA

### `stock.lot` (Defined in `farm_esg_carbon`)
  - **Class**: `StockLot`
  - **描述**: 
  - _inherit_: `stock.lot`
  - **核心字段**:
    - `carbon_footprint` (Float): Carbon Footprint (kg CO2e)

### `stock.lot` (Defined in `farm_esg_environmental`)
  - **Class**: `StockLot`
  - **描述**: 
  - _inherit_: `stock.lot`


## 8. 质量控制与溯源域 (Quality & Traceability)
### `agri.quality.control` (Defined in `farm_isl`)
  - **Class**: `AgriQualityControl`
  - **描述**: Agri ISL Quality Control
  - _inherit_: `agri.quality.mixin`
  - **核心字段**:
    - `ccp_monitoring` (Html): CCP Monitoring
    - `aql_sampling` (Html): AQL Sampling
    - `testing_procedures` (Html): Testing Procedures
    - `acceptance_criteria` (Html): Acceptance Criteria
    - `deviation_handling` (Html): Deviation Handling

### `cooperative.entity` (Defined in `farm_multi_farm_quality`)
  - **Class**: `CooperativeEntityExtensionQuality`
  - **描述**: 
  - _inherit_: `cooperative.entity`
  - **核心字段**:
    - `quality_control_standard_ids` (One2many): quality.control.standard

### `farm.haccp.check` (Defined in `farm_quality`)
  - **Class**: `FarmHaccpCheck`
  - **描述**: HACCP Monitoring Record
  - _inherit_: `agri.incident.alert.mixin`
  - **核心字段**:
    - `quality_check_id` (Many2one): quality.check
    - `actual_value` (Float): Measured Value
    - `is_violated` (Boolean): CL Violation
    - `corrective_action_taken` (Text): Corrective Action Taken
    - `ca_responsible_id` (Many2one): res.users

### `farm.haccp.point` (Defined in `farm_quality`)
  - **Class**: `FarmHaccpPoint`
  - **描述**: HACCP Critical Control Point

  - **核心字段**:
    - `quality_point_id` (Many2one): quality.point
    - `is_ccp` (Boolean): Is Critical Control Point
    - `cl_min` (Float): Critical Limit Min
    - `cl_max` (Float): Critical Limit Max
    - `cl_uom_id` (Many2one): uom.uom
    - `hazard_description` (Text): Identified Hazard
    - `corrective_action_plan` (Text): Standard Corrective Action

### `agri.isl.quality.control` (Defined in `farm_isl`)
  - **Class**: `AgriQualityControl`
  - **描述**: Farm ISL Quality Control
  - _inherit_: `agri.isl.quality.mixin`
  - **核心字段**:
    - `ccp_monitoring` (Html): CCP Monitoring
    - `aql_sampling` (Html): AQL Sampling
    - `testing_procedures` (Html): Testing Procedures
    - `acceptance_criteria` (Html): Acceptance Criteria
    - `deviation_handling` (Html): Deviation Handling

### `farm.quality.sample` (Defined in `farm_quality`)
  - **Class**: `FarmQualitySample`
  - **描述**: Quality Sample (Deprecated - Use agri.quality.sample)
  - _inherit_: `agri.quality.sample`


### `quality.control.standard` (Defined in `farm_multi_farm_quality`)
  - **Class**: `QualityControlStandard`
  - **描述**: Quality Control Standard
  - _inherit_: `mail.thread, mail.activity.mixin`
  - **核心字段**:
    - `name` (Char): Standard Name
    - `code` (Char): Standard Code
    - `cooperative_id` (Many2one): cooperative.entity
    - `product_category_id` (Many2one): product.category
    - `quality_threshold` (Float): Quality Threshold (%)
    - `inspection_criteria` (Text): Inspection Criteria
    - `certification_required` (Boolean): Certification Required
    - `certification_standard` (Char): Certification Standard
    - `is_active` (Boolean): Is Active
    - `description` (Text): Description

## 9. 农业特色供应链域 (Supply Chain & Procurement)
### `farm.transport.temperature` (Defined in `farm_supply_logistics`)
  - **Class**: `FarmTransportTemperature`
  - **描述**: Transport Temperature Log

  - **核心字段**:
    - `picking_id` (Many2one): stock.picking
    - `timestamp` (Datetime): Timestamp
    - `temperature` (Float): Temperature (℃)
    - `location_name` (Char): Location/Milestone

### `farm.vehicle` (Defined in `farm_supply_logistics`)
  - **Class**: `FarmVehicle`
  - **描述**: Farm Transport Vehicle

  - **核心字段**:
    - `name` (Char): License Plate
    - `model` (Char): Model
    - `vehicle_type` (Selection): vehicle_type
    - `capacity_weight` (Float): Max Payload (kg)

### `product.template` (Defined in `farm_supply_logistics`)
  - **Class**: `ProductTemplate`
  - **描述**: 
  - _inherit_: `product.template`
  - **核心字段**:
    - `requires_cold_chain` (Boolean): Cold Chain Required
    - `target_temperature_min` (Float): Min Temp (℃)
    - `target_temperature_max` (Float): Max Temp (℃)

### `product.template` (Defined in `farm_supply_procurement`)
  - **Class**: `ProductTemplate`
  - **描述**: 
  - _inherit_: `product.template`
  - **核心字段**:
    - `is_agri_input` (Boolean): Is Agri Input
    - `input_type` (Selection): input_type
    - `is_safety_approved` (Boolean): Safety Approved
    - `active_ingredient` (Char): Active Ingredient
    - `n_content` (Float): Nitrogen (%)
    - `p_content` (Float): Phosphorus (%)
    - `k_content` (Float): Potassium (%)
    - `withdrawal_period_days` (Integer): Withdrawal Period (Days)
    - `growth_cycle_days` (Integer): Growth Cycle (Days)

### `purchase.order.line` (Defined in `farm_supply_procurement`)
  - **Class**: `AgriPurchaseOrderLine`
  - **描述**: Covenant Line
  - _inherit_: `purchase.order.line, agri.nutrient.mixin, agri.sustainability.mixin`


### `purchase.order.line` (Defined in `farm_supply_procurement`)
  - **Class**: `PurchaseOrderLine`
  - **描述**: 
  - _inherit_: `purchase.order.line`
  - **核心字段**:
    - `is_compliance_warning` (Boolean): Compliance Warning

### `purchase.order.line` (Defined in `farm_supply_quality`)
  - **Class**: `PurchaseOrderLine`
  - **描述**: 
  - _inherit_: `purchase.order.line`
  - **核心字段**:
    - `quality_adjustment_amount` (Float): Quality Adjustment Amount
    - `quality_protein_content` (Float): Protein Content (%)
    - `quality_moisture_content` (Float): Moisture Content (%)
    - `quality_impurities_rate` (Float): Impurities Rate (%)
    - `quality_grade` (Selection): quality_grade
    - `base_unit_price` (Float): Base Unit Price
    - `quality_adjusted_unit_price` (Float): Quality Adjusted Unit Price
    - `quality_pricing_rule_id` (Many2one): quality.based.pricing

### `purchase.order` (Defined in `farm_supply_procurement`)
  - **Class**: `AgriPurchaseOrder`
  - **描述**: Resource Input Covenant
  - _inherit_: `purchase.order, agri.sustainability.mixin, agri.view.mixin`


### `purchase.order` (Defined in `farm_supply_procurement`)
  - **Class**: `PurchaseOrder`
  - **描述**: 
  - _inherit_: `purchase.order`
  - **核心字段**:
    - `joint_procurement_order_id` (Many2one): joint.procurement.order
    - `agri_task_id` (Many2one): project.task

### `purchase.order` (Defined in `farm_supply_quality`)
  - **Class**: `PurchaseOrder`
  - **描述**: 
  - _inherit_: `purchase.order`
  - **核心字段**:
    - `quality_based_pricing_enabled` (Boolean): Quality-Based Pricing Enabled
    - `acquisition_pricing_rules` (One2many): quality.based.pricing
    - `total_pricing_adjustments` (Float): Total Quality Adjustments

### `sale.order` (Defined in `farm_supply_procurement`)
  - **Class**: `SaleOrder`
  - **描述**: 
  - _inherit_: `sale.order`


### `stock.picking` (Defined in `farm_supply_logistics`)
  - **Class**: `StockPicking`
  - **描述**: 
  - _inherit_: `stock.picking`
  - **核心字段**:
    - `is_cold_chain` (Boolean): Is Cold Chain Transport
    - `actual_transport_temp` (Float): Actual Transport Temp (℃)
    - `vehicle_id` (Many2one): farm.vehicle
    - `driver_id` (Many2one): res.partner
    - `packaging_level` (Selection): packaging_level
    - `temperature_log_ids` (One2many): farm.transport.temperature

## 10. 金融、估值与结算域 (Financial & Valuation)
### `account.move` (Defined in `farm_multi_farm_financial`)
  - **Class**: `AccountMove`
  - **描述**: 
  - _inherit_: `account.move`


### `agri.biological.asset.fair.valuation` (Defined in `farm_valuation`)
  - **Class**: `BiologicalAssetFairValuation`
  - **描述**: Biological Asset Fair Value Valuation

  - **核心字段**:
    - `name` (Char): Valuation Reference
    - `asset_id` (Many2one): agri.biological.asset
    - `valuation_date` (Date): Valuation Date
    - `current_growth_progress` (Float): Current Growth Progress %
    - `target_yield` (Float): Target Yield
    - `current_yield_potential` (Float): Current Yield Potential
    - `market_price` (Float): Market Price (per unit)
    - `market_price_source` (Char): Market Price Source
    - `fair_value` (Float): Fair Value
    - `valuation_method` (Selection): valuation_method
    - `previous_valuation` (Float): Previous Valuation
    - `revaluation_amount` (Float): Revaluation Amount
    - `revaluation_type` (Selection): revaluation_type
    - `journal_entry_id` (Many2one): account.move
    - `is_accounting_entry_created` (Boolean): Accounting Entry Created
    - *... 以及其他 2 个业务字段*

### `agri.cost.calculation.line` (Defined in `farm_financial_basic`)
  - **Class**: `AgriCostCalculationLine`
  - **描述**: Agricultural Cost Calculation Line

  - **核心字段**:
    - `calculation_id` (Many2one): agri.cost.calculation
    - `template_id` (Many2one): agri.cost.template
    - `quantity` (Float): Quantity
    - `unit_cost` (Float): Unit Cost
    - `total_cost` (Float): Total Cost

### `agri.cost.calculation` (Defined in `farm_financial_basic`)
  - **Class**: `AgriCostCalculation`
  - **描述**: Agricultural Cost Calculation

  - **核心字段**:
    - `task_id` (Many2one): project.task
    - `land_parcel_id` (Many2one): farm.location
    - `area_value` (Float): Area Value
    - `area_unit` (Selection): area_unit
    - `total_seedling_cost` (Float): Total Seedling Cost
    - `total_fertilizer_cost` (Float): Total Fertilizer Cost
    - `total_pesticide_cost` (Float): Total Pesticide Cost
    - `total_labor_cost` (Float): Total Labor Cost
    - `total_machinery_cost` (Float): Total Machinery Cost
    - `total_irrigation_cost` (Float): Total Irrigation Cost
    - `total_other_cost` (Float): Total Other Cost
    - `total_cost` (Float): Total Calculated Cost
    - `cost_line_ids` (One2many): agri.cost.calculation.line

### `agri.cost.template` (Defined in `farm_financial_basic`)
  - **Class**: `AgriCostTemplate`
  - **描述**: Agricultural Cost Template
  - _inherit_: `mail.thread, mail.activity.mixin`
  - **核心字段**:
    - `name` (Char): Template Name
    - `code` (Char): Template Code
    - `category` (Selection): category
    - `unit_type` (Selection): unit_type
    - `unit_cost` (Float): Unit Cost
    - `description` (Text): Description
    - `is_active` (Boolean): Active
    - `labor_type` (Selection): labor_type
    - `machinery_type` (Selection): machinery_type
    - `fertilizer_type` (Selection): fertilizer_type
    - `pesticide_type` (Selection): pesticide_type

### `agri.industry.initialization.wizard` (Defined in `farm_financial_credit`)
  - **Class**: `AgriIndustryInitializationWizard`
  - **描述**: Industry Initialization Wizard

  - **核心字段**:
    - `industry_type` (Selection): industry_type
    - `include_varieties` (Boolean): Include Common Varieties
    - `include_growth_stages` (Boolean): Include Growth Stages
    - `include_agri_uom` (Boolean): Include Agricultural UOM
    - `include_task_templates` (Boolean): Include Task Templates
    - `include_quality_standards` (Boolean): Include Quality Standards

### `cooperative.entity` (Defined in `farm_multi_farm_financial`)
  - **Class**: `CooperativeEntityExtensionFinancial`
  - **描述**: 
  - _inherit_: `cooperative.entity`
  - **核心字段**:
    - `dividend_distribution_ids` (One2many): dividend.distribution
    - `internal_credit_ids` (One2many): internal.credit
    - `cooperative_treasury_ids` (One2many): cooperative.treasury
    - `internal_loan_ids` (One2many): internal.loan
    - `subsidy_disbursement_ids` (One2many): subsidy.disbursement
    - `cooperative_decision_ids` (One2many): cooperative.decision
    - `multi_sign_process_ids` (One2many): multi.sign.process

### `cooperative.member` (Defined in `farm_multi_farm_financial`)
  - **Class**: `CooperativeMemberExtensionFinancial`
  - **描述**: 
  - _inherit_: `cooperative.member`
  - **核心字段**:
    - `share_transaction_ids` (One2many): share.transaction
    - `dividend_line_ids` (One2many): dividend.line
    - `credit_transaction_ids` (One2many): credit.transaction
    - `internal_marketplace_transaction_supplier_ids` (One2many): internal.marketplace.transaction
    - `internal_marketplace_transaction_requester_ids` (One2many): internal.marketplace.transaction
    - `borrower_loan_ids` (One2many): internal.loan
    - `lender_loan_ids` (One2many): internal.loan
    - `subsidy_line_ids` (One2many): subsidy.disbursement.line
    - `sign_process_ids` (One2many): multi.sign.line

### `farm.industry.initialization` (Defined in `farm_financial_credit`)
  - **Class**: `FarmIndustryInitialization`
  - **描述**: Farm Industry Initialization

  - **核心字段**:
    - `name` (Char): Package Name
    - `industry_code` (Char): Industry Code
    - `description` (Text): Description
    - `is_active` (Boolean): Is Active
    - `version` (Char): Version
    - `has_varieties` (Boolean): Has Varieties
    - `has_growth_stages` (Boolean): Has Growth Stages
    - `has_agri_uom` (Boolean): Has Agricultural UOM
    - `has_task_templates` (Boolean): Has Task Templates
    - `has_quality_standards` (Boolean): Has Quality Standards
    - `varieties_count` (Integer): Varieties Count
    - `tasks_count` (Integer): Task Templates Count
    - `stages_count` (Integer): Growth Stages Count

### `project.task` (Defined in `farm_financial_basic`)
  - **Class**: `ProjectTask`
  - **描述**: 
  - _inherit_: `project.task`
  - **核心字段**:
    - `analytic_account_id` (Many2one): account.analytic.account
    - `total_production_costs` (Float): total_production_costs

## 11. 精密制造与变量控制域 (Precision Production & VRA)
### `mrp.bom` (Defined in `farm_operation`)
  - **Class**: `MrpBom`
  - **描述**: 
  - _inherit_: `mrp.bom, mail.thread, mail.activity.mixin`
  - **核心字段**:
    - `master_recipe_version` (Integer): Master Recipe Version
    - `master_recipe_phase_ids` (One2many): agri.master.bom.phase
    - `required_workcenter_id` (Many2one): mrp.workcenter
    - `ambient_requirement` (Text): Ambient Constraints
    - `recipe_batch_size` (Float): Recipe Batch Size
    - `production_drive_type` (Selection): production_drive_type

### `mrp.production` (Defined in `farm_operation`)
  - **Class**: `MrpProductionExtension`
  - **描述**: 
  - _inherit_: `mrp.production`


### `mrp.production` (Defined in `farm_operation`)
  - **Class**: `MrpProduction`
  - **描述**: 
  - _inherit_: `mrp.production, agri.precision.mixin`
  - **核心字段**:
    - `display_name_agri` (Char): Intervention Label

### `mrp.production` (Defined in `farm_operation`)
  - **Class**: `MrpProduction`
  - **描述**: 
  - _inherit_: `mrp.production, farm.operation.mixin`
  - **核心字段**:
    - `production_drive_type` (Selection): production_drive_type
    - `assigned_workcenter_id` (Many2one): mrp.workcenter
    - `recipe_phase_ids` (One2many): agri.bom.phase
    - `vra_prescription_id` (Many2one): agri.intervention.vra.prescription
    - `active_recipe_phase_ids` (Many2many): agri.bom.phase
    - `active_recipe_phase_id` (Many2one): agri.bom.phase
    - `phase_start_datetime` (Datetime): Global Recipe Start
    - `progress_percentage` (Float): Progress %

### `mrp.workorder` (Defined in `farm_operation`)
  - **Class**: `MrpWorkorderExtension`
  - **描述**: 
  - _inherit_: `mrp.workorder`
  - **核心字段**:
    - `active_execution_phase_id` (Many2one): agri.bom.phase

### `mrp.workorder` (Defined in `farm_operation`)
  - **Class**: `MrpWorkorder`
  - **描述**: 
  - _inherit_: `mrp.workorder, farm.operation.mixin`
  - **核心字段**:
    - `production_drive_type` (Selection): production_drive_type
    - `is_intervention_required` (Boolean): Intervention Needed

### `agri.graded.output` (Defined in `farm_operation`)
  - **Class**: `PrecisionGradedOutput`
  - **描述**: Graded Output Worklist

  - **核心字段**:
    - `res_model` (Char): Related Model
    - `res_id` (Many2oneReference): Related Record
    - `product_id` (Many2one): product.product
    - `grade` (Selection): grade
    - `quantity` (Float): Actual Quantity
    - `move_id` (Many2one): stock.move
    - `notes` (Text): Notes

### `agri.intervention.basis` (Defined in `farm_operation`)
  - **Class**: `PrecisionInterventionBasis`
  - **描述**: Intervention Rationale

  - **核心字段**:
    - `name` (Char): Evidence Summary
    - `source_type` (Selection): source_type
    - `parameter_name` (Char): Parameter
    - `recipe_standard_value` (Float): Standard
    - `actual_measured_value` (Float): Actual
    - `deviation_delta` (Float): Delta
    - `res_model` (Char): Related Model
    - `res_id` (Many2oneReference): Related Record
    - `create_date` (Datetime): Captured At

### `agri.intervention.log` (Defined in `farm_operation`)
  - **Class**: `PrecisionInterventionLog`
  - **描述**: Intervention Audit Log

  - **核心字段**:
    - `name` (Char): Action
    - `intervention_type` (Selection): intervention_type
    - `basis_id` (Many2one): agri.intervention.basis
    - `res_model` (Char): Related Model
    - `res_id` (Many2oneReference): Related Record
    - `user_id` (Many2one): res.users
    - `create_date` (Datetime): Timestamp

### `iiot.device` (Defined in `farm_iot`)
  - **Class**: `PrecisionIotDevice`
  - **描述**: Precision Production IoT Device (Integrated with Industrial IoT)

  - **核心字段**:
    - `iiot_device_id` (Many2one): iiot.device
    - `name` (Char): Device Name
    - `device_type` (Selection): device_type
    - `description` (Text): Description
    - `is_active` (Boolean): Active
    - `production_line_id` (Many2one): mrp.workcenter
    - `last_seen` (Datetime): Last Communication
    - `is_connected` (Boolean): Connected
    - `status` (Selection): status
    - `firmware_version` (Char): Firmware Version
    - `sensor_ids` (One2many): iiot.sensor
    - `reading_ids` (One2many): iiot.reading

### `iiot.reading` (Defined in `farm_iot`)
  - **Class**: `PrecisionIotReading`
  - **描述**: Precision Production IoT Reading (Integrated with Industrial IoT)

  - **核心字段**:
    - `name` (Char): Reading Reference
    - `device_id` (Many2one): iiot.device
    - `sensor_id` (Many2one): iiot.sensor
    - `parameter_name` (Char): parameter_name
    - `value` (Float): Value
    - `uom` (Char): Unit of Measure
    - `read_datetime` (Datetime): Reading Time
    - `is_valid` (Boolean): Valid
    - `validation_message` (Char): Validation Message
    - `production_id` (Many2one): mrp.production
    - `phase_id` (Many2one): agri.bom.phase
    - `workorder_id` (Many2one): mrp.workorder
    - `deviation_percent` (Float): Deviation (%)
    - `is_deviation_critical` (Boolean): Critical Deviation
    - `raw_data` (Text): Raw Data

### `iiot.sensor` (Defined in `farm_iot`)
  - **Class**: `PrecisionIotSensor`
  - **描述**: Precision Production IoT Sensor (Integrated with Industrial IoT)

  - **核心字段**:
    - `name` (Char): Sensor Name
    - `sensor_id` (Char): Sensor ID
    - `device_id` (Many2one): iiot.device
    - `sensor_type` (Selection): sensor_type
    - `parameter_name` (Char): Parameter Name
    - `description` (Text): Description
    - `is_active` (Boolean): Active
    - `is_calibrated` (Boolean): Calibrated
    - `calibration_date` (Date): Last Calibration Date
    - `calibration_next` (Date): Next Calibration Due
    - `unit_of_measure` (Char): Unit of Measure
    - `min_range` (Float): Minimum Range
    - `max_range` (Float): Maximum Range
    - `tolerance_percent` (Float): Tolerance (%)
    - `current_value` (Float): Current Value
    - *... 以及其他 4 个业务字段*

### `agri.master.bom.material` (Defined in `farm_operation`)
  - **Class**: `PrecisionMasterRecipeMaterial`
  - **描述**: Master Recipe Material Template

  - **核心字段**:
    - `phase_id` (Many2one): agri.master.bom.phase
    - `product_id` (Many2one): product.product
    - `quantity` (Float): Qty (per Batch Size)
    - `uom_id` (Many2one): uom.uom

### `agri.master.bom.parameter` (Defined in `farm_operation`)
  - **Class**: `PrecisionMasterRecipeParameter`
  - **描述**: Master Recipe Parameter Template

  - **核心字段**:
    - `bom_id` (Many2one): mrp.bom
    - `phase_id` (Many2one): agri.master.bom.phase
    - `name` (Char): Parameter Name
    - `target_value` (Float): Target Setpoint
    - `is_scalable` (Boolean): Scales with Batch Size
    - `tolerance_percent` (Float): Tolerance (%)
    - `uom_id` (Many2one): uom.uom

### `agri.master.bom.phase` (Defined in `farm_operation`)
  - **Class**: `PrecisionMasterRecipePhase`
  - **描述**: Master Recipe Phase Template

  - **核心字段**:
    - `bom_id` (Many2one): mrp.bom
    - `name` (Char): Phase Name
    - `sequence` (Integer): Sequence
    - `master_parameter_ids` (One2many): agri.master.bom.parameter
    - `master_material_ids` (One2many): agri.master.bom.material
    - `duration_expected` (Float): Planned Duration (Hours)
    - `sampling_plan` (Char): Sampling Plan
    - `required_workcenter_id` (Many2one): mrp.workcenter
    - `required_role` (Selection): required_role

### `agri.bom.control` (Defined in `farm_iot`)
  - **Class**: `PrecisionRecipeControl`
  - **描述**: Recipe-specific IoT Edge

  - **核心字段**:
    - `name` (Char): Bridge Name
    - `iiot_device_id` (Many2one): iiot.device
    - `mqtt_topic` (Char): MQTT Setpoint Topic
    - `recipe_parameter_id` (Many2one): agri.bom.parameter
    - `last_sync_value` (Float): Last Value

### `agri.bom.phase` (Defined in `farm_operation`)
  - **Class**: `PrecisionRecipePhase`
  - **描述**: 
  - _inherit_: `agri.bom.phase, agri.precision.mixin`


### `agri.bom.phase` (Defined in `farm_iot`)
  - **Class**: `PrecisionRecipePhaseIot`
  - **描述**: 
  - _inherit_: `agri.bom.phase`
  - **核心字段**:
    - `iot_device_ids` (Many2many): iiot.device
    - `iot_connected` (Boolean): IoT Connected
    - `iot_disconnected` (Boolean): IoT Disconnected
    - `iot_warning` (Boolean): IoT Warning
    - `iot_error` (Boolean): IoT Error
    - `iot_device_status` (Char): IoT Device Status
    - `iot_readings_count` (Integer): IoT Readings Count

### `product.template` (Defined in `farm_operation`)
  - **Class**: `ProductTemplate`
  - **描述**: 
  - _inherit_: `product.template`
  - **核心字段**:
    - `production_drive_type` (Selection): production_drive_type

### `stock.lot` (Defined in `farm_operation`)
  - **Class**: `StockLot`
  - **描述**: 
  - _inherit_: `stock.lot, agri.precision.mixin`


### `stock.lot` (Defined in `farm_operation`)
  - **Class**: `StockLot`
  - **描述**: 
  - _inherit_: `stock.lot, farm.operation.mixin`
  - **核心字段**:
    - `quality_grade` (Selection): quality_grade

## 12. 畜牧与动物资产域 (Livestock Management)
### `farm.livestock.bom.line` (Defined in `farm_livestock`)
  - **Class**: `FarmLivestockBomLine`
  - **描述**: Livestock BOM Component (ISL Layer)

  - **核心字段**:
    - `bom_line_id` (Many2one): mrp.bom.line
    - `dilution_ratio` (Float): Dilution Ratio (1:N)
    - `feeding_ratio` (Float): Feeding Ratio (%)
    - `feed_purpose` (Selection): feed_purpose

### `farm.livestock.event` (Defined in `farm_livestock`)
  - **Class**: `FarmLivestockEvent`
  - **描述**: Livestock Lifecycle Event

  - **核心字段**:
    - `lot_id` (Many2one): stock.lot
    - `event_type` (Selection): event_type
    - `event_date` (Datetime): Event Date
    - `location_id` (Many2one): farm.location
    - `responsible_id` (Many2one): res.users
    - `notes` (Text): Notes
    - `measured_weight` (Float): Measured Weight (kg)
    - `medicine_id` (Many2one): product.product
    - `dosage` (Float): Dosage
    - `uom_id` (Many2one): uom.uom
    - `is_anomaly` (Boolean): Anomaly Flag
    - `alert_severity` (Selection): alert_severity

### `farm.livestock.house.env` (Defined in `farm_livestock`)
  - **Class**: `FarmLivestockHouseEnv`
  - **描述**: Livestock House Environment Log

  - **核心字段**:
    - `location_id` (Many2one): farm.location
    - `capture_time` (Datetime): Capture Time
    - `temperature` (Float): Temperature (℃)
    - `humidity` (Float): Humidity (%)
    - `ammonia_level` (Float): Ammonia (ppm)
    - `co2_level` (Float): CO2 (ppm)
    - `comfort_index` (Float): Comfort Index

### `mrp.bom` (Defined in `farm_livestock`)
  - **Class**: `MrpBom`
  - **描述**: 
  - _inherit_: `mrp.bom`
  - **核心字段**:
    - `industry_type` (Selection): industry_type

### `mrp.production` (Defined in `farm_livestock`)
  - **Class**: `MrpProduction`
  - **描述**: 
  - _inherit_: `mrp.production`


### `stock.lot` (Defined in `farm_livestock`)
  - **Class**: `StockLot`
  - **描述**: 
  - _inherit_: `stock.lot`


## 13. 水产与高密度养殖域 (Aquaculture)
### `farm.aquaculture.bom.line` (Defined in `farm_aquaculture`)
  - **Class**: `FarmAquacultureBomLine`
  - **描述**: Aquaculture BOM Component (ISL Layer)

  - **核心字段**:
    - `bom_line_id` (Many2one): mrp.bom.line
    - `dose_rate_ppm` (Float): Dose Rate (ppm)
    - `application_method` (Selection): application_method
    - `water_condition` (Selection): water_condition

### `farm.aquaculture.bom` (Defined in `farm_aquaculture`)
  - **Class**: `FarmAquacultureBom`
  - **描述**: Aquaculture Stocking Recipe
  - _inherit_: `agri.bom.mixin`
  - **核心字段**:
    - `bom_id` (Many2one): mrp.bom
    - `min_dissolved_oxygen` (Float): Min Dissolved Oxygen (mg/L)
    - `optimal_temp_range` (Char): Optimal Temp Range (℃)
    - `max_stocking_density` (Float): Max Density (kg/m³)

### `farm.aquaculture.lss` (Defined in `farm_aquaculture`)
  - **Class**: `FarmAquacultureLSS`
  - **描述**: Life Support System Unit
  - _inherit_: `agri.resource.consumption.mixin`
  - **核心字段**:
    - `workcenter_id` (Many2one): mrp.workcenter
    - `lss_type` (Selection): lss_type
    - `last_service_date` (Date): Last Maintenance
    - `uv_bulb_hours` (Integer): UV Bulb Hours
    - `filter_backwash_frequency` (Integer): Backwash Frequency (Daily)

### `farm.aquaculture.production` (Defined in `farm_aquaculture`)
  - **Class**: `FarmAquacultureProduction`
  - **描述**: Aquaculture Growth Order
  - _inherit_: `agri.intervention.mixin, agri.agent.instruction.mixin, agri.incident.alert.mixin, agri.odoo19.performance.security.mixin`
  - **核心字段**:
    - `current_density` (Float): Current Density (kg/m³)
    - `aquaculture_config` (Json): Aquaculture Configuration
    - `production_id` (Many2one): mrp.production
    - `latest_do_level` (Float): Latest Dissolved Oxygen (mg/L)
    - `latest_water_temp` (Float): Latest Temp (℃)

### `farm.lot.aquaculture` (Defined in `farm_aquaculture`)
  - **Class**: `FarmLotAquaculture`
  - **描述**: Aquaculture Asset Batch
  - _inherit_: `agri.biological.inventory.mixin, agri.geospatial.mixin`
  - **核心字段**:
    - `lot_id` (Many2one): stock.lot
    - `water_volume_m3` (Float): Water Volume (m³)
    - `current_density` (Float): Current Density (kg/m³)

### `farm.ras.production` (Defined in `farm_aquaculture`)
  - **Class**: `FarmRasProduction`
  - **描述**: RAS Culture Order
  - _inherit_: `agri.intervention.mixin, agri.quality.gate.mixin, agri.agent.instruction.mixin`
  - **核心字段**:
    - `production_id` (Many2one): mrp.production
    - `predicted_ammonia_load` (Float): Predicted TAN Load (mg/L)
    - `total_energy_kwh` (Float): Total Energy Used (kWh)

### `mrp.bom` (Defined in `farm_aquaculture`)
  - **Class**: `MrpBom`
  - **描述**: 
  - _inherit_: `mrp.bom`
  - **核心字段**:
    - `industry_type` (Selection): industry_type

### `mrp.production` (Defined in `farm_aquaculture`)
  - **Class**: `MrpProduction`
  - **描述**: 
  - _inherit_: `mrp.production`


### `stock.lot` (Defined in `farm_aquaculture`)
  - **Class**: `StockLot`
  - **描述**: 
  - _inherit_: `stock.lot`


## 14. 大田作物域 (Field Crops)
### `farm.crop.bom.line` (Defined in `farm_field_crops`)
  - **Class**: `FarmCropBomLine`
  - **描述**: Crop BOM Component (ISL Layer)

  - **核心字段**:
    - `bom_line_id` (Many2one): mrp.bom.line
    - `application_rate` (Float): Application Rate (per Ha/Liter)
    - `spray_volume` (Float): Spray Volume (L/Ha)
    - `weather_condition` (Selection): weather_condition
    - `safety_interval_days` (Integer): Safety Interval (Days)

### `farm.crop.bom` (Defined in `farm_field_crops`)
  - **Class**: `FarmCropBom`
  - **描述**: Crop Farming Recipe (ISL Layer)
  - _inherit_: `agri.bom.mixin, agri.nutrient.mixin`
  - **核心字段**:
    - `bom_id` (Many2one): mrp.bom
    - `target_yield_mu` (Float): Target Yield per Mu (kg)
    - `growing_season` (Selection): growing_season
    - `phi_days` (Integer): Pre-Harvest Interval (PHI) Days

### `farm.crop.lot` (Defined in `farm_field_crops`)
  - **Class**: `FarmCropLot`
  - **描述**: Crop Harvest Batch (ISL Layer)
  - _inherit_: `agri.traceability.mixin, agri.nutrient.mixin`
  - **核心字段**:
    - `lot_id` (Many2one): stock.lot
    - `plot_origin_id` (Many2one): farm.location
    - `moisture_content` (Float): Grain Moisture (%)
    - `protein_content` (Float): Protein Content (%)

### `farm.crop.production` (Defined in `farm_field_crops`)
  - **Class**: `FarmCropProduction`
  - **描述**: Crop Farming Task (ISL Layer)
  - _inherit_: `agri.intervention.mixin, agri.weather.sensitive.mixin, agri.agent.instruction.mixin, agri.resource.consumption.mixin`
  - **核心字段**:
    - `production_id` (Many2one): mrp.production
    - `is_vra_enabled` (Boolean): Enable Variable Rate Application
    - `prescription_json` (Text): Prescription Map (JSON)

### `farm.field.crop.operation` (Defined in `farm_field_crops`)
  - **Class**: `FieldCropOperation`
  - **描述**: Field Crop Operation
  - _inherit_: `mail.thread, mail.activity.mixin`
  - **核心字段**:
    - `operation_id` (Many2one): project.task
    - `seeding_rate` (Float): seeding_rate
    - `fertilizer_application_rate` (Float): fertilizer_application_rate
    - `irrigation_schedule` (Char): irrigation_schedule
    - `crop_rotation_sequence` (Integer): crop_rotation_sequence
    - `planting_density` (Float): planting_density
    - `crop_type_id` (Many2one): product.template
    - `field_parcel_id` (Many2one): stock.location
    - `expected_yield` (Float): expected_yield

### `mrp.bom` (Defined in `farm_field_crops`)
  - **Class**: `MrpBom`
  - **描述**: 
  - _inherit_: `mrp.bom`
  - **核心字段**:
    - `industry_type` (Selection): industry_type

### `mrp.production` (Defined in `farm_field_crops`)
  - **Class**: `MrpProduction`
  - **描述**: 
  - _inherit_: `mrp.production`


### `stock.lot` (Defined in `farm_field_crops`)
  - **Class**: `StockLot`
  - **描述**: 
  - _inherit_: `stock.lot`


## 15. 系统级抽象特性 (Abstract Mixins)
### `agri.agricultural.campaign.mixin` (Defined in `farm_operation`)
  - **Class**: `AgriAgriculturalCampaignMixin`
  - **描述**: Agri Agricultural Campaign Shared Logic

  - **核心字段**:
    - `name` (Char): Season Name
    - `date_start` (Date): Start Date
    - `date_end` (Date): End Date
    - `is_active` (Boolean): Active
    - `description` (Text): Description
    - `base_temperature` (Float): Base Temp (℃)
    - `target_gdd` (Float): Target GDD
    - `accumulated_gdd` (Float): Current GDD
    - `predicted_harvest_date` (Float): Predicted Harvest
    - `land_parcel_id` (Many2one): farm.location

### `agri.batch.operation.mixin` (Defined in `farm_core`)
  - **Class**: `AgriBatchOperationMixin`
  - **描述**: Agricultural Batch Operation Mixin



### `agri.biological.asset.mixin` (Defined in `farm_core`)
  - **Class**: `AgriBiologicalAssetMixin`
  - **描述**: Agricultural Biological Traits Mixin

  - **核心字段**:
    - `agricultural_type` (Selection): agricultural_type
    - `birth_date` (Date): Birth/Germination Date
    - `maturity_date` (Date): Target Maturity Date
    - `is_mature` (Boolean): Physiological Maturity
    - `growth_stage_id` (Many2one): agri.industry.physio.stage
    - `dna_marker` (Char): Genetic Marker / DNA ID
    - `quality_grade` (Selection): quality_grade

### `agri.bom.line.mixin` (Defined in `farm_operation`)
  - **Class**: `AgriBomLineMixin`
  - **描述**: Agri Agricultural BOM Line Shared Logic

  - **核心字段**:
    - `dilution_ratio` (Float): Dilution Ratio (1:N)
    - `feeding_ratio` (Float): Feeding Ratio (%)

### `agri.bom.mixin` (Defined in `farm_operation`)
  - **Class**: `AgriBomMixin`
  - **描述**: Agri Agricultural BOM Shared Logic

  - **核心字段**:
    - `agri_activity_type` (Selection): agri_activity_type
    - `application_stage` (Selection): application_stage

### `agri.evidence.mixin` (Defined in `farm_core`)
  - **Class**: `AgriEvidenceMixin`
  - **描述**: Agri Evidence & Audit Mixin

  - **核心字段**:
    - `evidence_ids` (Many2many): ir.attachment
    - `evidence_hash` (Char): Evidence Hash
    - `evidence_source` (Selection): evidence_source
    - `is_verified` (Boolean): Evidence Verified
    - `verified_by_id` (Many2one): res.users
    - `verification_at` (Datetime): Verification Timestamp

### `agri.industry.planting.mixin` (Defined in `farm_core`)
  - **Class**: `AgriIndustryPlantingMixin`
  - **描述**: Agricultural Planting Standard Mixin

  - **核心字段**:
    - `phenology_stage_id` (Many2one): agri.industry.physio.stage
    - `seeding_depth` (Float): Target Seeding Depth (cm)
    - `target_plant_density` (Float): Target Plant Density (plants/ha)
    - `optimal_moisture_range` (Char): Optimal Moisture Range (%)

### `agri.industry.variety.mixin` (Defined in `farm_core`)
  - **Class**: `AgriIndustryVarietyMixin`
  - **描述**: Variety Traits Mixin

  - **核心字段**:
    - `scientific_name` (Char): Scientific Name
    - `breed_origin` (Char): Place of Origin
    - `resistance_level` (Selection): resistance_level

### `agri.inventory.mixin` (Defined in `farm_isl`)
  - **Class**: `AgriInventoryMixin`
  - **描述**: Agri Inventory ISL Abstract Base Model
  - _inherit_: `mail.thread, mail.activity.mixin`
  - **核心字段**:
    - `industry_type` (Selection): industry_type
    - `shelf_life_tracking` (Boolean): Shelf Life Tracking
    - `batch_tracking` (Boolean): Batch Tracking
    - `lot_tracking` (Boolean): Lot Tracking
    - `expiry_tracking` (Boolean): Expiry Tracking
    - `inventory_compliance` (Text): Inventory Compliance
    - `storage_requirements` (Text): Storage Requirements
    - `temperature_control` (Boolean): Temperature Control
    - `humidity_control` (Boolean): Humidity Control
    - `light_sensitive` (Boolean): Light Sensitive
    - `is_isl_model` (Boolean): Is ISL Model

### `agri.isl.model.redirector` (Defined in `farm_isl`)
  - **Class**: `AgriISLModelRedirector`
  - **描述**: Agri ISL Model Redirection Utility



### `agri.isl.optimization.mixin` (Defined in `farm_isl`)
  - **Class**: `AgriISLOptimizationMixin`
  - **描述**: Agri ISL Optimization Mixin



### `agri.manufacturing.mixin` (Defined in `farm_isl`)
  - **Class**: `AgriManufacturingMixin`
  - **描述**: Agri Manufacturing ISL Abstract Base Model
  - _inherit_: `mail.thread, mail.activity.mixin`
  - **核心字段**:
    - `industry_type` (Selection): industry_type
    - `industry_specialization` (Char): Industry Specialization
    - `compliance_requirements` (Text): Compliance Requirements
    - `industry_standards` (Char): Industry Standards
    - `safety_requirements` (Text): Safety Requirements
    - `quality_control_points` (Text): Quality Control Points
    - `industry_notes` (Html): Industry Notes
    - `industry_attachments` (Binary): Industry Attachments
    - `is_isl_model` (Boolean): Is ISL Model

### `agri.mcp.server` (Defined in `farm_ai_agent`)
  - **Class**: `MCPServer`
  - **描述**: Odoo MCP Service Provider



### `agri.odoo19.performance.security.mixin` (Defined in `farm_core`)
  - **Class**: `AgriOdoo19PerformanceSecurityMixin`
  - **描述**: Agricultural Odoo 19 Performance and Security Mixin

  - **核心字段**:
    - `config_settings` (Json): config_settings
    - `performance_metrics` (Json): performance_metrics
    - `security_level` (Selection): security_level
    - `access_log` (Json): access_log
    - `industry_access_control` (Json): industry_access_control

### `agri.product.mixin` (Defined in `farm_isl`)
  - **Class**: `AgriProductMixin`
  - **描述**: Agri Product ISL Abstract Base Model
  - _inherit_: `mail.thread, mail.activity.mixin`
  - **核心字段**:
    - `industry_type` (Selection): industry_type
    - `industry_category` (Char): Industry Category
    - `safety_data_sheet` (Binary): Safety Data Sheet
    - `safety_data_sheet_name` (Char): SDS Name
    - `regulatory_compliance` (Text): Regulatory Compliance
    - `shelf_life` (Float): Shelf Life (Days)
    - `storage_temperature` (Float): Storage Temperature (°C)
    - `storage_humidity` (Float): Storage Humidity (%)
    - `is_isl_model` (Boolean): Is ISL Model

### `agri.quality.mixin` (Defined in `farm_isl`)
  - **Class**: `AgriQualityMixin`
  - **描述**: Agri Quality Control ISL Abstract Base Model
  - _inherit_: `mail.thread, mail.activity.mixin`
  - **核心字段**:
    - `industry_type` (Selection): industry_type
    - `quality_standard` (Char): Quality Standard
    - `quality_procedures` (Html): Quality Procedures
    - `inspection_frequency` (Char): Inspection Frequency
    - `critical_control_points` (Text): Critical Control Points
    - `quality_metrics` (Text): Quality Metrics
    - `is_isl_model` (Boolean): Is ISL Model

### `agri.sales.purchase.mixin` (Defined in `farm_isl`)
  - **Class**: `AgriSalesPurchaseMixin`
  - **描述**: Agri Sales/Purchase ISL Abstract Base Model
  - _inherit_: `mail.thread, mail.activity.mixin`
  - **核心字段**:
    - `industry_type` (Selection): industry_type
    - `industry_certification` (Char): Industry Certification
    - `compliance_requirements` (Text): Compliance Requirements
    - `sales_compliance` (Text): Sales Compliance
    - `purchase_compliance` (Text): Purchase Compliance
    - `quality_assurance` (Boolean): Quality Assurance
    - `is_isl_model` (Boolean): Is ISL Model

### `agri.soil.analysis.mixin` (Defined in `farm_core`)
  - **Class**: `AgriSoilAnalysisMixin`
  - **描述**: Agricultural Soil Health Mixin

  - **核心字段**:
    - `ph_level` (Float): pH Level
    - `organic_matter` (Float): Organic Matter (%)
    - `nitrogen_content` (Float): Nitrogen (mg/kg)
    - `phosphorus_content` (Float): Phosphorus (mg/kg)
    - `potassium_content` (Float): Potassium (mg/kg)
    - `lead_content` (Float): Lead (Pb) (mg/kg)
    - `cadmium_content` (Float): Cadmium (Cd) (mg/kg)
    - `mercury_content` (Float): Mercury (Hg) (mg/kg)
    - `arsenic_content` (Float): Arsenic (As) (mg/kg)
    - `chromium_content` (Float): Chromium (Cr) (mg/kg)
    - `copper_content` (Float): Copper (Cu) (mg/kg)
    - `zinc_content` (Float): Zinc (Zn) (mg/kg)
    - `nickel_content` (Float): Nickel (Ni) (mg/kg)
    - `magnesium` (Float): Magnesium (mg/kg)
    - `calcium` (Float): Calcium (mg/kg)

### `agri.sustainability.algorithms` (Defined in `farm_esg_compliance`)
  - **Class**: `AgriSustainabilityAlgorithms`
  - **描述**: Sustainability Algorithms DNA



### `agri.view.mixin` (Defined in `farm_core`)
  - **Class**: `AgriViewMixin`
  - **描述**: Agri UI/UX View Adaptation Mixin



### `agri.view.mixin` (Defined in `farm_ux`)
  - **Class**: `AgriViewMixin`
  - **描述**: Global UI De-industrialization Injector



### `base.action.approve.mixin` (Defined in `farm_multi_farm`)
  - **Class**: `BaseActionApproveMixin`
  - **描述**: Base Action Approve Mixin



### `base.action.cancel.mixin` (Defined in `farm_multi_farm`)
  - **Class**: `BaseActionCancelMixin`
  - **描述**: Base Action Cancel Mixin



### `base.action.confirm.mixin` (Defined in `farm_multi_farm`)
  - **Class**: `BaseActionConfirmMixin`
  - **描述**: Base Action Confirm Mixin



### `base.action.reject.mixin` (Defined in `farm_multi_farm`)
  - **Class**: `BaseActionRejectMixin`
  - **描述**: Base Action Reject Mixin



### `base.amount.calculation.mixin` (Defined in `farm_multi_farm`)
  - **Class**: `BaseAmountCalculationMixin`
  - **描述**: Base Amount Calculation Mixin



### `base.available.amount.mixin` (Defined in `farm_multi_farm`)
  - **Class**: `BaseAvailableAmountMixin`
  - **描述**: Base Available Amount Mixin



### `base.available.credit.mixin` (Defined in `farm_multi_farm`)
  - **Class**: `BaseAvailableCreditMixin`
  - **描述**: Base Available Credit Mixin



### `base.certified.status.mixin` (Defined in `farm_multi_farm`)
  - **Class**: `BaseCertifiedStatusMixin`
  - **描述**: Base Certified Status Mixin



### `base.code.mixin` (Defined in `farm_multi_farm`)
  - **Class**: `BaseCodeMixin`
  - **描述**: Base Code Mixin



### `base.compliance.status.mixin` (Defined in `farm_multi_farm`)
  - **Class**: `BaseComplianceStatusMixin`
  - **描述**: Base Compliance Status Mixin



### `base.credit.limit.mixin` (Defined in `farm_multi_farm`)
  - **Class**: `BaseCreditLimitMixin`
  - **描述**: Base Credit Limit Mixin



### `base.investment.amount.mixin` (Defined in `farm_multi_farm`)
  - **Class**: `BaseInvestmentAmountMixin`
  - **描述**: Base Investment Amount Mixin



### `base.loan.amount.mixin` (Defined in `farm_multi_farm`)
  - **Class**: `BaseLoanAmountMixin`
  - **描述**: Base Loan Amount Mixin



### `base.net.amount.mixin` (Defined in `farm_multi_farm`)
  - **Class**: `BaseNetAmountMixin`
  - **描述**: Base Net Amount Mixin



### `base.sequence.mixin` (Defined in `farm_multi_farm`)
  - **Class**: `BaseSequenceMixin`
  - **描述**: Base Sequence Mixin



### `base.service.amount.mixin` (Defined in `farm_multi_farm`)
  - **Class**: `BaseServiceAmountMixin`
  - **描述**: Base Service Amount Mixin



### `base.settlement.direction.mixin` (Defined in `farm_multi_farm`)
  - **Class**: `BaseSettlementDirectionMixin`
  - **描述**: Base Settlement Direction Mixin



### `base.share.value.mixin` (Defined in `farm_multi_farm`)
  - **Class**: `BaseShareValueMixin`
  - **描述**: Base Share Value Mixin



### `base.total.amount.mixin` (Defined in `farm_multi_farm`)
  - **Class**: `BaseTotalAmountMixin`
  - **描述**: Base Total Amount Mixin



### `base.total.investment.mixin` (Defined in `farm_multi_farm`)
  - **Class**: `BaseTotalInvestmentMixin`
  - **描述**: Base Total Investment Mixin



### `farm.agri.science.mixin` (Defined in `farm_agri_science`)
  - **Class**: `AgriScienceMixin`
  - **描述**: Agri-Science Calculation Kernel

  - **核心字段**:
    - `physiology_profile_id` (Many2one): agri.physiology.profile
    - `cumulative_gdd` (Float): Cumulative GDD
    - `current_growth_stage_id` (Many2one): agri.growth.stage
    - `rue_actual` (Float): Radiation Use Efficiency (RUE)
    - `wue_actual` (Float): Water Use Efficiency (WUE)
    - `biological_stress_index` (Float): Stress Index (0-100)

### `farm.agricultural.bom.line.mixin` (Defined in `farm_operation`)
  - **Class**: `FarmAgriculturalBomLineMixin`
  - **描述**: Farm Agricultural BOM Line Shared Logic (Deprecated - Use agri.bom.line.mixin)
  - _inherit_: `agri.bom.line.mixin`


### `farm.agricultural.bom.mixin` (Defined in `farm_operation`)
  - **Class**: `FarmAgriculturalBomMixin`
  - **描述**: Farm Agricultural BOM Shared Logic (Deprecated - Use agri.bom.mixin)
  - _inherit_: `agri.bom.mixin`


### `farm.agricultural.campaign.base` (Defined in `farm_operation`)
  - **Class**: `FarmAgriculturalCampaignBase`
  - **描述**: Farm Agricultural Campaign Base Logic

  - **核心字段**:
    - `name` (Char): Season Name
    - `date_start` (Date): Start Date
    - `date_end` (Date): End Date
    - `is_active` (Boolean): Active
    - `description` (Text): Description
    - `base_temperature` (Float): Base Temp (℃)
    - `target_gdd` (Float): Target GDD
    - `accumulated_gdd` (Float): Current GDD
    - `predicted_harvest_date` (Date): Predicted Harvest
    - `land_parcel_id` (Many2one): farm.location

### `farm.agricultural.campaign.mixin` (Defined in `farm_operation`)
  - **Class**: `FarmAgriculturalCampaignMixin`
  - **描述**: Farm Agricultural Campaign Shared Logic (Deprecated - Use agri.agricultural.campaign.mixin)
  - _inherit_: `agri.agricultural.campaign.mixin`


### `farm.agricultural.intervention.mixin` (Defined in `farm_operation`)
  - **Class**: `FarmAgriculturalInterventionMixin`
  - **描述**: Farm Agricultural Intervention Shared Logic (Deprecated - Use agri.intervention.mixin)
  - _inherit_: `agri.intervention.mixin`


### `farm.core.common.fields` (Defined in `farm_core`)
  - **Class**: `CommonAgriculturalFields`
  - **描述**: Farm Core Common Fields

  - **核心字段**:
    - `agricultural_type` (Selection): agricultural_type
    - `identification_number` (Char): Identification No.
    - `batch_number` (Char): Batch Number
    - `growth_stage` (Selection): growth_stage
    - `generation` (Selection): generation
    - `n_content` (Float): Nitrogen (N) %
    - `p_content` (Float): Phosphorus (P) %
    - `k_content` (Float): Potassium (K) %
    - `growth_duration` (Integer): Growth Duration (Days)
    - `maturity_age_days` (Integer): Maturity Age (Days)
    - `quality_grade` (Selection): quality_grade
    - `withdrawal_period_days` (Integer): Withdrawal Period (Days)
    - `production_cycle` (Selection): production_cycle
    - `properties_definition` (PropertiesDefinition): Properties Definition
    - `company_id` (Many2one): res.company
    - *... 以及其他 1 个业务字段*

### `farm.core.gis.utils` (Defined in `farm_core`)
  - **Class**: `GISCoordinateUtils`
  - **描述**: Farm Core GIS Utilities



### `farm.inventory.mixin` (Defined in `farm_isl`)
  - **Class**: `AgriInventoryMixin`
  - **描述**: Farm Inventory ISL Abstract Base Model (Deprecated - Use agri.inventory.mixin)
  - _inherit_: `agri.inventory.mixin`


### `farm.manufacturing.mixin` (Defined in `farm_isl`)
  - **Class**: `AgriManufacturingMixin`
  - **描述**: Farm Manufacturing ISL Abstract Base Model (Deprecated - Use agri.manufacturing.mixin)
  - _inherit_: `agri.manufacturing.mixin`


### `farm.product.mixin` (Defined in `farm_isl`)
  - **Class**: `AgriProductMixin`
  - **描述**: Farm Product ISL Abstract Base Model (Deprecated - Use agri.product.mixin)
  - _inherit_: `agri.product.mixin`


### `agri.isl.quality.mixin` (Defined in `farm_isl`)
  - **Class**: `AgriQualityMixin`
  - **描述**: Farm Quality Control ISL Abstract Base Model (Deprecated - Use agri.quality.mixin)
  - _inherit_: `agri.quality.mixin`


### `farm.sales.purchase.mixin` (Defined in `farm_isl`)
  - **Class**: `AgriSalesPurchaseMixin`
  - **描述**: Farm Sales/Purchase ISL Abstract Base Model (Deprecated - Use agri.sales.purchase.mixin)
  - _inherit_: `agri.sales.purchase.mixin`


### `isl.model.redirector` (Defined in `farm_isl`)
  - **Class**: `ISLModelRedirector`
  - **描述**: ISL Model Redirection Utility (Deprecated - Use agri.isl.model.redirector)
  - _inherit_: `agri.isl.model.redirector`


### `isl.optimization.mixin` (Defined in `farm_isl`)
  - **Class**: `ISLOptimizationMixin`
  - **描述**: ISL Optimization Mixin (Deprecated - Use agri.isl.optimization.mixin)
  - _inherit_: `agri.isl.optimization.mixin`


### `mrp.bom.line.isl.abstract` (Defined in `farm_mrp`)
  - **Class**: `MrpBomLineIslAbstract`
  - **描述**: Abstract ISL for BOM Line



### `quality.based.pricing` (Defined in `farm_supply_quality`)
  - **Class**: `QualityBasedPricing`
  - **描述**: Quality-Based Pricing Rules
  - _inherit_: `mail.thread, mail.activity.mixin`
  - **核心字段**:
    - `name` (Char): Pricing Rule Name
    - `product_category_id` (Many2one): product.category
    - `quality_attribute` (Char): Quality Attribute
    - `base_price` (Float): Base Price
    - `min_value` (Float): Minimum Value for Premium
    - `max_value` (Float): Maximum Value for Premium
    - `premium_rate` (Float): Premium Rate (%)
    - `discount_rate` (Float): Discount Rate (%)
    - `active` (Boolean): Active
    - `purchase_order_id` (Many2one): purchase.order
    - `quality_min_threshold` (Float): Minimum Quality Threshold
    - `quality_max_threshold` (Float): Maximum Quality Threshold
    - `quality_grade_label` (Selection): quality_grade_label
    - `protein_content_coefficient` (Float): Protein Content Coefficient
    - `moisture_content_coefficient` (Float): Moisture Content Coefficient
    - *... 以及其他 4 个业务字段*

### `report.farm_green_monitor.reduction_trend_report` (Defined in `farm_green_monitor`)
  - **Class**: `FarmGreenMonitorReport`
  - **描述**: Fertilizer/Pesticide Reduction Trend Report



### `supply.chain.node.mixin` (Defined in `farm_supply_core`)
  - **Class**: `SupplyChainNodeMixin`
  - **描述**: Supply Chain Node Mixin (Deprecated - Use agri.supply.chain.node.mixin)
  - _inherit_: `agri.supply.chain.node.mixin`


### `supply.common.fields.mixin` (Defined in `farm_supply_core`)
  - **Class**: `SupplyCommonFieldsMixin`
  - **描述**: Supply Chain Common Fields Mixin

  - **核心字段**:
    - `is_compliance_approved` (Boolean): Compliance Approved
    - `compliance_date` (Date): Compliance Date
    - `safety_check_required` (Boolean): Safety Check Required
    - `quality_grade` (Selection): quality_grade
    - `quality_score` (Float): Quality Score
    - `shelf_life_days` (Integer): Shelf Life (Days)
    - `expiration_date` (Date): Expiration Date
    - `best_before_date` (Date): Best Before Date
    - `batch_number` (Char): Batch Number
    - `production_date` (Date): Production Date
    - `supplier_lot_number` (Char): Supplier Lot Number

## 16. 其他特定领域模型 (Other Domain Models)
### `accessibility.settings` (Defined in `farm_ux`)
  - **Class**: `AccessibilitySettings`
  - **描述**: Accessibility & Inclusive Design Settings

  - **核心字段**:
    - `name` (Char): Setting Name
    - `user_id` (Many2one): res.users
    - `screen_reader_enabled` (Boolean): Screen Reader Enabled
    - `keyboard_navigation` (Boolean): Keyboard Navigation
    - `font_scaling` (Float): Font Scaling Factor
    - `high_contrast_mode` (Boolean): High Contrast Mode
    - `large_touch_targets` (Boolean): Large Touch Targets
    - `reduced_motion` (Boolean): Reduced Motion
    - `color_blind_mode` (Boolean): Color Blind Mode
    - `inclusive_mode` (Boolean): Inclusive/Elder Mode
    - `voice_entry_enabled` (Boolean): Voice-First Entry
    - `voice_navigation` (Boolean): Voice Navigation
    - `hide_advanced_menus` (Boolean): Hide Advanced Menus
    - `simplified_kanban` (Boolean): Simplified Kanban Cards

### `agri.allergen` (Defined in `farm_processing`)
  - **Class**: `AgriAllergen`
  - **描述**: Agricultural Food Allergen

  - **核心字段**:
    - `name` (Char): Allergen Name
    - `code` (Char): Code
    - `description` (Text): Description

### `agri.biological.twin` (Defined in `farm_agri_science`)
  - **Class**: `AgriBiologicalTwin`
  - **描述**: Biological Digital Twin Engine
  - _inherit_: `mail.thread, mail.activity.mixin, agri.biological.asset.mixin`
  - **核心字段**:
    - `name` (Char): Twin Ref
    - `product_id` (Many2one): product.template
    - `location_id` (Many2one): farm.location
    - `start_date` (Date): Sowing/Start Date
    - `expected_harvest_date` (Date): Target Harvest Date
    - `accumulated_gdd` (Float): Accumulated GDD (℃)
    - `base_temp` (Float): Base Temperature (℃)
    - `target_gdd_harvest` (Float): Target GDD for Harvest
    - `current_stage_id` (Many2one): agri.industry.physio.stage
    - `health_score` (Float): Growth Health Score (0-100)
    - `predicted_yield` (Float): Predicted Yield (kg)
    - `confidence_level` (Selection): confidence_level
    - `accumulated_carbon` (Float): Accumulated Carbon (kg CO2e)
    - `carbon_intensity` (Float): Carbon Intensity (kg CO2e/kg yield)

### `agri.biological.twin` (Defined in `farm_greenhouse`)
  - **Class**: `FarmBiologicalTwin`
  - **描述**: 
  - _inherit_: `agri.biological.twin`


### `agri.ecological.activity` (Defined in `farm_ecology`)
  - **Class**: `AgriEcologicalActivity`
  - **描述**: Agricultural Ecological Activity
  - _inherit_: `mail.thread, mail.activity.mixin`
  - **核心字段**:
    - `name` (Char): Activity Name
    - `date` (Date): Date
    - `location_id` (Many2one): farm.location
    - `description` (Text): Description
    - `impact_category` (Selection): impact_category

### `agri.evidence` (Defined in `farm_mobile`)
  - **Class**: `AgriEvidence`
  - **描述**: Agricultural Field Evidence
  - _inherit_: `mail.thread, mail.activity.mixin`
  - **核心字段**:
    - `name` (Char): Evidence Label
    - `res_model` (Char): Related Model
    - `res_id` (Many2one_reference): Related ID
    - `photo` (Binary): Evidence Photo
    - `gps_lat` (Float): Latitude
    - `gps_lng` (Float): Longitude
    - `taken_at` (Datetime): Captured Time
    - `worker_id` (Many2one): hr.employee
    - `note` (Text): Field Notes
    - `is_on_site` (Boolean): Location Verified
    - `evidence_hash` (Char): Evidence Hash
    - `is_hash_verified` (Boolean): Hash Verified
    - `subsidy_application_id` (Many2one): farm.subsidy.application

### `agri.geospatial.grid.cell` (Defined in `farm_agri_science`)
  - **Class**: `AgriGeospatialGridCell`
  - **描述**: Agricultural Spatial Grid Cell

  - **核心字段**:
    - `location_id` (Many2one): farm.location
    - `name` (Char): Grid UID
    - `row` (Integer): Row Index
    - `col` (Integer): Column Index
    - `center_lat` (Float): Center Latitude
    - `center_lng` (Float): Center Longitude
    - `ndvi_index` (Float): NDVI (Satellite Index)
    - `soil_ph` (Float): Soil pH (Interpolated)
    - `soil_moisture` (Float): Soil Moisture (%)
    - `soil_nutrient_n` (Float): Soil Nitrogen (N) Level
    - `historical_rue` (Float): Historical RUE (g/MJ)
    - `lai_index` (Float): Leaf Area Index (LAI)
    - `water_stress` (Float): Water Stress Index
    - `cell_geojson` (Text): Cell Geometry (Polygon)

### `agri.gi.registry` (Defined in `farm_marketing`)
  - **Class**: `AgriGIRegistry`
  - **描述**: Geographical Indication Registry
  - _inherit_: `mail.thread, mail.activity.mixin`
  - **核心字段**:
    - `name` (Char): GI Name
    - `code` (Char): GI Code
    - `product_template_id` (Many2one): product.template
    - `protection_area_id` (Many2one): farm.location
    - `authority_name` (Char): Issuing Authority
    - `certificate_attachment_ids` (Many2many): ir.attachment
    - `is_active` (Boolean): Active
    - `description` (Text): GI Description

### `agri.growth.stage` (Defined in `farm_agri_science`)
  - **Class**: `AgriGrowthStage`
  - **描述**: Crop Growth Stage

  - **核心字段**:
    - `name` (Char): Stage Name
    - `profile_id` (Many2one): agri.physiology.profile
    - `gdd_threshold` (Float): GDD Threshold (Cumulative)
    - `stage_code` (Char): Stage Code (e.g. VE, V1, R1)
    - `description` (Text): Description

### `agri.health.schedule` (Defined in `farm_processing`)
  - **Class**: `AgriHealthSchedule`
  - **描述**: Agricultural Livestock Vaccination & Health Schedule

  - **核心字段**:
    - `name` (Char): name
    - `product_tmpl_id` (Many2one): product.template
    - `target_life_stage` (Selection): target_life_stage
    - `activity_summary` (Char): activity_summary
    - `activity_note` (Text): activity_note
    - `days_offset` (Integer): days_offset

### `agri.pest.disease` (Defined in `farm_knowledge`)
  - **Class**: `AgriPestDisease`
  - **描述**: Agricultural Pest & Disease Database
  - _inherit_: `mail.thread, mail.activity.mixin`
  - **核心字段**:
    - `name` (Char): name
    - `scientific_name` (Char): scientific_name
    - `category` (Selection): category
    - `symptoms` (Html): symptoms
    - `cause` (Text): cause
    - `prevention` (Html): prevention
    - `photo` (Binary): photo
    - `image_name` (Char): Image Name
    - `recommended_intervention_id` (Many2one): agri.intervention.template
    - `conventional_treatment` (Html): conventional_treatment
    - `organic_treatment` (Html): organic_treatment
    - `integrated_treatment` (Html): integrated_treatment
    - `conventional_products` (Many2many): product.template
    - `organic_products` (Many2many): product.template
    - `compliance_standards` (Char): compliance_standards
    - *... 以及其他 7 个业务字段*

### `agri.physiology.profile` (Defined in `farm_agri_science`)
  - **Class**: `AgriPhysiologyProfile`
  - **描述**: Crop Physiology Fingerprint

  - **核心字段**:
    - `name` (Char): Variety Name
    - `product_id` (Many2one): product.product
    - `temp_base` (Float): Base Temperature (T-base)
    - `temp_opt` (Float): Optimum Temperature (T-opt)
    - `temp_max` (Float): Maximum Temperature (T-max)
    - `logistic_l` (Float): Max Biomass (L)
    - `logistic_k` (Float): Growth Rate (k)
    - `logistic_gdd0` (Float): Inflexion GDD (GDD0)
    - `response_max_yield` (Float): Potential Max Yield (A)
    - `response_efficiency_c` (Float): Nutrient Efficiency Coefficient (c)
    - `stage_ids` (One2many): agri.growth.stage

### `agri.scenario.input.forecast` (Defined in `farm_planning`)
  - **Class**: `AgriScenarioInputForecast`
  - **描述**: Scenario Input Forecast

  - **核心字段**:
    - `scenario_id` (Many2one): agri.scenario
    - `product_id` (Many2one): product.product
    - `quantity` (Float): Forecasted Quantity

### `agri.scenario` (Defined in `farm_planning`)
  - **Class**: `AgriScenario`
  - **描述**: Planning Scenario (Simulation)
  - _inherit_: `mail.thread, mail.activity.mixin`
  - **核心字段**:
    - `name` (Char): Scenario Name
    - `route_id` (Many2one): agri.technical.route
    - `planned_area` (Float): Planned Area (Hectares)
    - `total_labor_forecast` (Float): Total Labor Forecast (Hours)
    - `input_forecast_ids` (One2many): agri.scenario.input.forecast

### `agri.service` (Defined in `farm_multi_farm`)
  - **Class**: `AgriService`
  - **描述**: Agricultural Service
  - _inherit_: `mail.thread, mail.activity.mixin`
  - **核心字段**:
    - `name` (Char): Service Name
    - `code` (Char): Service Code
    - `cooperative_id` (Many2one): cooperative.entity
    - `provider_member_id` (Many2one): cooperative.member
    - `service_category` (Selection): service_category
    - `capacity` (Float): Capacity
    - `capacity_unit` (Char): Capacity Unit
    - `unit_rate` (Float): Unit Rate
    - `currency_id` (Many2one): res.currency
    - `available_from` (Datetime): Available From
    - `available_to` (Datetime): Available To
    - `location` (Char): Service Location
    - `description` (Text): Description
    - `is_active` (Boolean): Is Active

### `agri.sustainability.biodiversity.indicator` (Defined in `farm_ecology`)
  - **Class**: `AgriBiodiversityIndicator`
  - **描述**: Biodiversity Observation Log
  - _inherit_: `mail.thread, mail.activity.mixin, agri.sustainability.mixin, agri.evidence.mixin`
  - **核心字段**:
    - `date` (Date): Observation Date
    - `location_id` (Many2one): farm.location
    - `indicator_type` (Selection): indicator_type
    - `species_name` (Char): Species/Common Name
    - `count_observed` (Integer): Population Abundance
    - `photo` (Binary): Photo Evidence
    - `notes` (Text): Contextual Notes

### `agri.sustainability.ecological.zone` (Defined in `farm_ecology`)
  - **Class**: `AgriEcologicalZone`
  - **描述**: Agricultural Ecological Infrastructure
  - _inherit_: `mail.thread, mail.activity.mixin, agri.geospatial.mixin`
  - **核心字段**:
    - `name` (Char): Ecological Zone Name
    - `zone_type` (Selection): zone_type
    - `area` (Float): Area (sqm)
    - `location_id` (Many2one): farm.location
    - `active` (Boolean): active

### `agri.technical.route.line` (Defined in `farm_planning`)
  - **Class**: `AgriTechnicalRouteLine`
  - **描述**: Route Sequence Line

  - **核心字段**:
    - `route_id` (Many2one): agri.technical.route
    - `sequence` (Integer): Sequence
    - `template_id` (Many2one): agri.intervention.template
    - `delay_days` (Integer): Delay from Start (Days)

### `agri.technical.route.line` (Defined in `farm_planning`)
  - **Class**: `AgriTechnicalRouteLine`
  - **描述**: Technical Route Sequence

  - **核心字段**:
    - `route_id` (Many2one): agri.technical.route
    - `sequence` (Integer): Sequence
    - `template_id` (Many2one): agri.intervention.template
    - `delay_from_start` (Integer): Delay Days (T+N)

### `agri.technical.route` (Defined in `farm_planning`)
  - **Class**: `AgriTechnicalRoute`
  - **描述**: 
  - _inherit_: `agri.technical.route`


### `agri.technical.route` (Defined in `farm_planning`)
  - **Class**: `AgriTechnicalRoute`
  - **描述**: Technical Route (Cultural Itinerary)
  - _inherit_: `mail.thread, mail.activity.mixin`
  - **核心字段**:
    - `name` (Char): Route Name
    - `activity_family` (Selection): activity_family
    - `line_ids` (One2many): agri.technical.route.line

### `agri.technical.route` (Defined in `farm_planning`)
  - **Class**: `AgriTechnicalRoute`
  - **描述**: Technical Route (Itinéraire Cultural)

  - **核心字段**:
    - `name` (Char): Route Name
    - `family` (Selection): family
    - `line_ids` (One2many): agri.technical.route.line

### `agri.weather.forecast` (Defined in `farm_weather`)
  - **Class**: `AgriWeatherForecast`
  - **描述**: Agricultural Weather Forecast

  - **核心字段**:
    - `date` (Date): Date
    - `location_id` (Many2one): farm.location
    - `temp_max` (Float): Max Temp (℃)
    - `temp_min` (Float): Min Temp (℃)
    - `precipitation` (Float): Precipitation (mm)
    - `condition` (Char): Condition
    - `icon` (Char): Icon ID
    - `humidity` (Float): Humidity (%)
    - `wind_speed` (Float): Wind Speed (m/s)
    - `is_warning` (Boolean): Weather Warning
    - `warning_type` (Selection): warning_type

### `agricultural.knowledge` (Defined in `farm_knowledge`)
  - **Class**: `AgriculturalKnowledge`
  - **描述**: Agricultural Knowledge Base
  - _inherit_: `mail.thread, mail.activity.mixin`
  - **核心字段**:
    - `name` (Char): name
    - `content` (Html): content
    - `category` (Selection): category
    - `knowledge_type` (Selection): knowledge_type
    - `tags` (Char): tags
    - `active` (Boolean): active
    - `author_id` (Many2one): res.users
    - `difficulty_level` (Selection): difficulty_level
    - `industry_specific` (Selection): industry_specific
    - `seasonality` (Selection): seasonality
    - `video_url` (Char): video_url
    - `attachment_ids` (Many2many): ir.attachment
    - `view_count` (Integer): view_count
    - `helpful_count` (Integer): helpful_count
    - `pest_disease_id` (Many2one): agri.pest.disease

### `contextual.help` (Defined in `farm_ux`)
  - **Class**: `ContextualHelp`
  - **描述**: Smart Contextual Help for Agricultural Operations

  - **核心字段**:
    - `name` (Char): Help Topic
    - `model_name` (Char): Model Name
    - `field_name` (Char): Field Name
    - `view_type` (Selection): view_type
    - `help_content` (Html): Help Content
    - `help_video_url` (Char): Video Tutorial URL
    - `help_image` (Binary): Help Image
    - `image_name` (Char): Image Name
    - `is_active` (Boolean): Is Active
    - `priority` (Integer): Priority
    - `target_roles` (Many2many): res.groups
    - `industry_context` (Selection): industry_context
    - `difficulty_level` (Selection): difficulty_level

### `cooperative.entity` (Defined in `farm_multi_farm`)
  - **Class**: `CooperativeEntityExtension`
  - **描述**: 
  - _inherit_: `cooperative.entity`
  - **核心字段**:
    - `member_ids` (One2many): cooperative.member
    - `agri_service_ids` (One2many): agri.service

### `cooperative.entity` (Defined in `farm_multi_farm`)
  - **Class**: `CooperativeEntityExtension`
  - **描述**: 
  - _inherit_: `cooperative.entity`
  - **核心字段**:
    - `member_ids` (One2many): cooperative.member
    - `share_transaction_ids` (One2many): share.transaction
    - `dividend_distribution_ids` (One2many): dividend.distribution
    - `internal_credit_ids` (One2many): internal.credit
    - `shared_machinery_ids` (One2many): shared.machinery.pool
    - `quality_control_standard_ids` (One2many): quality.control.standard
    - `joint_procurement_ids` (One2many): joint.procurement
    - `procurement_planning_ids` (One2many): procurement.planning
    - `agri_service_ids` (One2many): agri.service
    - `cooperative_treasury_ids` (One2many): cooperative.treasury
    - `internal_loan_ids` (One2many): internal.loan
    - `subsidy_disbursement_ids` (One2many): subsidy.disbursement
    - `cooperative_decision_ids` (One2many): cooperative.decision
    - `multi_sign_process_ids` (One2many): multi.sign.process
    - `joint_procurement_po_ids` (One2many): joint.procurement.po
    - *... 以及其他 2 个业务字段*

### `cooperative.entity` (Defined in `farm_multi_farm_equipment`)
  - **Class**: `CooperativeEntityExtensionEquipment`
  - **描述**: 
  - _inherit_: `cooperative.entity`
  - **核心字段**:
    - `shared_machinery_ids` (One2many): shared.machinery.pool

### `cooperative.entity` (Defined in `farm_multi_farm_procurement`)
  - **Class**: `CooperativeEntityExtensionProcurement`
  - **描述**: 
  - _inherit_: `cooperative.entity`
  - **核心字段**:
    - `joint_procurement_ids` (One2many): joint.procurement
    - `procurement_planning_ids` (One2many): procurement.planning
    - `joint_procurement_po_ids` (One2many): joint.procurement.po
    - `hub_spoke_distribution_ids` (One2many): hub.spoke.distribution
    - `netting_settlement_ids` (One2many): netting.settlement

### `cooperative.member` (Defined in `farm_multi_farm`)
  - **Class**: `CooperativeMemberExtension`
  - **描述**: 
  - _inherit_: `cooperative.member`
  - **核心字段**:
    - `service_order_ids` (One2many): service.order

### `cooperative.member` (Defined in `farm_multi_farm`)
  - **Class**: `CooperativeMemberExtension`
  - **描述**: 
  - _inherit_: `cooperative.member`
  - **核心字段**:
    - `share_transaction_ids` (One2many): share.transaction
    - `dividend_line_ids` (One2many): dividend.line
    - `credit_transaction_ids` (One2many): credit.transaction
    - `machinery_rental_ids` (One2many): machinery.rental
    - `internal_marketplace_transaction_supplier_ids` (One2many): internal.marketplace.transaction
    - `internal_marketplace_transaction_requester_ids` (One2many): internal.marketplace.transaction
    - `service_order_ids` (One2many): service.order
    - `borrower_loan_ids` (One2many): internal.loan
    - `lender_loan_ids` (One2many): internal.loan
    - `subsidy_line_ids` (One2many): subsidy.disbursement.line
    - `sign_process_ids` (One2many): multi.sign.line
    - `joint_procurement_po_member_ids` (One2many): joint.procurement.po.member
    - `hub_spoke_distribution_line_ids` (One2many): hub.spoke.distribution.line
    - `netting_settlement_ids` (One2many): netting.settlement

### `cooperative.member` (Defined in `farm_multi_farm_equipment`)
  - **Class**: `CooperativeMemberExtensionEquipment`
  - **描述**: 
  - _inherit_: `cooperative.member`
  - **核心字段**:
    - `machinery_rental_ids` (One2many): machinery.rental

### `cooperative.member` (Defined in `farm_multi_farm_procurement`)
  - **Class**: `CooperativeMemberExtensionProcurement`
  - **描述**: 
  - _inherit_: `cooperative.member`
  - **核心字段**:
    - `joint_procurement_po_member_ids` (One2many): joint.procurement.po.member
    - `hub_spoke_distribution_line_ids` (One2many): hub.spoke.distribution.line
    - `netting_settlement_ids` (One2many): netting.settlement

### `export.certificate` (Defined in `farm_sale_ch`)
  - **Class**: `ExportCertificate`
  - **描述**: Export Compliance Certificate

  - **核心字段**:
    - `order_id` (Many2one): sale.order
    - `product_name` (Char): Product Name
    - `destination_country` (Char): Destination Country
    - `certificate_number` (Char): Certificate Number
    - `issue_date` (Date): Issue Date
    - `valid_until` (Date): Valid Until
    - `inspector` (Char): Inspector
    - `compliance_details` (Text): Compliance Details
    - `is_active` (Boolean): Is Active
    - `attachment` (Binary): Certificate Attachment
    - `attachment_name` (Char): Attachment Name

### `export.country.standard` (Defined in `farm_sale_ch`)
  - **Class**: `ExportCountryStandard`
  - **描述**: 
  - _inherit_: `export.country.standard`
  - **核心字段**:
    - `import_date` (Datetime): Import Date
    - `imported_by` (Many2one): res.users
    - `custom_rules` (Text): Custom Rules
    - `last_updated` (Datetime): Last Updated
    - `update_frequency` (Selection): update_frequency
    - `contact_person` (Char): Contact Person
    - `official_source` (Char): Official Source
    - `next_review_date` (Date): Next Review Date

### `faq.entry` (Defined in `farm_knowledge`)
  - **Class**: `FAQEntry`
  - **描述**: Frequently Asked Questions

  - **核心字段**:
    - `sequence` (Integer): sequence
    - `question` (Char): question
    - `answer` (Html): answer
    - `category` (Selection): category
    - `active` (Boolean): active
    - `tags` (Char): tags
    - `target_model` (Char): Target Model
    - `knowledge_id` (Many2one): agricultural.knowledge

### `farm.allergen` (Defined in `farm_processing`)
  - **Class**: `FarmAllergen`
  - **描述**: Food Allergen (Deprecated - Use agri.allergen)
  - _inherit_: `agri.allergen`


### `farm.biosafety.access.log` (Defined in `farm_safety`)
  - **Class**: `FarmBiosafetyAccessLog`
  - **描述**: Bio-safety Access Log
  - _inherit_: `mail.thread, mail.activity.mixin`
  - **核心字段**:
    - `location_id` (Many2one): farm.location
    - `person_id` (Many2one): res.partner
    - `employee_id` (Many2one): hr.employee
    - `access_time` (Datetime): Access Time
    - `access_type` (Selection): access_type
    - `sanitization_confirmed` (Boolean): Sanitization Performed
    - `quarantine_period_passed` (Boolean): Quarantine Period Passed
    - `vehicle_plate` (Char): Vehicle Plate
    - `purpose` (Text): Purpose of Entry

### `farm.bom.grade.distribution` (Defined in `farm_processing`)
  - **Class**: `FarmBomGradeDistribution`
  - **描述**: Expected Grade Distribution in BOM

  - **核心字段**:
    - `bom_id` (Many2one): mrp.bom
    - `quality_grade` (Selection): quality_grade
    - `expected_percentage` (Float): Expected %

### `farm.bom.package.line` (Defined in `farm_processing`)
  - **Class**: `FarmBomPackageLine`
  - **描述**: BOM Finished Product Packaging Line

  - **核心字段**:
    - `bom_id` (Many2one): mrp.bom
    - `product_id` (Many2one): product.product
    - `package_level_id` (Many2one): farm.package.level
    - `quantity` (Float): quantity
    - `child_package_level_id` (Many2one): farm.package.level

### `farm.breeding.order` (Defined in `farm_breeding`)
  - **Class**: `FarmBreedingOrder`
  - **描述**: Nursery Growing Order
  - _inherit_: `agri.intervention.mixin, agri.quality.gate.mixin`
  - **核心字段**:
    - `production_id` (Many2one): mrp.production
    - `target_germination_rate` (Float): Target Germination (%)
    - `actual_germination_rate` (Float): Actual Germination (%)

### `farm.certification.dashboard` (Defined in `farm_certification`)
  - **Class**: `FarmCertificationDashboard`
  - **描述**: Certification Compliance Dashboard

  - **核心字段**:
    - `total_cert_count` (Integer): total_cert_count
    - `valid_cert_count` (Integer): valid_cert_count
    - `expired_cert_count` (Integer): expired_cert_count
    - `gap_cert_count` (Integer): gap_cert_count
    - `organic_cert_count` (Integer): organic_cert_count
    - `gap_compliant_count` (Integer): gap_compliant_count
    - `gap_audit_score_avg` (Float): gap_audit_score_avg
    - `expiring_cert_count` (Integer): expiring_cert_count
    - `expiring_certs` (Many2many): farm.gap.certification

### `farm.checkin` (Defined in `farm_mobile`)
  - **Class**: `FarmCheckIn`
  - **描述**: Agri Site Check-in
  - _inherit_: `mail.thread`
  - **核心字段**:
    - `name` (Char): Check-in ID
    - `worker_id` (Many2one): hr.employee
    - `intervention_id` (Many2one): mrp.production
    - `check_in_time` (Datetime): Check-in Time
    - `check_out_time` (Datetime): Check-out Time
    - `gps_lat` (Float): Check-in Latitude
    - `gps_lng` (Float): Check-in Longitude
    - `checkin_photo` (Binary): Site Photo
    - `is_on_site` (Boolean): On-site Verified
    - `site_distance` (Float): Distance to Site (m)

### `farm.aquaculture.bom` (Defined in `farm_processing`)
  - **Class**: `FarmChemicalBom`
  - **描述**: Chemical Processing BOM (ISL Layer)

  - **核心字段**:
    - `bom_id` (Many2one): mrp.bom
    - `hazard_class` (Selection): hazard_class
    - `reaction_temperature_limit` (Float): Max Reaction Temp (℃)

### `farm.aquaculture.production` (Defined in `farm_processing`)
  - **Class**: `FarmChemicalProduction`
  - **描述**: Chemical Production Order (ISL Layer)

  - **核心字段**:
    - `production_id` (Many2one): mrp.production
    - `leak_test_passed` (Boolean): Leak Test Passed
    - `solvent_recovery_qty` (Float): Solvent Recovered (L)

### `farm.consumer.feedback` (Defined in `farm_marketing`)
  - **Class**: `FarmConsumerFeedback`
  - **描述**: Consumer C2M Feedback

  - **核心字段**:
    - `lot_id` (Many2one): stock.lot
    - `product_id` (Many2one): product.template
    - `location_id` (Many2one): farm.location
    - `rating` (Selection): rating
    - `taste_score` (Integer): Taste/Sweetness Score (1-10)
    - `freshness_score` (Integer): Freshness Score (1-10)
    - `comment` (Text): Consumer Comments
    - `consumer_region` (Char): Consumer Region (City/Country)
    - `analysis_tag_ids` (Many2many): res.config.settings

### `farm.cooperative.member` (Defined in `farm_entity_reg`)
  - **Class**: `FarmCooperativeMember`
  - **描述**: Cooperative Member

  - **核心字段**:
    - `company_id` (Many2one): res.company
    - `partner_id` (Many2one): res.partner
    - `membership_date` (Date): Membership Date
    - `share_capital` (Float): Share Capital
    - `is_chairman` (Boolean): Is Chairman

### `farm.ecological.activity` (Defined in `farm_ecology`)
  - **Class**: `FarmEcologicalActivity`
  - **描述**: Ecological Maintenance Activity (Deprecated - Use agri.ecological.activity)
  - _inherit_: `agri.ecological.activity`


### `farm.entity` (Defined in `farm_multi_farm`)
  - **Class**: `FarmEntityExtension`
  - **描述**: 
  - _inherit_: `farm.entity`
  - **核心字段**:
    - `cooperative_member_ids` (One2many): cooperative.member

### `farm.entity` (Defined in `farm_multi_farm`)
  - **Class**: `FarmEntityExtension`
  - **描述**: 
  - _inherit_: `farm.entity`
  - **核心字段**:
    - `cooperative_member_ids` (One2many): cooperative.member

### `farm.equipment.checklist.line` (Defined in `farm_equipment`)
  - **Class**: `FarmEquipmentChecklistLine`
  - **描述**: Checklist Item

  - **核心字段**:
    - `checklist_id` (Many2one): farm.equipment.checklist
    - `name` (Char): Requirement
    - `is_mandatory` (Boolean): Mandatory
    - `requires_photo` (Boolean): Require Photo Evidence

### `farm.equipment.checklist` (Defined in `farm_equipment`)
  - **Class**: `FarmEquipmentChecklist`
  - **描述**: Equipment Pre-op Checklist

  - **核心字段**:
    - `name` (Char): Checklist Name
    - `equipment_type` (Selection): equipment_type
    - `line_ids` (One2many): farm.equipment.checklist.line
    - `active` (Boolean): active

### `farm.evidence` (Defined in `farm_mobile`)
  - **Class**: `FarmEvidence`
  - **描述**: Field Evidence (Deprecated - Use agri.evidence)
  - _inherit_: `agri.evidence`


### `farm.fermentation.order` (Defined in `farm_fermentation`)
  - **Class**: `FarmFermentationOrder`
  - **描述**: Fermentation Job
  - _inherit_: `agri.intervention.mixin, agri.agent.instruction.mixin, agri.incident.alert.mixin`
  - **核心字段**:
    - `production_id` (Many2one): mrp.production
    - `internal_temperature` (Float): Pit Temperature (℃)
    - `acidity_level` (Float): Current Acidity (pH)

### `farm.fermentation.vessel` (Defined in `farm_fermentation`)
  - **Class**: `FarmFermentationVessel`
  - **描述**: Fermentation Pit/Vessel
  - _inherit_: `agri.geospatial.mixin`
  - **核心字段**:
    - `workcenter_id` (Many2one): mrp.workcenter
    - `vessel_type` (Selection): vessel_type
    - `start_service_year` (Integer): Enable Year
    - `microbial_health_index` (Float): Microbial Health (0-100)

### `farm.flower.bom` (Defined in `farm_floriculture`)
  - **Class**: `FarmFlowerBom`
  - **描述**: Floral Recipe (ISL Layer)
  - _inherit_: `agri.bom.mixin`
  - **核心字段**:
    - `bom_id` (Many2one): mrp.bom
    - `recipe_type` (Selection): recipe_type
    - `target_light_hours` (Float): Target Light Hours
    - `target_temp_day` (Float): Target Day Temp
    - `target_temp_night` (Float): Target Night Temp
    - `target_temp_diff` (Float): Target DIF
    - `target_hydration_hours` (Float): Required Hydration (Hours)
    - `preservative_formula_notes` (Text): Preservative Formula Notes
    - `target_storage_temp` (Float): Target Storage Temp (℃)

### `farm.flower.order` (Defined in `farm_floriculture`)
  - **Class**: `FarmFlowerOrder`
  - **描述**: Floral Growing/Treatment Order (ISL Layer)
  - _inherit_: `agri.intervention.mixin, agri.growth.cycle.mixin, agri.quality.gate.mixin, agri.weather.sensitive.mixin, agri.agent.instruction.mixin`
  - **核心字段**:
    - `production_id` (Many2one): mrp.production
    - `source_nursery_batch_id` (Many2one): farm.nursery.batch
    - `actual_hydration_hours` (Float): Actual Hydration Duration

### `farm.greenhouse.control.action` (Defined in `farm_greenhouse`)
  - **Class**: `FarmGreenhouseControlAction`
  - **描述**: Greenhouse Control Action

  - **核心字段**:
    - `rule_id` (Many2one): farm.greenhouse.control.rule
    - `device_id` (Many2one): iiot.device
    - `command` (Char): MQTT Command
    - `value` (Char): Value/Setting

### `farm.greenhouse.control.rule` (Defined in `farm_greenhouse`)
  - **Class**: `FarmGreenhouseControlRule`
  - **描述**: Greenhouse Automation Rule

  - **核心字段**:
    - `name` (Char): Rule Name
    - `greenhouse_id` (Many2one): farm.location
    - `parameter` (Selection): parameter
    - `threshold_low` (Float): Low Threshold
    - `threshold_high` (Float): High Threshold
    - `action_ids` (One2many): farm.greenhouse.control.action
    - `active` (Boolean): active
    - `is_ai_controlled` (Boolean): AI/Twin Controlled
    - `ai_adjustment_log` (Text): AI Adjustment History

### `farm.greenhouse.energy.log` (Defined in `farm_greenhouse`)
  - **Class**: `FarmGreenhouseEnergyLog`
  - **描述**: Greenhouse Energy Consumption

  - **核心字段**:
    - `greenhouse_id` (Many2one): farm.location
    - `date` (Date): Date
    - `kwh_consumed` (Float): Electricity (kWh)
    - `water_consumed` (Float): Water (L)
    - `carbon_footprint` (Float): Estimated Carbon (kg CO2e)

### `farm.health.schedule` (Defined in `farm_processing`)
  - **Class**: `FarmHealthSchedule`
  - **描述**: Livestock Vaccination & Health Schedule (Deprecated - Use agri.health.schedule)
  - _inherit_: `agri.health.schedule`


### `farm.industry.workcenter` (Defined in `farm_processing`)
  - **Class**: `FarmIndustryWorkcenter`
  - **描述**: Specialized Production Facility (ISL Layer)

  - **核心字段**:
    - `workcenter_id` (Many2one): mrp.workcenter
    - `facility_type` (Selection): facility_type
    - `surface_area` (Float): Surface Area (sqm)
    - `volume_capacity` (Float): Volume Capacity (m3)
    - `has_climate_control` (Boolean): Climate Controlled
    - `main_sensor_topic` (Char): Primary Telemetry Topic

### `farm.lot.brew` (Defined in `farm_fermentation`)
  - **Class**: `FarmLotBrew`
  - **描述**: Brewed Batch
  - _inherit_: `agri.traceability.mixin, agri.biological.valuation.mixin`
  - **核心字段**:
    - `lot_id` (Many2one): stock.lot
    - `vintage_start_date` (Date): Aging Start
    - `is_aged_product` (Boolean): Aged Product

### `farm.lot.flower` (Defined in `farm_floriculture`)
  - **Class**: `FarmLotFlower`
  - **描述**: Floral Batch (ISL Layer)
  - _inherit_: `agri.traceability.mixin, agri.incident.alert.mixin`
  - **核心字段**:
    - `lot_id` (Many2one): stock.lot
    - `bloom_stage_at_harvest` (Selection): bloom_stage_at_harvest
    - `predicted_vase_life` (Integer): Predicted Vase-life (Days)
    - `is_preserved` (Boolean): Preservation Completed
    - `hydration_end_time` (Datetime): Hydration Completed At
    - `preservative_used` (Char): Preservative Agent
    - `max_transport_temp` (Float): Cold-chain Redline
    - `current_batch_temp` (Float): Latest Recorded Temp (℃)
    - `temperature_violation` (Boolean): Violation Detected

### `farm.lot.grape` (Defined in `farm_viticulture`)
  - **Class**: `FarmLotGrape`
  - **描述**: Grape Batch
  - _inherit_: `agri.traceability.mixin, agri.quality.gate.mixin`
  - **核心字段**:
    - `lot_id` (Many2one): stock.lot
    - `brix_level` (Float): Brix (Sugar)
    - `titratable_acidity` (Float): TA (g/L)
    - `ph_level` (Float): Juice pH
    - `juice_yield_volume` (Float): Extracted Juice (L)
    - `pressing_ratio` (Float): Pressing Ratio (L/kg)

### `farm.lot.harvest` (Defined in `farm_processing`)
  - **Class**: `FarmLotHarvest`
  - **描述**: Land Harvest Lot (ISL Layer)

  - **核心字段**:
    - `lot_id` (Many2one): stock.lot
    - `terroir_attributes_json` (Text): Terroir Attributes (JSON)

### `farm.lot.medicinal` (Defined in `farm_medicinal_plants`)
  - **Class**: `FarmLotMedicinal`
  - **描述**: Medicinal Asset/Batch
  - _inherit_: `agri.traceability.mixin`
  - **核心字段**:
    - `lot_id` (Many2one): stock.lot
    - `altitude_meters` (Float): Harvest Altitude (m)
    - `soil_ph_at_origin` (Float): Origin Soil pH
    - `analysis_date` (Date): Last Analysis
    - `certified_compound_level` (Float): Certified Active Compound (%)

### `farm.lot.rice` (Defined in `farm_symbiosis`)
  - **Class**: `FarmLotRice`
  - **描述**: Symbiotic Rice Batch
  - _inherit_: `agri.traceability.mixin`
  - **核心字段**:
    - `lot_id` (Many2one): stock.lot
    - `linked_fish_lot_id` (Many2one): stock.lot

### `farm.lot.wine` (Defined in `farm_winery`)
  - **Class**: `FarmLotWine`
  - **描述**: Wine Batch
  - _inherit_: `agri.traceability.mixin, agri.biological.valuation.mixin`
  - **核心字段**:
    - `lot_id` (Many2one): stock.lot
    - `barrel_entry_date` (Date): Barrel Entry
    - `aging_months` (Integer): Months in Wood
    - `alcohol_final` (Float): Alcohol (%)
    - `residual_sugar` (Float): RS (g/L)
    - `free_so2` (Float): Free SO2 (mg/L)

### `farm.manure.batch` (Defined in `farm_waste_mgmt`)
  - **Class**: `FarmManureBatch`
  - **描述**: Manure Batch Record (Deprecated - Use agri.manure.batch)
  - _inherit_: `agri.manure.batch`


### `farm.manure.ledger` (Defined in `farm_waste_mgmt`)
  - **Class**: `FarmManureLedger`
  - **描述**: Monthly Manure Resource Utilization Ledger (Deprecated - Use agri.manure.ledger)
  - _inherit_: `agri.manure.ledger`


### `farm.market.price` (Defined in `farm_valuation`)
  - **Class**: `MarketPrice`
  - **描述**: Market Price Reference

  - **核心字段**:
    - `name` (Char): Price Reference
    - `product_id` (Many2one): product.template
    - `date` (Date): Price Date
    - `unit_price` (Float): Unit Price
    - `unit_of_measure` (Many2one): uom.uom
    - `source` (Char): Source
    - `futures_contract` (Char): Futures Contract
    - `futures_price` (Float): Futures Price
    - `price_volatility` (Float): Volatility Index
    - `confidence_level` (Selection): confidence_level

### `farm.medicinal.production` (Defined in `farm_medicinal_plants`)
  - **Class**: `FarmMedicinalProduction`
  - **描述**: Medicinal Processing Order
  - _inherit_: `agri.intervention.mixin, agri.growth.cycle.mixin, agri.quality.gate.mixin`
  - **核心字段**:
    - `production_id` (Many2one): mrp.production
    - `current_compound_level` (Float): Active Compound (%)
    - `target_compound_level` (Float): Standard Threshold (%)
    - `is_daodi_verified` (Boolean): Daodi Origin Verified

### `farm.medicinal.recipe` (Defined in `farm_medicinal_plants`)
  - **Class**: `FarmMedicinalRecipe`
  - **描述**: Medicinal Processing Protocol

  - **核心字段**:
    - `bom_id` (Many2one): mrp.bom
    - `drying_temperature` (Float): Drying Target Temp (℃)
    - `max_humidity_threshold` (Float): Max Humidity (%)

### `agri.isl.mrp.bom` (Defined in `farm_processing`)
  - **Class**: `FarmMrpBomExtension`
  - **描述**: 
  - _inherit_: `agri.isl.mrp.bom`
  - **核心字段**:
    - `is_parameter_required` (Boolean): Parameter Required
    - `target_temp` (Float): Target Temp
    - `target_ph` (Float): Target pH
    - `target_brix` (Float): Target Brix
    - `target_proofing_time` (Float): Target Proofing Time

### `farm.mushroom.batch` (Defined in `farm_mushroom`)
  - **Class**: `FarmMushroomBatch`
  - **描述**: Mushroom Fruiting Batch
  - _inherit_: `agri.biological.inventory.mixin, agri.growth.cycle.mixin, agri.traceability.mixin`
  - **核心字段**:
    - `lot_id` (Many2one): stock.lot
    - `contamination_rate` (Float): Contamination Rate (%)
    - `is_cleared_for_fruiting` (Boolean): Cleared for Fruiting

### `farm.mushroom.production` (Defined in `farm_mushroom`)
  - **Class**: `FarmMushroomProduction`
  - **描述**: Mushroom Fruiting Cycle
  - _inherit_: `agri.intervention.mixin, agri.agent.instruction.mixin, agri.incident.alert.mixin, agri.odoo19.performance.security.mixin`
  - **核心字段**:
    - `biological_efficiency` (Float): Biological Efficiency (%)
    - `mushroom_config` (Json): Mushroom Configuration
    - `production_id` (Many2one): mrp.production
    - `current_flush_number` (Integer): Current Flush
    - `biological_efficiency` (Float): Biological Efficiency (%)

### `farm.mushroom.recipe` (Defined in `farm_mushroom`)
  - **Class**: `FarmMushroomRecipe`
  - **描述**: Mushroom Substrate Recipe
  - _inherit_: `agri.bom.mixin, agri.nutrient.mixin`
  - **核心字段**:
    - `bom_id` (Many2one): mrp.bom
    - `target_co2_level` (Float): Max CO2 Threshold (ppm)
    - `target_humidity` (Float): Target Humidity (%)
    - `sterilization_temp` (Float): Sterilization Temp (℃)

### `farm.nursery.batch` (Defined in `farm_breeding`)
  - **Class**: `FarmNurseryBatch`
  - **描述**: Breeding Nursery Batch
  - _inherit_: `mail.thread, mail.activity.mixin, agri.growth.cycle.mixin, agri.biological.inventory.mixin, agri.traceability.mixin`
  - **核心字段**:
    - `lot_id` (Many2one): stock.lot
    - `parent_p1_id` (Many2one): stock.lot
    - `parent_p2_id` (Many2one): stock.lot
    - `sowing_date` (Date): Sowing Date
    - `estimated_transplant_gdd` (Float): Target GDD for Transplant
    - `target_land_area` (Float): Target Field Area (mu/ha)
    - `target_density` (Float): Target Planting Density

### `farm.orchard.cycle` (Defined in `farm_orchard_horticulture`)
  - **Class**: `FarmOrchardCycle`
  - **描述**: Annual Nurturing Cycle
  - _inherit_: `agri.intervention.mixin, agri.weather.sensitive.mixin, agri.agent.instruction.mixin`
  - **核心字段**:
    - `production_id` (Many2one): mrp.production
    - `intervention_scope` (Selection): intervention_scope
    - `target_tree_ids` (Many2many): stock.lot

### `farm.package.level` (Defined in `farm_processing`)
  - **Class**: `FarmPackageLevel`
  - **描述**: Farm Package Level (e.g., Item, Inner Carton, Pallet)

  - **核心字段**:
    - `name` (Char): name
    - `code` (Char): code
    - `parent_level_id` (Many2one): farm.package.level
    - `child_level_ids` (One2many): farm.package.level

### `farm.package` (Defined in `farm_processing`)
  - **Class**: `FarmPackage`
  - **描述**: Farm Package Instance

  - **核心字段**:
    - `name` (Char): name
    - `display_name` (Char): display_name
    - `package_level_id` (Many2one): farm.package.level
    - `product_id` (Many2one): product.product
    - `lot_id` (Many2one): stock.lot
    - `quantity` (Float): quantity
    - `parent_package_id` (Many2one): farm.package
    - `child_package_ids` (One2many): farm.package
    - `location_id` (Many2one): farm.location
    - `create_date` (Datetime): create_date
    - `barcode` (Char): barcode

### `farm.pest.disease` (Defined in `farm_knowledge`)
  - **Class**: `FarmPestDisease`
  - **描述**: Pest & Disease Database (Deprecated - Use agri.pest.disease)
  - _inherit_: `agri.pest.disease`


### `farm.pharma.bom` (Defined in `farm_processing`)
  - **Class**: `FarmPharmaBom`
  - **描述**: Pharmaceutical Processing BOM (ISL Layer)

  - **核心字段**:
    - `bom_id` (Many2one): mrp.bom
    - `gmp_standard` (Char): GMP Standard Reference
    - `active_ingredient_id` (Many2one): product.product
    - `concentration_target` (Float): Target Concentration (%)
    - `safety_data_sheet` (Binary): MSDS Document

### `farm.pharma.production` (Defined in `farm_processing`)
  - **Class**: `FarmPharmaProduction`
  - **描述**: Pharmaceutical Production Order (ISL Layer)

  - **核心字段**:
    - `production_id` (Many2one): mrp.production
    - `batch_record_ref` (Char): Electronic Batch Record (EBR) ID
    - `potency_verified` (Boolean): Potency Verified
    - `impurity_level` (Float): Impurity Level (%)

### `farm.processing.artisan.log` (Defined in `farm_processing`)
  - **Class**: `FarmProcessingArtisanLog`
  - **描述**: Artisan-Level Processing Precision Log
  - _inherit_: `mail.thread, mail.activity.mixin`
  - **核心字段**:
    - `production_id` (Many2one): mrp.production
    - `workorder_id` (Many2one): mrp.workorder
    - `parameter_name` (Char): Artisan Parameter
    - `target_value` (Float): Target Value (Precise)
    - `actual_value` (Float): Actual Value
    - `tolerance` (Float): Allowed Tolerance (+/-)
    - `measured_by` (Many2one): res.users
    - `deviation` (Float): Deviation
    - `quality_grade` (Selection): quality_grade

### `farm.processing.bom.line` (Defined in `farm_processing`)
  - **Class**: `FarmProcessingBomLineExtension`
  - **描述**: 
  - _inherit_: `farm.processing.bom.line`
  - **核心字段**:
    - `ingredient_role` (Selection): ingredient_role

### `farm.processing.bom.line` (Defined in `farm_processing`)
  - **Class**: `FarmProcessingBomLine`
  - **描述**: Processing BOM Component (ISL Layer)

  - **核心字段**:
    - `bom_line_id` (Many2one): mrp.bom.line
    - `blend_ratio` (Float): Blend Ratio
    - `additive_type` (Selection): additive_type
    - `processing_role` (Selection): processing_role

### `farm.processing.bom` (Defined in `farm_processing`)
  - **Class**: `FarmProcessingBom`
  - **描述**: Food Processing BOM (ISL Layer)

  - **核心字段**:
    - `bom_id` (Many2one): mrp.bom
    - `target_moisture_content` (Float): Target Moisture (%)
    - `target_temperature` (Float): Storage Temp (℃)
    - `allergen_ids` (Many2many): farm.allergen
    - `expected_yield_rate` (Float): Expected Yield Rate
    - `industry_type` (Selection): industry_type

### `farm.processing.production` (Defined in `farm_processing`)
  - **Class**: `FarmProcessingProduction`
  - **描述**: Farm Food Processing Order (ISL Layer)
  - _inherit_: `agri.isl.mrp.production`
  - **核心字段**:
    - `energy_reading_start` (Float): energy_reading_start
    - `energy_reading_end` (Float): energy_reading_end
    - `energy_cost_total` (Float): energy_cost_total
    - `water_consumption` (Float): Water Consumption
    - `electricity_consumption` (Float): Electricity Consumption
    - `total_energy_cost` (Float): Total Energy Cost (Measure)
    - `current_moisture_content` (Float): Current Moisture (%)
    - `current_weight_loss_ratio` (Float): Current Weight Loss (%)
    - `is_ready_for_harvest` (Boolean): Ready for Collection
    - `processing_bom_id` (Many2one): farm.processing.bom

### `farm.processing.waste` (Defined in `farm_waste_mgmt`)
  - **Class**: `ProcessingWaste`
  - **描述**: Processing Waste Management

  - **核心字段**:
    - `name` (Char): Waste Reference
    - `production_id` (Many2one): mrp.production
    - `product_id` (Many2one): product.product
    - `quantity` (Float): Quantity
    - `uom_id` (Many2one): uom.uom
    - `disposal_method` (Selection): disposal_method
    - `notes` (Text): Disposal Details

### `farm.product.certificate` (Defined in `farm_cert_ch`)
  - **Class**: `FarmProductCertificate`
  - **描述**: Edible Agri-Product Certificate
  - _inherit_: `mail.thread, mail.activity.mixin`
  - **核心字段**:
    - `certificate_no` (Char): Certificate No.
    - `picking_id` (Many2one): stock.picking
    - `lot_id` (Many2one): stock.lot
    - `product_id` (Many2one): product.product
    - `producer_name` (Char): Producer Name
    - `origin_location_id` (Many2one): farm.location
    - `production_date` (Date): Production Date
    - `commitment_statement` (Html): Commitment Statement
    - `quality_check_ids` (Many2many): farm.quality.check
    - `certificate_qr_code` (Char): Certificate QR Code

### `agri.isl.product.template` (Defined in `farm_processing`)
  - **Class**: `FarmAgriProduct`
  - **描述**: 
  - _inherit_: `agri.isl.product.template`
  - **核心字段**:
    - `industry_tag` (Selection): industry_tag
    - `n_content` (Float): Nitrogen (N) %
    - `p_content` (Float): Phosphorus (P) %
    - `k_content` (Float): Potassium (K) %
    - `sc_category_ids` (Many2many): farm.sc.category
    - `allergen_ids` (Many2many): farm.allergen
    - `nutrition_table` (Text): Nutrition Data (JSON/Text)
    - `is_potency_standardized` (Boolean): Standardize by Potency
    - `target_purity` (Float): Target Purity %

### `farm.regional.oversight` (Defined in `farm_multi_farm`)
  - **Class**: `FarmRegionalOversight`
  - **描述**: Regional Agricultural Oversight Dashboard
  - _inherit_: `mail.thread, mail.activity.mixin`
  - **核心字段**:
    - `name` (Char): Region/Zone Name
    - `agency_id` (Many2one): res.partner
    - `cooperative_ids` (Many2many): cooperative.entity
    - `total_land_area` (Float): Total Monitored Area (Ha)
    - `total_predicted_yield` (Float): Regional Yield Forecast (kg)
    - `avg_compliance_score` (Float): Regional Compliance Avg (%)
    - `alert_count` (Integer): Active Compliance Alerts

### `farm.resource.usage` (Defined in `farm_agritourism`)
  - **Class**: `FarmResourceUsage`
  - **描述**: Farm Resource Usage for Agritourism

  - **核心字段**:
    - `agritourism_operation_id` (Many2one): farm.agritourism.operation
    - `resource_id` (Many2one): farm.resource
    - `usage_start_time` (Float): Usage Start Time
    - `usage_end_time` (Float): Usage End Time
    - `assigned_staff` (Many2one): hr.employee
    - `usage_notes` (Text): Usage Notes

### `farm.sc.category` (Defined in `farm_processing`)
  - **Class**: `FarmScCategory`
  - **描述**: Food Production Category

  - **核心字段**:
    - `name` (Char): Category Name
    - `code` (Char): Category Code

### `farm.seed.batch` (Defined in `farm_seed_industry`)
  - **Class**: `FarmSeedBatch`
  - **描述**: Seed Inventory Batch
  - _inherit_: `agri.traceability.mixin, agri.biological.inventory.mixin, agri.certification.status.mixin`
  - **核心字段**:
    - `lot_id` (Many2one): stock.lot
    - `parent_p1_hash` (Char): P1 (Sire) Hash
    - `parent_p2_hash` (Char): P2 (Dam) Hash
    - `germination_rate` (Float): Germination Rate (%)
    - `purity_rate` (Float): Purity Rate (%)
    - `clarity_rate` (Float): Clarity Rate (%)
    - `moisture_content` (Float): Moisture Content (%)
    - `thousand_seed_weight` (Float): Thousand Seed Weight (g)
    - `pvp_certificate_id` (Char): PVP Certificate No.
    - `is_pvp_compliant` (Boolean): PVP Status OK

### `farm.seed.production` (Defined in `farm_seed_industry`)
  - **Class**: `FarmSeedProduction`
  - **描述**: Seed Propagation Order
  - _inherit_: `agri.intervention.mixin, agri.quality.gate.mixin`
  - **核心字段**:
    - `production_id` (Many2one): mrp.production

### `farm.seed.recipe` (Defined in `farm_seed_industry`)
  - **Class**: `FarmSeedRecipe`
  - **描述**: Seed Treatment Recipe
  - _inherit_: `agri.bom.mixin, agri.nutrient.mixin`
  - **核心字段**:
    - `bom_id` (Many2one): mrp.bom
    - `film_forming_ratio` (Float): Film-forming Ratio (%)
    - `target_moisture_content` (Float): Target Moisture (%)

### `farm.social.network` (Defined in `farm_ux`)
  - **Class**: `FarmSocialNetwork`
  - **描述**: Farm Social Network & Collaboration Platform

  - **核心字段**:
    - `name` (Char): Network Name
    - `network_type` (Selection): network_type
    - `member_ids` (Many2many): res.partner
    - `admin_ids` (Many2many): res.users
    - `description` (Text): Description
    - `is_active` (Boolean): Is Active
    - `created_by` (Many2one): res.users
    - `created_date` (Datetime): Created Date
    - `privacy_level` (Selection): privacy_level
    - `message_board` (Text): Message Board
    - `shared_resources` (Text): Shared Resources

### `farm.storage.env` (Defined in `farm_waste_mgmt`)
  - **Class**: `StorageEnvironment`
  - **描述**: Storage Environment Log

  - **核心字段**:
    - `location_id` (Many2one): farm.location
    - `timestamp` (Datetime): Timestamp
    - `temperature` (Float): Temperature (℃)
    - `humidity` (Float): Humidity (%)
    - `co2_level` (Float): CO2 Level (ppm)
    - `is_alert` (Boolean): Is Alert
    - `alert_message` (Char): Alert Message

### `farm.subsidy.application` (Defined in `farm_subsidy_ch`)
  - **Class**: `FarmSubsidyApplication`
  - **描述**: 
  - _inherit_: `farm.subsidy.application`
  - **核心字段**:
    - `crop_type_china` (Selection): crop_type_china
    - `declared_area_mu` (Float): Declared Area (mu)

### `farm.symbiotic.order` (Defined in `farm_symbiosis`)
  - **Class**: `FarmSymbioticOrder`
  - **描述**: Symbiotic Cycle
  - _inherit_: `agri.intervention.mixin, agri.quality.gate.mixin, agri.weather.sensitive.mixin`
  - **核心字段**:
    - `production_id` (Many2one): mrp.production
    - `contains_aquatic_toxins` (Boolean): High Aquatic Toxicity Detected

### `farm.symbiotic.plot` (Defined in `farm_symbiosis`)
  - **Class**: `FarmSymbioticPlot`
  - **描述**: Symbiotic Field
  - _inherit_: `agri.geospatial.mixin`
  - **核心字段**:
    - `location_id` (Many2one): farm.location
    - `trench_area_ratio` (Float): Trench Area Ratio (%)
    - `target_water_depth_cm` (Float): Target Water Depth (cm)

### `farm.symbiotic.recipe` (Defined in `farm_symbiosis`)
  - **Class**: `FarmSymbioticRecipe`
  - **描述**: Co-culture Recipe
  - _inherit_: `agri.bom.mixin, agri.nutrient.mixin`
  - **核心字段**:
    - `bom_id` (Many2one): mrp.bom
    - `fish_manure_nitrogen_credit` (Float): Fertilizer Credit from Fish (kg/mu)

### `farm.training.certification` (Defined in `farm_training`)
  - **Class**: `FarmTrainingCertification`
  - **描述**: Farm Training Certification (Deprecated - Use agri.training.certification)
  - _inherit_: `agri.training.certification`


### `farm.training.skill` (Defined in `farm_training`)
  - **Class**: `FarmTrainingSkill`
  - **描述**: Farm Training Skill (Deprecated - Use agri.training.skill)
  - _inherit_: `agri.training.skill`


### `farm.training.training_record` (Defined in `farm_training`)
  - **Class**: `FarmTrainingTrainingRecord`
  - **描述**: Farm Training Record (Deprecated - Use agri.training.training_record)
  - _inherit_: `agri.training.training_record`


### `farm.trait.value` (Defined in `farm_breeding`)
  - **Class**: `FarmTraitValue`
  - **描述**: Breeding Trait Value

  - **核心字段**:
    - `name` (Char): Trait Name
    - `value` (Char): Measured Value
    - `score` (Float): Score (0-10)
    - `lot_id` (Many2one): stock.lot
    - `company_id` (Many2one): res.company

### `farm.viticulture.cycle` (Defined in `farm_viticulture`)
  - **Class**: `FarmViticultureCycle`
  - **描述**: Vineyard Annual Cycle
  - _inherit_: `agri.intervention.mixin, agri.growth.cycle.mixin, agri.weather.sensitive.mixin`
  - **核心字段**:
    - `production_id` (Many2one): mrp.production
    - `pruned_buds_per_vine` (Integer): Pruned Buds per Vine
    - `target_brix` (Float): Target Ripeness (Brix)

### `farm.viticulture.plot` (Defined in `farm_viticulture`)
  - **Class**: `FarmViticulturePlot`
  - **描述**: Vineyard Plot
  - _inherit_: `agri.geospatial.mixin`
  - **核心字段**:
    - `location_id` (Many2one): farm.location
    - `trellis_system` (Selection): trellis_system
    - `vine_spacing` (Float): Vine Spacing (m)
    - `row_orientation` (Float): Row Azimuth (Degree)

### `farm.voice.recognition.alias` (Defined in `farm_ux`)
  - **Class**: `VoiceRecognitionAlias`
  - **描述**: Voice Recognition Alias for Agricultural Terms

  - **核心字段**:
    - `alias` (Char): Spoken Alias / Phonetic
    - `target_term` (Char): Standard Term

### `farm.weather.forecast` (Defined in `farm_weather`)
  - **Class**: `FarmWeatherForecast`
  - **描述**: Farm Weather Forecast (Deprecated - Use agri.weather.forecast)
  - _inherit_: `agri.weather.forecast`


### `farm.winery.production` (Defined in `farm_winery`)
  - **Class**: `FarmWineryProduction`
  - **描述**: Vinification Order
  - _inherit_: `agri.intervention.mixin, agri.agent.instruction.mixin, agri.incident.alert.mixin`
  - **核心字段**:
    - `production_id` (Many2one): mrp.production
    - `current_brix` (Float): Current Brix
    - `current_temp` (Float): Current Temp (℃)

### `farm.winery.recipe` (Defined in `farm_winery`)
  - **Class**: `FarmWineryRecipe`
  - **描述**: Winery Protocol

  - **核心字段**:
    - `bom_id` (Many2one): mrp.bom
    - `target_alcohol_pct` (Float): Target Alcohol (%)
    - `fermentation_temp_target` (Float): Target Temp (℃)

### `farm.winery.vessel` (Defined in `farm_winery`)
  - **Class**: `FarmWineryVessel`
  - **描述**: Winery Vessel/Barrel

  - **核心字段**:
    - `workcenter_id` (Many2one): mrp.workcenter
    - `vessel_type` (Selection): vessel_type
    - `capacity_liters` (Float): Volume Capacity (L)
    - `current_fill_level` (Float): Current Fill (%)

### `form.layout.template` (Defined in `farm_ux`)
  - **Class**: `FormLayoutTemplate`
  - **描述**: Form Layout Template for Industry-Specific Views

  - **核心字段**:
    - `name` (Char): Template Name
    - `model_name` (Char): Model Name
    - `industry_type` (Selection): industry_type
    - `layout_definition` (Text): Layout Definition
    - `is_active` (Boolean): Is Active
    - `description` (Text): Description
    - `user_role` (Selection): user_role
    - `version` (Char): Version
    - `created_by` (Many2one): res.users
    - `created_date` (Datetime): Created Date

### `hr.employee` (Defined in `farm_training`)
  - **Class**: `HrEmployee`
  - **描述**: 
  - _inherit_: `hr.employee`
  - **核心字段**:
    - `skill_ids` (Many2many): farm.training.skill
    - `certification_ids` (Many2many): farm.training.certification
    - `training_record_ids` (One2many): farm.training.training_record

### `internal.settlement` (Defined in `farm_multi_farm`)
  - **Class**: `InternalSettlementExtension`
  - **描述**: 
  - _inherit_: `internal.settlement`
  - **核心字段**:
    - `settlement_type` (Selection): settlement_type

### `internal.settlement` (Defined in `farm_multi_farm`)
  - **Class**: `InternalSettlementExtension`
  - **描述**: 
  - _inherit_: `internal.settlement`
  - **核心字段**:
    - `settlement_type` (Selection): settlement_type
    - `joint_procurement_id` (Many2one): joint.procurement
    - `joint_po_member_id` (Many2one): joint.procurement.po.member

### `internal.settlement` (Defined in `farm_multi_farm_procurement`)
  - **Class**: `InternalSettlementExtensionProcurement`
  - **描述**: 
  - _inherit_: `internal.settlement`
  - **核心字段**:
    - `joint_procurement_id` (Many2one): joint.procurement
    - `joint_po_member_id` (Many2one): joint.procurement.po.member

### `ir.actions.act_window` (Defined in `farm_ux`)
  - **Class**: `IrActionsActWindow`
  - **描述**: 
  - _inherit_: `ir.actions.act_window`


### `ir.ui.menu` (Defined in `farm_ux`)
  - **Class**: `IrUiMenu`
  - **描述**: 
  - _inherit_: `ir.ui.menu`


### `joint.procurement.line` (Defined in `farm_multi_farm_procurement`)
  - **Class**: `JointProcurementLine`
  - **描述**: Joint Procurement Line

  - **核心字段**:
    - `procurement_id` (Many2one): joint.procurement
    - `member_id` (Many2one): cooperative.member
    - `product_id` (Many2one): product.product
    - `quantity` (Float): Quantity
    - `unit_price` (Float): Unit Price
    - `member_amount` (Float): Member Amount
    - `markup_amount` (Float): Markup Amount
    - `settlement_id` (Many2one): internal.settlement

### `maintenance.equipment` (Defined in `farm_equipment`)
  - **Class**: `FarmEquipment`
  - **描述**: 
  - _inherit_: `maintenance.equipment`
  - **核心字段**:
    - `checklist_id` (Many2one): farm.equipment.checklist

### `marketplace.demand.match` (Defined in `farm_multi_farm_procurement`)
  - **Class**: `MarketplaceDemandMatch`
  - **描述**: Marketplace Demand Match

  - **核心字段**:
    - `listing_id` (Many2one): internal.marketplace
    - `member_id` (Many2one): cooperative.member
    - `quantity` (Float): Quantity
    - `priority` (Integer): Priority
    - `match_date` (Date): Match Date

### `mrp.bom.byproduct` (Defined in `farm_processing`)
  - **Class**: `MrpBomByproduct`
  - **描述**: 
  - _inherit_: `mrp.bom.byproduct`
  - **核心字段**:
    - `cost_share` (Float): Cost Share (%)

### `mrp.bom.line` (Defined in `farm_mrp`)
  - **Class**: `MrpBomLine`
  - **描述**: 
  - _inherit_: `mrp.bom.line`
  - **核心字段**:
    - `isl_record_type` (Char): isl_record_type

### `mrp.bom.line` (Defined in `farm_processing`)
  - **Class**: `MrpBomLine`
  - **描述**: 
  - _inherit_: `mrp.bom.line`
  - **核心字段**:
    - `ingredient_role` (Selection): ingredient_role

### `mrp.bom` (Defined in `farm_mrp`)
  - **Class**: `MrpBom`
  - **描述**: 
  - _inherit_: `mrp.bom`
  - **核心字段**:
    - `industry_type` (Selection): industry_type
    - `isl_record_type` (Char): isl_record_type

### `mrp.bom` (Defined in `farm_processing`)
  - **Class**: `MrpBom`
  - **描述**: 
  - _inherit_: `mrp.bom`
  - **核心字段**:
    - `industry_type` (Selection): industry_type
    - `expected_yield_rate` (Float): Expected Yield Rate
    - `process_description` (Text): Process Description
    - `target_temp` (Float): Target Temp
    - `target_ph` (Float): Target pH
    - `target_brix` (Float): Target Brix
    - `target_proofing_time` (Float): Target Proofing Time
    - `standard_duration` (Float): Standard Duration
    - `haccp_instructions` (Html): HACCP Instructions
    - `processing_type` (Selection): processing_type
    - `dilution_ratio` (Float): Dilution Ratio
    - `sc_category_id` (Many2one): farm.sc.category
    - `grade_distribution_ids` (One2many): farm.bom.grade.distribution
    - `mass_balance_tolerance` (Float): Mass Balance Tolerance (%)
    - `allergen_ids` (Many2many): farm.allergen

### `mrp.bom` (Defined in `farm_processing`)
  - **Class**: `MrpBom`
  - **描述**: 
  - _inherit_: `mrp.bom`
  - **核心字段**:
    - `packaging_line_ids` (One2many): farm.bom.package.line

### `mrp.bom` (Defined in `farm_ux`)
  - **Class**: `BomInjection`
  - **描述**: 
  - _inherit_: `mrp.bom, agri.view.mixin`


### `mrp.production` (Defined in `farm_mobile`)
  - **Class**: `AgriIntervention`
  - **描述**: 
  - _inherit_: `mrp.production`
  - **核心字段**:
    - `check_in_ids` (One2many): farm.checkin
    - `evidence_ids` (One2many): farm.evidence
    - `current_check_in_id` (Many2one): farm.checkin

### `mrp.production` (Defined in `farm_mrp`)
  - **Class**: `MrpProduction`
  - **描述**: 
  - _inherit_: `mrp.production`
  - **核心字段**:
    - `industry_type` (Selection): industry_type
    - `isl_record_type` (Char): isl_record_type

### `mrp.production` (Defined in `farm_processing`)
  - **Class**: `MrpProduction`
  - **描述**: 
  - _inherit_: `mrp.production`
  - **核心字段**:
    - `artisan_log_ids` (One2many): farm.processing.artisan.log
    - `is_artisan_batch` (Boolean): Artisan/Premium Batch

### `mrp.production` (Defined in `farm_ux`)
  - **Class**: `ProductionInjection`
  - **描述**: 
  - _inherit_: `mrp.production, agri.view.mixin`


### `mrp.routing.workcenter` (Defined in `farm_processing`)
  - **Class**: `MrpRoutingWorkcenter`
  - **描述**: 
  - _inherit_: `mrp.routing.workcenter`


### `mrp.routing.workcenter` (Defined in `farm_processing`)
  - **Class**: `MrpRoutingWorkcenter`
  - **描述**: 
  - _inherit_: `mrp.routing.workcenter`


### `mrp.workcenter` (Defined in `farm_processing`)
  - **Class**: `MrpWorkcenter`
  - **描述**: 
  - _inherit_: `mrp.workcenter`


### `mrp.workcenter` (Defined in `farm_processing`)
  - **Class**: `MrpWorkcenter`
  - **描述**: 
  - _inherit_: `mrp.workcenter`
  - **核心字段**:
    - `energy_type` (Selection): energy_type
    - `energy_cost_per_hour` (Float): Energy Cost per Hour

### `mrp.workcenter` (Defined in `farm_processing`)
  - **Class**: `MrpWorkcenter`
  - **描述**: 
  - _inherit_: `mrp.workcenter`
  - **核心字段**:
    - `industry_capability` (Selection): industry_capability
    - `energy_type` (Selection): energy_type
    - `energy_cost_per_hour` (Float): Energy Cost per Hour

### `mrp.workcenter` (Defined in `farm_ux`)
  - **Class**: `WorkcenterInjection`
  - **描述**: 
  - _inherit_: `mrp.workcenter, agri.view.mixin`


### `mrp.workorder` (Defined in `farm_processing`)
  - **Class**: `MrpWorkorder`
  - **描述**: 
  - _inherit_: `mrp.workorder`
  - **核心字段**:
    - `actual_energy_consumption` (Float): Actual Energy Consumption
    - `process_parameters` (Text): Process Parameters (e.g. Temperature, Pressure)
    - `qty_produced_workorder` (Float): Produced Qty (Workorder)
    - `qty_scrapped_workorder` (Float): Scrapped Qty (Workorder)
    - `qty_input_workorder` (Float): Input Qty (Workorder)
    - `loss_rate_workorder` (Float): Loss Rate (Workorder) (%)

### `multi.sensory.interaction` (Defined in `farm_ux`)
  - **Class**: `MultiSensoryInteraction`
  - **描述**: Multi-Sensory Interaction Configuration

  - **核心字段**:
    - `name` (Char): Feature Name
    - `interaction_type` (Selection): interaction_type
    - `model_name` (Char): Model Name
    - `field_name` (Char): Field Name
    - `is_enabled` (Boolean): Is Enabled
    - `voice_commands` (Text): Voice Commands
    - `gesture_mappings` (Text): Gesture Mappings
    - `audio_notification` (Boolean): Audio Notification
    - `haptic_feedback` (Boolean): Haptic Feedback
    - `visual_enhancement` (Boolean): Visual Enhancement
    - `large_font_support` (Boolean): Large Font Support
    - `high_contrast_mode` (Boolean): High Contrast Mode
    - `screen_reader_compatible` (Boolean): Screen Reader Compatible
    - `keyboard_shortcuts` (Text): Keyboard Shortcuts
    - `description` (Text): Description

### `pos.order.line` (Defined in `farm_pos`)
  - **Class**: `PosOrderLine`
  - **描述**: 
  - _inherit_: `pos.order.line`
  - **核心字段**:
    - `lot_id` (Many2one): stock.lot

### `pos.order` (Defined in `farm_pos`)
  - **Class**: `PosOrder`
  - **描述**: 
  - _inherit_: `pos.order`
  - **核心字段**:
    - `picking_location_id` (Many2one): stock.location

### `procurement.planning.line` (Defined in `farm_multi_farm_procurement`)
  - **Class**: `ProcurementPlanningLine`
  - **描述**: Procurement Planning Line

  - **核心字段**:
    - `planning_id` (Many2one): procurement.planning
    - `product_id` (Many2one): product.product
    - `total_required` (Float): Total Required
    - `total_available` (Float): Total Available
    - `total_allocated` (Float): Total Allocated
    - `remaining_quantity` (Float): Remaining Quantity
    - `allocation_lines` (One2many): procurement.allocation.line

### `product.template` (Defined in `farm_agritourism`)
  - **Class**: `ProductTemplate`
  - **描述**: 
  - _inherit_: `product.template`
  - **核心字段**:
    - `is_experience_package` (Boolean): Is Experience Package

### `product.template` (Defined in `farm_processing`)
  - **Class**: `ProductTemplate`
  - **描述**: 
  - _inherit_: `product.template`
  - **核心字段**:
    - `is_agri_material` (Boolean): Is Agri Material
    - `is_processed_food` (Boolean): Is Processed Food
    - `substitute_product_ids` (Many2many): product.template

### `product.template` (Defined in `farm_ux`)
  - **Class**: `ProductInjection`
  - **描述**: 
  - _inherit_: `product.template, agri.view.mixin`


### `product.template` (Defined in `farm_valuation`)
  - **Class**: `ProductTemplateMarketPrice`
  - **描述**: 
  - _inherit_: `product.template`
  - **核心字段**:
    - `market_price` (Float): Market Price
    - `market_price_date` (Date): Market Price Date
    - `market_price_uom` (Many2one): uom.uom
    - `expected_yield_per_unit` (Float): Expected Yield per Unit

### `project.task` (Defined in `farm_green_monitor`)
  - **Class**: `ProjectTask`
  - **描述**: 
  - _inherit_: `project.task`
  - **核心字段**:
    - `total_fertilizer_used` (Float): Total Fertilizer Used (kg)
    - `total_pesticide_used` (Float): Total Pesticide Used (kg)
    - `fertilizer_per_mu` (Float): Fertilizer (kg/mu)
    - `pesticide_per_mu` (Float): Pesticide (kg/mu)

### `project.task` (Defined in `farm_safety`)
  - **Class**: `ProjectTask`
  - **描述**: 
  - _inherit_: `project.task`
  - **核心字段**:
    - `prevention_template_id` (Many2one): farm.prevention.template

### `res.company` (Defined in `farm_entity_reg`)
  - **Class**: `ResCompany`
  - **描述**: 
  - _inherit_: `res.company`
  - **核心字段**:
    - `unified_social_credit_code` (Char): Unified Social Credit Code
    - `registration_no` (Char): Registration No.
    - `entity_type` (Selection): entity_type
    - `license_attachment_ids` (Many2many): ir.attachment
    - `license_expiry_date` (Date): License Expiry Date
    - `is_license_expired` (Boolean): License Expired

### `res.company` (Defined in `farm_label`)
  - **Class**: `ResCompany`
  - **描述**: 
  - _inherit_: `res.company`
  - **核心字段**:
    - `label_background_image` (Binary): Label Background Image

### `res.config.settings` (Defined in `farm_label`)
  - **Class**: `ResConfigSettings`
  - **描述**: 
  - _inherit_: `res.config.settings`
  - **核心字段**:
    - `label_background_image` (Binary): label_background_image

### `res.config.settings` (Defined in `farm_weather`)
  - **Class**: `ResConfigSettings`
  - **描述**: 
  - _inherit_: `res.config.settings`
  - **核心字段**:
    - `weather_api_key` (Char): weather_api_key

### `res.partner` (Defined in `farm_marketing`)
  - **Class**: `FarmPartner`
  - **描述**: 
  - _inherit_: `res.partner`
  - **核心字段**:
    - `loyalty_points` (Float): Farm Loyalty Points

### `res.partner` (Defined in `farm_multi_farm`)
  - **Class**: `ResPartner`
  - **描述**: 
  - _inherit_: `res.partner`
  - **核心字段**:
    - `internal_credit_balance` (Float): Internal Credit Balance

### `res.partner` (Defined in `farm_ux`)
  - **Class**: `PartnerInjection`
  - **描述**: 
  - _inherit_: `res.partner, agri.view.mixin`


### `sale.order.line` (Defined in `farm_agritourism`)
  - **Class**: `SaleOrderLine`
  - **描述**: 
  - _inherit_: `sale.order.line`
  - **核心字段**:
    - `lot_id` (Many2one): stock.lot

### `sale.order.line` (Defined in `farm_floriculture`)
  - **Class**: `SaleOrderLine`
  - **描述**: 
  - _inherit_: `sale.order.line`


### `sale.order.line` (Defined in `farm_marketing`)
  - **Class**: `FarmSaleOrderLine`
  - **描述**: 
  - _inherit_: `sale.order.line`
  - **核心字段**:
    - `lot_id` (Many2one): stock.lot
    - `required_integrity_score` (Float): Required Integrity
    - `is_reserved` (Boolean): Is Locked

### `sale.order` (Defined in `farm_agritourism`)
  - **Class**: `SaleOrder`
  - **描述**: 
  - _inherit_: `sale.order`
  - **核心字段**:
    - `agri_task_ids` (One2many): project.task
    - `booking_ids` (One2many): farm.booking
    - `booking_count` (Integer): booking_count

### `sale.order` (Defined in `farm_floriculture`)
  - **Class**: `SaleOrder`
  - **描述**: 
  - _inherit_: `sale.order`


### `sale.order` (Defined in `farm_marketing`)
  - **Class**: `FarmSaleOrder`
  - **描述**: 
  - _inherit_: `sale.order`
  - **核心字段**:
    - `is_preorder` (Boolean): Pre-order Reservation
    - `reservation_expiry` (Datetime): Reservation Expiry
    - `export_country_id` (Many2one): res.country
    - `is_export_compliant` (Boolean): Export Compliant

### `stock.lot` (Defined in `farm_breeding`)
  - **Class**: `FarmLotBreeding`
  - **描述**: 
  - _inherit_: `stock.lot`
  - **核心字段**:
    - `trait_value_ids` (One2many): farm.trait.value
    - `trait_score_avg` (Float): Average Trait Score
    - `father_id` (Many2one): stock.lot
    - `mother_id` (Many2one): stock.lot
    - `gender` (Selection): gender

### `stock.lot` (Defined in `farm_breeding`)
  - **Class**: `StockLotExtensionBreeding`
  - **描述**: 
  - _inherit_: `stock.lot`
  - **核心字段**:
    - `father_id` (Many2one): stock.lot
    - `mother_id` (Many2one): stock.lot
    - `trait_score_avg` (Selection): trait_score_avg
    - `trait_value_ids` (One2many): farm.trait.value

### `stock.lot` (Defined in `farm_certification`)
  - **Class**: `FarmLotCert`
  - **描述**: 
  - _inherit_: `stock.lot`
  - **核心字段**:
    - `certification_level` (Selection): certification_level

### `stock.lot` (Defined in `farm_label`)
  - **Class**: `StockLot`
  - **描述**: 
  - _inherit_: `stock.lot`


### `stock.lot` (Defined in `farm_marketing`)
  - **Class**: `FarmLotMarketing`
  - **描述**: 
  - _inherit_: `stock.lot`
  - **核心字段**:
    - `traceability_url` (Char): Traceability URL
    - `is_premium_brand` (Boolean): Premium Brand Lot
    - `allowed_partner_ids` (Many2many): res.partner
    - `integrity_score` (Float): Organic Integrity Score
    - `story_title` (Char): Growth Story Title
    - `story_content` (Html): Growth Story Content
    - `marketing_image_ids` (Many2many): ir.attachment
    - `avg_temp` (Float): Average Growth Temperature (℃)
    - `water_purity` (Char): Water Purity Grade
    - `is_near_expiry` (Boolean): Near Expiry
    - `promotion_link_id` (Many2one): loyalty.program

### `stock.lot` (Defined in `farm_marketing`)
  - **Class**: `StockLot`
  - **描述**: 
  - _inherit_: `stock.lot`
  - **核心字段**:
    - `feedback_ids` (One2many): farm.consumer.feedback
    - `avg_consumer_rating` (Float): Avg Consumer Rating

### `stock.lot` (Defined in `farm_marketing`)
  - **Class**: `StockLot`
  - **描述**: 
  - _inherit_: `stock.lot`
  - **核心字段**:
    - `gi_registry_id` (Many2one): agri.gi.registry
    - `gi_security_code` (Char): GI Anti-counterfeit Code

### `stock.lot` (Defined in `farm_mrp`)
  - **Class**: `StockLot`
  - **描述**: 
  - _inherit_: `stock.lot`
  - **核心字段**:
    - `isl_summary_info` (Char): ISL Contextual Info
    - `isl_record_type` (Char): isl_record_type

### `stock.lot` (Defined in `farm_multi_farm`)
  - **Class**: `StockLotExtension`
  - **描述**: 
  - _inherit_: `stock.lot`
  - **核心字段**:
    - `assigned_cooperative_id` (Many2one): cooperative.entity
    - `cooperative_purpose` (Selection): cooperative_purpose
    - `is_government_audited` (Boolean): Government Audit Passed

### `stock.lot` (Defined in `farm_multi_farm`)
  - **Class**: `StockLotExtension`
  - **描述**: 
  - _inherit_: `stock.lot`
  - **核心字段**:
    - `assigned_cooperative_id` (Many2one): cooperative.entity
    - `cooperative_purpose` (Selection): cooperative_purpose
    - `is_government_audited` (Boolean): Government Audit Passed

### `stock.lot` (Defined in `farm_orchard_horticulture`)
  - **Class**: `OrchardStockLot`
  - **描述**: 
  - _inherit_: `stock.lot, agri.biological.inventory.mixin, agri.growth.cycle.mixin, agri.biological.valuation.mixin, agri.geospatial.mixin, agri.traceability.mixin`
  - **核心字段**:
    - `is_fruit_tree` (Boolean): Is Fruit Tree
    - `tree_variety_id` (Many2one): agri.industry.variety
    - `planting_date` (Date): Planting Date
    - `expected_harvest_gdd` (Float): Target GDD for Ripening
    - `maturity_status` (Float): Maturity Progress (%)

### `stock.lot` (Defined in `farm_processing`)
  - **Class**: `AgriStockLotHealth`
  - **描述**: 
  - _inherit_: `stock.lot`
  - **核心字段**:
    - `health_activity_ids` (One2many): mail.activity

### `stock.lot` (Defined in `farm_processing`)
  - **Class**: `StockLotHealth`
  - **描述**: Stock Lot Health (Deprecated - Use stock.lot with agri.health.schedule)
  - _inherit_: `stock.lot`
  - **核心字段**:
    - `health_activity_ids` (One2many): mail.activity

### `stock.lot` (Defined in `farm_processing`)
  - **Class**: `StockLot`
  - **描述**: 
  - _inherit_: `stock.lot`
  - **核心字段**:
    - `lot_purpose` (Selection): lot_purpose
    - `birth_date` (Date): Birth/Hatch Date
    - `life_stage` (Selection): life_stage
    - `current_weight` (Float): Current Weight (kg)
    - `gender` (Selection): gender
    - `last_gps_lat` (Float): Last Latitude
    - `last_gps_lng` (Float): Last Longitude
    - `last_location_update` (Datetime): Last Location Sync
    - `parent_lot_ids` (Many2many): stock.lot
    - `child_lot_ids` (One2many): stock.lot
    - `full_traceability_path` (Text): Full Traceability Path
    - `quality_grade` (Selection): quality_grade
    - `harvest_date` (Date): Harvest Date
    - `plot_id` (Many2one): farm.location
    - `active_content` (Float): Active Content (%)
    - *... 以及其他 5 个业务字段*

### `stock.move.line` (Defined in `farm_processing`)
  - **Class**: `StockMoveLine`
  - **描述**: 
  - _inherit_: `stock.move.line`


### `stock.move` (Defined in `farm_processing`)
  - **Class**: `StockMove`
  - **描述**: 
  - _inherit_: `stock.move`
  - **核心字段**:
    - `industry_context` (Selection): industry_context

### `stock.move` (Defined in `farm_ux`)
  - **Class**: `MoveInjection`
  - **描述**: 
  - _inherit_: `stock.move, agri.view.mixin`


### `stock.picking.type` (Defined in `farm_multi_farm`)
  - **Class**: `StockPickingType`
  - **描述**: 
  - _inherit_: `stock.picking.type`
  - **核心字段**:
    - `is_advancing_distribution` (Boolean): Is Advancing Distribution

### `stock.picking` (Defined in `farm_cert_ch`)
  - **Class**: `StockPicking`
  - **描述**: 
  - _inherit_: `stock.picking`
  - **核心字段**:
    - `requires_cert_ch` (Boolean): Requires Cert. (China)
    - `certificate_ch_ids` (One2many): farm.product.certificate

### `stock.picking` (Defined in `farm_multi_farm_equipment`)
  - **Class**: `StockPicking`
  - **描述**: 
  - _inherit_: `stock.picking`


### `stock.picking` (Defined in `farm_ux`)
  - **Class**: `PickingInjection`
  - **描述**: 
  - _inherit_: `stock.picking, agri.view.mixin`


### `stock.quant` (Defined in `farm_ux`)
  - **Class**: `QuantInjection`
  - **描述**: 
  - _inherit_: `stock.quant, agri.view.mixin`


### `term.mapping` (Defined in `farm_ux`)
  - **Class**: `TermMapping`
  - **描述**: Term Mapping for Agricultural Terminology

  - **核心字段**:
    - `name` (Char): Mapping Name
    - `source_term` (Char): Source Term (Industrial)
    - `target_term` (Char): Target Term (Agricultural)
    - `language_code` (Char): Language Code
    - `industry_context` (Selection): industry_context
    - `region_specific` (Boolean): Region Specific
    - `region_code` (Char): Region Code
    - `is_active` (Boolean): Is Active
    - `description` (Text): Description
    - `example_usage` (Text): Example Usage

### `workspace.customization` (Defined in `farm_ux`)
  - **Class**: `WorkspaceCustomization`
  - **描述**: Personalized Workspace Customization

  - **核心字段**:
    - `name` (Char): Customization Name
    - `user_id` (Many2one): res.users
    - `dashboard_widgets` (Text): Dashboard Widgets
    - `theme_preference` (Selection): theme_preference
    - `quick_actions` (Text): Quick Actions
    - `language_preference` (Char): Language Preference
    - `timezone_preference` (Char): Timezone Preference
    - `font_size` (Selection): font_size
    - `layout_preference` (Text): Layout Preferences
    - `is_active` (Boolean): Is Active
    - `last_updated` (Datetime): Last Updated
