from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class FarmMedicinalPlantsOperation(models.Model):
    """
    Medicinal plants operation model for managing cultivation, processing, and quality control of medicinal plants
    """
    _name = 'farm.medicinal.plants.operation'
    _description = 'Farm Medicinal Plants Operation'
    _inherit = 'project.task'  # Inherit from project.task to leverage existing task functionality

    # Plant and Variety Information
    plant_species = fields.Char('Plant Species', help='Scientific name of medicinal plant')
    variety = fields.Char('Variety')
    daodi_requirements = fields.Char('Daodi Requirements', help='Traditional authentic origin requirements')
    cultivation_method = fields.Selection([
        ('organic', 'Organic'),
        ('natural', 'Natural'),
        ('conventional', 'Conventional'),
        ('gmp', 'GMP Certified'),
    ], string='Cultivation Method')

    # Environmental Monitoring for Medicinal Quality
    environmental_factors = fields.Text('Environmental Factors Affecting Quality')
    light_intensity = fields.Float('Light Intensity (lux)')
    soil_ph = fields.Float('Soil pH')
    cultivation_altitude = fields.Float('Cultivation Altitude (m)')
    soil_type = fields.Char('Soil Type')

    # Active Ingredient Management
    active_ingredients = fields.Text('Active Ingredients Profile')
    target_compound = fields.Char('Target Active Compound')
    current_compound_level = fields.Float('Current Active Compound Level (%)')
    target_compound_level = fields.Float('Target Active Compound Level (%)')
    compound_analysis_date = fields.Date('Last Compound Analysis Date')
    compound_analysis_status = fields.Selection([
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('below_standard', 'Below Standard'),
        ('above_standard', 'Above Standard'),
        ('optimal', 'Optimal'),
    ], string='Compound Analysis Status', compute='_compute_compound_status', store=True)

    # GMP Compliance
    gmp_compliant = fields.Boolean('GMP Compliant', default=False)
    gmp_certification_number = fields.Char('GMP Certification Number')
    gmp_inspection_date = fields.Date('Last GMP Inspection Date')
    gmp_status = fields.Selection([
        ('compliant', 'Compliant'),
        ('non_compliant', 'Non-Compliant'),
        ('pending_review', 'Pending Review'),
    ], string='GMP Status')

    # Harvest Management for Medicinal Plants
    optimal_harvest_window = fields.Date('Optimal Harvest Window')
    harvest_timing_factor = fields.Char('Harvest Timing Factor',
                                       help='Based on active compound peak levels')
    harvest_method = fields.Selection([
        ('selective', 'Selective Harvesting'),
        ('whole_plant', 'Whole Plant Harvesting'),
        ('part_specific', 'Part-Specific Harvesting'),
    ], string='Harvest Method')

    # Quality Control
    quality_grade = fields.Selection([
        ('premium', 'Premium'),
        ('standard', 'Standard'),
        ('substandard', 'Substandard'),
    ], string='Quality Grade', compute='_compute_quality_grade', store=True)
    quality_notes = fields.Text('Quality Notes')
    quality_certifications = fields.Char('Quality Certifications')

    # Processing Management
    processing_method = fields.Selection([
        ('drying', 'Drying'),
        ('extraction', 'Extraction'),
        ('powdering', 'Powdering'),
        ('cutting', 'Cutting'),
        ('other', 'Other'),
    ], string='Processing Method')
    processing_date = fields.Date('Processing Date')
    processed_quantity = fields.Float('Processed Quantity')

    # Medicinal Plant specific stages
    medicinal_plant_stage = fields.Selection([
        ('variety_selection', 'Variety Selection'),
        ('land_preparation', 'Land Preparation'),
        ('planting', 'Planting'),
        ('growth_monitoring', 'Growth Monitoring'),
        ('environmental_control', 'Environmental Control'),
        ('compound_monitoring', 'Active Compound Monitoring'),
        ('harvest_preparation', 'Harvest Preparation'),
        ('harvesting', 'Harvesting'),
        ('processing', 'Processing'),
        ('quality_control', 'Quality Control'),
        ('packaging', 'Packaging'),
        ('storage', 'Storage'),
    ], string='Medicinal Plant Stage', default='variety_selection')

    @api.depends('current_compound_level', 'target_compound_level')
    def _compute_compound_status(self):
        """Compute active compound analysis status"""
        for record in self:
            if not record.current_compound_level or not record.target_compound_level:
                record.compound_analysis_status = 'pending'
            elif record.current_compound_level < record.target_compound_level * 0.8:
                record.compound_analysis_status = 'below_standard'
            elif record.current_compound_level > record.target_compound_level * 1.2:
                record.compound_analysis_status = 'above_standard'
            elif abs(record.current_compound_level - record.target_compound_level) <= record.target_compound_level * 0.1:
                record.compound_analysis_status = 'optimal'
            else:
                record.compound_analysis_status = 'completed'

    @api.depends('compound_analysis_status', 'gmp_compliant')
    def _compute_quality_grade(self):
        """Compute quality grade based on compound status and compliance"""
        for record in self:
            if record.compound_analysis_status == 'below_standard' or not record.gmp_compliant:
                record.quality_grade = 'substandard'
            elif record.compound_analysis_status == 'optimal' and record.gmp_compliant:
                record.quality_grade = 'premium'
            else:
                record.quality_grade = 'standard'

    def action_update_compound_level(self, level, compound_name=None):
        """Update active compound level"""
        self.ensure_one()
        self.write({
            'current_compound_level': level,
            'compound_analysis_date': fields.Date.today(),
            'compound_analysis_status': 'in_progress'  # Reset status for new analysis
        })

        body = _("ACTIVE COMPOUND LEVEL UPDATE: %s%% %s. Analysis date: %s") % (
            level, compound_name or self.target_compound or "active compound", fields.Date.today())
        self.message_post(body=body)
        return True

    def action_schedule_harvest(self, harvest_date, method=None):
        """Schedule medicinal plant harvest based on compound levels"""
        self.ensure_one()
        self.write({
            'optimal_harvest_window': harvest_date,
            'harvest_method': method or self.harvest_method
        })

        body = _("HARVEST SCHEDULED: Optimal harvest date %s using %s method") % (
            harvest_date, method or self.harvest_method or "default method")
        self.message_post(body=body)
        return True

    def action_perform_quality_check(self, grade, notes=None):
        """Perform quality check and update grade"""
        self.ensure_one()
        self.write({
            'quality_grade': grade,
            'quality_notes': notes
        })

        body = _("QUALITY CHECK PERFORMED: Grade %s. %s") % (grade, notes or "")
        self.message_post(body=body)
        return True

    def action_update_gmp_status(self, status, inspection_date=None):
        """Update GMP compliance status"""
        self.ensure_one()
        updates = {'gmp_status': status}
        if inspection_date:
            updates['gmp_inspection_date'] = inspection_date
        self.write(updates)

        body = _("GMP STATUS UPDATE: %s. Inspection date: %s") % (
            status, inspection_date or "Not specified")
        self.message_post(body=body)
        return True


class FarmMedicinalPlantsAnalysis(models.Model):
    """
    Medicinal plants analysis model for tracking active ingredient tests
    """
    _name = 'farm.medicinal.plants.analysis'
    _description = 'Farm Medicinal Plants Analysis'
    _order = 'analysis_date desc'

    operation_id = fields.Many2one('farm.medicinal.plants.operation', string='Operation', required=True)
    analysis_date = fields.Date('Analysis Date', default=fields.Date.today, required=True)
    analyst = fields.Char('Analyst')
    target_compound = fields.Char('Target Compound')
    compound_level = fields.Float('Compound Level (%)')
    testing_method = fields.Char('Testing Method')
    analysis_notes = fields.Text('Analysis Notes')
    analysis_status = fields.Selection([
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ], string='Analysis Status', default='pending')

    @api.model
    def create(self, vals):
        """Override create to update operation with current values"""
        record = super().create(vals)
        if record.operation_id and record.compound_level:
            # Update the current values in the operation
            record.operation_id.write({
                'current_compound_level': record.compound_level,
                'compound_analysis_date': record.analysis_date,
                'target_compound': record.target_compound or record.operation_id.target_compound,
            })
        return record