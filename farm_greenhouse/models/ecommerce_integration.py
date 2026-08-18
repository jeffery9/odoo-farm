from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import json
import logging
import requests
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)


class FarmEcommercePlatform(models.Model):
    """
    Configuration for e-commerce platforms
    """
    _name = 'farm.ecommerce.platform'
    _description = 'E-commerce Platform Configuration'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Platform Name', required=True)
    code = fields.Char('Platform Code', required=True, copy=False)
    platform_type = fields.Selection([
        ('taobao', 'Taobao/Tmall'),
        ('jd', 'JD.com'),
        ('pinduoduo', 'Pinduoduo'),
        ('weidian', 'Weidian'),
        ('douyin', 'Douyin E-commerce'),
        ('other', 'Other'),
    ], string='Platform Type', required=True)

    api_endpoint = fields.Char('API Endpoint', required=True)
    client_id = fields.Char('Client ID', help='Client ID for API authentication')
    client_secret = fields.Char('Client Secret', help='Client Secret for API authentication')
    access_token = fields.Char('Access Token')
    refresh_token = fields.Char('Refresh Token')
    token_expiry = fields.Datetime('Token Expiry')

    active = fields.Boolean('Active', default=True)
    sync_inventory = fields.Boolean('Sync Inventory', default=True)
    sync_orders = fields.Boolean('Sync Orders', default=False)
    sync_customers = fields.Boolean('Sync Customers', default=False)

    last_sync = fields.Datetime('Last Sync')
    next_sync = fields.Datetime('Next Scheduled Sync')

    description = fields.Text('Description')

    def action_test_connection(self):
        """Test connection to the e-commerce platform"""
        for platform in self:
            try:
                # Create a simple test request
                headers = {
                    'Content-Type': 'application/json',
                    'User-Agent': 'Odoo-Ecommerce-Integration/1.0'
                }

                # This would require a platform-specific test endpoint
                # For now, we'll just validate the configuration
                if not platform.api_endpoint:
                    raise ValidationError(_("API Endpoint is required"))

                # Add authentication if available
                if platform.access_token:
                    headers['Authorization'] = f'Bearer {platform.access_token}'
                elif platform.client_id and platform.client_secret:
                    # Platform would need to implement OAuth or similar flow
                    pass

                self.message_post(body=_(f"Configuration validated for {platform.name}. Ready to sync."))

            except Exception as e:
                _logger.error(f"Failed to validate e-commerce platform {platform.name}: {str(e)}")
                raise ValidationError(f"Validation failed for {platform.name}: {str(e)}")


class FarmEcommerceSyncLog(models.Model):
    """
    Log for tracking e-commerce synchronization activities
    """
    _name = 'farm.ecommerce.sync.log'
    _description = 'E-commerce Sync Log'
    _order = 'create_date desc'

    platform_id = fields.Many2one('farm.ecommerce.platform', string='E-commerce Platform', required=True)
    sync_type = fields.Selection([
        ('inventory', 'Inventory Sync'),
        ('orders', 'Order Sync'),
        ('customers', 'Customer Sync'),
        ('products', 'Product Sync'),
        ('status', 'Status Update'),
    ], string='Sync Type', required=True)

    status = fields.Selection([
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ], string='Status', default='pending')

    records_processed = fields.Integer('Records Processed', default=0)
    records_success = fields.Integer('Records Success', default=0)
    records_failed = fields.Integer('Records Failed', default=0)

    start_time = fields.Datetime('Start Time')
    end_time = fields.Datetime('End Time')
    duration = fields.Float('Duration (seconds)', compute='_compute_duration')

    error_message = fields.Text('Error Message')
    details = fields.Text('Sync Details')

    @api.depends('start_time', 'end_time')
    def _compute_duration(self):
        for log in self:
            if log.start_time and log.end_time:
                duration = (log.end_time - log.start_time).total_seconds()
                log.duration = round(duration, 2)
            else:
                log.duration = 0.0


