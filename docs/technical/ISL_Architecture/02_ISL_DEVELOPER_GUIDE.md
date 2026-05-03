# 02_ISL_DEVELOPER_GUIDE



---

## 📄 Source Document: _INHERITS_IMPLEMENTATION.md

# ISL Architecture: _inherits Implementation Guide

## Overview
This document provides comprehensive guidance on implementing the ISL (Industry Specialized Layer) architecture using the `_inherits` mechanism for maximum data integrity and proper model relationships.

## Understanding _inherits vs _inherit

### _inherits Mechanism
The `_inherits` mechanism creates a one-to-one relationship between models where:
- The inheriting model owns the base model record
- The base model record is automatically deleted when the ISL record is deleted (cascade delete)
- All fields from the base model are accessible through the ISL model
- The ISL model has its own database table with a foreign key to the base model
- Provides complete ownership and control of the base record

### _inherit Mechanism
The `_inherit` mechanism extends an existing model by:
- Adding new fields to the existing model's database table
- Sharing the same database table between models
- Not creating ownership relationships
- Allowing multiple models to extend the same base model

## ISL Architecture with _inherits

The ISL architecture uses `_inherits` to create industry-specialized extensions of core Odoo models while maintaining all base functionality.

### 1. Basic _inherits Pattern

```python
class FarmMRPProduction(models.Model):
    _name = 'farm.mrp.production'
    _description = 'Farm ISL MRP Production Order'
    _inherits = {'mrp.production': 'mrp_production_id'}
    _inherit = ['farm.manufacturing.mixin']  # Abstract model for industry features

    mrp_production_id = fields.Many2one(
        'mrp.production',
        string='Base MRP Production',
        required=True,
        ondelete='cascade'
    )

    # Industry-specific fields
    haccp_plan = fields.Html('HACCP Plan')  # Food processing
    gmp_compliance = fields.Boolean('GMP Compliance')  # Pharmaceutical
    safety_procedures = fields.Html('Safety Procedures')  # Chemical
```

### 2. _inherits with Industry Specialization

```python
class FarmProcessingProduction(models.Model):
    _name = 'farm.processing.production'
    _description = 'Farm Food Processing Production Order'
    _inherits = {'mrp.production': 'mrp_production_id'}  # Direct extension of base model
    _inherit = ['farm.manufacturing.mixin']  # Industry abstract functionality

    mrp_production_id = fields.Many2one(
        'mrp.production',
        string='Base MRP Production',
        required=True,
        ondelete='cascade'
    )

    # Food processing specific fields
    energy_reading_start = fields.Float(string='Energy Reading Start')
    energy_reading_end = fields.Float(string='Energy Reading End')
    haccp_instructions = fields.Html("HACCP Critical Instructions")
    target_temp = fields.Float('Standard Temperature (℃)')
    target_ph = fields.Float("Target pH")

    def write(self, vals):
        # Ensure industry type is set for food processing
        if 'industry_type' not in vals and not self.industry_type:
            vals['industry_type'] = 'food_processing'
        return super().write(vals)

    @api.model_create_multi
    def create(self, vals_list):
        # Ensure industry type is set for food processing
        for vals in vals_list:
            if 'industry_type' not in vals or not vals.get('industry_type'):
                vals['industry_type'] = 'food_processing'
        return super().create(vals_list)
```

### 3. _inherits with Polymorphic Links

```python
class FarmProcessingProduction(models.Model):
    _name = 'farm.processing.production'
    _description = 'Farm Food Processing Order'
    _inherits = {'mrp.production': 'mrp_production_id'}
    _inherit = ['farm.manufacturing.mixin']

    mrp_production_id = fields.Many2one(
        'mrp.production',
        string='Base Production Order',
        required=True,
        ondelete='cascade'
    )

    # Polymorphic link to processing-specific BOM
    processing_bom_id = fields.Many2one(
        'farm.processing.bom',
        string='Processing Recipe',
        compute='_compute_processing_bom_id'
    )

    @api.depends('bom_id')
    def _compute_processing_bom_id(self):
        for rec in self:
            if rec.bom_id:
                processing_bom = self.env['farm.processing.bom'].search(
                    [('bom_id', '=', rec.bom_id.id)], limit=1
                )
                rec.processing_bom_id = processing_bom
            else:
                rec.processing_bom_id = False
```

## Architecture Benefits of _inherits in ISL

