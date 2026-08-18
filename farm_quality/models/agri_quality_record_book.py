# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import hashlib
import json

class AgriQualityRecordBook(models.Model):
    """
    [GxP Compliance Layer] Agricultural Quality Record Book.
    Aggregates quality checks into an immutable, cryptographically signed ledger.
    """
    _name = 'agri.quality.record.book'
    _description = 'Agricultural Quality Record Book'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Record Book Name", required=True, tracking=True)
    code = fields.Char("Reference Code", required=True, readonly=True, copy=False, default=lambda self: _('New'))
    book_type = fields.Selection([
        ('general', 'General Quality Log'),
        ('pesticide', 'Pesticide Application Log'),
        ('fertilizer', 'Fertilization Log'),
        ('haccp', 'HACCP Monitoring Log'),
        ('lims', 'LIMS Laboratory Log')
    ], string="Type", default='general', required=True, tracking=True)

    date_start = fields.Date("Start Date", required=True, default=fields.Date.context_today)
    date_end = fields.Date("End Date")
    
    user_id = fields.Many2one('res.users', string="Responsible Inspector", default=lambda self: self.env.user, tracking=True)
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company, required=True)
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('locked', 'Locked & Signed (GxP)')
    ], string="State", default='draft', required=True, tracking=True)
    
    check_ids = fields.One2many('agri.quality.check', 'record_book_id', string="Quality Records")
    template_id = fields.Many2one('agri.quality.record.book.template', string="Record Book Template", tracking=True)
    
    # GxP Cryptographic Anti-Tampering [US-GxP-01]
    cryptographic_signature = fields.Char("Merkle Root / Book Signature", readonly=True, copy=False)
    signature_date = fields.Datetime("Signature Timestamp", readonly=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('code', _('New')) == _('New'):
                vals['code'] = self.env['ir.sequence'].next_by_code('agri.quality.record.book') or _('RB')
        return super().create(vals_list)

    def action_activate(self):
        self.ensure_one()
        if self.state == 'draft':
            self.write({'state': 'active'})

    def action_lock(self):
        """ Lock the record book and calculate cryptographic SHA-256 signature (GxP Auditing) """
        self.ensure_one()
        if self.state != 'active':
            raise UserError(_("Only active record books can be locked and signed."))
            
        # Collect and canonicalize all checks inside this book
        records_payload = []
        for check in self.check_ids:
            records_payload.append({
                'id': check.id,
                'name': check.name or '',
                'lot': check.lot_id.name or '',
                'point': check.point_id.name or '',
                'state': check.quality_state or '',
                'measure': check.measure or 0.0,
                'blockchain_hash': check.blockchain_hash or ''
            })
            
        # Serialize to JSON and compute SHA-256 as the Record Book signature
        payload_str = json.dumps(records_payload, sort_keys=True)
        book_hash = hashlib.sha256(payload_str.encode('utf-8')).hexdigest()
        
        self.write({
            'state': 'locked',
            'cryptographic_signature': book_hash,
            'signature_date': fields.Datetime.now()
        })
        self.message_post(body=_("<b>GxP Audit Alert:</b> Record Book locked and sealed with Cryptographic Signature:<br/><code>%s</code>") % book_hash)

    def write(self, vals):
        for rec in self:
            if rec.state == 'locked' and any(f not in ['message_follower_ids', 'activity_ids'] for f in vals):
                raise UserError(_("GxP ANTI-TAMPERING: Locked record books cannot be modified."))
        return super().write(vals)

    def unlink(self):
        for rec in self:
            if rec.state == 'locked':
                raise UserError(_("GxP ANTI-TAMPERING: Locked record books cannot be deleted."))
        return super().unlink()

    def action_generate_from_template(self):
        """ Generate quality check records from the linked template """
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_("You can only generate records from a template in Draft state."))
        if not self.template_id:
            raise UserError(_("Please select a template first."))
            
        checks_vals = []
        for line in self.template_id.line_ids:
            checks_vals.append({
                'name': line.name,
                'point_id': line.point_id.id if line.point_id else False,
                'record_book_id': self.id,
                'instruction': line.instruction or '',
                'quality_state': 'none',
            })
            
        if checks_vals:
            self.env['agri.quality.check'].create(checks_vals)
            
        self.message_post(body=_("Successfully generated %s quality check records from template: <b>%s</b>") % (len(checks_vals), self.template_id.name))

class AgriQualityRecordBookTemplate(models.Model):
    _name = 'agri.quality.record.book.template'
    _description = 'Agricultural Quality Record Book Template'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Template Name", required=True, tracking=True)
    book_type = fields.Selection([
        ('general', 'General Quality Log'),
        ('pesticide', 'Pesticide Application Log'),
        ('fertilizer', 'Fertilization Log'),
        ('haccp', 'HACCP Monitoring Log'),
        ('lims', 'LIMS Laboratory Log')
    ], string="Type", default='general', required=True, tracking=True)
    description = fields.Text("Description/Objective")
    active = fields.Boolean("Active", default=True)
    line_ids = fields.One2many('agri.quality.record.book.template.line', 'template_id', string="Instruction Lines", copy=True)

class AgriQualityRecordBookTemplateLine(models.Model):
    _name = 'agri.quality.record.book.template.line'
    _description = 'Quality Record Book Template Line'
    _order = 'sequence, id'

    template_id = fields.Many2one('agri.quality.record.book.template', string="Template", required=True, ondelete='cascade')
    sequence = fields.Integer("Sequence", default=10)
    name = fields.Char("Instruction Step/Name", required=True)
    point_id = fields.Many2one('agri.quality.point', string="Target Quality Point")
    instruction = fields.Text("Inspection/Filling Instructions")
