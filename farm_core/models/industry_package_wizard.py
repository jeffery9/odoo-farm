from odoo import fields, models, api, _

class IndustryPackageWizard(models.TransientModel):
    """
    Wizard for applying industry data packages
    """
    _name = 'farm.industry.package.wizard'
    _description = 'Industry Package Application Wizard'

    package_id = fields.Many2one(
        'agri.industry.data.package',
        string="Industry Package",
        required=True
    )

    confirmation_message = fields.Char(
        string="Confirmation Message",
        compute='_compute_confirmation_message'
    )

    @api.depends('package_id')
    def _compute_confirmation_message(self):
        for record in self:
            if record.package_id:
                record.confirmation_message = _("Apply the '%s' package? This will initialize your system with industry-specific data.") % record.package_id.name
            else:
                record.confirmation_message = ""

    def action_apply_selected_package(self):
        """Apply the selected package"""
        self.ensure_one()
        if not self.package_id:
            raise Exception(_("Please select an industry package to apply."))

        # Call the apply method on the selected package
        return self.package_id.action_apply_package()