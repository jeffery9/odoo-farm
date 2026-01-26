from odoo import models, fields, api
from odoo.exceptions import ValidationError

class CarbonFootprintCalculation(models.Model):
    """
    US-30-09: Carbon Footprint Calculation
    Carbon footprint calculation model for agricultural products and operations
    """
    _name = 'farm.sustainability.carbon.footprint.calculation'
    _description = 'Carbon Footprint Calculation'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Calculation Name', required=True)
    calculation_date = fields.Date('Calculation Date', default=fields.Date.context_today)
    calculation_type = fields.Selection([
        ('product', 'Product Carbon Footprint'),
        ('process', 'Process Carbon Footprint'),
        ('operation', 'Operational Carbon Footprint'),
        ('farm', 'Farm-level Carbon Footprint')
    ], string='Calculation Type', required=True)
    calculation_method = fields.Selection([
        ('cradle_to_gate', 'Cradle to Gate'),
        ('cradle_to_grave', 'Cradle to Grave'),
        ('gate_to_gate', 'Gate to Gate')
    ], string='Calculation Method', default='cradle_to_gate')

    # Product/operation reference
    product_id = fields.Many2one('product.product', 'Product/Operation')
    lot_id = fields.Many2one('stock.lot', 'Batch/Lot')
    campaign_id = fields.Many2one('farm.agricultural.campaign', 'Agricultural Campaign')

    # Carbon footprint components
    direct_emissions_co2e = fields.Float('Direct Emissions (kg CO2e)', help='Direct emissions from farming operations')
    indirect_energy_emissions_co2e = fields.Float('Indirect Energy Emissions (kg CO2e)', help='Emissions from energy consumption')
    supply_chain_emissions_co2e = fields.Float('Supply Chain Emissions (kg CO2e)', help='Emissions from inputs and materials')
    total_carbon_footprint = fields.Float('Total Carbon Footprint (kg CO2e)', compute='_compute_total_footprint', store=True)

    # Input data
    input_materials_footprint = fields.Float('Input Materials Footprint (kg CO2e)', help='Carbon footprint of inputs used')
    energy_consumption_kwh = fields.Float('Energy Consumption (kWh)', help='Total energy consumed')
    fuel_consumption_liters = fields.Float('Fuel Consumption (L)', help='Fuel consumed in operations')
    water_consumption_m3 = fields.Float('Water Consumption (m3)', help='Water consumed in operations')
    land_use_area = fields.Float('Land Use Area (m2)', help='Area of land used in production')

    # Output and efficiency metrics
    output_quantity = fields.Float('Output Quantity', help='Quantity of product produced')
    product_yield_kg = fields.Float('Product Yield (kg)', help='Total yield in kg')
    footprint_per_unit = fields.Float('Carbon Footprint per Unit (kg CO2e/unit)', compute='_compute_footprint_per_unit', store=True)
    footprint_per_kg_yield = fields.Float('Carbon Footprint per kg Yield (kg CO2e/kg)', compute='_compute_footprint_per_kg_yield', store=True)

    # Calculation details
    calculation_notes = fields.Text('Calculation Notes')
    algorithm_version = fields.Char('Algorithm Version', default='1.0')
    verification_status = fields.Selection([
        ('not_verified', 'Not Verified'),
        ('pending', 'Verification Pending'),
        ('verified', 'Verified'),
        ('certified', 'Certified')
    ], string='Verification Status', default='not_verified')

    # Related industry model
    industry_model_id = fields.Many2one('farm.sustainability.industry.carbon.model', 'Industry Carbon Model',
                                        help='Industry-specific carbon model used for calculation')

    # Additional environmental impacts
    water_footprint_m3 = fields.Float('Water Footprint (m3)', help='Water footprint in cubic meters')
    land_footprint_m2 = fields.Float('Land Footprint (m2)', help='Land footprint in square meters')

    @api.depends('direct_emissions_co2e', 'indirect_energy_emissions_co2e', 'supply_chain_emissions_co2e')
    def _compute_total_footprint(self):
        """Compute total carbon footprint from all components"""
        for record in self:
            record.total_carbon_footprint = (record.direct_emissions_co2e or 0) + \
                                          (record.indirect_energy_emissions_co2e or 0) + \
                                          (record.supply_chain_emissions_co2e or 0)

    @api.depends('total_carbon_footprint', 'output_quantity')
    def _compute_footprint_per_unit(self):
        """Compute carbon footprint per unit of output"""
        for record in self:
            if record.output_quantity and record.output_quantity > 0:
                record.footprint_per_unit = record.total_carbon_footprint / record.output_quantity
            else:
                record.footprint_per_unit = 0.0

    @api.depends('total_carbon_footprint', 'product_yield_kg')
    def _compute_footprint_per_kg_yield(self):
        """Compute carbon footprint per kg of product yield"""
        for record in self:
            if record.product_yield_kg and record.product_yield_kg > 0:
                record.footprint_per_kg_yield = record.total_carbon_footprint / record.product_yield_kg
            else:
                record.footprint_per_kg_yield = 0.0

    @api.constrains('direct_emissions_co2e', 'indirect_energy_emissions_co2e',
                    'supply_chain_emissions_co2e', 'output_quantity', 'product_yield_kg')
    def _check_positive_values(self):
        """Ensure all carbon footprint values are non-negative"""
        for record in self:
            if record.direct_emissions_co2e < 0:
                raise ValidationError("Direct emissions cannot be negative.")
            if record.indirect_energy_emissions_co2e < 0:
                raise ValidationError("Indirect energy emissions cannot be negative.")
            if record.supply_chain_emissions_co2e < 0:
                raise ValidationError("Supply chain emissions cannot be negative.")
            if record.output_quantity < 0:
                raise ValidationError("Output quantity cannot be negative.")
            if record.product_yield_kg < 0:
                raise ValidationError("Product yield cannot be negative.")

    @api.onchange('product_id')
    def _onchange_product_id(self):
        """Update based on product selection"""
        if self.product_id:
            if not self.name:
                self.name = f"Carbon Footprint - {self.product_id.name}"
            if self.product_id.carbon_emission_factor:
                # Use product's emission factor as a starting point
                self.input_materials_footprint = self.product_id.carbon_emission_factor

    def action_calculate_carbon_footprint(self):
        """Calculate carbon footprint based on available data"""
        for record in self:
            # Calculate direct emissions based on fuel consumption
            # Using typical emission factor of 2.68 kg CO2e/L for diesel
            direct_emissions = (record.fuel_consumption_liters or 0) * 2.68

            # Calculate indirect energy emissions (2.83 kg CO2e/kWh for coal-based electricity as example)
            indirect_energy_emissions = (record.energy_consumption_kwh or 0) * 0.5  # assuming cleaner energy mix

            # Calculate supply chain emissions from inputs
            supply_chain_emissions = record.input_materials_footprint or 0

            # Update the record with calculated values
            record.write({
                'direct_emissions_co2e': direct_emissions,
                'indirect_energy_emissions_co2e': indirect_energy_emissions,
                'supply_chain_emissions_co2e': supply_chain_emissions
            })

    def action_verify_calculation(self):
        """Mark the calculation as verified"""
        for record in self:
            record.verification_status = 'verified'

    def action_reset_calculation(self):
        """Reset calculated values to allow recalculation"""
        for record in self:
            record.write({
                'direct_emissions_co2e': 0,
                'indirect_energy_emissions_co2e': 0,
                'supply_chain_emissions_co2e': 0,
                'total_carbon_footprint': 0,
                'footprint_per_unit': 0,
                'footprint_per_kg_yield': 0
            })