from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class AgriBiogasProduction(models.Model):
    """
    US-057-04: 沼气/生物质能转化量化
    Model for biogas and bioenergy production from waste
    """
    _name = 'agri.biogas.production'
    _description = 'Agricultural Biogas Production'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Biogas Production Batch', required=True, copy=False)
    production_date = fields.Date('Production Date', required=True, default=fields.Date.context_today)

    # Input materials (waste)
    input_waste_type = fields.Selection([
        ('animal_manure', 'Animal Manure'),
        ('crop_residue', 'Crop Residue'),
        ('food_waste', 'Food Waste'),
        ('sewage_sludge', 'Sewage Sludge'),
        ('green_waste', 'Green Waste'),
        ('other', 'Other'),
    ], string='Input Waste Type', required=True)

    input_quantity = fields.Float('Input Quantity', required=True)
    input_uom = fields.Many2one('uom.uom', string='Input UOM', required=True)

    # Biogas production
    biogas_volume = fields.Float('Biogas Volume (m3)', help='Volume of biogas produced')
    methane_content = fields.Float('Methane Content (%)', help='Percentage of methane in biogas')

    # Energy calculation
    energy_output_kwh = fields.Float('Energy Output (kWh)', compute='_compute_energy_output', store=True)
    coal_equivalent_ton = fields.Float('Coal Equivalent (ton)', compute='_compute_coal_equivalent', store=True,
                                       help='Standard coal equivalent replacement value')

    # Process parameters
    digester_temperature = fields.Float('Digester Temperature (°C)')
    retention_time_days = fields.Integer('Retention Time (days)')
    ph_level = fields.Float('pH Level')

    # Environmental benefits
    co2_reduction_ton = fields.Float('CO2 Reduction Equivalent (ton)', compute='_compute_co2_reduction', store=True)

    # Equipment and location
    digester_id = fields.Many2one('maintenance.equipment', string='Biogas Digester')
    production_location_id = fields.Many2one('farm.location', string='Production Location')

    # Integration with carbon footprint (Epic 30)
    related_carbon_impact_id = fields.Many2one('agri.carbon.ledger', string='Related Carbon Impact')

    # Related to circular economy
    related_circular_flow_id = fields.Many2one('agri.sustainability.circular.flow',
                                               string='Related Circular Flow')

    # Status
    status = fields.Selection([
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ], string='Status', default='planned')

    @api.depends('biogas_volume', 'methane_content')
    def _compute_energy_output(self):
        """Calculate energy output in kWh"""
        for record in self:
            if record.biogas_volume and record.methane_content:
                # 1 m3 methane ≈ 10 kWh energy
                energy_kwh = record.biogas_volume * (record.methane_content / 100) * 10
                record.energy_output_kwh = energy_kwh
            else:
                record.energy_output_kwh = 0.0

    @api.depends('energy_output_kwh')
    def _compute_coal_equivalent(self):
        """Calculate standard coal equivalent (1 kgce = 8.14 kWh)"""
        for record in self:
            if record.energy_output_kwh:
                # 1 ton coal equivalent = 8140 kWh
                coal_equivalent_ton = record.energy_output_kwh / 8140.0
                record.coal_equivalent_ton = coal_equivalent_ton
            else:
                record.coal_equivalent_ton = 0.0

    @api.depends('coal_equivalent_ton')
    def _compute_co2_reduction(self):
        """Calculate CO2 reduction based on coal displacement (1 ton coal ≈ 2.6 tons CO2)"""
        for record in self:
            if record.coal_equivalent_ton:
                # Standard approximation: coal combustion produces ~2.6 tons CO2 per ton coal
                co2_reduction_ton = record.coal_equivalent_ton * 2.6
                record.co2_reduction_ton = co2_reduction_ton
            else:
                record.co2_reduction_ton = 0.0

    @api.constrains('input_quantity', 'biogas_volume', 'methane_content')
    def _check_positive_values(self):
        for record in self:
            if record.input_quantity <= 0:
                raise ValidationError(_("Input quantity must be positive."))
            if record.biogas_volume < 0:
                raise ValidationError(_("Biogas volume cannot be negative."))
            if record.methane_content < 0 or record.methane_content > 100:
                raise ValidationError(_("Methane content must be between 0 and 100%."))

    def action_start_production(self):
        """Start biogas production process"""
        for record in self:
            record.status = 'in_progress'
            record.message_post(body=_("Biogas production started"))

    def action_complete_production(self):
        """Complete biogas production process"""
        for record in self:
            record.status = 'completed'
            record.message_post(body=_("Biogas production completed. Energy output: %.2f kWh") % record.energy_output_kwh)

    def action_generate_energy_report(self):
        """Generate energy production report"""
        energy_report = f"""
        Biogas Production Report: {self.name}
        Production Date: {self.production_date}

        Input Materials:
        - Type: {dict(self._fields['input_waste_type'].selection).get(self.input_waste_type, self.input_waste_type)}
        - Quantity: {self.input_quantity} {self.input_uom.name}

        Energy Output:
        - Biogas Volume: {self.biogas_volume} m³
        - Methane Content: {self.methane_content}%
        - Energy Output: {self.energy_output_kwh} kWh
        - Coal Equivalent: {self.coal_equivalent_ton} tons
        - CO2 Reduction: {self.co2_reduction_ton} tons

        Process Parameters:
        - Digester Temp: {self.digester_temperature}°C
        - Retention Time: {self.retention_time_days} days
        - pH Level: {self.ph_level}
        """
        return {
            'type': 'ir.actions.act_window',
            'name': _('Biogas Production Report'),
            'res_model': 'agri.biogas.production',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
            'context': {'default_report_content': energy_report}
        }