### 1. Complete Ownership
- The ISL model completely owns its base model record
- Cascade deletion ensures data integrity
- No orphaned base records when ISL records are deleted

### 2. Field Isolation
- Industry-specific fields are in the ISL model's table
- Base model fields remain in the original table
- Clear separation of concerns

### 3. Method Override Capability
- ISL models can completely override base model methods
- Industry-specific business logic is properly isolated
- Base model functionality remains unchanged

### 4. Relationship Management
- Foreign key relationships are explicitly defined
- Data integrity is maintained through constraints
- Proper cleanup when records are deleted

## Complete _inherits Implementation Pattern

### 1. Abstract Base Models (in farm_isl)
```python
# In farm_isl/models/isl_abstract_models.py
class FarmManufacturingMixin(models.AbstractModel):
    _name = 'farm.manufacturing.mixin'
    _description = 'Farm Manufacturing ISL Abstract Base Model'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Common industry fields
    industry_type = fields.Selection([
        ('food_processing', 'Food Processing'),
        ('pharmaceutical', 'Pharmaceutical'),
        ('chemical', 'Chemical'),
        ('general', 'General Manufacturing')
    ], string='Industry Type', default='general', required=True)

    industry_specialization = fields.Char('Industry Specialization')
    compliance_requirements = fields.Text('Compliance Requirements')
```

### 2. Centralized ISL Models (in farm_isl)
```python
# In farm_isl/models/isl_concrete_models.py
class FarmMRPProduction(models.Model):
    _name = 'farm.mrp.production'
    _description = 'Farm ISL MRP Production Order'
    _inherits = {'mrp.production': 'mrp_production_id'}
    _inherit = ['farm.manufacturing.mixin']

    mrp_production_id = fields.Many2one(
        'mrp.production',
        string='Base MRP Production',
        required=True,
        ondelete='cascade'
    )

    # Industry-specific fields that apply across all industries
    quality_gate_checks = fields.Text('Quality Gate Checks')
```

### 3. Industry-Specific Extensions (in farm_{industry})
```python
# In farm_processing/models/processing_isl.py (MODIFIED - using _inherits instead of _inherit)
class FarmProcessingProduction(models.Model):
    _name = 'farm.processing.production'
    _description = 'Farm Food Processing Production Order'
    _inherits = {'mrp.production': 'mrp_production_id'}  # Direct base extension
    _inherit = ['farm.manufacturing.mixin']  # Abstract functionality

    mrp_production_id = fields.Many2one(
        'mrp.production',
        string='Base Production Order',
        required=True,
        ondelete='cascade'
    )

    # Food processing specific fields
    energy_reading_start = fields.Float(string='Energy Reading Start')
    haccp_instructions = fields.Html("HACCP Critical Instructions")
    target_temp = fields.Float('Standard Temperature (℃)')

    def action_confirm(self):
        # Food processing specific validation
        if self.industry_type == 'food_processing' and not self.haccp_instructions:
            raise UserError(_("Food processing requires HACCP instructions"))

        # Call parent method to maintain base functionality
        return super().action_confirm()
```

## Data Migration with _inherits

When migrating to the _inherits pattern:

```python
def migrate_to_isl_inherits(self):
    """Migrate existing data to use _inherits pattern"""
    # Get all base records that need ISL extension
    base_records = self.env['mrp.production'].search([])

    for base_record in base_records:
        # Create ISL record with _inherits relationship
        isl_record = self.env['farm.mrp.production'].create({
            'mrp_production_id': base_record.id,  # This creates the _inherits relationship
            'industry_type': self.determine_industry_type(base_record),
            'haccp_plan': self.extract_haccp_data(base_record) if self.is_food_processing(base_record) else False,
            'gmp_compliance': self.is_pharmaceutical_production(base_record),
        })

def determine_industry_type(self, base_record):
    """Determine appropriate industry type for base record"""
    product_category = base_record.product_id.categ_id.name.lower()

    if 'food' in product_category or 'process' in product_category:
        return 'food_processing'
    elif 'pharma' in product_category:
        return 'pharmaceutical'
    elif 'chem' in product_category:
        return 'chemical'
    else:
        return 'general'
```

## Security and Access Control with _inherits

The `_inherits` pattern works well with Odoo security:

```python
# In security/ir.model.access.csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_isl_farm_mrp_production,farm.mrp.production,model_farm_mrp_production,farm_security.group_farm_user,1,1,1,1
```

