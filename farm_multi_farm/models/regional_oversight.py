from odoo import models, fields, api, _

class FarmRegionalOversight(models.Model):
    """
    G2B: Regional Agricultural Oversight for Government Agencies.
    Aggregates data from multiple cooperatives/farms.
    """
    _name = 'farm.regional.oversight'
    _description = 'Regional Agricultural Oversight Dashboard'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Region/Zone Name", required=True)
    agency_id = fields.Many2one('res.partner', string="Regulatory Body", required=True)
    
    # Aggregation
    cooperative_ids = fields.Many2many('cooperative.entity', string="Monitored Cooperatives")
    total_land_area = fields.Float("Total Monitored Area (Ha)", compute='_compute_totals')
    
    # Prediction Aggregation (L3 -> L4)
    total_predicted_yield = fields.Float("Regional Yield Forecast (kg)", compute='_compute_yield_forecast')
    
    # Compliance Health
    avg_compliance_score = fields.Float("Regional Compliance Avg (%)", compute='_compute_compliance')
    alert_count = fields.Integer("Active Compliance Alerts", compute='_compute_compliance')

    def _compute_totals(self):
        for rec in self:
            farms = rec.cooperative_ids.mapped('member_farm_ids')
            rec.total_land_area = sum(farms.mapped('company_id').mapped('partner_id').mapped('land_area')) / 10000.0 # Mock

    def _compute_yield_forecast(self):
        """
        Aggregates Predicted Yield from all Biological Twins in the region.
        """
        for rec in self:
            farms = rec.cooperative_ids.mapped('member_farm_ids')
            companies = farms.mapped('company_id')
            # Query biological twins across companies
            twins = self.env['farm.biological.twin'].sudo().search([
                ('location_id.company_id', 'in', companies.ids)
            ])
            rec.total_predicted_yield = sum(twins.mapped('predicted_yield'))

    def _compute_compliance(self):
        for rec in self:
            # Aggregate export compliance status
            farms = rec.cooperative_ids.mapped('member_farm_ids')
            companies = farms.mapped('company_id')
            compliances = self.env['farm.export.compliance'].sudo().search([
                ('company_id', 'in', companies.ids)
            ])
            blocked = len(compliances.filtered(lambda c: c.compliance_status == 'blocked'))
            rec.alert_count = blocked
            rec.avg_compliance_score = (1 - (blocked / len(compliances))) * 100 if compliances else 100.0

    def action_refresh_regional_data(self):
        """ Manually trigger recalculation of regional metrics """
        self._compute_totals()
        self._compute_yield_forecast()
        self._compute_compliance()
        return True
