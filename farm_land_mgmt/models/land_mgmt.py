from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


class LandCropRotationHistory(models.Model):
    """
    US-01-09: 土地健康与轮作档案 (Land Health & Crop Rotation Records)
    Model to track crop rotation history for land parcels
    """
    _name = 'farm.land.crop.rotation.history'
    _description = 'Land Crop Rotation History'
    _order = 'planting_date desc'

    name = fields.Char('Rotation Record', required=True)
    land_parcel_id = fields.Many2one('farm.location', string='Land Parcel', required=True)
    product_id = fields.Many2one('product.template', string='Crop Planted', required=True)
    planting_date = fields.Date('Planting Date', required=True)
    harvest_date = fields.Date('Harvest Date')
    yield_amount = fields.Float('Yield Amount')
    notes = fields.Text('Notes')
    rotation_date = fields.Date('Rotation Date', default=fields.Date.context_today, required=True)
    rotation_sequence = fields.Integer('Rotation Sequence', help='Position in the rotation cycle')

    # Continuous cropping obstacle risk assessment (from farm_core implementation)
    continuous_cropping_risk = fields.Float("Continuous Cropping Risk Score",
                                           help="Risk score based on crop type and previous planting history")
    continuous_cropping_warning = fields.Boolean("Continuous Cropping Warning",
                                                 compute='_compute_continuous_cropping_warning',
                                                 store=True)
    warning_reason = fields.Char("Warning Reason", compute='_compute_continuous_cropping_warning', store=True)

    state = fields.Selection([
        ('planted', 'Planted'),
        ('harvested', 'Harvested'),
        ('archived', 'Archived')
    ], string="Status", default='planted')

    @api.model_create_multi
    def create(self, vals_list):
        records = []
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('farm.land.crop.rotation.history') or _('CRH')

            # Check for continuous cropping risk during creation
            if vals.get('land_parcel_id') and vals.get('product_id'):
                land_parcel_id = self.env['stock.location'].browse(vals['land_parcel_id'])
                product_id = self.env['product.template'].browse(vals['product_id'])
                planting_date = vals.get('planting_date', fields.Date.today())

                # Call the risk check method to populate values
                risk_info = self.check_continuous_cropping_risk(land_parcel_id.id, product_id.id, planting_date)
                if risk_info['has_risk']:
                    vals['continuous_cropping_warning'] = True
                    vals['continuous_cropping_risk'] = risk_info['risk_level']
                    vals['warning_reason'] = risk_info['message']

            records.append(super().create(vals))
        return records[0] if len(records) == 1 else records

    @api.depends('product_id', 'land_parcel_id', 'planting_date')
    def _compute_continuous_cropping_warning(self):
        """Compute warning for continuous cropping based on crop type and location history"""
        for record in self:
            warning = False
            reason = ""

            if record.product_id and record.land_parcel_id and record.planting_date:
                # Check if same crop was planted in last 3 years in same location
                three_years_ago = record.planting_date.replace(year=record.planting_date.year - 3)

                previous_plantings = self.search([
                    ('land_parcel_id', '=', record.land_parcel_id.id),
                    ('product_id', '=', record.product_id.id),
                    ('planting_date', '>=', three_years_ago),
                    ('id', '!=', record.id),  # Exclude current record
                    ('state', '!=', 'archived')
                ])

                if len(previous_plantings) > 0:
                    # Calculate risk based on frequency
                    risk_score = len(previous_plantings) * 20  # 20 points per previous planting
                    record.continuous_cropping_risk = min(100, risk_score)

                    # Check crop family for more sophisticated risk assessment
                    crop_family = record.product_id.categ_id.name or "Unknown"
                    if crop_family in ['Solanaceae', 'Legumes', 'Brassicas']:  # Common susceptible families
                        risk_score += 10
                        record.continuous_cropping_risk = min(100, risk_score)

                    warning = True
                    reason = f"Same crop '{record.product_id.display_name}' was previously planted in this location within 3 years ({len(previous_plantings)} times)"
                else:
                    record.continuous_cropping_risk = 0.0

            else:
                record.continuous_cropping_risk = 0.0

            record.continuous_cropping_warning = warning
            record.warning_reason = reason if warning else ""

    @api.model
    def check_continuous_cropping_risk(self, land_parcel_id, product_id, planting_date=None):
        """
        Check if planting a specific crop in a location poses a continuous cropping risk
        """
        if not planting_date:
            planting_date = fields.Date.today()

        # Check if same crop was planted in last 3 years in same location
        three_years_ago = planting_date.replace(year=planting_date.year - 3)

        previous_plantings = self.search([
            ('land_parcel_id', '=', land_parcel_id),
            ('product_id', '=', product_id),
            ('planting_date', '>=', three_years_ago),
            ('state', '!=', 'archived')
        ])

        if len(previous_plantings) > 0:
            return {
                'has_risk': True,
                'risk_level': min(len(previous_plantings) * 20, 100),
                'previous_plantings': len(previous_plantings),
                'message': f"Warning: Same crop '{product_id.display_name if hasattr(product_id, 'display_name') else product_id}' was planted in this location {len(previous_plantings)} time(s) in the last 3 years, which may cause continuous cropping obstacles."
            }
        else:
            return {
                'has_risk': False,
                'risk_level': 0,
                'previous_plantings': 0,
                'message': "No continuous cropping risks detected for this crop in this location."
            }


