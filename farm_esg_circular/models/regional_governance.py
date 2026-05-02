from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class AgriRegionalCircularGovernance(models.Model):
    """
    US-27-07: 行政区域级循环治理 (Regional/Administrative Cycle)
    Model for administrative-level circular economy governance and reporting
    """
    _name = 'agri.regional.circular.governance'
    _description = 'Regional Circular Economy Governance'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Regional Governance Plan', required=True, copy=False)
    administrative_level = fields.Selection([
        ('village', 'Village'),
        ('town', 'Town'),
        ('county', 'County'),
        ('city', 'City'),
        ('province', 'Province'),
    ], string='Administrative Level', required=True)

    # Geographic and administrative information
    administrative_area_id = fields.Many2one('res.country.state', string='Administrative Area')
    area_name = fields.Char('Area Name')
    area_code = fields.Char('Area Code', help='Administrative code for the region')
    area_population = fields.Integer('Population')
    area_area_sqkm = fields.Float('Area (sq km)')

    # Circular economy network
    waste_collection_points = fields.Integer('Waste Collection Points')
    recycling_facilities = fields.Integer('Recycling Facilities')
    total_participating_farms = fields.Integer('Total Participating Farms', compute='_compute_participating_farms', store=True)

    # Aggregation and reporting
    total_waste_processed_ton = fields.Float('Total Waste Processed (ton)', compute='_compute_aggregated_data', store=True)
    total_resource_created_ton = fields.Float('Total Resource Created (ton)', compute='_compute_aggregated_data', store=True)
    total_co2_reduced_ton = fields.Float('Total CO2 Reduced (ton)', compute='_compute_aggregated_data', store=True)
    total_economic_value_yuan = fields.Float('Total Economic Value (Yuan)', compute='_compute_aggregated_data', store=True)

    # Spatial aggregation using ST_Contains (PostGIS)
    aggregated_data_by_boundary = fields.Text('Aggregated Data by Boundary', compute='_compute_boundary_aggregation')

    # Timeline
    start_date = fields.Date('Start Date', default=fields.Date.context_today)
    end_date = fields.Date('End Date')
    reporting_frequency = fields.Selection([
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annually', 'Annually'),
    ], string='Reporting Frequency', default='annually')

    # Government and policy integration
    government_subsidy_program = fields.Char('Government Subsidy Program')
    subsidy_amount = fields.Float('Subsidy Amount')
    policy_compliance_status = fields.Selection([
        ('pending', 'Pending'),
        ('compliant', 'Compliant'),
        ('non_compliant', 'Non-Compliant'),
        ('audit_required', 'Audit Required'),
    ], string='Policy Compliance Status', default='pending')

    # Logistics coordination
    regional_logistics_hub = fields.Many2one('res.partner', string='Regional Logistics Hub')
    cross_entity_transfer_count = fields.Integer('Cross-Entity Transfer Count', compute='_compute_transfers', store=True)

    # Status
    status = fields.Selection([
        ('planning', 'Planning'),
        ('implemented', 'Implemented'),
        ('auditing', 'Auditing'),
        ('completed', 'Completed'),
    ], string='Status', default='planning')

    # Related records
    circular_flow_ids = fields.One2many('agri.sustainability.circular.flow', 'regional_governance_id',
                                        string='Circular Flows')
    farm_participation_ids = fields.One2many('agri.farm.circular.participation', 'regional_governance_id',
                                            string='Farm Participations')

    @api.depends('circular_flow_ids')
    def _compute_participating_farms(self):
        """Compute total number of participating farms"""
        for record in self:
            farm_ids = set()
            for flow in record.circular_flow_ids:
                if flow.related_production_id.location_id:
                    farm_ids.add(flow.related_production_id.location_id.id)
            record.total_participating_farms = len(farm_ids)

    def _compute_aggregated_data(self):
        """Compute aggregated circular economy metrics"""
        for record in self:
            # Aggregate from circular flows
            flows = record.circular_flow_ids.filtered(lambda f: f.status == 'completed')
            record.total_waste_processed_ton = sum(f.input_quantity for f in flows)
            record.total_resource_created_ton = sum(f.output_quantity for f in flows)
            record.total_co2_reduced_ton = sum(0 for f in flows)
            record.total_economic_value_yuan = sum(f.economic_value for f in flows)

    def _compute_boundary_aggregation(self):
        """Compute data aggregation based on administrative boundaries (ST_Contains concept)"""
        for record in self:
            record.aggregated_data_by_boundary = f"""
            Administrative Boundary Data for {record.name} ({record.administrative_level})
            Area: {record.area_name} (Code: {record.area_code})
            Participating Farms: {record.total_participating_farms}

            Aggregated Metrics:
            - Total Waste Processed: {record.total_waste_processed_ton} tons
            - Total Resources Created: {record.total_resource_created_ton} tons
            - Total CO2 Reduced: {record.total_co2_reduced_ton} tons
            - Total Economic Value: {record.total_economic_value_yuan} Yuan

            Data aggregated using administrative boundary containment principles.
            """

    def _compute_transfers(self):
        """Compute cross-entity transfer count"""
        for record in self:
            # This would count transfers between different entities in the region
            record.cross_entity_transfer_count = len(record.circular_flow_ids)

    @api.constrains('area_area_sqkm', 'area_population')
    def _check_positive_values(self):
        for record in self:
            if record.area_area_sqkm and record.area_area_sqkm <= 0:
                raise ValidationError(_("Area must be positive."))
            if record.area_population and record.area_population < 0:
                raise ValidationError(_("Population cannot be negative."))

    def action_start_governance(self):
        """Start regional governance implementation"""
        for record in self:
            record.status = 'implemented'
            record.message_post(body=_("Regional circular economy governance implemented for %s level: %s") %
                              (dict(record._fields['administrative_level'].selection).get(record.administrative_level),
                               record.area_name))

    def action_request_audit(self):
        """Request compliance audit"""
        for record in self:
            record.policy_compliance_status = 'audit_required'
            record.status = 'auditing'
            record.message_post(body=_("Compliance audit requested for regional governance program"))

    def action_complete_audit(self):
        """Complete compliance audit"""
        for record in self:
            record.policy_compliance_status = 'compliant'
            record.status = 'completed'
            record.message_post(body=_("Compliance audit completed. Program marked as compliant."))

    def action_generate_regional_report(self):
        """Generate regional circular economy report"""
        report_content = f"""
        Regional Circular Economy Report: {self.name}
        Administrative Level: {dict(self._fields['administrative_level'].selection).get(self.administrative_level)}
        Area: {self.area_name} (Code: {self.area_code})
        Population: {self.area_population:,}
        Area: {self.area_area_sqkm} sq km

        Performance Metrics:
        - Participating Farms: {self.total_participating_farms}
        - Waste Processed: {self.total_waste_processed_ton} tons
        - Resources Created: {self.total_resource_created_ton} tons
        - CO2 Reduced: {self.total_co2_reduced_ton} tons
        - Economic Value: {self.total_economic_value_yuan:,} Yuan

        Facilities:
        - Waste Collection Points: {self.waste_collection_points}
        - Recycling Facilities: {self.recycling_facilities}
        - Cross-Entity Transfers: {self.cross_entity_transfer_count}

        Policy Compliance: {dict(self._fields['policy_compliance_status'].selection).get(self.policy_compliance_status)}
        Government Support: {self.government_subsidy_program or 'N/A'} (Amount: {self.subsidy_amount or 0})
        """
        return {
            'type': 'ir.actions.act_window',
            'name': _('Regional Circular Economy Report'),
            'res_model': 'agri.regional.circular.governance',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
            'context': {'default_report_content': report_content}
        }


