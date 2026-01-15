from odoo import models, fields, api, _

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def get_formview_action(self, access_uid=None):
        """ US-TECH-06-23: Transparent redirection to Agri ISL Product View. """
        res = super(ProductTemplate, self).get_formview_action(access_uid=access_uid)
        
        # Check if an ISL record exists for this template
        isl_record = self.env['farm.agri.product'].search([('product_tmpl_id', '=', self.id)], limit=1)
        if isl_record:
            res.update({
                'res_model': 'farm.agri.product',
                'res_id': isl_record.id,
            })
        return res

    # US-04-05: 替代品关系 (Maintained at Base level for cross-industry visibility)
    substitute_product_ids = fields.Many2many(
        'product.template',
        'product_template_substitute_rel',
        'product_id',
        'substitute_id',
        string="Substitute Products",
        help="Products that can be used as substitutes for this product."
    )