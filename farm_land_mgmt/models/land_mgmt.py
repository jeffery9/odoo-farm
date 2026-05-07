from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


class LandCropRotationHistory(models.Model):
    """
    Farm-specific extension of the agricultural land crop rotation history model.
    This ensures backward compatibility while using the new agri.* namespace.
    """
    _name = 'farm.land.crop.rotation.history'
    _description = 'Land Crop Rotation History (Deprecated - Use agri.land.crop.rotation.history)'
    _inherit = 'agri.land.crop.rotation.history'

    def _register_hook(self):
        """Display deprecation warning when module is installed."""
        import logging
        _logger = logging.getLogger(__name__)
        _logger.warning(
            "farm.land.crop.rotation.history is deprecated. "
            "Please update your code to use agri.land.crop.rotation.history instead."
        )
        return super()._register_hook()


class LandHealthRecord(models.Model):
    """
    Farm-specific extension of the agricultural land health record model.
    This ensures backward compatibility while using the new agri.* namespace.
    """
    _name = 'farm.land.health.record'
    _description = 'Land Health Record (Deprecated - Use agri.land.health.record)'
    _inherit = 'agri.land.health.record'

    def _register_hook(self):
        """Display deprecation warning when module is installed."""
        import logging
        _logger = logging.getLogger(__name__)
        _logger.warning(
            "farm.land.health.record is deprecated. "
            "Please update your code to use agri.land.health.record instead."
        )
        return super()._register_hook()


