from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class SafePODConfiguration(models.Model):
    """
    安全交付确认(Safe POD)配置 [US-09-17]
    """
    _name = 'safe.pod.configuration'
    _description = 'Safe POD Configuration for Delivery Confirmation'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('POD Configuration Name', required=True, default=lambda self: _('New'))
    delivery_checklist_template = fields.Text('Delivery Confirmation Checklist Template',
                                             help='Template for delivery confirmation checklist that will be auto-populated for each delivery')
    temperature_monitoring_required = fields.Boolean('Temperature Monitoring Required',
                                                   help='Whether temperature monitoring is required for this delivery type')
    requires_photo_confirmation = fields.Boolean('Requires Photo Confirmation', default=True)
    requires_signature_confirmation = fields.Boolean('Requires Signature Confirmation', default=True)
    requires_id_verification = fields.Boolean('Requires ID Verification', default=False)
    requires_temperature_logs = fields.Boolean('Requires Temperature Logs', default=False)
    auto_generate_checklist = fields.Boolean('Auto Generate Checklist', default=True)
    checklist_items = fields.Text('Checklist Items',
                                 help='List of items that need to be confirmed during delivery, separated by newlines')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('safe.pod.configuration') or '/'
        return super().create(vals)


class DeliveryTrackingRecord(models.Model):
    """
    交付跟踪记录 [US-09-17]
    """
    _name = 'delivery.tracking.record'
    _description = 'Delivery Tracking Record with POD Confirmation'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Delivery Record Name', required=True, default=lambda self: _('New'))
    delivery_order_id = fields.Many2one('stock.picking', string='Delivery Order', required=True)
    pod_config_id = fields.Many2one('safe.pod.configuration', string='POD Configuration', required=True)
    transporter_id = fields.Many2one('res.partner', string='Transporter',
                                     domain=[('is_company', '=', True), ('supplier_rank', '>', 0)])
    delivery_status = fields.Selection([
        ('pending', 'Pending'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('confirmed', 'Confirmed (POD Signed)'),
        ('exception', 'Exception'),
    ], string='Delivery Status', default='pending', required=True)
    delivered_datetime = fields.Datetime('Delivered Date & Time')
    pod_confirmed_datetime = fields.Datetime('POD Confirmed Date & Time')
    is_pod_confirmed = fields.Boolean('Is POD Confirmed', default=False)
    pod_confirmation_image = fields.Binary('POD Confirmation Image')
    pod_confirmation_filename = fields.Char('POD Confirmation Filename')
    delivered_by_signature = fields.Char('Delivered By (Signature)')
    received_by_signature = fields.Char('Received By (Signature)')
    temperature_logs = fields.Text('Temperature Logs', help='Temperature logs during delivery if required')
    delivery_notes = fields.Text('Delivery Notes')
    confirmation_checklist = fields.Text('Confirmation Checklist',
                                        help='Auto-generated checklist based on POD configuration')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('delivery.tracking.record') or '/'
        return super().create(vals)

    def action_confirm_pod(self):
        """Confirm POD with all required elements based on configuration"""
        for record in self:
            # Check if all required confirmations are provided based on POD config
            pod_config = record.pod_config_id
            errors = []

            if pod_config.requires_signature_confirmation and not record.received_by_signature:
                errors.append("Received by signature is required but not provided")
            if pod_config.requires_photo_confirmation and not record.pod_confirmation_image:
                errors.append("POD confirmation image is required but not provided")
            if pod_config.temperature_monitoring_required and not record.temperature_logs:
                errors.append("Temperature logs are required but not provided")

            if errors:
                raise ValidationError(_("Missing required POD confirmations:\n") + "\n".join(errors))

            # If all validations pass, confirm the POD
            record.write({
                'is_pod_confirmed': True,
                'pod_confirmed_datetime': fields.Datetime.now(),
                'delivery_status': 'confirmed'
            })

            # Add a message to the chatter
            record.message_post(
                body=_("POD confirmed by %s at %s") % (record.received_by_signature or 'N/A', fields.Datetime.now())
            )

    def action_delivered(self):
        """Mark as delivered (before POD confirmation)"""
        self.write({
            'delivered_datetime': fields.Datetime.now(),
            'delivery_status': 'delivered'
        })

    def action_upload_pod_image(self, image_data, filename):
        """Upload POD confirmation image"""
        self.write({
            'pod_confirmation_image': image_data,
            'pod_confirmation_filename': filename
        })