class LandHealthRecord(models.Model):
    """
    US-01-09: 土地健康与轮作档案 (Land Health & Crop Rotation Records)
    Model to track land health metrics and soil analysis
    """
    _name = 'farm.land.health.record'
    _description = 'Land Health Record'
    _order = 'analysis_date desc'

    name = fields.Char('Health Record', required=True)
    land_parcel_id = fields.Many2one('farm.location', string='Land Parcel', required=True)
    analysis_date = fields.Date('Analysis Date', default=fields.Date.context_today, required=True)
    n_level = fields.Float('Nitrogen Level (N)')
    p_level = fields.Float('Phosphorus Level (P)')
    k_level = fields.Float('Potassium Level (K)')
    ph_level = fields.Float('pH Level')
    organic_matter = fields.Float('Organic Matter (%)')
    soil_texture = fields.Char('Soil Texture')
    moisture_level = fields.Float('Moisture Level (%)')
    compaction_level = fields.Float('Compaction Level (Bar)')
    salinity_level = fields.Float('Salinity Level (dS/m)')
    soil_temperature = fields.Float('Soil Temperature (°C)')
    pest_disease_incidence = fields.Text('Pest/Disease Incidence')
    soil_health_score = fields.Float('Soil Health Score (0-100)', compute='_compute_soil_health_score', store=True)
    health_status = fields.Selection([
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
        ('critical', 'Critical')
    ], string='Health Status', compute='_compute_health_status', store=True)
    recommendations = fields.Text('Recommendations')
    next_analysis_date = fields.Date('Next Analysis Date')

    @api.depends('n_level', 'p_level', 'k_level', 'ph_level', 'organic_matter', 'moisture_level')
    def _compute_soil_health_score(self):
        """Compute soil health score based on various parameters"""
        for record in self:
            score = 0.0

            # Nitrogen level (optimal range 20-40 mg/kg)
            if 20 <= record.n_level <= 40:
                score += 15
            elif 10 <= record.n_level <= 60:
                score += 10
            elif 5 <= record.n_level <= 80:
                score += 5

            # Phosphorus level (optimal range 15-25 mg/kg)
            if 15 <= record.p_level <= 25:
                score += 15
            elif 10 <= record.p_level <= 30:
                score += 10
            elif 5 <= record.p_level <= 40:
                score += 5

            # Potassium level (optimal range 100-200 mg/kg)
            if 100 <= record.k_level <= 200:
                score += 15
            elif 50 <= record.k_level <= 300:
                score += 10
            elif 25 <= record.k_level <= 400:
                score += 5

            # pH level (optimal range 6.0-7.0)
            if 6.0 <= record.ph_level <= 7.0:
                score += 15
            elif 5.5 <= record.ph_level <= 7.5:
                score += 10
            elif 5.0 <= record.ph_level <= 8.0:
                score += 5

            # Organic matter (optimal range 3-6%)
            if 3 <= record.organic_matter <= 6:
                score += 15
            elif 2 <= record.organic_matter <= 8:
                score += 10
            elif 1 <= record.organic_matter <= 10:
                score += 5

            # Moisture level (optimal range 20-30%)
            if 20 <= record.moisture_level <= 30:
                score += 10
            elif 15 <= record.moisture_level <= 35:
                score += 5

            # Cap the score at 100
            record.soil_health_score = min(100.0, score)

    @api.depends('soil_health_score')
    def _compute_health_status(self):
        """Compute health status based on soil health score"""
        for record in self:
            if record.soil_health_score >= 80:
                record.health_status = 'excellent'
            elif record.soil_health_score >= 60:
                record.health_status = 'good'
            elif record.soil_health_score >= 40:
                record.health_status = 'fair'
            elif record.soil_health_score >= 20:
                record.health_status = 'poor'
            else:
                record.health_status = 'critical'

    @api.model
    def schedule_next_analysis(self):
        """Schedule the next analysis date based on current analysis"""
        for record in self:
            # Default to 6 months from current analysis
            next_date = fields.Date.from_string(record.analysis_date) + timedelta(days=180)
            record.next_analysis_date = next_date