class FarmLocation(models.Model):
    _inherit = 'farm.location'  # Inherit from the core farm.location model

    # 土地承包权信息 [US-041-01]
    land_contract_no = fields.Char("Land Contract No.")
    contractor_id = fields.Many2one('res.partner', string="Contractor")

    # Land Nature - keep the farm_land_mgmt specific values for compatibility
    land_nature = fields.Selection(selection_add=[
        ('general_farmland', 'General Farmland'),
        ('permanent_basic_farmland', 'Permanent Basic Farmland'),
        ('construction_land', 'Construction Land'),
        ('other', 'Other')
    ])

    # US-001-09: Land Health & Crop Rotation Records
    land_health_records = fields.One2many('farm.land.health.record', 'land_parcel_id', string='Land Health Records')
    crop_rotation_history = fields.One2many('farm.land.crop.rotation.history', 'land_parcel_id', string='Crop Rotation History')
    last_rotation_date = fields.Date('Last Rotation Date', compute='_compute_last_rotation', store=True, precompute=True)
    current_crop_type = fields.Char('Current Crop Type', compute='_compute_current_crop', store=True, precompute=True)
    soil_health_score = fields.Float('Current Soil Health Score', compute='_compute_current_health_score', store=True, precompute=True)
    health_status = fields.Selection([
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
        ('critical', 'Critical')
    ], string='Health Status', compute='_compute_current_health_status', store=True, precompute=True)
    consecutive_planting_count = fields.Integer('Consecutive Planting Count', help='Number of consecutive seasons the same crop was planted')
    rotation_risk_score = fields.Float('Rotation Risk Score', compute='_compute_rotation_risk', store=True, precompute=True)

    @api.depends('crop_rotation_history')
    def _compute_last_rotation(self):
        """Compute the last rotation date"""
        for record in self:
            if record.crop_rotation_history:
                last_rotation = max(record.crop_rotation_history, key=lambda r: r.planting_date or datetime.min.date())
                record.last_rotation_date = last_rotation.planting_date
            else:
                record.last_rotation_date = False

    @api.depends('crop_rotation_history')
    def _compute_current_crop(self):
        """Compute the current crop type based on most recent rotation"""
        for record in self:
            if record.crop_rotation_history:
                current_rotation = max(record.crop_rotation_history, key=lambda r: r.planting_date or datetime.min.date())
                record.current_crop_type = current_rotation.product_id.name if current_rotation.product_id else False
            else:
                record.current_crop_type = False

    @api.depends('land_health_records')
    def _compute_current_health_score(self):
        """Compute the current soil health score based on the most recent record"""
        for record in self:
            if record.land_health_records:
                latest_record = max(record.land_health_records, key=lambda r: r.analysis_date or datetime.min.date())
                record.soil_health_score = latest_record.soil_health_score
            else:
                record.soil_health_score = 0.0

    @api.depends('land_health_records')
    def _compute_current_health_status(self):
        """Compute the current health status based on the most recent record"""
        for record in self:
            if record.land_health_records:
                latest_record = max(record.land_health_records, key=lambda r: r.analysis_date or datetime.min.date())
                record.health_status = latest_record.health_status
            else:
                record.health_status = 'critical'

    @api.depends('crop_rotation_history')
    def _compute_rotation_risk(self):
        """Compute rotation risk score based on consecutive planting patterns"""
        for record in self:
            risk_score = 0.0
            if record.crop_rotation_history:
                sorted_rotations = sorted(record.crop_rotation_history, key=lambda r: r.planting_date or datetime.min.date())
                if len(sorted_rotations) >= 2:
                    recent_rotations = sorted_rotations[-5:]
                    product_ids = [r.product_id.id for r in recent_rotations if r.product_id]
                    if len(product_ids) >= 2:
                        if len(set(product_ids[-3:])) == 1:
                            risk_score = 80.0
                        elif len(set(product_ids[-2:])) == 1:
                            risk_score = 50.0
                        else:
                            unique_crops = len(set(product_ids))
                            total_crops = len(product_ids)
                            if unique_crops / total_crops > 0.7:
                                risk_score = 20.0
                            else:
                                risk_score = 40.0
            record.rotation_risk_score = risk_score

    def action_add_health_record(self):
        """Add a new health record for this land parcel"""
        for record in self:
            return {
                'name': _('Add Land Health Record'),
                'type': 'ir.actions.act_window',
                'res_model': 'farm.land.health.record',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'default_land_parcel_id': record.id,
                    'default_name': f"Health Record - {record.name}",
                }
            }

    def action_add_rotation_record(self):
        """Add a new rotation record for this land parcel"""
        for record in self:
            return {
                'name': _('Add Crop Rotation Record'),
                'type': 'ir.actions.act_window',
                'res_model': 'farm.land.crop.rotation.history',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'default_land_parcel_id': record.id,
                    'default_name': f"Rotation - {record.name}",
                }
            }

    # Additional rotation-related fields
    last_crop_planted = fields.Many2one('product.template', "Last Crop Planted",
                                        compute='_compute_rotation_info', store=True, precompute=True)
    last_planting_date = fields.Date("Last Planting Date", compute='_compute_rotation_info', store=True, precompute=True)
    continuous_cropping_risk_alert = fields.Boolean("Continuous Cropping Alert",
                                                    compute='_compute_rotation_info', store=True, precompute=True)

    @api.depends('crop_rotation_history.planting_date', 'crop_rotation_history.product_id',
                 'crop_rotation_history.continuous_cropping_warning')
    def _compute_rotation_info(self):
        """Compute rotation-related information"""
        for location in self:
            recent_planting = self.env['farm.land.crop.rotation.history'].search([
                ('land_parcel_id', '=', location.id)
            ], order='planting_date desc', limit=1)
            location.last_crop_planted = recent_planting.product_id if recent_planting else False
            location.last_planting_date = recent_planting.planting_date if recent_planting else False
            location.continuous_cropping_risk_alert = recent_planting.continuous_cropping_warning if recent_planting else False

    def action_view_rotation_timeline(self):
        """View rotation timeline for this land parcel"""
        for record in self:
            return {
                'name': _('Rotation Timeline'),
                'type': 'ir.actions.act_window',
                'res_model': 'farm.land.crop.rotation.history',
                'view_mode': 'list,form',
                'domain': [('land_parcel_id', '=', record.id)],
                'context': {'default_land_parcel_id': record.id}
            }

    def action_view_rotation_history(self):
        """Action to view rotation history from location form"""
        self.ensure_one()
        action = {
            'type': 'ir.actions.act_window',
            'name': 'Rotation History',
            'res_model': 'farm.land.crop.rotation.history',
            'view_mode': 'list,form',
            'domain': [('land_parcel_id', '=', self.id)],
            'context': {
                'default_land_parcel_id': self.id,
                'default_planting_date': fields.Date.today()
            }
        }
        return action

    def action_view_health_history(self):
        """View health history for this land parcel"""
        for record in self:
            return {
                'name': _('Health History'),
                'type': 'ir.actions.act_window',
                'res_model': 'farm.land.health.record',
                'view_mode': 'list,form',
                'domain': [('land_parcel_id', '=', record.id)],
                'context': {'default_land_parcel_id': record.id}
            }

    # Soil analysis integration for land health management - link to the proper location
    soil_analysis_ids = fields.One2many('farm.soil.analysis', 'location_id', string="Soil Analyses")
    latest_ph = fields.Float("Latest pH", compute='_compute_latest_soil_stats', store=True, precompute=True)
    latest_organic_matter = fields.Float("Organic Matter (%)", compute='_compute_latest_soil_stats', store=True, precompute=True)

    @api.depends('soil_analysis_ids.state', 'soil_analysis_ids.ph_level')
    def _compute_latest_soil_stats(self):
        for loc in self:
            latest = self.env['farm.soil.analysis'].search([
                ('location_id', '=', loc.id),
                ('state', '=', 'done')
            ], order='analysis_date desc', limit=1)
            loc.latest_ph = latest.ph_level if latest else 0.0
            loc.latest_organic_matter = latest.organic_matter if latest else 0.0

    def action_view_soil_analyses(self):
        """Action to view soil analyses for this location"""
        self.ensure_one()
        action = {
            'type': 'ir.actions.act_window',
            'name': 'Soil Analyses',
            'res_model': 'farm.soil.analysis',
            'view_mode': 'list,form',
            'domain': [('location_id', '=', self.id)],
            'context': {
                'default_location_id': self.id,
                'default_analysis_date': fields.Date.today()
            }
        }
        return action

    @api.constrains('land_nature', 'is_land_parcel')
    def _check_land_nature_validity(self):
        for record in self:
            if hasattr(record, 'is_land_parcel') and record.is_land_parcel and record.land_nature == 'construction_land':
                raise ValidationError(_("Land marked as 'Construction Land' cannot be a 'Land Parcel'."))