Since the ISL model has its own database table, standard access controls apply.

## View Integration with _inherits

Views work seamlessly with `_inherits`:

```xml
<!-- The ISL model can access all base model fields -->
<record id="view_isl_mrp_production_form" model="ir.ui.view">
    <field name="name">farm.mrp.production.form</field>
    <field name="model">farm.mrp.production</field>
    <field name="arch" type="xml">
        <form string="ISL MRP Production">
            <sheet>
                <group>
                    <group>
                        <!-- Base model fields from mrp.production -->
                        <field name="name"/>
                        <field name="product_id"/>
                        <field name="product_qty"/>
                        <field name="date_planned_start"/>
                    </group>
                    <group>
                        <!-- ISL specific fields -->
                        <field name="industry_type"/>
                        <field name="haccp_plan" invisible="industry_type != 'food_processing'"/>
                        <field name="gmp_compliance" invisible="industry_type != 'pharmaceutical'"/>
                    </group>
                </group>
            </sheet>
        </form>
    </field>
</record>
```

## Best Practices for _inherits in ISL

### 1. Always Define Foreign Key Field
```python
# Correct
mrp_production_id = fields.Many2one(
    'mrp.production',
    string='Base MRP Production',
    required=True,
    ondelete='cascade'
)

# Incorrect - no explicit foreign key
class BadExample(models.Model):
    _name = 'bad.example'
    _inherits = {'mrp.production': 'production_id'}  # But no production_id field defined
```

### 2. Use Descriptive Foreign Key Names
```python
# Good - descriptive names
mrp_production_id = fields.Many2one('mrp.production', ...)
stock_lot_id = fields.Many2one('stock.lot', ...)
sale_order_id = fields.Many2one('sale.order', ...)
```

### 3. Set ondelete='cascade'
Always use `ondelete='cascade'` to maintain data integrity:

```python
mrp_production_id = fields.Many2one(
    'mrp.production',
    required=True,
    ondelete='cascade'  # Ensures base record is deleted when ISL record is deleted
)
```

### 4. Initialize Industry Type
```python
@api.model_create_multi
def create(self, vals_list):
    for vals in vals_list:
        if 'industry_type' not in vals or not vals.get('industry_type'):
            vals['industry_type'] = 'your_default_industry'
    return super().create(vals_list)

def write(self, vals):
    if 'industry_type' not in vals and not self.industry_type:
        vals['industry_type'] = 'your_default_industry'
    return super().write(vals)
```

## Migration Path from _inherit to _inherits

If converting from `_inherit` pattern to `_inherits`, follow these steps:

1. **Create New ISL Models with _inherits**:
```python
# New pattern (recommended)
class FarmProcessingProduction(models.Model):
    _name = 'farm.processing.production'
    _inherits = {'mrp.production': 'mrp_production_id'}
    _inherit = ['farm.manufacturing.mixin']
```

2. **Migrate Existing Data**:
```python
def migrate_to_inherits_pattern(self):
    # For each existing record based on _inherit pattern
    old_records = self.env['farm.mrp.production'].search([('industry_type', '=', 'food_processing')])

    for old_record in old_records:
        # Create new ISL record with _inherits relationship
        new_record = self.env['farm.processing.production'].create({
            # Link to same base record if exists
            'mrp_production_id': old_record.mrp_production_id,  # This is key
            'energy_reading_start': old_record.energy_reading_start,
            'haccp_instructions': old_record.haccp_instructions,
            'industry_type': old_record.industry_type,
        })
```

This guide ensures the ISL architecture properly uses the `_inherits` mechanism for complete ownership, proper relationships, and maximum flexibility in industry specialization.



---

## 📄 Source Document: INDUSTRY_ISOLATION_GUIDE.md

# ISL Architecture: Industry Isolation Guide

## Overview
This document provides comprehensive guidance on using the ISL (Industry Specialized Layer) architecture to properly isolate business logic for different industries while maintaining shared core functionality.

## Purpose of Industry Isolation

The ISL architecture enables:
1. **Business Logic Separation**: Keep industry-specific logic isolated from other industries
2. **Shared Infrastructure**: Maintain common functionality across all industries
3. **Scalability**: Add new industries without affecting existing ones
4. **Maintainability**: Modify one industry's logic without impacting others
5. **Compliance**: Meet industry-specific regulatory requirements

