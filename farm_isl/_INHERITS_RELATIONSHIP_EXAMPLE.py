# ISL Architecture: _inherits Relationship Examples

# This file demonstrates proper _inherits relationships in the ISL architecture

from odoo import models, fields, api, _
from odoo.exceptions import UserError


# 1. CENTRALIZED ISL MODEL (in farm_isl module)
class FarmMRPProduction(models.Model):
    """
    Centralized ISL model that extends base MRP Production with industry specialization
    This follows the _inherits pattern to own the base record completely
    """
    _name = 'agri.isl.mrp.production'
    _description = 'Farm ISL MRP Production Order'
    _inherits = {'mrp.production': 'mrp_production_id'}  # Owns base production record
    _inherit = ['agri.isl.manufacturing.mixin']  # Industry abstract functionality

    # Foreign key relationship - CRITICAL for _inherits
    mrp_production_id = fields.Many2one(
        'mrp.production',
        string='Base MRP Production',
        required=True,
        ondelete='cascade'  # Ensures base record is deleted when ISL record is deleted
    )

    # ISL-specific fields (available to all industries)
    quality_gate_checks = fields.Text('Quality Gate Checks')
    industry_notes = fields.Html('Industry Notes')


# 2. INDUSTRY-SPECIFIC MODEL (in farm_processing module)
class FarmProcessingProduction(models.Model):
    """
    Industry-specific model that uses _inherits to directly extend base Odoo model
    This approach provides complete ownership of the base record by the industry model
    """
    _name = 'farm.processing.production'
    _description = 'Farm Food Processing Production Order'
    _inherits = {'mrp.production': 'mrp_production_id'}  # Direct inheritance from base
    _inherit = ['agri.isl.manufacturing.mixin']  # Abstract industry functionality

    # Foreign key relationship - CRITICAL for _inherits
    mrp_production_id = fields.Many2one(
        'mrp.production',
        string='Base Production Order',
        required=True,
        ondelete='cascade'
    )

    # Food processing specific fields
    energy_reading_start = fields.Float(string='Energy Reading Start', copy=False)
    energy_reading_end = fields.Float(string='Energy Reading End', copy=False)
    energy_cost_total = fields.Float(string='Total Energy Cost', compute='_compute_energy_cost')
    haccp_instructions = fields.Html("HACCP Critical Instructions")
    target_temp = fields.Float('Standard Temperature (℃)')
    target_ph = fields.Float("Target pH")

    @api.depends('energy_reading_start', 'energy_reading_end')
    def _compute_energy_cost(self):
        for rec in self:
            rec.energy_cost_total = (rec.energy_reading_end - rec.energy_reading_start) * 1.0

    def write(self, vals):
        # Ensure industry type is set for food processing
        if 'industry_type' not in vals and not self.industry_type:
            vals['industry_type'] = 'field_crop'
        return super().write(vals)

    @api.model_create_multi
    def create(self, vals_list):
        # Ensure industry type is set for food processing
        for vals in vals_list:
            if 'industry_type' not in vals or not vals.get('industry_type'):
                vals['industry_type'] = 'field_crop'
        return super().create(vals_list)

    def action_confirm(self):
        # Industry-specific validation
        if self.industry_type == 'field_crop' and not self.haccp_instructions:
            raise UserError(_("Food processing production requires HACCP instructions"))

        # Call parent method to maintain all base functionality
        return super().action_confirm()