class SoilAnalysis(models.Model):
    """
    DEPRECATED: Soil Analysis Management. [US-014-2026]
    This model is maintained for backward compatibility.
    Use agri.soil.analysis for new implementations.
    """
    _name = 'farm.soil.analysis'
    _description = 'Soil Analysis Report (Deprecated - Use agri.soil.analysis)'
    _inherit = ['agri.soil.analysis', 'mail.thread', 'mail.activity.mixin']
    _order = 'analysis_date desc'

    location_id = fields.Many2one('farm.location', string="Land Parcel", required=True)
    laboratory_id = fields.Many2one('res.partner', string="Laboratory", domain=[('is_company', '=', True)])

    # Recommendations
    recommendation = fields.Text("Fertilization Recommendations")
    remediation_advice = fields.Text("Soil Remediation Advice", help="Recommendations for improving soil health")

    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Validated'),
        ('cancel', 'Cancelled')
    ], string="Status", default='draft', tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('farm.soil.analysis') or _('SOIL')
        return super().create(vals_list)

    def action_validate(self):
        self.write({'state': 'done'})

    def get_historical_trends(self):
        """
        Get historical trends for heavy metals and nutrients for this location
        Returns a dictionary with historical data for charting
        """
        if not self.location_id:
            return {}

        # Get all soil analyses for this location ordered by date
        all_analyses = self.search([
            ('location_id', '=', self.location_id.id)
        ], order='analysis_date asc')

        if not all_analyses:
            return {}

        # Prepare data for charting
        trend_data = {
            'dates': [],
            'ph_levels': [],
            'organic_matter': [],
            'nitrogen': [],
            'phosphorus': [],
            'potassium': [],
            'heavy_metals': {
                'lead': [],
                'cadmium': [],
                'mercury': [],
                'arsenic': [],
                'chromium': [],
                'copper': [],
                'zinc': [],
                'nickel': []
            }
        }

        for analysis in all_analyses:
            trend_data['dates'].append(analysis.analysis_date.strftime('%Y-%m-%d') if analysis.analysis_date else '')
            trend_data['ph_levels'].append(analysis.ph_level or 0.0)
            trend_data['organic_matter'].append(analysis.organic_matter or 0.0)
            trend_data['nitrogen'].append(analysis.nitrogen_content or 0.0)
            trend_data['phosphorus'].append(analysis.phosphorus_content or 0.0)
            trend_data['potassium'].append(analysis.potassium_content or 0.0)

            trend_data['heavy_metals']['lead'].append(analysis.lead_content or 0.0)
            trend_data['heavy_metals']['cadmium'].append(analysis.cadmium_content or 0.0)
            trend_data['heavy_metals']['mercury'].append(analysis.mercury_content or 0.0)
            trend_data['heavy_metals']['arsenic'].append(analysis.arsenic_content or 0.0)
            trend_data['heavy_metals']['chromium'].append(analysis.chromium_content or 0.0)
            trend_data['heavy_metals']['copper'].append(analysis.copper_content or 0.0)
            trend_data['heavy_metals']['zinc'].append(analysis.zinc_content or 0.0)
            trend_data['heavy_metals']['nickel'].append(analysis.nickel_content or 0.0)

        return trend_data

    def _register_hook(self):
        """Display deprecation warning when module is installed."""
        import logging
        _logger = logging.getLogger(__name__)
        _logger.warning(
            "farm.soil.analysis is deprecated. "
            "Please update your code to use agri.soil.analysis instead."
        )
        return super()._register_hook()