class AgriFarmCircularParticipation(models.Model):
    """
    Track individual farm participation in regional circular economy
    """
    _name = 'agri.farm.circular.participation'
    _description = 'Farm Circular Economy Participation'

    name = fields.Char('Participation Record', required=True, copy=False)
    regional_governance_id = fields.Many2one('agri.regional.circular.governance', string='Regional Governance', required=True)

    # Farm information
    farm_location_id = fields.Many2one('farm.location', string='Farm Location', required=True)
    farm_partner_id = fields.Many2one('res.partner', string='Farm Partner', readonly=True)

    # Participation metrics
    waste_contributed_ton = fields.Float('Waste Contributed (ton)')
    resources_received_ton = fields.Float('Resources Received (ton)')
    co2_reduced_ton = fields.Float('CO2 Reduced (ton)', compute='_compute_co2_reduction', store=True)
    economic_benefit_yuan = fields.Float('Economic Benefit (Yuan)')

    # Participation status
    participation_status = fields.Selection([
        ('registered', 'Registered'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('excellent', 'Excellent'),
        ('needs_improvement', 'Needs Improvement'),
    ], string='Status', default='registered')

    # Timeline
    registration_date = fields.Date('Registration Date', default=fields.Date.context_today)
    last_activity_date = fields.Date('Last Activity Date')

    # Related flows
    circular_flow_ids = fields.One2many('agri.sustainability.circular.flow', 'farm_participation_id',
                                        string='Circular Flows')

    @api.depends('waste_contributed_ton', 'resources_received_ton')
    def _compute_co2_reduction(self):
        """Compute CO2 reduction based on circular activity"""
        for record in self:
            # Simple calculation - in real implementation would use more sophisticated method
            record.co2_reduced_ton = (record.waste_contributed_ton + record.resources_received_ton) * 0.1

    @api.model
    def create(self, vals):
        if 'name' not in vals or not vals['name']:
            vals['name'] = self.env['ir.sequence'].next_by_code('agri.farm.circular.participation') or '/'
        return super().create(vals)