## Core Isolation Principles

### 1. Industry Type Segregation
Each ISL model includes an `industry_type` field that determines which industry-specific logic applies:

```python
industry_type = fields.Selection([
    ('food_processing', 'Food Processing'),
    ('pharmaceutical', 'Pharmaceutical'),
    ('chemical', 'Chemical'),
    ('livestock', 'Livestock'),
    ('aquaculture', 'Aquaculture'),
    ('crop', 'Crop Agriculture'),
    ('general', 'General Manufacturing')
], string='Industry Type', default='general', required=True)
```

### 2. Industry-Specific Validation
Each industry implements its own validation logic:

```python
def _validate_industry_requirements(self):
    if self.industry_type == 'food_processing':
        if not self.haccp_plan:
            raise UserError(_("Food processing production requires HACCP plan"))
    elif self.industry_type == 'pharmaceutical':
        if not self.gmp_compliance:
            raise UserError(_("Pharmaceutical production requires GMP compliance"))
    elif self.industry_type == 'livestock':
        if not self.health_certification:
            raise UserError(_("Livestock operations require health certification"))
    # Add other industry validations
    return True
```

### 3. Industry-Specific Fields
Each industry defines its own specialized fields while sharing common infrastructure:

- **Food Processing**: HACCP plans, allergen controls, kill dates
- **Pharmaceutical**: GMP compliance, sterility dates, pharmacological classes
- **Chemical**: Safety coefficients, explosion-proof requirements, hazard classes
- **Livestock**: Breeding status, health index, feed conversion ratios
- **Aquaculture**: Water quality parameters, stocking density, harvest timing

## Implementation Pattern for Industry Isolation

### 1. Centralized Abstract Models
The `farm_isl` module provides abstract base models with common industry functionality:

```python
class FarmManufacturingMixin(models.AbstractModel):
    _name = 'farm.manufacturing.mixin'
    # Common industry infrastructure
    industry_type = fields.Selection([...])
    # Common methods and fields
```

### 2. Industry-Specific Extensions
Each industry extends the centralized models with specialized functionality:

```python
# In farm_processing module
class FarmProcessingProduction(models.Model):
    _name = 'farm.processing.production'
    _description = 'Farm Food Processing Order (ISL Layer)'
    _inherit = ['farm.mrp.production', 'farm.agri.production.mixin']

    # Food Processing specific fields
    haccp_instructions = fields.Html("HACCP Critical Instructions")
    target_temp = fields.Float('Standard Temperature (℃)')
    target_ph = fields.Float("Target pH")

    def write(self, vals):
        # Ensure industry type is set to food processing
        if 'industry_type' not in vals and not self.industry_type:
            vals['industry_type'] = 'food_processing'
        return super().write(vals)
```

### 3. Industry-Specific Views
Each industry has its own view customizations through specialized view files:

```xml
<!-- farm_processing/views/processing_production_views.xml -->
<record id="view_processing_production_form" model="ir.ui.view">
    <field name="name">farm.processing.production.form</field>
    <field name="model">farm.processing.production</field>
    <field name="arch" type="xml">
        <form string="Food Processing Production">
            <sheet>
                <group>
                    <group>
                        <field name="name"/>
                        <field name="product_id"/>
                        <!-- Common fields -->
                    </group>
                    <group string="Food Processing Specific">
                        <field name="haccp_instructions"/>
                        <field name="target_temp"/>
                        <field name="target_ph"/>
                        <!-- Industry-specific fields -->
                    </group>
                </group>
            </sheet>
        </form>
    </field>
</record>
```

## Industry Isolation Mechanisms

### 1. Data Isolation
- Each industry's data is tagged with `industry_type`
- Business logic only applies to records matching the industry type
- Reports and queries are filtered by industry type

### 2. Business Logic Isolation
- Industry-specific methods only execute for matching industry types
- Validation rules apply only to relevant industries
- Computed fields use industry-specific logic

### 3. User Interface Isolation
- Industry-specific fields appear only when relevant
- Industry-specific workflows apply only to matching records
- Industry-specific actions are available based on type

### 4. Security Isolation
- Industry-specific security rules can be applied
- Access controls can be fine-tuned by industry
- Industry-specific audit trails maintained

## Best Practices for Industry Isolation

