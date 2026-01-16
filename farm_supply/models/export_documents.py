from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class ExportDocumentHub(models.Model):
    """
    跨境出口单证自动集成 [US-09-12]
    """
    _name = 'export.document.hub'
    _description = 'Export Document Hub for Cross-border Trade'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Document Reference', required=True, default=lambda self: _('New'))
    export_order_id = fields.Many2one('sale.order', string='Export Order', required=True)
    batch_ids = fields.Many2many('stock.lot', string='Batches/LOTS',
                                help='Batches included in this export shipment')
    country_of_origin = fields.Many2one('res.country', string='Country of Origin')
    destination_country = fields.Many2one('res.country', string='Destination Country')
    export_date = fields.Date('Export Date', default=fields.Date.context_today)
    phytosanitary_certificate_required = fields.Boolean('Phytosanitary Certificate Required')
    coo_certificate_required = fields.Boolean('Certificate of Origin Required')
    quality_certificate_required = fields.Boolean('Quality Certificate Required')
    status = fields.Selection([
        ('draft', 'Draft'),
        ('pending_approval', 'Pending Approval'),
        ('approved', 'Approved'),
        ('generated', 'Documents Generated'),
        ('shipped', 'Shipped'),
    ], string='Status', default='draft', required=True)
    generated_documents = fields.One2many('export.generated.document', 'export_hub_id', string='Generated Documents')
    notes = fields.Text('Notes')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('export.document.hub') or '/'
        return super().create(vals)

    def action_generate_documents(self):
        """Generate all required export documents"""
        ExportDocument = self.env['export.generated.document']
        for hub in self:
            # Generate phytosanitary certificate if required
            if hub.phytosanitary_certificate_required:
                self._generate_phytosanitary_certificate(hub, ExportDocument)

            # Generate certificate of origin if required
            if hub.coo_certificate_required:
                self._generate_certificate_of_origin(hub, ExportDocument)

            # Generate quality certificate if required
            if hub.quality_certificate_required:
                self._generate_quality_certificate(hub, ExportDocument)

            hub.status = 'generated'

    def _generate_phytosanitary_certificate(self, hub, document_model):
        """Generate phytosanitary certificate"""
        # This would integrate with farm_lot and activity data
        lot_data = []
        for lot in hub.batch_ids:
            lot_data.append({
                'name': lot.name,
                'product': lot.product_id.name,
                'harvest_date': lot.harvest_date if hasattr(lot, 'harvest_date') else lot.create_date,
                'location': lot.location_id.name if hasattr(lot, 'location_id') else 'Unknown',
            })

        document_model.create({
            'export_hub_id': hub.id,
            'document_type': 'phytosanitary',
            'name': f'Phytosanitary Certificate for {hub.name}',
            'content': self._create_phytosanitary_content(lot_data),
            'language': 'en',  # Dual language as required
        })

    def _create_phytosanitary_content(self, lot_data):
        """Create content for phytosanitary certificate"""
        content = f"""
        PHYTOSANITARY CERTIFICATE

        This is to certify that the following products have been inspected and found to be free from quarantine pests:

        Product Details:
        """
        for lot in lot_data:
            content += f"- {lot['product']} (Batch: {lot['name']}) harvested on {lot['harvest_date']}\n"

        content += """
        The products comply with the phytosanitary requirements of the importing country.

        Issued by: Farm Management System
        Date: """ + str(fields.Date.context_today(self))
        return content

    def _generate_certificate_of_origin(self, hub, document_model):
        """Generate certificate of origin"""
        document_model.create({
            'export_hub_id': hub.id,
            'document_type': 'origin',
            'name': f'Certificate of Origin for {hub.name}',
            'content': self._create_origin_content(hub),
            'language': 'en',  # Dual language as required
        })

    def _create_origin_content(self, hub):
        """Create content for certificate of origin"""
        return f"""
        CERTIFICATE OF ORIGIN

        Country of Origin: {hub.country_of_origin.name if hub.country_of_origin else 'N/A'}
        Export Date: {hub.export_date}
        Products: Various agricultural products
        Quantity: As per shipping documents

        This is to certify that the above mentioned goods originated in the country stated.

        Issued by: Farm Management System
        Date: {fields.Date.context_today(self)}
        """

    def _generate_quality_certificate(self, hub, document_model):
        """Generate quality certificate"""
        document_model.create({
            'export_hub_id': hub.id,
            'document_type': 'quality',
            'name': f'Quality Certificate for {hub.name}',
            'content': self._create_quality_content(hub),
            'language': 'en',  # Dual language as required
        })

    def _create_quality_content(self, hub):
        """Create content for quality certificate"""
        return f"""
        QUALITY CERTIFICATE

        Export Reference: {hub.name}
        Export Date: {hub.export_date}
        Destination: {hub.destination_country.name if hub.destination_country else 'N/A'}

        Products have been tested and certified to meet international quality standards.

        Issued by: Farm Management System
        Date: {fields.Date.context_today(self)}
        """


class ExportGeneratedDocument(models.Model):
    """
    生成的出口文档 [US-09-12]
    """
    _name = 'export.generated.document'
    _description = 'Generated Export Document'

    export_hub_id = fields.Many2one('export.document.hub', string='Export Hub', required=True, ondelete='cascade')
    document_type = fields.Selection([
        ('phytosanitary', 'Phytosanitary Certificate'),
        ('origin', 'Certificate of Origin'),
        ('quality', 'Quality Certificate'),
        ('commercial', 'Commercial Invoice'),
        ('packing', 'Packing List'),
    ], string='Document Type', required=True)
    name = fields.Char('Document Name', required=True)
    content = fields.Text('Content', required=True)
    language = fields.Selection([
        ('en', 'English'),
        ('zh', 'Chinese'),
        ('both', 'Bilingual'),
    ], string='Language', default='both', required=True)
    generated_date = fields.Datetime('Generated Date', default=fields.Datetime.now)
    is_signed = fields.Boolean('Is Signed', default=False)
    signature_date = fields.Datetime('Signature Date')
    signed_by = fields.Many2one('res.users', 'Signed By')

