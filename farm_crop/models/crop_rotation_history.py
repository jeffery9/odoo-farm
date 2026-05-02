from odoo import models, fields, api, _
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)


class CropRotationHistory(models.Model):
    """
    Crop Rotation History - Track planting history for land health management
    US-01-09: Land Health and Crop Rotation Records
    """
    _name = 'farm.crop.rotation.history'
    _description = 'Crop Rotation History'
    _order = 'planting_date desc'

    name = fields.Char("History Reference", required=True, default=lambda self: _('New'))
    location_id = fields.Many2one('farm.location', string="Land Parcel", required=True)
    product_id = fields.Many2one('product.template', string="Crop Planted", required=True)

    planting_date = fields.Date("Planting Date", required=True)
    harvesting_date = fields.Date("Harvesting Date")

    campaign_id = fields.Many2one('farm.agricultural.campaign', string="Associated Campaign")
    season = fields.Char("Growing Season", help="e.g. Spring 2026, Autumn 2025")

    # Planting details
    planting_quantity = fields.Float("Quantity Planted")
    unit_of_measure = fields.Many2one('uom.uom', string="Unit of Measure")
    notes = fields.Text("Notes")

    # Continuous cropping obstacle risk assessment
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
                vals['name'] = self.env['ir.sequence'].next_by_code('farm.crop.rotation.history') or _('CRH')

            # Check for continuous cropping risk during creation
            if vals.get('location_id') and vals.get('product_id'):
                location_id = self.env['farm.location'].browse(vals['location_id'])
                product_id = self.env['product.template'].browse(vals['product_id'])
                planting_date = vals.get('planting_date', fields.Date.today())

                # Call the risk check method to populate values
                risk_info = self.check_continuous_cropping_risk(location_id.id, product_id.id, planting_date)
                if risk_info['has_risk']:
                    vals['continuous_cropping_warning'] = True
                    vals['continuous_cropping_risk'] = risk_info['risk_level']
                    vals['warning_reason'] = risk_info['message']

            records.append(super().create(vals))
        return records[0] if len(records) == 1 else records

    @api.depends('product_id', 'location_id', 'planting_date')
    def _compute_continuous_cropping_warning(self):
        """Compute warning for continuous cropping based on crop type and location history"""
        for record in self:
            warning = False
            reason = ""

            if record.product_id and record.location_id and record.planting_date:
                # Check if same crop was planted in last 3 years in same location
                three_years_ago = record.planting_date.replace(year=record.planting_date.year - 3)

                previous_plantings = self.search([
                    ('location_id', '=', record.location_id.id),
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
    def check_continuous_cropping_risk(self, location_id, product_id, planting_date=None):
        """
        Check if planting a specific crop in a location poses a continuous cropping risk
        """
        if not planting_date:
            planting_date = fields.Date.today()

        # Check if same crop was planted in last 3 years in same location
        three_years_ago = planting_date.replace(year=planting_date.year - 3)

        previous_plantings = self.search([
            ('location_id', '=', location_id),
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


class FarmLocationExtension(models.Model):
    """Extension of FarmLocation to add rotation history functionality"""
    _inherit = 'farm.location'

    # Add field to store crop rotation history
    rotation_history_ids = fields.One2many('farm.crop.rotation.history', 'location_id', string="Rotation History")

    # Add rotation-related computed fields
    last_crop_planted = fields.Many2one('product.template', "Last Crop Planted",
                                        compute='_compute_rotation_info', store=True)
    last_planting_date = fields.Date("Last Planting Date", compute='_compute_rotation_info', store=True)
    continuous_cropping_risk_alert = fields.Boolean("Continuous Cropping Alert",
                                                    compute='_compute_rotation_info', store=True)

    @api.depends('rotation_history_ids.planting_date', 'rotation_history_ids.product_id',
                 'rotation_history_ids.continuous_cropping_warning')
    def _compute_rotation_info(self):
        """Compute rotation-related information"""
        for location in self:
            # Get the most recent planting record
            recent_planting = self.env['farm.crop.rotation.history'].search([
                ('location_id', '=', location.id)
            ], order='planting_date desc', limit=1)

            location.last_crop_planted = recent_planting.product_id if recent_planting else False
            location.last_planting_date = recent_planting.planting_date if recent_planting else False
            location.continuous_cropping_risk_alert = recent_planting.continuous_cropping_warning if recent_planting else False

    def action_view_rotation_history(self):
        """Action to view rotation history from location form"""
        action = {
            'type': 'ir.actions.act_window',
            'name': 'Rotation History',
            'res_model': 'farm.crop.rotation.history',
            'view_mode': 'list,form',
            'domain': [('location_id', '=', self.id)],
            'context': {
                'default_location_id': self.id,
                'default_planting_date': fields.Date.today()
            }
        }
        return action


class ProductTemplateExtension(models.Model):
    """Extension of product template to add crop-specific information"""
    _inherit = 'product.template'

    # Crop-specific fields for rotation management
    crop_family = fields.Char("Botanical Family", help="e.g., Solanaceae, Legumes, Brassicas")
    continuous_cropping_susceptible = fields.Boolean("Susceptible to Continuous Cropping",
                                                     help="Indicates if this crop is susceptible to continuous cropping obstacles")
    recommended_rotation_interval = fields.Integer("Recommended Rotation Interval (years)",
                                                   help="Recommended time interval before replanting same crop",
                                                   default=3)


class AgriCampaignExtension(models.Model):
    """Extension of agri campaign to check rotation risks during planning"""
    _inherit = 'farm.agricultural.campaign'

    def action_plan_campaign(self):
        """Override campaign planning to check for rotation risks"""
        result = super().action_plan_campaign() if hasattr(super(), 'action_plan_campaign') else {}

        # Check for continuous cropping risks during campaign planning
        for campaign in self:
            if campaign.land_parcel_id and campaign.crop_variety_id:
                rotation_model = self.env['farm.crop.rotation.history']
                risk_info = rotation_model.check_continuous_cropping_risk(
                    campaign.land_parcel_id.id,
                    campaign.crop_variety_id,
                    campaign.planned_start_date
                )

                if risk_info['has_risk']:
                    # Add activity or warning to campaign
                    message = f"Rotation Risk Alert: {risk_info['message']}"
                    campaign.message_post(body=message, subtype_xmlid='mail.mt_note')

        return result
class FarmLocationExtension(models.Model):
    _inherit = 'farm.location'
    
    def action_view_soil_analyses_history(self):
        return True
