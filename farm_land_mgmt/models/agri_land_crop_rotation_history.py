from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

class AgriLandCropRotationHistory(models.Model):
    """
    US-001-09: 土地健康与轮作档案 (Land Health & Crop Rotation Records)
    Model to track crop rotation history for land parcels
    """
    _name = 'agri.land.crop.rotation.history'
    _description = 'Agricultural Land Crop Rotation History'
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
                vals['name'] = self.env['ir.sequence'].next_by_code('agri.land.crop.rotation.history') or _('CRH')

            # Check for continuous cropping risk during creation
            if vals.get('land_parcel_id') and vals.get('product_id'):
                land_parcel_id = self.env['farm.location'].browse(vals['land_parcel_id'])
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