# Common compute methods and utility functions
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class CommonComputeMethodsMixin(models.AbstractModel):
    """
    Common compute methods that can be reused across different modules
    """
    _name = 'common.compute.methods.mixin'
    _description = 'Common Compute Methods Mixin'

    @api.model
    def compute_yield_rate(self, output_qty, input_qty):
        """
        Compute yield rate as percentage
        """
        if input_qty > 0:
            return (output_qty / input_qty) * 100
        else:
            return 0.0

    @api.model
    def compute_efficiency_rate(self, output_qty, resource_consumption):
        """
        Compute efficiency rate (output per unit of resource)
        """
        if resource_consumption > 0:
            return output_qty / resource_consumption
        else:
            return 0.0

    @api.model
    def compute_variance(self, actual_value, standard_value):
        """
        Compute variance between actual and standard values
        """
        return actual_value - standard_value

    @api.model
    def compute_percentage_difference(self, base_value, new_value):
        """
        Compute percentage difference between values
        """
        if base_value != 0:
            return ((new_value - base_value) / base_value) * 100
        else:
            return 0.0


class ByproductCostShareMixin(models.AbstractModel):
    """
    Mixin for handling byproduct cost share calculations
    """
    _name = 'byproduct.cost.share.mixin'
    _description = 'Byproduct Cost Share Mixin'

    byproduct_cost_share_total = fields.Float(
        "Byproduct Cost Share Total (%)",
        compute='_compute_byproduct_cost_share_total',
        store=True
    )
    finished_product_cost_share = fields.Float(
        "Finished Product Cost Share (%)",
        compute='_compute_finished_product_cost_share',
        store=True
    )

    @api.depends('byproduct_ids', 'byproduct_ids.cost_share')
    def _compute_byproduct_cost_share_total(self):
        for record in self:
            record.byproduct_cost_share_total = sum(record.byproduct_ids.mapped('cost_share'))

    @api.depends('byproduct_cost_share_total')
    def _compute_finished_product_cost_share(self):
        for record in self:
            record.finished_product_cost_share = max(0.0, 100.0 - record.byproduct_cost_share_total)

    @api.constrains('byproduct_ids', 'byproduct_ids.cost_share')
    def _check_byproduct_cost_share_total(self):
        """ US-04-03: 确保副产品成本分摊比例不超过100% """
        for record in self:
            if record.byproduct_cost_share_total > 100.0:
                raise ValidationError(
                    _("Byproduct cost share total cannot exceed 100%%. Current total is %s%%")
                    % record.byproduct_cost_share_total
                )