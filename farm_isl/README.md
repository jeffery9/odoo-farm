# Industry Specialized Layer (ISL) Module Architecture

The ISL module implements a standardized architecture for industry-specific extensions to core Odoo models. The architecture follows the single responsibility principle and provides a consistent pattern for extending core functionality with industry-specific requirements.

## Architecture Overview

The ISL architecture follows these key design principles:

1. **Separation of Concerns**: Abstract models handle common functionality, concrete models extend Odoo core models
2. **Inheritance Pattern**: Uses `_inherits` mechanism to extend core Odoo models while maintaining all base functionality
3. **Industry Specialization**: Common industry fields and validation across all ISL models
4. **Automatic Redirection**: Built-in mechanism to redirect to ISL models when available
5. **Performance Optimization**: Caching and optimization utilities for efficient operations
6. **Data Migration**: Utilities for migrating existing data to ISL architecture

## Core Components

### 1. Abstract Base Models (`isl_abstract_models.py`)
Provide common functionality and industry-specific fields for different functional areas:

- `FarmManufacturingMixin`: For manufacturing-related models (MRP Production, BOM, Work Centers, Work Orders)
- `FarmInventoryMixin`: For inventory-related models (Stock Lots, Stock Pickings)
- `FarmSalesPurchaseMixin`: For sales/purchase-related models (Sale Orders, Purchase Orders)
- `FarmProductMixin`: For product-related models (Product Templates)
- `FarmQualityMixin`: For quality control models (Quality Control Points)

### 2. Concrete ISL Models (`isl_concrete_models.py`)
Extend core Odoo models using the `_inherits` mechanism:

- `FarmMRPProduction`: Extends `mrp.production`
- `FarmMRPBom`: Extends `mrp.bom`
- `FarmMRPWorkcenter`: Extends `mrp.workcenter`
- `FarmMRPWorkorder`: Extends `mrp.workorder`
- `FarmStockLot`: Extends `stock.lot`
- `FarmStockPicking`: Extends `stock.picking`
- `FarmSaleOrder`: Extends `sale.order`
- `FarmPurchaseOrder`: Extends `purchase.order`
- `FarmProductTemplate`: Extends `product.template`
- `FarmQualityControl`: Extends `quality.point`

### 3. Redirection System (`isl_redirection.py`)
- `ISLModelRedirector`: Provides automatic redirection from base models to ISL models
- `ISLIndustryExtension`: Manages industry-specific extensions

### 4. Performance Utilities (`isl_performance.py`)
- `ISLOptimizationMixin`: Provides caching and performance optimization

### 5. Migration Utilities (`isl_migration.py`)
- `ISLMigrationUtility`: Transient model for migrating existing data to ISL architecture

## Industry Types Support

All ISL models support the following industry types with specific requirements:

- `food_processing`: Food processing industry with HACCP, allergen control, kill dates
- `pharmaceutical`: Pharmaceutical industry with GMP compliance, sterility dates, pharmacological classes
- `chemical`: Chemical industry with safety coefficients, explosion-proof requirements, hazard classes
- `general`: General manufacturing without industry-specific requirements

## Implementation Standards

1. **Model Naming**: All ISL models follow the pattern `farm.{module}.{model}` (e.g., `farm.mrp.production`)
2. **Field Structure**: Common industry_type field with validation methods for each industry
3. **Inheritance**: Use `_inherits` for extension, never `_inherit` for ISL models
4. **Relationship Field**: Use base model name with `_id` suffix (e.g., `mrp_production_id`)
5. **Validation Methods**: Industry-specific validation in `_validate_{model}_compliance` methods
6. **Security**: Comprehensive access rights defined in `ir.model.access.csv`

## Usage Pattern

1. Create base Odoo model instances as usual
2. ISL records are automatically created via the redirection mechanism
3. Industry-specific fields and validation are available on ISL models
4. Use the ISL model for industry-specific operations while maintaining access to base functionality

## Extension Points

The ISL architecture provides several extension points for additional functionality:

- New industry types can be added to the `industry_type` selection field
- Industry-specific extension modules can be created using the `ISLIndustryExtension` model
- Custom validation methods can be added to specific ISL models
- View customizations can be added for industry-specific user interfaces