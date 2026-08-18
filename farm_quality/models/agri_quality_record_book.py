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
                'template_line_id': line.id,
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

    def action_open_spc_wizard(self):
        """ Opens the SPC Analysis Wizard for this line """
        self.ensure_one()
        wizard = self.env['agri.quality.spc.wizard'].create({
            'template_line_id': self.id,
        })
        try:
            wizard.action_calculate()
        except UserError:
            pass
            
        return {
            'name': _('SPC Process Control Analysis'),
            'type': 'ir.actions.act_window',
            'res_model': 'agri.quality.spc.wizard',
            'res_id': wizard.id,
            'view_mode': 'form',
            'target': 'new',
        }

class AgriQualitySpcWizard(models.TransientModel):
    _name = 'agri.quality.spc.wizard'
    _description = 'SPC Statistical Process Control Wizard'

    template_line_id = fields.Many2one('agri.quality.record.book.template.line', string="Inspection Step/Line", required=True)
    date_from = fields.Date("From Date")
    date_to = fields.Date("To Date")

    sample_count = fields.Integer("Sample Count (N)", readonly=True)
    mean_val = fields.Float("Process Mean (X-bar)", digits=(16, 4), readonly=True)
    max_val = fields.Float("Maximum Value", digits=(16, 4), readonly=True)
    min_val = fields.Float("Minimum Value", digits=(16, 4), readonly=True)
    std_dev = fields.Float("Standard Deviation (Sigma)", digits=(16, 4), readonly=True)
    ucl = fields.Float("Upper Control Limit (UCL)", digits=(16, 4), readonly=True)
    lcl = fields.Float("Lower Control Limit (LCL)", digits=(16, 4), readonly=True)
    
    cp = fields.Float("Process Capability (Cp)", digits=(16, 4), readonly=True)
    cpk = fields.Float("Process Capability Index (Cpk)", digits=(16, 4), readonly=True)
    cpk_status = fields.Char("Capability Evaluation", readonly=True)

    spc_chart_ascii = fields.Text("ASCII Run & Control Chart", readonly=True)

    def action_calculate(self):
        self.ensure_one()
        domain = [
            ('template_line_id', '=', self.template_line_id.id),
            ('quality_state', 'in', ['pass', 'fail']),
            ('test_type', '=', 'measure')
        ]
        if self.date_from:
            domain.append(('create_date', '>=', self.date_from))
        if self.date_to:
            domain.append(('create_date', '<=', self.date_to))
            
        checks = self.env['agri.quality.check'].search(domain, order='create_date asc')
        measures = [c.measure for c in checks if c.measure is not None]
        
        N = len(measures)
        self.sample_count = N
        if N < 2:
            raise UserError(_("SPC analysis requires at least 2 historical measurement records. Found %s.") % N)
            
        mean = sum(measures) / N
        max_v = max(measures)
        min_v = min(measures)
        
        variance = sum((x - mean) ** 2 for x in measures) / (N - 1)
        sigma = math.sqrt(variance)
        
        ucl = mean + 3 * sigma
        lcl = mean - 3 * sigma
        
        point = self.template_line_id.point_id
        cp, cpk, cpk_status = 0.0, 0.0, _('N/A - Tolerance Limits Not Defined')
        if point and point.test_type == 'measure' and point.tolerance_max > point.tolerance_min:
            usl = point.tolerance_max
            lsl = point.tolerance_min
            if sigma > 0:
                cp = (usl - lsl) / (6 * sigma)
                cpk = min((usl - mean) / (3 * sigma), (mean - lsl) / (3 * sigma))
                if cpk >= 1.33:
                    cpk_status = _("Excellent (Process is highly capable)")
                elif cpk >= 1.0:
                    cpk_status = _("Acceptable (Process is capable)")
                elif cpk >= 0.67:
                    cpk_status = _("Marginal (Barely capable, monitor closely)")
                else:
                    cpk_status = _("Unacceptable (Process is out of control)")
            else:
                cpk_status = _("Undetermined (Sigma is 0)")
        
        C = min(N, 15)
        measures_subset = measures[-C:]
        
        y_max = max(max(measures_subset), ucl)
        y_min = min(min(measures_subset), lcl)
        y_padding = (y_max - y_min) * 0.05 if y_max > y_min else 1.0
        y_max += y_padding
        y_min -= y_padding
        y_range = y_max - y_min if y_max > y_min else 1.0
        
        ucl_row = int(round((ucl - y_min) / y_range * 9)) if y_range > 0 else 9
        mean_row = int(round((mean - y_min) / y_range * 9)) if y_range > 0 else 5
        lcl_row = int(round((lcl - y_min) / y_range * 9)) if y_range > 0 else 0
        
        chart_lines = []
        for r in range(9, -1, -1):
            row_val = y_min + (r / 9.0) * y_range if y_range > 0 else y_min
            if r == ucl_row:
                label = "UCL  "
            elif r == mean_row:
                label = "Mean "
            elif r == lcl_row:
                label = "LCL  "
            else:
                label = "     "
            line_chars = []
            for c in range(C):
                v = measures_subset[c]
                point_row = int(round((v - y_min) / y_range * 9)) if y_range > 0 else 5
                if point_row == r:
                    line_chars.append('*')
                elif r == ucl_row:
                    line_chars.append('⠤')
                elif r == mean_row:
                    line_chars.append('─')
                elif r == lcl_row:
                    line_chars.append('⠤')
                else:
                    line_chars.append(' ')
            row_str = f"{label}│ {'  '.join(line_chars)}"
            if r == ucl_row:
                row_str += f"  (UCL: {ucl:.4f})"
            elif r == mean_row:
                row_str += f"  (Mean: {mean:.4f})"
            elif r == lcl_row:
                row_str += f"  (LCL: {lcl:.4f})"
            else:
                row_str += f"   [{row_val:.4f}]"
            chart_lines.append(row_str)
            
        axis_line = "     └─" + "──" * (3 * C - 2)
        chart_lines.append(axis_line)
        sample_labels = "       " + "  ".join(f"{i+1}" for i in range(C))
        chart_lines.append(sample_labels)
        
        chart_text = "\n".join(chart_lines)
        
        self.write({
            'mean_val': mean,
            'max_val': max_v,
            'min_val': min_v,
            'std_dev': sigma,
            'ucl': ucl,
            'lcl': lcl,
            'cp': cp,
            'cpk': cpk,
            'cpk_status': cpk_status,
            'spc_chart_ascii': chart_text
        })
        
        return {
            'name': _('SPC Analysis Results'),
            'type': 'ir.actions.act_window',
            'res_model': 'agri.quality.spc.wizard',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }
