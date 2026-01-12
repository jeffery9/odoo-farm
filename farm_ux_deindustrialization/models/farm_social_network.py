from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class FarmSocialNetwork(models.Model):
    """
    农场社交网络 [US-16-08]
    """
    _name = 'farm.social.network'
    _description = 'Farm Social Network & Collaboration Platform'

    name = fields.Char('Network Name', required=True, translate=True)
    network_type = fields.Selection([
        ('coop_members', 'Cooperative Members'),
        ('regional_farmers', 'Regional Farmers'),
        ('specialty_crops', 'Specialty Crops'),
        ('knowledge_sharing', 'Knowledge Sharing'),
        ('resource_sharing', 'Resource Sharing'),
    ], string='Network Type', required=True)
    member_ids = fields.Many2many('res.partner', string='Members')
    admin_ids = fields.Many2many('res.users', string='Administrators')
    description = fields.Text('Description', translate=True)
    is_active = fields.Boolean('Is Active', default=True)
    created_by = fields.Many2one('res.users', string='Created By', default=lambda self: self.env.user)
    created_date = fields.Datetime('Created Date', default=fields.Datetime.now)
    privacy_level = fields.Selection([
        ('public', 'Public'),
        ('private', 'Private'),
        ('invite_only', 'Invite Only'),
    ], string='Privacy Level', default='private')
    message_board = fields.Text('Message Board', help='Public message board content')
    shared_resources = fields.Text('Shared Resources', help='Shared resources and experiences')