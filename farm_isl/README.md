# Industry Specialized Layer (ISL) Module Architecture

The ISL module implements a standardized architecture for industry-specific extensions to core Odoo models. The architecture follows the single responsibility principle and provides a consistent pattern for extending core agricultural functionality with vertical industry requirements.

## Architecture Overview

The ISL architecture follows these key design principles:

1. **Separation of Concerns**: Abstract models handle common functionality, concrete models extend Odoo core models.
2. **Inheritance Pattern**: Uses the `_inherits` mechanism to extend core Odoo models while maintaining all base functionality and avoiding base table bloating.
3. **Industry Specialization**: Common industry fields and validation across all ISL models tailored for the agricultural domain.
4. **Automatic Redirection**: Built-in intelligent routing (`agri.isl.model.redirector`) to redirect base models to their specific ISL counterparts.

## Core Components

### 1. Abstract Base Models (`agri_isl_abstract_models.py`)
Provide common functionality and industry-specific fields for different functional areas:

- `AgriManufacturingMixin`: For manufacturing/intervention models (MRP Production, BOM, Work Centers, Work Orders).
- `AgriInventoryMixin`: For inventory-related models (Stock Lots, Stock Pickings).
- `AgriSalesPurchaseMixin`: For sales/purchase-related models (Sale Orders, Purchase Orders).
- `AgriProductMixin`: For product-related models (Product Templates).
- `AgriQualityMixin`: For quality control models.

### 2. Concrete ISL Models (`agri_isl_concrete_models.py`)
Extend core Odoo models using the `_inherits` mechanism. These serve as the central bridging proxy:

- `AgriMRPProduction`: Extends `mrp.production`
- `AgriMRPBom`: Extends `mrp.bom`
- `AgriMRPWorkcenter`: Extends `mrp.workcenter`
- `AgriMRPWorkorder`: Extends `mrp.workorder`
- `AgriStockLot`: Extends `stock.lot`
- `AgriStockPicking`: Extends `stock.picking`
- `AgriSaleOrder`: Extends `sale.order`
- `AgriPurchaseOrder`: Extends `purchase.order`
- `AgriProductTemplate`: Extends `product.template`
- `AgriQualityControl`: Extends `quality.point`

### 3. Redirection System (`agri_isl_redirection.py`)
- `AgriISLModelRedirector`: Provides automatic routing from generic base records to vertical ISL records.
- `AgriISLIndustryExtension`: Manages dynamic industry-specific extensions.

### 4. Migration & Performance Utilities
- Provided via `agri_isl_migration.py` and `agri_isl_performance.py`.

## Supported Agricultural Domains (De-industrialized)

All ISL models support the following vertical agricultural industries:

- `field_crop`: Traditional agriculture, planting, and harvesting.
- `livestock`: Animal husbandry, breeding, and feeding operations.
- `aquaculture`: Water-based farming, RAS systems, and fish production.
- `general`: General agriculture without specific vertical requirements.

## Implementation Standards

1. **Namespace Unification**: All ISL models MUST follow the strict `agri.isl.*` namespace (e.g., `agri.isl.mrp.production` or `agri.isl.livestock.production`).
2. **Field Structure**: Common `industry_type` field utilizing the agricultural domains listed above.
3. **Inheritance Rule**: Use the `_inherits` (delegation inheritance) mechanism for extension to create proper ownership relationships without polluting base L1 tables.
4. **Relationship Linking**: Use the base model name with the `_id` suffix (e.g., `mrp_production_id`).
5. **Foreign Key Safety**: Always define the Many2one field for the base model relationship with `ondelete='cascade'`.

## Distributed Specialization Pattern

The ISL architecture is a hybrid approach combining centralized infrastructure with distributed specialization:
- **Core Infrastructure** (`farm_isl`): Provides the abstract mixins, standard concrete proxies, and the Redirector logic.
- **Industry Apps** (`farm_livestock`, `farm_aquaculture`, `farm_crop`): Inject their unique models by inheriting from the central `agri.isl.*` proxies, allowing each vertical to maintain specialized UI and behaviors securely.

## Advanced Architectural Guidelines

1. **Granular Trait Composition (按需特质混入原则)**: When composing behavior traits (such as `agri.isl.trait.food_safety` or `agri.isl.trait.livestock`) into concrete ISL models, vertical developers MUST adhere to strict granular composition. Avoid blank-check multiple inheritance. Exclude unused traits to maintain physical table narrowness.
2. **Multi-level Cascade Safeguard (多级级联物理删除防护)**: When deleting ISL records via cascading foreign keys (`ondelete='cascade'`), developers MUST override the `unlink()` method in the proxy model to guard against forensic traceability shattering. If the record is linked to active dynamic Matter carriers or holds unresolved GxP inspections, delete propagation must be locked with a `UserError`.