### 1. Industry-Specific Model Creation
```python
# Good: Industry-specific extension of centralized ISL model
class FarmLivestockBom(models.Model):
    _name = 'farm.livestock.bom'
    _description = 'Livestock Breeding BOM (ISL Layer)'
    _inherit = ['farm.mrp.bom', 'farm.agri.bom.mixin']

    # Livestock-specific fields
    growth_days_expected = fields.Integer("Expected Growth Days")
    daily_feed_intake = fields.Float("Avg Daily Feed (kg)")
```

### 2. Industry Type Enforcement
```python
@api.model_create_multi
def create(self, vals_list):
    for vals in vals_list:
        if 'industry_type' not in vals or not vals.get('industry_type'):
            vals['industry_type'] = 'livestock'  # Industry-specific default
    return super().create(vals_list)

def write(self, vals):
    if 'industry_type' not in vals and not self.industry_type:
        vals['industry_type'] = 'livestock'  # Ensure industry type is maintained
    return super().write(vals)
```

### 3. Industry-Specific Validation
```python
def _validate_livestock_compliance(self):
    """Livestock-specific validation logic"""
    if self.industry_type != 'livestock':
        return True  # Only apply to livestock industry

    # Livestock-specific validation
    if self.breeding_status == 'pregnant' and not self.pregnancy_test_date:
        raise UserError(_("Pregnant livestock must have pregnancy test date"))

    return True
```

### 4. Industry-Neutral Core Logic
Keep core infrastructure logic in the centralized ISL models:

```python
# In farm_isl/models/isl_concrete_models.py - industry-neutral
class FarmMRPProduction(models.Model):
    _name = 'farm.mrp.production'
    _inherits = {'mrp.production': 'mrp_production_id'}
    _inherit = ['farm.manufacturing.mixin']

    # Industry-neutral core logic
    def action_confirm(self):
        # Common logic that applies to all industries
        self._validate_common_requirements()

        # Industry-specific validation
        self._validate_industry_requirements()

        # Delegate to base model
        return self.mrp_production_id.action_confirm()
```

## Industry-Specific Module Structure

Each industry module should follow this structure:

```
farm_{industry}/
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── {industry}_isl.py          # Industry-specific ISL extensions
│   └── {other_models}.py
├── views/
│   ├── {industry}_views.xml       # Industry-specific views
│   └── menu.xml
├── security/
│   └── ir.model.access.csv
└── data/
    └── {industry}_data.xml
```

## Data Isolation Implementation

The ISL architecture implements data isolation through several mechanisms:

### 1. Industry Type Assignment
Each ISL record must have an industry type assigned:

```python
industry_type = fields.Selection([
    ('food_processing', 'Food Processing'),
    ('pharmaceutical', 'Pharmaceutical'),
    ('chemical', 'Chemical'),
    ('livestock', 'Livestock'),
    ('aquaculture', 'Aquaculture'),
    ('crop', 'Crop Agriculture'),
    ('general', 'General Manufacturing')
], string='Industry Type', default='general', required=True)
```

### 2. Industry-Specific Views
Views use visibility conditions to show only relevant fields:

```xml
<page string="Industry Specific" invisible="industry_type != 'food_processing'">
    <group>
        <field name="haccp_plan" placeholder="HACCP Plan for food processing"/>
    </group>
</page>
```

### 3. Data Migration for Industry Assignment
When onboarding existing data to ISL architecture:

```python
def migrate_to_industry_specific(isl_record, source_record):
    """Assign proper industry type and migrate industry-specific data"""
    industry_type = determine_industry_from_context(source_record)
    isl_record.write({'industry_type': industry_type})

    if industry_type == 'livestock':
        # Migrate livestock-specific data
        isl_record.write({
            'health_index': source_record.get('health_data', 100.0),
            'breeding_status': source_record.get('breeding_data', 'immature')
        })
    elif industry_type == 'food_processing':
        # Migrate food processing-specific data
        isl_record.write({
            'haccp_plan': source_record.get('haccp_data'),
            'target_temp': source_record.get('temperature_target', 0.0)
        })
```

## Two Approaches to Industry-Specific Extensions

The ISL architecture supports two approaches for industry-specific extensions:

