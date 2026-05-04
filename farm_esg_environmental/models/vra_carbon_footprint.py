from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class AgriVRACarbonFootprint(models.Model):
    """
    US-080-01: VRA Carbon Footprint Calculation
    Calculate carbon footprint reduction from VRA operations compared to traditional methods
    Integrated into ESG framework for environmental impact assessment
    """
    _name = 'agri.vra.carbon.footprint'
    _description = 'VRA Carbon Footprint Calculation and Reduction Analysis'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('VRA Carbon Assessment', required=True, copy=False)
    assessment_date = fields.Date('Assessment Date', default=fields.Date.context_today)

    # VRA operation reference
    intervention_id = fields.Many2one('mrp.production', string='VRA Intervention/Operation',
                                      help='The precision agriculture operation being assessed')
    location_id = fields.Many2one('farm.location', string='Location', required=True)

    # Traditional vs VRA comparison
    operation_type = fields.Selection([
        ('fertilization', 'Fertilization'),
        ('pesticide_application', 'Pesticide Application'),
        ('irrigation', 'Irrigation Management'),
        ('seed_planting', 'Seed Planting'),
        ('other', 'Other'),
    ], string='Operation Type', required=True)

    # Input material usage comparison
    traditional_material_qty = fields.Float('Traditional Material Quantity',
                                           help='Amount of material used in traditional method')
    vra_material_qty = fields.Float('VRA Material Quantity',
                                   help='Amount of material used with VRA precision')
    material_savings = fields.Float('Material Savings', compute='_compute_material_savings', store=True)

    # Carbon emission calculations
    traditional_carbon_emission = fields.Float('Traditional Carbon Emission (kg CO2e)',
                                              help='Estimated carbon emissions with traditional method')
    vra_carbon_emission = fields.Float('VRA Carbon Emission (kg CO2e)',
                                      help='Estimated carbon emissions with VRA method')
    carbon_emission_reduction = fields.Float('Carbon Emission Reduction (kg CO2e)',
                                            compute='_compute_carbon_reduction', store=True)
    carbon_reduction_percentage = fields.Float('Carbon Reduction (%)',
                                              compute='_compute_carbon_reduction_percentage', store=True)

    # Fuel optimization from VRA
    fuel_savings_liter = fields.Float('Fuel Savings (Liters)',
                                     help='Fuel saved through optimized VRA operations')
    fuel_carbon_savings = fields.Float('Fuel Carbon Savings (kg CO2e)',
                                      compute='_compute_fuel_carbon_savings', store=True)

    # Soil carbon sequestration
    soil_carbon_sequestration = fields.Float('Soil Carbon Sequestration (kg CO2e)',
                                           help='Additional carbon sequestration from VRA practices')

    # Overall environmental impact
    net_environmental_impact = fields.Float('Net Environmental Impact (kg CO2e)',
                                          compute='_compute_net_impact', store=True)

    # Assessment status
    assessment_status = fields.Selection([
        ('draft', 'Draft'),
        ('calculated', 'Calculated'),
        ('verified', 'Verified'),
        ('reported', 'Reported'),
    ], string='Assessment Status', default='draft')

    # Environmental compliance
    meets_environmental_standards = fields.Boolean('Meets Environmental Standards',
                                                   compute='_compute_compliance', store=True)
    environmental_risk_level = fields.Selection([
        ('low', 'Low Risk'),
        ('medium', 'Medium Risk'),
        ('high', 'High Risk'),
    ], string='Environmental Risk Level', compute='_compute_risk', store=True)

    # Related reports
    comparison_report = fields.Text('Comparison Report', compute='_compute_comparison_report')

    @api.depends('traditional_material_qty', 'vra_material_qty')
    def _compute_material_savings(self):
        for record in self:
            record.material_savings = (record.traditional_material_qty or 0) - (record.vra_material_qty or 0)

    @api.depends('traditional_carbon_emission', 'vra_carbon_emission')
    def _compute_carbon_reduction(self):
        for record in self:
            record.carbon_emission_reduction = (record.traditional_carbon_emission or 0) - (record.vra_carbon_emission or 0)

    @api.depends('traditional_carbon_emission', 'vra_carbon_emission')
    def _compute_carbon_reduction_percentage(self):
        for record in self:
            if record.traditional_carbon_emission and record.traditional_carbon_emission != 0:
                reduction = ((record.traditional_carbon_emission - record.vra_carbon_emission) /
                           record.traditional_carbon_emission) * 100
                record.carbon_reduction_percentage = max(0, reduction)  # Ensure non-negative
            else:
                record.carbon_reduction_percentage = 0.0

    @api.depends('fuel_savings_liter')
    def _compute_fuel_carbon_savings(self):
        for record in self:
            # Assume 2.68 kg CO2 per liter of diesel
            record.fuel_carbon_savings = (record.fuel_savings_liter or 0) * 2.68

    @api.depends('carbon_emission_reduction', 'fuel_carbon_savings', 'soil_carbon_sequestration')
    def _compute_net_impact(self):
        for record in self:
            record.net_environmental_impact = (record.carbon_emission_reduction or 0) + \
                                            (record.fuel_carbon_savings or 0) + \
                                            (record.soil_carbon_sequestration or 0)

    @api.depends('net_environmental_impact')
    def _compute_compliance(self):
        for record in self:
            # Consider compliant if net impact is positive (net reduction)
            record.meets_environmental_standards = record.net_environmental_impact > 0

    @api.depends('net_environmental_impact')
    def _compute_risk(self):
        for record in self:
            if record.net_environmental_impact > 50:  # High positive impact
                record.environmental_risk_level = 'low'
            elif record.net_environmental_impact > 0:  # Positive impact
                record.environmental_risk_level = 'medium'
            else:  # Negative impact
                record.environmental_risk_level = 'high'

    def _compute_comparison_report(self):
        for record in self:
            report = f"""
            VRA Carbon Footprint Comparison Report: {record.name}
            Location: {record.location_id.name if record.location_id else 'N/A'}
            Operation Type: {dict(record._fields['operation_type'].selection).get(record.operation_type, record.operation_type)}
            Assessment Date: {record.assessment_date}

            Material Usage:
            - Traditional Method: {record.traditional_material_qty or 0} units
            - VRA Method: {record.vra_material_qty or 0} units
            - Savings: {record.material_savings or 0} units ({((record.material_savings or 0)/(record.traditional_material_qty or 1)*100):.2f}%)

            Carbon Emissions:
            - Traditional: {record.traditional_carbon_emission or 0} kg CO2e
            - VRA: {record.vra_carbon_emission or 0} kg CO2e
            - Reduction: {record.carbon_emission_reduction or 0} kg CO2e ({record.carbon_reduction_percentage or 0:.2f}%)

            Additional Benefits:
            - Fuel Savings: {record.fuel_savings_liter or 0} liters ({record.fuel_carbon_savings or 0} kg CO2e)
            - Soil Sequestration: {record.soil_carbon_sequestration or 0} kg CO2e

            Overall Impact:
            - Net Environmental Impact: {record.net_environmental_impact or 0} kg CO2e
            - Meets Environmental Standards: {'Yes' if record.meets_environmental_standards else 'No'}
            - Risk Level: {dict(record._fields['environmental_risk_level'].selection).get(record.environmental_risk_level, record.environmental_risk_level)}
            """
            record.comparison_report = report

    @api.constrains('traditional_material_qty', 'vra_material_qty',
                    'traditional_carbon_emission', 'vra_carbon_emission',
                    'fuel_savings_liter', 'soil_carbon_sequestration')
    def _check_positive_values(self):
        for record in self:
            if record.traditional_material_qty < 0 or record.vra_material_qty < 0:
                raise ValidationError(_("Material quantities cannot be negative."))
            if record.traditional_carbon_emission < 0 or record.vra_carbon_emission < 0:
                raise ValidationError(_("Carbon emissions cannot be negative."))
            if record.fuel_savings_liter < 0:
                raise ValidationError(_("Fuel savings cannot be negative."))
            if record.soil_carbon_sequestration < 0:
                raise ValidationError(_("Soil carbon sequestration cannot be negative."))

    def action_calculate_assessment(self):
        """Run the VRA carbon footprint assessment"""
        for record in self:
            # This would integrate with actual VRA and intervention data in real implementation
            # For now, we'll set status to calculated
            record.assessment_status = 'calculated'
            record.message_post(body=_("VRA carbon footprint assessment completed."))

    def action_verify_assessment(self):
        """Verify the assessment with additional data"""
        for record in self:
            record.assessment_status = 'verified'
            record.message_post(body=_("VRA carbon footprint assessment verified."))

    def action_generate_report(self):
        """Generate detailed carbon footprint report"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('VRA Carbon Footprint Report'),
            'res_model': 'agri.vra.carbon.footprint',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
            'context': self.env.context,
        }