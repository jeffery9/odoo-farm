from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class AgriHazardousWasteRecord(models.Model):
    """
    US-057-03: 危险废弃物（药瓶/地膜）合规处置
    Model for hazardous waste tracking and compliance
    """
    _name = 'agri.hazardous.waste.record'
    _description = 'Agricultural Hazardous Waste Record'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Hazardous Waste Record', required=True, copy=False)
    waste_type = fields.Selection([
        ('pesticide_container', 'Pesticide Container'),
        ('fertilizer_bag', 'Fertilizer Bag'),
        ('plastic_film', 'Plastic Film/Mulch'),
        ('battery', 'Battery'),
        ('oil', 'Used Oil'),
        ('other', 'Other'),
    ], string='Waste Type', required=True)

    # Waste details
    description = fields.Text('Waste Description')
    quantity = fields.Float('Quantity', required=True)
    unit_uom = fields.Many2one('uom.uom', string='Unit of Measure', required=True)

    # Collection and handling
    collection_date = fields.Date('Collection Date', required=True, default=fields.Date.context_today)
    collection_location_id = fields.Many2one('farm.location', string='Collection Location')
    collected_by = fields.Many2one('res.users', string='Collected By', default=lambda self: self.env.user)

    # Transfer details (Waste Transfer Manifest)
    transfer_to_partner = fields.Many2one('res.partner', string='Transferred To (Waste Handler)')
    transfer_date = fields.Date('Transfer Date')
    transfer_manifest_number = fields.Char('Transfer Manifest Number')
    transfer_weight = fields.Float('Transfer Weight (kg)')

    # Compliance and audit trail
    compliance_status = fields.Selection([
        ('pending', 'Pending'),
        ('in_transit', 'In Transit'),
        ('disposed', 'Disposed'),
        ('non_compliant', 'Non-Compliant'),
    ], string='Compliance Status', default='pending', required=True)

    # Regulatory compliance
    regulatory_reference = fields.Char('Regulatory Reference')
    disposal_method = fields.Selection([
        ('incineration', 'Incineration'),
        ('landfill', 'Licensed Landfill'),
        ('recycling', 'Specialized Recycling'),
        ('chemical_treatment', 'Chemical Treatment'),
    ], string='Disposal Method')

    # Compliance documentation
    disposal_certificate = fields.Binary('Disposal Certificate', attachment=True)
    disposal_certificate_name = fields.Char('Certificate Name')

    # Reporting for audit
    audit_trail = fields.Text('Audit Trail', compute='_compute_audit_trail')

    # Related to circular economy
    related_circular_flow_id = fields.Many2one('agri.sustainability.circular.flow',
                                               string='Related Circular Flow')

    @api.constrains('quantity')
    def _check_positive_quantity(self):
        for record in self:
            if record.quantity <= 0:
                raise ValidationError(_("Quantity must be positive."))

    def _compute_audit_trail(self):
        """Generate audit trail for compliance reporting"""
        for record in self:
            audit_info = f"""
            Hazardous Waste Record: {record.name}
            Waste Type: {dict(record._fields['waste_type'].selection).get(record.waste_type, record.waste_type)}
            Collection Date: {record.collection_date}
            Collected By: {record.collected_by.name if record.collected_by else 'N/A'}
            Collection Location: {record.collection_location_id.name if record.collection_location_id else 'N/A'}

            Transfer Information:
            - Transferred To: {record.transfer_to_partner.name if record.transfer_to_partner else 'Not Transferred'}
            - Transfer Date: {record.transfer_date or 'N/A'}
            - Manifest Number: {record.transfer_manifest_number or 'N/A'}
            - Transfer Weight: {record.transfer_weight or 0} kg
            - Disposal Method: {dict(record._fields['disposal_method'].selection).get(record.disposal_method, record.disposal_method) or 'N/A'}

            Compliance Status: {dict(record._fields['compliance_status'].selection).get(record.compliance_status, record.compliance_status)}
            """
            record.audit_trail = audit_info

    def action_generate_compliance_report(self):
        """Generate compliance report for regulatory requirements"""
        return {
            'type': 'ir.actions.act_window',
            'name': _('Hazardous Waste Compliance Report'),
            'res_model': 'agri.hazardous.waste.record',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
            'context': self.env.context,
        }

    def action_transfer_waste(self):
        """Mark waste as transferred to handler"""
        for record in self:
            record.compliance_status = 'in_transit'
            record.transfer_date = fields.Date.context_today(record)
            record.message_post(body=_("Hazardous waste transferred to %s") %
                              (record.transfer_to_partner.name if record.transfer_to_partner else 'handler'))

    def action_mark_disposed(self):
        """Mark waste as properly disposed"""
        for record in self:
            record.compliance_status = 'disposed'
            record.message_post(body=_("Hazardous waste properly disposed through %s") %
                              (dict(record._fields['disposal_method'].selection).get(record.disposal_method, record.disposal_method) or 'method'))