### Approach 1: Direct Extension from Base Models with _inherits (Recommended)
```python
# Industry-specific model using _inherits mechanism (RECOMMENDED)
class FarmProcessingProduction(models.Model):
    _name = 'farm.processing.production'
    _description = 'Farm Food Processing Order'
    _inherits = {'mrp.production': 'mrp_production_id'}  # Direct relationship to base model
    _inherit = ['farm.manufacturing.mixin']  # Abstract industry functionality

    # Critical: Define the foreign key field
    mrp_production_id = fields.Many2one(
        'mrp.production',
        string='Base Production Order',
        required=True,
        ondelete='cascade'  # Ensures proper cleanup
    )

    # Food processing specific fields
    energy_reading_start = fields.Float(string='Energy Reading Start')
    haccp_instructions = fields.Html("HACCP Critical Instructions")
```

### Approach 2: Extension from Centralized ISL Models (Alternative)
```python
# Industry extends centralized ISL model (also valid)
class FarmProcessingProduction(models.Model):
    _name = 'farm.processing.production'
    _description = 'Farm Food Processing Order'
    _inherit = ['farm.mrp.production', 'farm.agri.production.mixin']  # Extends centralized ISL

    # Food processing specific fields
    energy_reading_start = fields.Float(string='Energy Reading Start')
    haccp_instructions = fields.Html("HACCP Critical Instructions")
```

### Key Considerations for _inherits Approach (Recommended)

The `_inherits` approach is recommended because it provides:
- **Complete ownership**: The ISL record owns its base record
- **Proper cleanup**: Cascade deletion maintains data integrity
- **Clear relationships**: Explicit foreign key relationships
- **Better performance**: Direct database relationships

When using `_inherits`, always remember to:
1. Define the Many2one field for the base model relationship
2. Use `ondelete='cascade'` for proper cleanup
3. Use descriptive field names (e.g., `mrp_production_id`, `stock_lot_id`)
4. Set the proper industry type during creation/updates

## Data Migration for Industry Isolation

When onboarding a new industry:

1. **Define Industry Type**: Add to the `industry_type` selection
2. **Create ISL Extensions**: Extend centralized models with industry-specific logic
3. **Migrate Existing Data**: Use migration utilities to assign proper industry types
4. **Configure Views**: Set up industry-specific UI elements
5. **Implement Validation**: Add industry-specific business rules

## Testing Industry Isolation

### 1. Unit Tests
```python
def test_food_processing_specific_logic(self):
    """Test that food processing logic only applies to food processing records"""
    processing_record = self.env['farm.processing.production'].create({
        'name': 'Test Processing',
        'industry_type': 'food_processing',
        'haccp_instructions': 'Test HACCP Plan'
    })

    # Test processing-specific validation
    with self.assertRaises(UserError):
        processing_record.write({'haccp_instructions': False})  # Should fail validation
```

### 2. Integration Tests
```python
def test_industry_separation(self):
    """Test that one industry's logic doesn't affect another"""
    livestock_record = self.env['farm.livestock.production'].create({
        'name': 'Test Livestock',
        'industry_type': 'livestock',
        'health_index': 95.0
    })

    processing_record = self.env['farm.processing.production'].create({
        'name': 'Test Processing',
        'industry_type': 'food_processing',
        'target_temp': 75.0
    })

    # Ensure each record only triggers its own industry-specific logic
    livestock_record.write({'health_index': 90.0})  # Should only validate livestock rules
    processing_record.write({'target_temp': 80.0})   # Should only validate processing rules
```

## Benefits of Proper Industry Isolation

1. **Reduced Complexity**: Each industry's logic is isolated and manageable
2. **Easier Maintenance**: Changes in one industry don't affect others
3. **Regulatory Compliance**: Industry-specific requirements can be implemented
4. **Scalability**: New industries can be added without disrupting existing ones
5. **Security**: Industry-specific access controls and data isolation
6. **Auditability**: Industry-specific audit trails and compliance reporting

## Common Pitfalls to Avoid

1. **Cross-Industry Dependencies**: Avoid business logic that assumes other industries exist
2. **Non-Industry-Specific Logic in Industry Modules**: Keep core functionality in centralized ISL
3. **Hardcoded Industry Logic**: Use `industry_type` field in conditional logic
4. **Inconsistent Field Naming**: Follow consistent naming patterns across industries
5. **Missing Industry Type Enforcement**: Always ensure proper industry type assignment

This guide ensures that the ISL architecture properly isolates business logic across different industries while maintaining the benefits of shared infrastructure.



---

## 📄 Source Document: INTEGRATION_GUIDE.md

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

