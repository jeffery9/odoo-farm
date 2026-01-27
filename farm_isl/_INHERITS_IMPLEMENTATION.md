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