class FarmLocation(models.Model):
    _inherit = 'farm.location'  # Inherit from the core farm.location model instead of stock.location

    # 土地承包权信息 [US-18-01]
    land_contract_no = fields.Char("Land Contract No.")
    contractor_id = fields.Many2one('res.partner', string="Contractor")

    # Land Nature - keep the farm_land_mgmt specific values for compatibility but reference core values
    land_nature = fields.Selection(selection_add=[
        ('general_farmland', 'General Farmland'),
        ('permanent_basic_farmland', 'Permanent Basic Farmland'),
        ('construction_land', 'Construction Land'),
        ('other', 'Other')
    ])

    # US-01-09: Land Health & Crop Rotation Records
    land_health_records = fields.One2many('farm.land.health.record', 'land_parcel_id', string='Land Health Records')
    crop_rotation_history = fields.One2many('farm.land.crop.rotation.history', 'land_parcel_id', string='Crop Rotation History')
    last_rotation_date = fields.Date('Last Rotation Date', compute='_compute_last_rotation', store=True)
    current_crop_type = fields.Char('Current Crop Type', compute='_compute_current_crop', store=True)
    soil_health_score = fields.Float('Current Soil Health Score', compute='_compute_current_health_score', store=True)
    health_status = fields.Selection([
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
        ('critical', 'Critical')
    ], string='Health Status', compute='_compute_current_health_status', store=True)
    consecutive_planting_count = fields.Integer('Consecutive Planting Count', help='Number of consecutive seasons the same crop was planted')
    rotation_risk_score = fields.Float('Rotation Risk Score', compute='_compute_rotation_risk', store=True)

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
                record.current_crop_type = current_rotation.crop_type
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
                record.health_status = 'unknown'

    @api.depends('crop_rotation_history')
    def _compute_rotation_risk(self):
        """Compute rotation risk score based on consecutive planting patterns"""
        for record in self:
            risk_score = 0.0
            if record.crop_rotation_history:
                # Check for consecutive planting of same crop type
                sorted_rotations = sorted(record.crop_rotation_history, key=lambda r: r.planting_date or datetime.min.date())

                if len(sorted_rotations) >= 2:
                    # Look at the last few rotations to identify patterns
                    recent_rotations = sorted_rotations[-5:]  # Last 5 rotations
                    crop_types = [r.crop_type for r in recent_rotations if r.crop_type]

                    if len(crop_types) >= 2:
                        # Check if recent crops are the same (monoculture risk)
                        if len(set(crop_types[-3:])) == 1:  # Same crop in last 3 rotations
                            risk_score = 80.0  # High risk
                        elif len(set(crop_types[-2:])) == 1:  # Same crop in last 2 rotations
                            risk_score = 50.0  # Medium risk
                        else:
                            # Check diversity in recent rotations
                            unique_crops = len(set(crop_types))
                            total_crops = len(crop_types)
                            if unique_crops / total_crops > 0.7:  # High diversity
                                risk_score = 20.0
                            else:
                                risk_score = 40.0  # Medium risk

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
                                        compute='_compute_rotation_info', store=True)
    last_planting_date = fields.Date("Last Planting Date", compute='_compute_rotation_info', store=True)
    continuous_cropping_risk_alert = fields.Boolean("Continuous Cropping Alert",
                                                    compute='_compute_rotation_info', store=True)

    @api.depends('crop_rotation_history.planting_date', 'crop_rotation_history.product_id',
                 'crop_rotation_history.continuous_cropping_warning')
    def _compute_rotation_info(self):
        """Compute rotation-related information"""
        for location in self:
            # Get the most recent planting record
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
                'view_mode': 'tree,form',
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
            'view_mode': 'tree,form',
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
                'view_mode': 'tree,form',
                'domain': [('land_parcel_id', '=', record.id)],
                'context': {'default_land_parcel_id': record.id}
            }

    # Soil analysis integration for land health management - link to the proper location
    soil_analysis_ids = fields.One2many('farm.soil.analysis', 'location_id', string="Soil Analyses")
    latest_ph = fields.Float("Latest pH", compute='_compute_latest_soil_stats', store=True)
    latest_organic_matter = fields.Float("Organic Matter (%)", compute='_compute_latest_soil_stats', store=True)

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
            'view_mode': 'tree,form',
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
            if record.is_land_parcel and record.land_nature == 'construction_land':
                raise ValidationError(_("Land marked as 'Construction Land' cannot be a 'Land Parcel'."))

