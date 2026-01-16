# Common validation and constraint methods
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class CommonValidationsMixin(models.AbstractModel):
    """
    Common validation and constraint methods that can be reused across different modules
    """
    _name = 'common.validations.mixin'
    _description = 'Common Validations Mixin'

    @api.constrains('season_start_date', 'season_end_date')
    def _check_season_dates(self):
        """Ensure season end date is after start date"""
        for record in self:
            if record.season_start_date and record.season_end_date:
                if record.season_start_date > record.season_end_date:
                    raise ValidationError(_("Season end date must be after start date."))

    @api.constrains('product_tmpl_id', 'season_start_date', 'season_end_date')
    def _check_overlapping_seasons(self):
        """Ensure no overlapping seasons for the same product"""
        for record in self:
            overlapping = self.search([
                ('id', '!=', record.id),
                ('product_tmpl_id', '=', record.product_tmpl_id.id),
                ('season_start_date', '<=', record.season_end_date),
                ('season_end_date', '>=', record.season_start_date),
                ('state', '=', 'active'),
            ])
            if overlapping:
                raise ValidationError(_(
                    "Seasonal recipes cannot overlap for the same product. "
                    "Overlapping with: %s" % ', '.join(overlapping.mapped('name'))
                ))

    @api.constrains('max_variance_tolerance')
    def _check_variance_tolerance_range(self):
        """Ensure variance tolerance is within reasonable range"""
        for record in self:
            if record.max_variance_tolerance < 0 or record.max_variance_tolerance > 10:
                raise ValidationError(_("Max variance tolerance should be between 0% and 10%"))