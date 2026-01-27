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