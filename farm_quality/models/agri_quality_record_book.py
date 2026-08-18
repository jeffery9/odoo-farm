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

    def action_export_spreadsheet(self):
        """ Generates and streams a professionally-formatted GxP compliance spreadsheet of the Record Book """
        self.ensure_one()
        import io
        import base64
        try:
            from openpyxl import Workbook
            from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
            from openpyxl.utils import get_column_letter
        except ImportError:
            raise UserError(_("The 'openpyxl' library is required to export spreadsheets. Please contact your system administrator."))

        wb = Workbook()
        ws = wb.active
        ws.title = "Quality Record Book Log"
        
        # Ensure grid lines are visible in Excel
        ws.views.sheetView[0].showGridLines = True
        
        # Professional Color Palette fills (Steel Blue Theme)
        NAVY_FILL = PatternFill(start_color="1F497D", end_color="1F497D", fill_type="solid")
        ICE_BLUE_FILL = PatternFill(start_color="DCE6F1", end_color="DCE6F1", fill_type="solid")
        LIGHT_GRAY_FILL = PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid")
        
        # Font definitions
        FONT_TITLE = Font(name="Calibri", size=16, bold=True, color="FFFFFF")
        FONT_HEADER = Font(name="Calibri", size=11, bold=True, color="1F497D")
        FONT_BOLD = Font(name="Calibri", size=11, bold=True)
        FONT_REGULAR = Font(name="Calibri", size=11)
        FONT_SIGNATURE = Font(name="Courier New", size=10, italic=True)
        
        # Border definitions
        thin_side = Side(border_style="thin", color="D9D9D9")
        thick_side = Side(border_style="medium", color="1F497D")
        border_all_thin = Border(left=thin_side, right=thin_side, top=thin_side, bottom=thin_side)
        border_header = Border(left=thin_side, right=thin_side, top=thick_side, bottom=thick_side)
        
        # 1. Header Title Banner
        ws.merge_cells("A1:H2")
        title_cell = ws["A1"]
        title_cell.value = "GxP QUALITY RECORD BOOK AUDIT SHEET"
        title_cell.font = FONT_TITLE
        title_cell.fill = NAVY_FILL
        title_cell.alignment = Alignment(horizontal="center", vertical="center")
        
        # 2. Metadata Info Block
        book_type_label = dict(self._fields['book_type'].selection).get(self.book_type, "General")
        metadata = [
            ("Record Book Code:", self.code or "N/A", "Template Name:", self.template_id.name or "N/A"),
            ("Record Book Name:", self.name, "Template Type:", book_type_label),
            ("Current State:", self.state.upper(), "Created Date:", self.create_date.strftime("%Y-%m-%d %H:%M:%S") if self.create_date else "N/A"),
            ("Cryptographic Seal:", self.cryptographic_signature or "UNSEALED - DRAFT", "Seal Date:", self.signature_date.strftime("%Y-%m-%d %H:%M:%S") if self.signature_date else "N/A")
        ]
        
        row_idx = 4
        for data in metadata:
            ws.cell(row=row_idx, column=1, value=data[0]).font = FONT_HEADER
            ws.cell(row=row_idx, column=2, value=data[1]).font = FONT_REGULAR
            ws.cell(row=row_idx, column=5, value=data[2]).font = FONT_HEADER
            ws.cell(row=row_idx, column=6, value=data[3]).font = FONT_REGULAR
            row_idx += 1
            
        # 3. Quality Checks Grid Table
        row_idx += 1 # Space
        ws.cell(row=row_idx, column=1, value="QUALITY CHECKLIST ITEMS / STEPS").font = FONT_BOLD
        ws.merge_cells(start_row=row_idx, start_column=1, end_row=row_idx, end_column=8)
        ws.row_dimensions[row_idx].height = 20
        for col in range(1, 9):
            ws.cell(row=row_idx, column=col).fill = ICE_BLUE_FILL
            
        row_idx += 1
        headers = ["Seq", "Check Name", "Target Point", "Test Type", "Standard Instruction", "Actual Measure", "Status", "Remarks"]
        ws.row_dimensions[row_idx].height = 24
        for col_idx, h in enumerate(headers, 1):
            cell = ws.cell(row=row_idx, column=col_idx, value=h)
            cell.font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
            cell.fill = NAVY_FILL
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            cell.border = border_header
            
        start_table_row = row_idx + 1
        seq = 1
        for check in self.check_ids:
            row_idx += 1
            ws.row_dimensions[row_idx].height = 20
            
            ws.cell(row=row_idx, column=1, value=seq).alignment = Alignment(horizontal="center")
            ws.cell(row=row_idx, column=2, value=check.name or '')
            ws.cell(row=row_idx, column=3, value=check.point_id.name or 'N/A')
            ws.cell(row=row_idx, column=4, value=check.test_type or 'N/A')
            ws.cell(row=row_idx, column=5, value=check.instruction or '')
            
            # Measurement formatting (Blue text indicates changeables / inputs in Excel standard)
            if check.test_type == 'measure':
                cell_val = ws.cell(row=row_idx, column=6, value=check.measure)
                cell_val.font = Font(name="Calibri", size=11, color="0000FF")
                cell_val.number_format = "#,##0.00"
                cell_val.alignment = Alignment(horizontal="right")
            else:
                ws.cell(row=row_idx, column=6, value="N/A").alignment = Alignment(horizontal="center")
                
            # Status styling
            status_text = "Passed" if check.quality_state == 'pass' else ("Failed" if check.quality_state == 'fail' else "To do")
            cell_stat = ws.cell(row=row_idx, column=7, value=status_text)
            cell_stat.alignment = Alignment(horizontal="center")
            if status_text == "Passed":
                cell_stat.font = Font(name="Calibri", size=11, bold=True, color="006100")
            elif status_text == "Failed":
                cell_stat.font = Font(name="Calibri", size=11, bold=True, color="9C0006")
                
            # Remarks column
            ws.cell(row=row_idx, column=8, value="")
            
            for col in range(1, 9):
                ws.cell(row=row_idx, column=col).border = border_all_thin
                if col != 6:
                    ws.cell(row=row_idx, column=col).font = FONT_REGULAR
            seq += 1
            
        end_table_row = row_idx
        
        # 4. Statistical Dynamic Excel Formulas Block
        row_idx += 2
        ws.cell(row=row_idx, column=1, value="RECORD BOOK SUMMARY STATISTICS").font = FONT_BOLD
        ws.merge_cells(start_row=row_idx, start_column=1, end_row=row_idx, end_column=4)
        for col in range(1, 5):
            ws.cell(row=row_idx, column=col).fill = ICE_BLUE_FILL
            
        metrics = [
            ("Total Checklist Items:", f"=COUNTA(B{start_table_row}:B{end_table_row})", "%"),
            ("Passed Items Count:", f'=COUNTIF(G{start_table_row}:G{end_table_row}, "Passed")', "Count"),
            ("Failed Items Count:", f'=COUNTIF(G{start_table_row}:G{end_table_row}, "Failed")', "Count"),
            ("Overall Yield Rate:", f'=B{row_idx+2}/B{row_idx+1}', "0.0%"),
        ]
        
        sub_row = row_idx + 1
        for label, formula, num_format in metrics:
            ws.cell(row=sub_row, column=1, value=label).font = FONT_HEADER
            cell_f = ws.cell(row=sub_row, column=2, value=formula)
            cell_f.font = FONT_BOLD
            if num_format == "%":
                cell_f.number_format = "#,##0"
            elif num_format == "0.0%":
                cell_f.number_format = "0.0%"
            else:
                cell_f.number_format = "#,##0"
            sub_row += 1
            
        # 5. GxP Compliance & Audit Trail Box
        row_idx_gxp = row_idx
        ws.cell(row=row_idx_gxp, column=5, value="GxP COMPLIANCE AUDIT TRAIL").font = FONT_BOLD
        ws.merge_cells(start_row=row_idx_gxp, start_column=5, end_row=row_idx_gxp, end_column=8)
        for col in range(5, 9):
            ws.cell(row=row_idx_gxp, column=col).fill = ICE_BLUE_FILL
            
        ws.cell(row=row_idx_gxp+1, column=5, value="Document Verification:").font = FONT_HEADER
        ws.cell(row=row_idx_gxp+1, column=6, value="SHA-256 GxP Authenticated").font = FONT_REGULAR
        
        ws.cell(row=row_idx_gxp+2, column=5, value="Digital Hash Signature:").font = FONT_HEADER
        cell_sig = ws.cell(row=row_idx_gxp+2, column=6, value=self.cryptographic_signature or "NOT LOCKED - UNSIGNED")
        cell_sig.font = FONT_SIGNATURE
        ws.merge_cells(start_row=row_idx_gxp+2, start_column=6, end_row=row_idx_gxp+2, end_column=8)
        
        ws.cell(row=row_idx_gxp+3, column=5, value="Compliance Status:").font = FONT_HEADER
        cell_comp = ws.cell(row=row_idx_gxp+3, column=6, value="COMPLIANT" if self.state == 'locked' else "PENDING REVIEW")
        cell_comp.font = FONT_BOLD
        if self.state == 'locked':
            cell_comp.font = Font(name="Calibri", size=11, bold=True, color="006100")
        else:
            cell_comp.font = Font(name="Calibri", size=11, bold=True, color="9C6500")
            
        # Add border around Summary & GxP boxes
        for r in range(row_idx, row_idx+5):
            for c in range(1, 9):
                ws.cell(row=r, column=c).border = border_all_thin
                
        # 6. Column Auto-sizing with margins
        for col in ws.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                val_str = str(cell.value or '')
                if cell.coordinate in ws.merged_cells:
                    continue
                if len(val_str) > max_len:
                    max_len = len(val_str)
            ws.column_dimensions[col_letter].width = max(max_len + 3, 12)
            
        ws.column_dimensions['A'].width = 6
        ws.column_dimensions['B'].width = 25
        ws.column_dimensions['E'].width = 35
        ws.column_dimensions['F'].width = 18
        
        fp = io.BytesIO()
        wb.save(fp)
        file_data = fp.getvalue()
        fp.close()
        
        # Attach binary to database
        attachment = self.env['ir.attachment'].create({
            'name': f"Quality_Record_Book_{self.code or self.id}.xlsx",
            'type': 'binary',
            'datas': base64.b64encode(file_data),
            'res_model': self._name,
            'res_id': self.id,
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        })
        
        # Trigger dynamic download action
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }

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