# 3. ANOTHER INDUSTRY EXAMPLE (in farm_livestock module)
class FarmLivestockProduction(models.Model):
    """
    Livestock-specific model using _inherits pattern
    """
    _name = 'farm.livestock.production'
    _description = 'Livestock Growth Order (ISL Layer)'
    _inherits = {'mrp.production': 'production_id'}  # Direct inheritance from base
    _inherit = ['agri.isl.manufacturing.mixin']  # Abstract functionality

    # Foreign key relationship - CRITICAL for _inherits
    production_id = fields.Many2one(
        'mrp.production',
        string='Base Production Order',
        required=True,
        ondelete='cascade'
    )

    # Livestock specific fields
    initial_total_weight = fields.Float("Initial Total Weight (kg)")
    final_total_weight = fields.Float("Final Total Weight (kg)")
    fcr = fields.Float("Feed Conversion Ratio (FCR)", compute='_compute_fcr')
    avg_daily_gain_recorded = fields.Float("Recorded ADG (kg/day)")

    @api.depends('initial_total_weight', 'final_total_weight')
    def _compute_fcr(self):
        for rec in self:
            gain = rec.final_total_weight - rec.initial_total_weight
            rec.fcr = (rec.production_id.product_qty / gain) if gain > 0 else 0.0

    def write(self, vals):
        # Ensure industry type is set for livestock
        if 'industry_type' not in vals and not self.industry_type:
            vals['industry_type'] = 'livestock'
        return super().write(vals)


# 4. RELATIONSHIP PATTERN COMPARISON

# Pattern A: Direct _inherits (RECOMMENDED)
class RecommendedPattern(models.Model):
    """Recommended: Direct _inherits from base Odoo model"""
    _name = 'recommended.pattern'
    _inherits = {'mrp.production': 'mrp_production_id'}

    mrp_production_id = fields.Many2one(
        'mrp.production',
        required=True,
        ondelete='cascade'
    )
    # Industry-specific fields here


# Pattern B: Indirect _inherit (ALSO VALID but less direct)
class AlternativePattern(models.Model):
    """Alternative: Inherit from centralized ISL model"""
    _name = 'alternative.pattern'
    _inherit = 'agri.isl.mrp.production'  # Extends existing ISL model

    # Additional industry-specific fields here


# 5. DATA FLOW WITH _INHERITS

def create_isl_production_with_inherits():
    """
    Example of how to create ISL records using _inherits pattern
    """
    # Step 1: Create base production record
    base_production = env['mrp.production'].create({
        'name': 'Base Production Order',
        'product_id': env.ref('some_product').id,
        'product_qty': 100,
    })

    # Step 2: Create ISL record that owns the base record via _inherits
    isl_production = env['farm.processing.production'].create({
        'mrp_production_id': base_production.id,  # This creates the _inherits relationship
        'industry_type': 'field_crop',
        'haccp_instructions': 'Follow HACCP guidelines...',
        'target_temp': 75.0,
    })

    # Now isl_production has access to ALL base production fields AND ISL fields
    print(f"Production Name: {isl_production.name}")  # Base field (from mrp.production)
    print(f"Industry Type: {isl_production.industry_type}")  # ISL field
    print(f"HACCP Instructions: {isl_production.haccp_instructions}")  # Industry field

    # When isl_production is deleted, base_production is automatically deleted (cascade)


# 6. SECURITY AND ACCESS CONTROL
"""
The _inherits pattern works well with security:
- Each ISL model has its own security rules
- Permissions apply to the ISL model's table
- Base model access follows standard Odoo security
- Foreign key relationships maintain data integrity
"""


# 7. VIEW INTEGRATION
"""
Views can access both base and ISL fields seamlessly:
<record id="view_form" model="ir.ui.view">
    <field name="model">farm.processing.production</field>
    <field name="arch" type="xml">
        <form>
            <sheet>
                <group>
                    <field name="name"/>  # Base field from mrp.production
                    <field name="product_id"/>  # Base field from mrp.production
                </group>
                <group>
                    <field name="industry_type"/>  # ISL field
                    <field name="haccp_instructions"/>  # Industry field
                </group>
            </sheet>
        </form>
    </field>
</record>
"""

# Summary: The _inherits mechanism provides the strongest relationship between
# ISL models and their base models, ensuring complete ownership and proper
# data integrity while maintaining access to all base functionality.