class ProductTemplate(models.Model):
    """Extension of product template to add crop-specific information"""
    _inherit = 'product.template'

    # Crop-specific fields for rotation management
    crop_family = fields.Char("Botanical Family", help="e.g., Solanaceae, Legumes, Brassicas")
    continuous_cropping_susceptible = fields.Boolean("Susceptible to Continuous Cropping",
                                                     help="Indicates if this crop is susceptible to continuous cropping obstacles")
    recommended_rotation_interval = fields.Integer("Recommended Rotation Interval (years)",
                                                   help="Recommended time interval before replanting same crop",
                                                   default=3)

class FarmActivity(models.Model):
    _name = 'project.project'
    _inherit = 'project.project'

    @api.constrains('activity_family', 'land_parcel_ids')
    def _check_activity_land_use_compliance(self):
        for record in self:
            if record.activity_family in ['aquaculture', 'agritourism'] and record.land_parcel_ids:
                for parcel in record.land_parcel_ids:
                    # Check if this is the core stock.location or extended farm.location
                    if hasattr(parcel, 'land_nature') and parcel.land_nature == 'permanent_basic_farmland':
                        raise ValidationError(_("Activity Type '%s' is not allowed on 'Permanent Basic Farmland' for parcel '%s'.") % (record.activity_family, parcel.name))

class ProjectTask(models.Model):
    _name = 'project.task'
    _inherit = 'project.task'

    @api.constrains('land_parcel_id', 'project_id')
    def _check_task_land_use_compliance(self):
        for record in self:
            if record.project_id and record.land_parcel_id:
                # The land_parcel_id field should now reference farm.location
                record.project_id._check_activity_land_use_compliance()