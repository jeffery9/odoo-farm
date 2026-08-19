from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)


class AgriESGRedLineConfig(models.Model):
    """
    Configuration for ESG red lines (deforestation, water extraction, etc.)
    US-66-05: Supply Chain ESG Red Line Monitoring and Warning
    """
    _name = 'agri.esg.red.line.config'
    _description = 'Agri ESG Red Line Configuration'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Red Line Name', required=True)
    red_line_type = fields.Selection([
        ('deforestation', 'Deforestation Risk'),
        ('water_extraction', 'Water Extraction'),
        ('soil_degradation', 'Soil Degradation'),
        ('protected_area', 'Protected Area Violation'),
        ('carbon_emission', 'Carbon Emission Excess'),
        ('chemical_runoff', 'Chemical Runoff Risk'),
        ('biodiversity_loss', 'Biodiversity Loss'),
    ], string='Red Line Type', required=True)

    # For geofencing-based red lines
    coordinates = fields.Text("Boundary Coordinates",
                             help="GPS coordinates in 'lon,lat;lon,lat' format for sensitive areas")
    buffer_distance_km = fields.Float("Buffer Distance (km)", default=1.0,
                                     help="Buffer zone around sensitive areas")

    # For threshold-based red lines
    threshold_value = fields.Float("Threshold Value", help="Critical threshold that triggers red line violation")
    threshold_unit = fields.Char("Threshold Unit", help="Unit of measurement for the threshold value")
    threshold_description = fields.Text("Threshold Description")

    # Compliance monitoring
    active_monitoring = fields.Boolean("Active Monitoring", default=True)
    monitoring_frequency = fields.Selection([
        ('real_time', 'Real-time'),
        ('hourly', 'Hourly'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
    ], string='Monitoring Frequency', default='daily')

    description = fields.Text("Description")
    remediation_plan = fields.Text("Remediation Plan", help="Steps to take when red line is breached")

    @api.constrains('coordinates')
    def _check_coordinates_format(self):
        """Validate coordinates format"""
        for record in self:
            if record.coordinates:
                try:
                    # Validate format: lon,lat;lon,lat;...
                    points = [tuple(map(float, p.split(','))) for p in record.coordinates.split(';') if ',' in p]
                    for point in points:
                        if len(point) != 2:
                            raise ValidationError("Invalid coordinate format. Use 'lon,lat;lon,lat' format.")
                        lon, lat = point
                        if not (-180 <= lon <= 180) or not (-90 <= lat <= 90):
                            raise ValidationError(f"Invalid coordinate values: {lon}, {lat}. Must be within valid ranges.")
                except (ValueError, IndexError):
                    raise ValidationError("Invalid coordinate format. Use 'lon,lat;lon,lat' format with numeric values.")


class AgriESGRedLineMonitoring(models.Model):
    """
    Core model for tracking ESG red line compliance checks
    US-66-05: Supply Chain ESG Red Line Monitoring and Warning
    """
    _name = 'agri.esg.red.line.monitoring'
    _description = 'Agri ESG Red Line Monitoring'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'detection_date desc'

    name = fields.Char('Monitoring Record', required=True, copy=False)
    red_line_config_id = fields.Many2one('agri.esg.red.line.config', string='Red Line Configuration', required=True)

    batch_lot_id = fields.Many2one('stock.lot', string='Batch/Lot',
                                  help='The product batch being monitored for ESG compliance')
    location_id = fields.Many2one('farm.location', string='Location',
                                 help='Location where the potential red line violation occurred')

    detection_date = fields.Datetime('Detection Date', default=fields.Datetime.now)
    compliance_status = fields.Selection([
        ('compliant', 'Compliant'),
        ('warning', 'Warning'),
        ('violation', 'Violation'),
        ('critical', 'Critical Violation'),
        ('resolved', 'Resolved'),
    ], string='Compliance Status', default='compliant', tracking=True)

    current_value = fields.Float('Current Value', help='Current measurement that triggered the status')
    threshold_value = fields.Float('Threshold Value', related='red_line_config_id.threshold_value', readonly=True)

    # ESG-specific fields
    carbon_footprint_kg = fields.Float('Carbon Footprint (kg CO2e)', help='Carbon footprint of the batch')
    water_usage_m3 = fields.Float('Water Usage (m3)', help='Water consumed in production')
    land_use_area = fields.Float('Land Use Area (m2)', help='Area of land used')

    # Geofencing-specific fields
    is_in_protected_area = fields.Boolean('In Protected Area', help='Whether location is in a protected area')
    distance_to_boundary_km = fields.Float('Distance to Boundary (km)', help='Distance from sensitive area boundary')

    # Detection details
    detection_method = fields.Selection([
        ('geofence', 'Geofencing Detection'),
        ('threshold_monitoring', 'Threshold Monitoring'),
        ('manual_audit', 'Manual Audit'),
        ('iot_sensor', 'IoT Sensor'),
        ('telemetry', 'Telemetry Data'),
    ], string='Detection Method')

    detection_details = fields.Text('Detection Details', help='Specific details about the compliance check')
    automated_check = fields.Boolean('Automated Check', default=True, help='Whether this was an automated check')

    # Response and resolution
    alert_issued = fields.Boolean('Alert Issued', default=False)
    corrective_actions = fields.Text('Corrective Actions Required')
    remediation_date = fields.Datetime('Remediation Date')
    resolution_notes = fields.Text('Resolution Notes')

    @api.model
    def create(self, vals):
        """Override create to set default name and trigger compliance check"""
        if 'name' not in vals or not vals['name']:
            vals['name'] = self.env['ir.sequence'].next_by_code('agri.esg.red.line.monitoring') or '/'

        record = super().create(vals)

        # Trigger compliance check after creation
        record._check_compliance_status()

        return record

    def write(self, vals):
        """Override write to trigger compliance check if relevant fields change"""
        result = super().write(vals)

        # Check compliance status if relevant fields are updated
        if any(field in vals for field in ['current_value', 'location_id', 'is_in_protected_area', 'distance_to_boundary_km']):
            self._check_compliance_status()

        return result

    def _check_compliance_status(self):
        """Check compliance status based on configuration and current values"""
        for record in self:
            config = record.red_line_config_id

            if config.red_line_type == 'protected_area':
                # For protected areas, compliance depends on location
                if record.is_in_protected_area:
                    record.compliance_status = 'violation'
                    record.detection_details = f'Product location {record.location_id.name if record.location_id else "unknown"} is in protected area'
                elif record.distance_to_boundary_km and record.distance_to_boundary_km < config.buffer_distance_km:
                    record.compliance_status = 'warning'
                    record.detection_details = f'Product location within {config.buffer_distance_km}km buffer zone'
                else:
                    record.compliance_status = 'compliant'

            elif config.threshold_value:  # For threshold-based red lines
                current_val = record.current_value or 0
                threshold = config.threshold_value

                if current_val <= threshold:
                    record.compliance_status = 'compliant'
                elif current_val <= threshold * 1.1:  # 10% buffer
                    record.compliance_status = 'warning'
                elif current_val <= threshold * 1.3:  # 30% buffer
                    record.compliance_status = 'violation'
                else:
                    record.compliance_status = 'critical'

                record.detection_details = f'Current value {current_val} vs threshold {threshold}'
            else:
                # Default to compliant if no specific check defined
                record.compliance_status = 'compliant'

    def action_issue_red_line_alert(self):
        """Issue alert when red line is approached or crossed"""
        for record in self:
            if record.compliance_status in ['warning', 'violation', 'critical'] and not record.alert_issued:
                # Create an activity to alert responsible users
                self.env['mail.activity'].create({
                    'activity_type_id': self.env.ref('mail.mail_activity_data_alert').id,
                    'summary': f'ESG Red Line Alert: {record.name}',
                    'note': f'Compliance check {record.name} is at {record.compliance_status} level. Type: {record.red_line_config_id.red_line_type}. Details: {record.detection_details}',
                    'res_id': record.id,
                    'res_model_id': self.env['ir.model'].sudo().search([('model', '=', 'agri.esg.red.line.monitoring')]).id,
                    'user_id': self.env.user.id,
                })

                record.alert_issued = True
                record.message_post(body=_(f'ESG Red Line Alert issued for {record.name}. Status: {record.compliance_status}'))

    def action_resolve_violation(self):
        """Mark a violation as resolved with notes"""
        for record in self:
            if record.compliance_status in ['warning', 'violation', 'critical']:
                record.compliance_status = 'resolved'
                record.remediation_date = fields.Datetime.now()
                record.message_post(body=_(f'ESG Red Line violation resolved. Resolution notes: {record.resolution_notes or "No notes provided"}'))

    def action_check_batch_compliance(self, batch_lot_id):
        """Check compliance for a specific batch/lot"""
        # This method would typically be called from batch/lot records
        # to run ESG compliance checks on them
        config_records = self.env['agri.esg.red.line.config'].search([('active_monitoring', '=', True)])

        results = []
        for config in config_records:
            # Create a monitoring record for this batch and config
            monitoring_record = self.create({
                'red_line_config_id': config.id,
                'batch_lot_id': batch_lot_id,
                'detection_method': 'automated_batch_check',
                'automated_check': True,
            })

            # Perform the specific compliance check based on red line type
            monitoring_record._perform_specific_check()
            results.append(monitoring_record.id)

        return results

    def _perform_specific_check(self):
        """Perform specific type of compliance check based on red line type"""
        for record in self:
            if not record.batch_lot_id or not record.location_id:
                continue

            config = record.red_line_config_id

            if config.red_line_type == 'deforestation':
                # Check if location is in deforestation-risk area
                record.current_value = self._check_deforestation_risk(record.location_id, config)
            elif config.red_line_type == 'water_extraction':
                # Check water usage against thresholds
                record.current_value = self._check_water_usage(record.batch_lot_id, config)
            elif config.red_line_type == 'carbon_emission':
                # Check carbon footprint against thresholds
                record.current_value = self._check_carbon_footprint(record.batch_lot_id, config)
            elif config.red_line_type == 'protected_area':
                # Check if location is in protected area
                record.is_in_protected_area, record.distance_to_boundary_km = \
                    self._check_protected_area_compliance(record.location_id, config)

            # Update compliance status based on new values
            record._check_compliance_status()

            # Issue alerts if needed
            if record.compliance_status in ['warning', 'violation', 'critical']:
                record.action_issue_red_line_alert()

    def _check_deforestation_risk(self, location, config):
        """Check deforestation risk for a location"""
        # This would integrate with geofencing to check if the location
        # is in a deforestation-risk area
        if config.coordinates and location.gps_coordinates:
            try:
                # Use the GIS utilities from farm_core
                gis_utils_model = self.env['farm.core.gis.utils']
                # Parse coordinates: assume format is "lat,lon" for location
                coords = location.gps_coordinates.split(',')
                if len(coords) >= 2:
                    lat = float(coords[0])
                    lon = float(coords[1])
                    is_in_risk_area = gis_utils_model.is_point_in_polygon(
                        config.coordinates,
                        lon,  # longitude first for the GIS utility
                        lat   # latitude second for the GIS utility
                    )
                    return 1.0 if is_in_risk_area else 0.0
            except (ValueError, AttributeError, IndexError):
                # Handle malformed coordinates
                return 0.0
        return 0.0

    def _check_water_usage(self, batch_lot, config):
        """Check water usage for a batch"""
        # This would integrate with water usage tracking
        # For now, return a placeholder value
        return batch_lot.water_usage_m3 or 0.0

    def _check_carbon_footprint(self, batch_lot, config):
        """Check carbon footprint for a batch"""
        # This would integrate with carbon footprint calculations
        # Look for related carbon footprint records
        carbon_calc = self.env['farm.sustainability.carbon.footprint.calculation'].search([
            ('lot_id', '=', batch_lot.id)
        ], limit=1)

        if carbon_calc:
            return carbon_calc.total_carbon_footprint
        return 0.0

    def _check_protected_area_compliance(self, location, config):
        """Check if location is in protected area and distance to boundary"""
        is_in_area = False
        distance_km = float('inf')

        if config.coordinates and location.gps_coordinates:
            # Use the GIS utilities from farm_core
            gis_utils_model = self.env['farm.core.gis.utils']

            # Check if point is in protected polygon
            try:
                coords = location.gps_coordinates.split(',')
                if len(coords) >= 2:
                    lat = float(coords[0])
                    lon = float(coords[1])
                    is_in_area = gis_utils_model.is_point_in_polygon(config.coordinates, lon, lat)

                    # Calculate distance to boundary (simplified approach)
                    # In a real implementation, this would calculate the actual distance to polygon boundary
                    distance_km = 0.0 if is_in_area else config.buffer_distance_km + 1.0
            except (ValueError, AttributeError, IndexError):
                # If coordinates are malformed, return safe defaults
                pass

        return is_in_area, distance_km

    @api.model
    def _cron_check_compliance(self):
        """Scheduled job to check ESG compliance automatically"""
        active_configs = self.env['agri.esg.red.line.config'].search([
            ('active_monitoring', '=', True),
            ('monitoring_frequency', '!=', 'real_time')
        ])

        for config in active_configs:
            # Find recently created/updated batches or locations that need checking
            recent_lots = self.env['stock.lot'].search([
                ('create_date', '>', fields.Datetime.now() - timedelta(days=1))
            ])

            for lot in recent_lots:
                # Create monitoring record for this combination
                self.create({
                    'red_line_config_id': config.id,
                    'batch_lot_id': lot.id,
                    'detection_method': 'cron_check',
                    'automated_check': True,
                })._perform_specific_check()


class AgriStockLot(models.Model):
    """Extend stock.lot to add ESG compliance checking"""
    _inherit = 'stock.lot'

    # Add ESG compliance fields
    esg_compliance_status = fields.Selection([
        ('pending', 'Pending'),
        ('compliant', 'Compliant'),
        ('warning', 'Warning'),
        ('violation', 'Violation'),
        ('critical', 'Critical Violation'),
        ('resolved', 'Resolved'),
    ], string='ESG Compliance Status', compute='_compute_esg_compliance_status', store=True, precompute=True)

    esg_monitoring_ids = fields.One2many('agri.esg.red.line.monitoring', 'batch_lot_id',
                                        string='ESG Monitoring Records')
    last_esg_check = fields.Datetime('Last ESG Check')

    water_usage_m3 = fields.Float('Water Usage (m3)', help='Water consumed in production of this lot')
    land_use_area_m2 = fields.Float('Land Use Area (m2)', help='Area of land used for this lot')

    @api.depends('esg_monitoring_ids.compliance_status')
    def _compute_esg_compliance_status(self):
        """Compute overall ESG compliance status based on monitoring records"""
        for lot in self:
            if not lot.esg_monitoring_ids:
                lot.esg_compliance_status = 'pending'
            else:
                # Determine status based on worst compliance among all records
                statuses = lot.esg_monitoring_ids.mapped('compliance_status')
                if 'critical' in statuses:
                    lot.esg_compliance_status = 'critical'
                elif 'violation' in statuses:
                    lot.esg_compliance_status = 'violation'
                elif 'warning' in statuses:
                    lot.esg_compliance_status = 'warning'
                elif 'resolved' in statuses:
                    # If there are resolved violations, it might still be compliant depending on current status
                    unresolved = lot.esg_monitoring_ids.filtered(lambda r: r.compliance_status in ['violation', 'critical', 'warning'])
                    if unresolved:
                        lot.esg_compliance_status = 'warning'  # At least checked and working on it
                    else:
                        lot.esg_compliance_status = 'compliant'
                else:
                    lot.esg_compliance_status = 'compliant'

    def action_check_esg_compliance(self):
        """Manually trigger ESG compliance check for this batch"""
        self.ensure_one()

        monitoring_model = self.env['agri.esg.red.line.monitoring']
        results = monitoring_model.action_check_batch_compliance(self.id)

        self.last_esg_check = fields.Datetime.now()

        return {
            'type': 'ir.actions.act_window',
            'name': _('ESG Compliance Monitoring'),
            'res_model': 'agri.esg.red.line.monitoring',
            'view_mode': 'list,form',
            'domain': [('id', 'in', results)],
            'context': self.env.context,
        }