class AgriEnergyRecoveryIntegration(models.Model):
    """
    Integration model to push data to carbon footprint ledger (Epic 30)
    """
    _name = 'agri.energy.recovery.integration'
    _description = 'Energy Recovery to Carbon Footprint Integration'

    biogas_production_id = fields.Many2one('agri.biogas.production', string='Biogas Production', required=True)
    carbon_ledger_id = fields.Many2one('agri.carbon.ledger', string='Carbon Ledger Entry')
    integration_date = fields.Date('Integration Date', default=fields.Date.context_today)
    co2_reduction_ton = fields.Float('CO2 Reduction (ton)', readonly=True)
    energy_output_kwh = fields.Float('Energy Output (kWh)', readonly=True)
    coal_equivalent_ton = fields.Float('Coal Equivalent (ton)', readonly=True)
    integration_status = fields.Selection([
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ], string='Integration Status', default='pending')

    def action_push_to_carbon_ledger(self):
        """Push biogas production data to carbon footprint ledger (Epic 30 integration)"""
        for record in self:
            if not record.biogas_production_id:
                continue

            # Create or update carbon ledger entry
            carbon_data = {
                'name': f'Biogas CO2 Reduction - {record.biogas_production_id.name}',
                'date': record.integration_date or fields.Date.context_today(record),
                'location_id': record.biogas_production_id.production_location_id.id,
                'factor_id': self._get_carbon_factor_id(),  # Would need to find appropriate factor
                'quantity': record.biogas_production_id.coal_equivalent_ton,
                'impact_type': 'sequestration',  # Since this is a reduction
                'total_co2e': -record.biogas_production_id.co2_reduction_ton,  # Negative since it's a reduction
            }

            try:
                carbon_ledger = self.env['agri.carbon.ledger'].create(carbon_data)
                record.carbon_ledger_id = carbon_ledger.id
                record.integration_status = 'completed'

                record.biogas_production_id.message_post(
                    body=_("Carbon impact recorded: %s tons CO2 reduction") %
                    record.biogas_production_id.co2_reduction_ton
                )
            except Exception as e:
                record.integration_status = 'failed'
                record.biogas_production_id.message_post(
                    body=_("Failed to record carbon impact: %s") % str(e)
                )

    def _get_carbon_factor_id(self):
        """Get or create appropriate carbon factor for biogas CO2 reduction"""
        factor = self.env['agri.carbon.factor'].search([
            ('name', 'ilike', 'biogas'),
            ('category', '=', 'waste')
        ], limit=1)

        if not factor:
            # Create a default factor if not existing
            factor = self.env['agri.carbon.factor'].create({
                'name': 'Biogas CO2 Reduction Factor',
                'category': 'waste',
                'emission_factor': -2.6,  # Negative since it's a reduction
                'uom_id': self.env.ref('uom.product_uom_ton').id,
                'source': 'Calculated from standard coal equivalent'
            })

        return factor.id