class AgriHazardousWasteComplianceReport(models.TransientModel):
    """
    Report model for hazardous waste compliance - supports "一键导出" requirement
    """
    _name = 'agri.hazardous.waste.compliance.report'
    _description = 'Hazardous Waste Compliance Report Generator'

    date_from = fields.Date('Date From', required=True, default=lambda self: fields.Date.context_today(self))
    date_to = fields.Date('Date To', required=True, default=lambda self: fields.Date.context_today(self))
    location_ids = fields.Many2many('farm.location', 'agri_hazardous_waste_compliance_report_farm_location_rel', 'report_id', 'location_id', string='Locations')
    waste_type = fields.Selection([
        ('pesticide_container', 'Pesticide Container'),
        ('fertilizer_bag', 'Fertilizer Bag'),
        ('plastic_film', 'Plastic Film/Mulch'),
        ('battery', 'Battery'),
        ('oil', 'Used Oil'),
        ('other', 'Other'),
        ('all', 'All Types'),
    ], string='Waste Type', default='all')

    def action_generate_report(self):
        """Generate and export compliance report"""
        domain = [
            ('collection_date', '>=', self.date_from),
            ('collection_date', '<=', self.date_to),
        ]

        if self.location_ids:
            domain.append(('collection_location_id', 'in', self.location_ids.ids))

        if self.waste_type and self.waste_type != 'all':
            domain.append(('waste_type', '=', self.waste_type))

        records = self.env['agri.hazardous.waste.record'].search(domain)

        # Generate report content
        report_content = f"""
        危险废弃物处置台账 (Hazardous Waste Disposal Ledger)
        Period: {self.date_from} to {self.date_to}
        Generated: {fields.Datetime.context_timestamp(self, fields.Datetime.now())}

        Total Records: {len(records)}
        """

        total_quantity = sum(record.quantity for record in records if record.quantity)
        report_content += f"\nTotal Waste Quantity: {total_quantity} {records[0].unit_uom.name if records else 'units'}\n\n"

        for record in records:
            report_content += f"""
            Record: {record.name}
            Type: {dict(record._fields['waste_type'].selection).get(record.waste_type, record.waste_type)}
            Location: {record.collection_location_id.name if record.collection_location_id else 'N/A'}
            Date: {record.collection_date}
            Status: {dict(record._fields['compliance_status'].selection).get(record.compliance_status, record.compliance_status)}
            Transferred To: {record.transfer_to_partner.name if record.transfer_to_partner else 'N/A'}
            Disposal Method: {dict(record._fields['disposal_method'].selection).get(record.disposal_method, record.disposal_method) or 'N/A'}

            """

        # Return report data (in real implementation, would export PDF/Excel)
        return {
            'type': 'ir.actions.act_window',
            'name': _('Hazardous Waste Compliance Report'),
            'res_model': 'agri.hazardous.waste.compliance.report',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_report_content': report_content,
                'default_report_title': f'危废处置台账_{self.date_from}_{self.date_to}'
            },
        }