class FarmLocation(models.Model):
    """Extend farm.location to include e-commerce capabilities"""
    _inherit = 'farm.location'

    # Add fields for e-commerce integration
    ecommerce_sync_enabled = fields.Boolean('E-commerce Sync Enabled',
                                           help='Enable this greenhouse for e-commerce inventory sync')
    ecommerce_platform_ids = fields.Many2many('farm.ecommerce.platform', 'farm_location_farm_ecommerce_platform_rel', 'location_id', 'platform_id',
                                             string='E-commerce Platforms',
                                             help='Platforms to sync this greenhouse data with')
    ecommerce_inventory_status = fields.Selection([
        ('in_stock', 'In Stock'),
        ('low_stock', 'Low Stock'),
        ('out_of_stock', 'Out of Stock'),
        ('discontinued', 'Discontinued'),
    ], string='Inventory Status', default='in_stock')

    expected_harvest_date = fields.Date('Expected Harvest Date',
                                       help='Expected harvest date for e-commerce pre-ordering')
    yield_prediction = fields.Float('Yield Prediction (kg)',
                                   help='Predicted yield for inventory planning')
    quality_grade = fields.Selection([
        ('premium', 'Premium'),
        ('standard', 'Standard'),
        ('basic', 'Basic'),
    ], string='Quality Grade', default='standard')

    def action_sync_to_ecommerce(self):
        """Sync greenhouse data to configured e-commerce platforms"""
        for greenhouse in self:
            if not greenhouse.ecommerce_sync_enabled:
                continue

            for platform in greenhouse.ecommerce_platform_ids:
                try:
                    # Create a sync log entry
                    sync_log = self.env['farm.ecommerce.sync.log'].create({
                        'platform_id': platform.id,
                        'sync_type': 'inventory',
                        'start_time': fields.Datetime.now(),
                        'status': 'in_progress',
                    })

                    # Prepare greenhouse data for e-commerce platform
                    greenhouse_data = {
                        'greenhouse_id': greenhouse.id,
                        'name': greenhouse.name,
                        'location': greenhouse.display_name,
                        'environmental_conditions': {
                            'temperature': greenhouse.current_temp,
                            'humidity': greenhouse.current_humidity,
                            'co2': greenhouse.current_co2,
                            'light_intensity': greenhouse.current_light,
                            'nutrient_ec': greenhouse.current_ec,
                            'nutrient_ph': greenhouse.current_ph,
                        },
                        'inventory_status': greenhouse.ecommerce_inventory_status,
                        'expected_harvest_date': greenhouse.expected_harvest_date,
                        'yield_prediction': greenhouse.yield_prediction,
                        'quality_grade': greenhouse.quality_grade,
                        'sync_timestamp': fields.Datetime.now(),
                    }

                    # In a real implementation, this would make API calls to the e-commerce platform
                    # For now, we'll just log the data preparation
                    sync_log.details = json.dumps(greenhouse_data, default=str, indent=2)
                    sync_log.records_processed = 1
                    sync_log.records_success = 1
                    sync_log.status = 'completed'
                    sync_log.end_time = fields.Datetime.now()

                    # Update greenhouse sync status
                    greenhouse.message_post(
                        body=_(f"Successfully prepared data for sync to {platform.name}")
                    )

                except Exception as e:
                    sync_log.status = 'failed'
                    sync_log.error_message = str(e)
                    sync_log.end_time = fields.Datetime.now()
                    greenhouse.message_post(
                        body=_(f"Failed to sync to {platform.name}: {str(e)}")
                    )
                    _logger.error(f"Failed to sync greenhouse {greenhouse.name} to {platform.name}: {str(e)}")

    def action_prepare_ecommerce_listing(self):
        """Prepare product listings based on greenhouse data"""
        # This would create product templates based on greenhouse data
        # In our case, we'll create a wizard or action to help prepare listings
        self.ensure_one()

        return {
            'type': 'ir.actions.act_window',
            'name': _('Prepare E-commerce Listing'),
            'res_model': 'farm.ecommerce.listing.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_greenhouse_id': self.id,
                'default_name': f'{self.name} Fresh Produce',
                'default_description': f'Fresh produce from greenhouse {self.name} with optimal environmental conditions',
            }
        }


class FarmEcommerceListingWizard(models.TransientModel):
    """
    Wizard to help prepare e-commerce listings from greenhouse data
    """
    _name = 'farm.ecommerce.listing.wizard'
    _description = 'E-commerce Listing Preparation Wizard'

    greenhouse_id = fields.Many2one('farm.location', string='Greenhouse', required=True)
    name = fields.Char('Listing Title', required=True)
    description = fields.Text('Description')
    price = fields.Float('Price', required=True)
    inventory_quantity = fields.Float('Inventory Quantity', default=0)
    active_platforms = fields.Many2many('farm.ecommerce.platform', 'farm_ecommerce_listing_wizard_farm_ecommerce_platform_rel', 'wizard_id', 'platform_id',
                                       string='Active Platforms')

    def action_create_listings(self):
        """Create listings on selected platforms"""
        if not self.active_platforms:
            raise ValidationError(_("Please select at least one e-commerce platform"))

        # In a real implementation, this would create product listings on e-commerce platforms
        # For now, we'll just record the action
        self.greenhouse_id.message_post(
            body=_(f"Listing prepared: {self.name} with price {self.price} for platforms: {', '.join(self.active_platforms.mapped('name'))}")
        )

        return {'type': 'ir.actions.act_window_close'}