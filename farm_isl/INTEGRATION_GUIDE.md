# ISL Module Integration Guide

## Overview
This document provides guidance on how to properly integrate other farm modules with the ISL (Industry Specialized Layer) architecture for consistent functionality and standardization across the farm module ecosystem.

## ISL Architecture Components

### 1. Abstract Models
Abstract models provide common industry functionality for different business domains:

- `farm.manufacturing.mixin`: For manufacturing-related models (MRP Production, BOM, Work Centers, Work Orders)
- `farm.inventory.mixin`: For inventory-related models (Stock Lots, Stock Pickings)
- `farm.sales.purchase.mixin`: For sales/purchase-related models (Sale Orders, Purchase Orders)
- `farm.product.mixin`: For product-related models (Product Templates)
- `farm.quality.mixin`: For quality control models (Quality Control Points)

### 2. Concrete ISL Models
Concrete models extend core Odoo models using the `_inherits` pattern:

- Follow naming convention: `farm.{module}.{model}`
- Use `_inherits` to extend core functionality while maintaining access to base model
- Include base model reference with `{base_model}_id` field pattern
- Implement industry-specific validation methods

### 3. Utility Components
- `isl.model.redirector`: Automatic redirection from base models to ISL models
- `isl.optimization.mixin`: Performance optimization and caching
- `isl.migration.utility`: Data migration tools

## Integration Standards for Other Modules

### 1. Supply Module Integration
The `farm_supply` module should be refactored to use ISL patterns:

```python
# Instead of creating direct extensions, use ISL pattern:
class FarmSupplyOrder(models.Model):
    _name = 'farm.supply.order'
    _inherits = {'purchase.order': 'purchase_order_id'}
    _inherit = ['farm.sales.purchase.mixin']

    purchase_order_id = fields.Many2one(
        'purchase.order',
        string='Base Purchase Order',
        required=True,
        ondelete='cascade'
    )

    # Supply-specific fields with industry specialization
    supply_category = fields.Selection([
        ('seed', 'Seed'),
        ('fertilizer', 'Fertilizer'),
        ('pesticide', 'Pesticide'),
        ('equipment', 'Equipment')
    ], string='Supply Category')
```

### 2. Core Module Integration
When creating new functionality in core modules, consider ISL integration:

```python
# In farm_core or other modules, extend using ISL patterns:
class FarmCoreOperation(models.Model):
    _name = 'farm.core.operation'
    _inherits = {'stock.move': 'stock_move_id'}  # Example of extending existing model
    _inherit = ['farm.inventory.mixin']

    stock_move_id = fields.Many2one(
        'stock.move',
        string='Base Stock Move',
        required=True,
        ondelete='cascade'
    )
```

### 3. Security Configuration
All ISL-related models should have proper security configuration in their respective modules:

```xml
<!-- In the module's security/ir.model.access.csv file -->
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_farm_supply_order,farm.supply.order,model_farm_supply_order,farm_security.group_farm_user,1,1,1,1
```

### 4. Menu Structure
ISL models should be accessible through unified menu structure:

```xml
<!-- In the module's views/menu.xml file -->
<menuitem id="menu_isl_supply_order"
          name="ISL Supply Orders"
          parent="farm_isl_sales_purchase_menu"
          action="action_isl_supply_order"
          sequence="30"/>
```

## Best Practices for ISL Integration

### 1. Model Design
- Use `_inherits` for extension, never `_inherit` for ISL models
- Follow naming convention: `farm.{domain}.{model}`
- Always include proper base model reference
- Implement industry-specific validation methods
- Use consistent industry_type field with validation

### 2. Data Migration
- When implementing new ISL models for existing data, use the migration utilities
- Ensure backward compatibility during transitions
- Test data integrity throughout the migration process

### 3. Performance Considerations
- Use the redirection utility for automatic base-to-ISL routing
- Leverage caching mechanisms for improved performance
- Consider the impact on existing functionality

### 4. View Integration
- Provide views that show both base and ISL model data
- Include navigation between base and ISL models
- Maintain consistent UI experience across all modules

## Migration Checklist for Existing Modules

When integrating existing modules with ISL architecture:

1. **Identify Core Models** - Determine which core Odoo models need industry specialization
2. **Design ISL Extension** - Create appropriate ISL model using `_inherits`
3. **Implement Abstract Model Inheritance** - Use appropriate mixin for the business domain
4. **Add Industry Fields** - Include industry-specific fields and validation
5. **Update Security** - Add appropriate access rights in security files
6. **Create Views** - Develop user interfaces for ISL functionality
7. **Implement Migration** - Create migration path for existing data
8. **Test Integration** - Ensure proper functionality and data integrity
9. **Update Documentation** - Document the new ISL integration

## Common Integration Patterns

### 1. Inventory Extensions
```python
class FarmInventoryExtension(models.Model):
    _name = 'farm.inventory.extension'
    _inherits = {'stock.lot': 'stock_lot_id'}  # or stock.picking, stock.move, etc.
    _inherit = ['farm.inventory.mixin']
```

### 2. Manufacturing Extensions
```python
class FarmManufacturingExtension(models.Model):
    _name = 'farm.manufacturing.extension'
    _inherits = {'mrp.production': 'mrp_production_id'}  # or mrp.bom, mrp.workorder, etc.
    _inherit = ['farm.manufacturing.mixin']
```

### 3. Sales/Purchase Extensions
```python
class FarmSalesPurchaseExtension(models.Model):
    _name = 'farm.sales.purchase.extension'
    _inherits = {'sale.order': 'sale_order_id'}  # or purchase.order, etc.
    _inherit = ['farm.sales.purchase.mixin']
```

This guide ensures consistent application of the ISL architecture across all farm modules, maintaining standardized patterns and integration points.