class SoilAnalysis(models.Model):
    """
    Soil Analysis Management - moved from farm_core for better responsibility alignment
    US-01-09: Land Health and Crop Rotation Records - Heavy metals and nutrient tracking
    """
    _name = 'farm.soil.analysis'
    _description = 'Soil Analysis Report'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'analysis_date desc'

    name = fields.Char("Report Reference", required=True, default=lambda self: _('New'))
    location_id = fields.Many2one('stock.location', string="Land Parcel", required=True)
    analysis_date = fields.Date("Analysis Date", default=fields.Date.today, required=True)
    laboratory_id = fields.Many2one('res.partner', string="Laboratory", domain=[('is_company', '=', True)])

    # Nutrient indicators
    ph_level = fields.Float("pH Level", digits=(10, 2))
    organic_matter = fields.Float("Organic Matter (%)")
    nitrogen_content = fields.Float("Nitrogen (mg/kg)")
    phosphorus_content = fields.Float("Phosphorus (mg/kg)")
    potassium_content = fields.Float("Potassium (mg/kg)")

    # Heavy metals indicators (for US-01-09: Land Health and Crop Rotation Records)
    lead_content = fields.Float("Lead (Pb) (mg/kg)")
    cadmium_content = fields.Float("Cadmium (Cd) (mg/kg)")
    mercury_content = fields.Float("Mercury (Hg) (mg/kg)")
    arsenic_content = fields.Float("Arsenic (As) (mg/kg)")
    chromium_content = fields.Float("Chromium (Cr) (mg/kg)")
    copper_content = fields.Float("Copper (Cu) (mg/kg)")
    zinc_content = fields.Float("Zinc (Zn) (mg/kg)")
    nickel_content = fields.Float("Nickel (Ni) (mg/kg)")

    # Trace elements
    magnesium = fields.Float("Magnesium (mg/kg)")
    calcium = fields.Float("Calcium (mg/kg)")

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
    _inherit = 'project.task'

    @api.constrains('land_parcel_id', 'project_id')
    def _check_task_land_use_compliance(self):
        for record in self:
            if record.project_id and record.land_parcel_id:
                # The land_parcel_id field should now reference farm.location
                record.project_id._check_activity_land_use_compliance()
