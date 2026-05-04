from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class AgriVRAWaterProtectionZone(models.Model):
    """
    US-080-02: VRA Water Body Protection Strategies
    Water body protection VRA strategies with buffer zones and contamination prevention
    """
    _name = 'agri.vra.water.protection.zone'
    _description = 'VRA Water Body Protection and Buffer Zone Management'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Water Protection Zone', required=True, copy=False)
    zone_code = fields.Char('Zone Code', required=True, copy=False, default=lambda self: self._generate_zone_code())

    # Location and water body information
    water_body_name = fields.Char('Water Body Name', required=True)
    location_id = fields.Many2one('farm.location', string='Farm Location', required=True)
    gps_coordinates = fields.Char('GPS Coordinates', help='Center point coordinates of the water body')

    # Buffer zone specifications
    buffer_zone_type = fields.Selection([
        ('chemical', 'Chemical Buffer Zone'),
        ('mechanical', 'Mechanical Buffer Zone'),
        ('biological', 'Biological Buffer Zone'),
        ('combined', 'Combined Buffer Zone'),
    ], string='Buffer Zone Type', required=True)

    buffer_distance_meters = fields.Float('Buffer Distance (meters)', required=True,
                                         help='Minimum distance from water body edge')

    # VRA application restrictions
    prohibited_materials = fields.Many2many('product.product', string='Prohibited Materials',
                                           help='Materials that cannot be applied in this zone')
    restricted_operations = fields.Selection([
        ('none', 'No Restrictions'),
        ('limited', 'Limited Application'),
        ('prohibited', 'Prohibited'),
    ], string='VRA Operations Restriction', default='limited')

    # Seasonal restrictions
    seasonal_restrictions = fields.Boolean('Seasonal Restrictions',
                                          help='Are there seasonal limitations on VRA applications?')
    restricted_season_start = fields.Selection([
        ('01', 'January'), ('02', 'February'), ('03', 'March'),
        ('04', 'April'), ('05', 'May'), ('06', 'June'),
        ('07', 'July'), ('08', 'August'), ('09', 'September'),
        ('10', 'October'), ('11', 'November'), ('12', 'December'),
    ], string='Restricted Season Start')
    restricted_season_end = fields.Selection([
        ('01', 'January'), ('02', 'February'), ('03', 'March'),
        ('04', 'April'), ('05', 'May'), ('06', 'June'),
        ('07', 'July'), ('08', 'August'), ('09', 'September'),
        ('10', 'October'), ('11', 'November'), ('12', 'December'),
    ], string='Restricted Season End')

    # Monitoring and compliance
    monitoring_frequency = fields.Selection([
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annually', 'Annually'),
    ], string='Monitoring Frequency', default='monthly')

    last_inspection_date = fields.Date('Last Inspection Date')
    next_inspection_date = fields.Date('Next Inspection Date')

    # Compliance status
    compliance_status = fields.Selection([
        ('compliant', 'Compliant'),
        ('warning', 'Warning'),
        ('violation', 'Violation'),
        ('not_applicable', 'Not Applicable'),
    ], string='Compliance Status', default='compliant')

    # Historical compliance records
    compliance_history_ids = fields.One2many('agri.vra.water.compliance.history',
                                           'protection_zone_id', string='Compliance History')

    # VRA prescription integration
    active_prescription_ids = fields.Many2many('agri.intervention.vra.prescription', relation='agri_water_protection_rx_rel',
                                             string='Active VRA Prescriptions')

    # Environmental risk assessment
    environmental_risk_level = fields.Selection([
        ('low', 'Low Risk'),
        ('medium', 'Medium Risk'),
        ('high', 'High Risk'),
    ], string='Environmental Risk Level', compute='_compute_risk_level', store=True, precompute=True)

    # Zone effectiveness metrics
    zone_effectiveness_score = fields.Float('Zone Effectiveness Score (0-100)',
                                          compute='_compute_effectiveness_score', store=True, precompute=True)

    # Status and metadata
    active = fields.Boolean('Active', default=True)
    notes = fields.Text('Notes and Observations')

    @api.model
    def _generate_zone_code(self):
        """Generate a unique zone code"""
        return self.env['ir.sequence'].next_by_code('agri.vra.water.protection.zone') or 'WZ-NEW'

    @api.depends('compliance_status')
    def _compute_risk_level(self):
        """Compute environmental risk level based on compliance status"""
        for record in self:
            if record.compliance_status == 'violation':
                record.environmental_risk_level = 'high'
            elif record.compliance_status == 'warning':
                record.environmental_risk_level = 'medium'
            else:
                record.environmental_risk_level = 'low'

    def _compute_effectiveness_score(self):
        """Compute zone effectiveness based on compliance history and buffer specifications"""
        for record in self:
            base_score = 100.0

            # Adjust based on compliance status
            if record.compliance_status == 'violation':
                base_score -= 50
            elif record.compliance_status == 'warning':
                base_score -= 20

            # Adjust based on buffer distance (minimum recommended is 10m for chemicals)
            if record.buffer_zone_type == 'chemical':
                if record.buffer_distance_meters < 10:
                    base_score -= 30
                elif record.buffer_distance_meters < 20:
                    base_score -= 10

            # Adjust based on seasonal compliance
            if record.seasonal_restrictions and not record.restricted_season_start:
                base_score -= 15

            record.zone_effectiveness_score = max(0, min(100, base_score))

    @api.constrains('buffer_distance_meters', 'restricted_season_start', 'restricted_season_end')
    def _check_constraints(self):
        for record in self:
            if record.buffer_distance_meters <= 0:
                raise ValidationError(_("Buffer distance must be greater than zero."))

            # Check that seasonal restrictions make sense
            if (record.seasonal_restrictions and
                record.restricted_season_start and
                record.restricted_season_end and
                record.restricted_season_start > record.restricted_season_end):
                raise ValidationError(_("Start season cannot be after end season."))

    def action_schedule_inspection(self):
        """Schedule the next inspection based on frequency"""
        for record in self:
            # This would integrate with the calendar/scheduling system in real implementation
            record.next_inspection_date = fields.Date.add(
                fields.Date.context_today(record),
                months={'daily': 0, 'weekly': 0, 'monthly': 1, 'quarterly': 3, 'annually': 12}
                [record.monitoring_frequency]
            )
            record.message_post(body=_("Inspection scheduled for %s") % record.next_inspection_date)

    def action_record_compliance_check(self):
        """Record a compliance check event"""
        for record in self:
            self.env['agri.vra.water.compliance.history'].create({
                'protection_zone_id': record.id,
                'check_date': fields.Date.context_today(record),
                'compliance_status': record.compliance_status,
                'notes': f'Automated compliance check for zone {record.name}'
            })
            record.last_inspection_date = fields.Date.context_today(record)

    def action_update_compliance_status(self):
        """Update compliance status based on current conditions"""
        for record in self:
            # In a real implementation, this would check actual conditions
            # For now, just recompute based on zone characteristics
            record._compute_risk_level()

    def action_generate_water_protection_report(self):
        """Generate detailed water protection report"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('VRA Water Protection Report'),
            'res_model': 'agri.vra.water.protection.zone',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
            'context': self.env.context,
        }


class AgriVRAWaterComplianceHistory(models.Model):
    """
    Historical records for water protection zone compliance
    """
    _name = 'agri.vra.water.compliance.history'
    _description = 'VRA Water Protection Zone Compliance History'
    _order = 'check_date desc'

    protection_zone_id = fields.Many2one('agri.vra.water.protection.zone',
                                       string='Protection Zone', required=True)
    check_date = fields.Date('Check Date', required=True,
                            default=fields.Date.context_today)
    compliance_status = fields.Selection([
        ('compliant', 'Compliant'),
        ('warning', 'Warning'),
        ('violation', 'Violation'),
        ('not_applicable', 'Not Applicable'),
    ], string='Compliance Status', required=True)

    inspector_id = fields.Many2one('res.users', string='Inspector')
    notes = fields.Text('Notes')
    evidence_photos = fields.Binary('Evidence Photos', attachment=True)
    evidence_photo_name = fields.Char('Photo Name')

    # VRA operations during inspection period
    vras_performed = fields.Integer('VRA Operations Performed')
    materials_applied = fields.Char('Materials Applied During Period')
    weather_conditions = fields.Char('Weather Conditions')

    # Corrective actions if needed
    corrective_actions_required = fields.Boolean('Corrective Actions Required')
    corrective_actions = fields.Text('Corrective Actions Taken')
    follow_up_required = fields.Boolean('Follow-up Required')
    follow_up_date = fields.Date('Follow-up Date')