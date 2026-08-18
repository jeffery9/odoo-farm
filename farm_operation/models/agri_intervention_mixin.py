from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import math
import base64
import datetime
import re
import logging

_logger = logging.getLogger(__name__)


class AgriInterventionMixin(models.AbstractModel):
    """
    Abstract base model for agricultural intervention functionality.
    This mixin provides shared logic across different agricultural intervention implementations.
    """
    _name = 'agri.intervention.mixin'
    _description = 'Agri Agricultural Intervention Shared Logic'
    _inherit = ['agri.intervention.base', 'agri.resource.consumption.mixin', 'agri.incident.alert.mixin']

    # Registry for intervention plugins
    @api.model
    def _get_intervention_plugins(self):
        res = super(AgriInterventionMixin, self)._get_intervention_plugins()
        res.extend([
            {'name': 'weather_gating', 'class': 'agri.intervention.plugin.weather'},
            {'name': 'spatial_audit', 'class': 'agri.intervention.plugin.spatial'},
            {'name': 'yield_calibration', 'class': 'agri.intervention.plugin.yield'},
            {'name': 'nutrient_tracking', 'class': 'agri.intervention.plugin.nutrient'},
            {'name': 'compliance', 'class': 'agri.intervention.plugin.compliance'},
            {'name': 'labor_tracking', 'class': 'agri.intervention.plugin.labor'},
            {'name': 'iot_monitoring', 'class': 'agri.intervention.plugin.iot'},
            {'name': 'harvest_grading', 'class': 'agri.intervention.plugin.harvest'},
            {'name': 'work_verification', 'class': 'agri.intervention.plugin.verification'},
        ])
        return res

    # Basic intervention fields (location_id is now in base)
    agri_task_id = fields.Many2one(
        'project.task',
        string="Production Task",
        help="The specific production task this intervention belongs to."
    )

    campaign_id = fields.Many2one(
        'farm.agricultural.campaign',
        string="Campaign/Season",
        help="The production season this intervention belongs to."
    )

    biological_asset_id = fields.Many2one(
        'agri.biological.asset',
        string="Target Biological Asset",
        help="The living asset this intervention is performed upon."
    )

    # ---------------------------------------------------------
    # [Agri-Precision Absorbed DNA] 
    # Yield Calibration, Cycle Counting, and IoT Status
    # ---------------------------------------------------------
    
    # 1. Uncertainty: Dynamic Yield Tracking
    expected_yield_accuracy = fields.Float("Expected Yield Accuracy (%)", default=100.0)
    last_metrology_date = fields.Datetime("Last Calibration/Sampling")

    # 2. Intervention: Cycle Tracking
    intervention_count = fields.Integer("Intervention Cycles", default=0, copy=False)

    # 3. IoT Integration: Environment Condition
    iot_device_ids = fields.Many2many('iiot.device', 'agri_intervention_mixin_iiot_device_rel', 'mixin_id', 'device_id',
        string='IoT Devices',
        help='IoT devices directly associated with this intervention for environmental gating.'
    )
    iot_status = fields.Selection([
        ('normal', 'Normal'),
        ('monitoring', 'Monitoring'),
        ('warning', 'Warning'),
        ('critical', 'Critical')
    ], string="IoT Environmental Status", default='normal', tracking=True)

    def action_update_yield_estimate(self, new_qty):
        """ [Uncertainty] Mid-process yield calibration based on field sampling. """
        self.ensure_one()
        self.product_qty = new_qty
        self.last_metrology_date = fields.Datetime.now()
        self.message_post(body=_("YIELD CALIBRATION: New expected quantity set to %s.") % new_qty)

    def action_trigger_iot_based_intervention(self, sensor_readings_summary):
        """
        Automatically adjust IoT status via Plugin.
        """
        self.ensure_one()
        self.intervention_count += 1
        
        # Use IoT Plugin
        plugin = self.env['agri.intervention.plugin.iot']
        plugin.update_iot_status(self, sensor_readings_summary)
        return True


    # Agricultural-specific intervention classification
    intervention_type = fields.Selection([
        ('tillage', 'Soil Preparation'),
        ('sowing', 'Sowing/Planting'),
        ('fertilizing', 'Fertilizing'),
        ('irrigation', 'Irrigation'),
        ('protection', 'Crop Protection'),
        ('aerial_spraying', 'Aerial Spraying'),
        ('harvesting', 'Harvesting'),
        ('feeding', 'Feeding'),
        ('medical', 'Medical/Prevention'),
    ], string="Intervention Type")

    # Ekylibre Mapping: Intervention Parameters
    # doer_ids = fields.Many2many('hr.employee', string="Doers/Workers")
    tool_ids = fields.Many2many('maintenance.equipment', 'agri_intervention_mixin_maintenance_equipment_rel', 'mixin_id', 'equipment_id', string="Tools/Machinery")

    procedure_name = fields.Char("Procedure/Method", help="e.g. Mechanical sowing, manual weeding")

    # US-041-02: China Real-name Registration
    operator_id_card = fields.Char("Operator ID Card", help="Required for pesticide/veterinary real-name registration.")
    product_registration_no = fields.Char("Product Registration No.", help="Pesticide or veterinary product registration number.")

    # Harvest Grading [US-002-04]
    grade_a_qty = fields.Float("Grade A Quantity")
    grade_b_qty = fields.Float("Grade B Quantity")
    grade_c_qty = fields.Float("Grade C Quantity")

    @api.constrains('grade_a_qty', 'grade_b_qty', 'grade_c_qty')
    def _check_graded_quantities(self):
        for intervention in self:
            if intervention.intervention_type == 'harvesting' and (intervention.grade_a_qty < 0 or intervention.grade_b_qty < 0 or intervention.grade_c_qty < 0):
                raise UserError(_("Graded quantities cannot be negative."))

    # Ekylibre Mapping: Costing [US-Mapping]
    input_cost = fields.Float("Input Cost", compute='_compute_agri_costs', store=True, precompute=True)
    tool_cost = fields.Float("Tool/Machinery Cost", compute='_compute_agri_costs', store=True, precompute=True)
    doer_cost = fields.Float("Labor Cost", compute='_compute_agri_costs', store=True, precompute=True)
    energy_cost = fields.Float("Energy/Utility Cost", compute='_compute_agri_costs', store=True, precompute=True)
    total_agri_cost = fields.Float("Total Intervention Cost", compute='_compute_agri_costs', store=True, precompute=True)

    # US-002-03: Soil Nutrient Inputs (RESTORED)
    pure_n_qty = fields.Float("Pure Nitrogen (N) kg", compute='_compute_agri_costs', store=True, precompute=True)
    pure_p_qty = fields.Float("Pure Phosphorus (P) kg", compute='_compute_agri_costs', store=True, precompute=True)
    pure_k_qty = fields.Float("Pure Potassium (K) kg", compute='_compute_agri_costs', store=True, precompute=True)

    # @api.depends('move_raw_ids.state', 'move_raw_ids.product_uom_qty', 'workorder_ids.duration', 'is_working')
    def _compute_agri_costs(self):
        for mo in self:
            # 1. 投入品成本 (Actual Cost from Moves)
            inputs = 0.0
            for move in mo.move_raw_ids:
                inputs += move.product_uom_qty * move.product_id.standard_price

            # 2. 劳动力成本
            labor = 0.0
            if hasattr(mo, 'agri_task_id') and mo.agri_task_id and hasattr(mo.agri_task_id, 'worklog_ids'):
                labor = sum(mo.agri_task_id.worklog_ids.mapped(lambda l: l.quantity * (l.employee_id.hourly_cost or 50.0)))

            # 3. 工具与机械成本
            tools = 0.0
            if mo.workorder_ids:
                tools = sum(mo.workorder_ids.mapped(lambda w: (w.duration / 60.0) * w.workcenter_id.costs_hour))

            # 4. 能耗成本
            energy = 0.0
            if hasattr(mo, 'electricity_consumption'):
                energy += mo.electricity_consumption * 1.5
            if hasattr(mo, 'water_consumption'):
                energy += mo.water_consumption * 4.0

            mo.input_cost = inputs
            mo.doer_cost = labor
            mo.tool_cost = tools
            mo.energy_cost = energy
            mo.total_agri_cost = inputs + labor + tools + energy

    # 工时追踪 [US-036-03]
    work_start_datetime = fields.Datetime("Work Start")
    is_working = fields.Boolean("In Progress", default=False)

    # Simplified Approval System [US-039-01]
    approval_state = fields.Selection([
        ('draft', 'Draft'),
        ('to_approve', 'Awaiting Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string="Approval Status", default='draft', tracking=True)

    approver_id = fields.Many2one('res.users', string="Approver", tracking=True)
    approval_date = fields.Datetime("Approval Date", readonly=True)

    simplified_state = fields.Selection([
        ('draft', 'Draft'),
        ('approval', 'Approval'),
        ('ready', 'Ready'),
        ('progress', 'In Progress'),
        ('done', 'Completed'),
    ], string="Simplified State", compute='_compute_simplified_state', store=True, precompute=True)

    @api.depends('state', 'approval_state')
    def _compute_simplified_state(self):
        for rec in self:
            if rec.state == 'draft' and rec.approval_state == 'draft':
                rec.simplified_state = 'draft'
            elif rec.approval_state == 'to_approve':
                rec.simplified_state = 'approval'
            elif rec.state == 'confirmed' or rec.approval_state == 'approved':
                rec.simplified_state = 'ready'
            elif rec.state == 'progress':
                rec.simplified_state = 'progress'
            elif rec.state in ['to_close', 'done']:
                rec.simplified_state = 'done'
            else:
                rec.simplified_state = 'draft'

    # Drone and spatial audit fields
    actual_flight_area = fields.Float("Actual Flown Area (mu/ha)")
    drone_id = fields.Many2one('maintenance.equipment', string="Drone Used", )

    # 空间审计 [US-053-04]
    out_of_bounds_count = fields.Integer("OOB Point Count", compute='_compute_spatial_audit', help="Number of telemetry points outside the parcel.")
    spatial_compliance_rate = fields.Float("Spatial Compliance (%)", compute='_compute_spatial_audit')

    @api.depends('location_id', 'is_working')
    def _compute_spatial_audit(self):
        """ 统计该任务期间所有 GPS 记录的合规性 """
        for mo in self:
            parcel = mo.location_id
            if not parcel or not hasattr(parcel, 'gps_coordinates') or not parcel.gps_coordinates:
                mo.out_of_bounds_count = 0
                mo.spatial_compliance_rate = 100.0
                continue

            # Create a temporary fence object for boundary check
            if hasattr(self.env['farm.geofence'], 'new'):
                temp_fence = self.env['farm.geofence'].new({
                    'coordinates': parcel.gps_coordinates
                })

                # Get telemetry records during this task
                telemetries = self.env['iiot.telemetry'].search([
                    ('production_id', '=', mo.agri_task_id.id if mo.agri_task_id else False),
                    ('gps_lat', '!=', 0),
                    ('gps_lng', '!=', 0)
                ])

                if not telemetries:
                    mo.out_of_bounds_count = 0
                    mo.spatial_compliance_rate = 100.0
                    continue

                oob_count = 0
                for t in telemetries:
                    if not temp_fence.is_point_inside(t.gps_lng, t.gps_lat):
                        oob_count += 1

                mo.out_of_bounds_count = oob_count
                mo.spatial_compliance_rate = ((len(telemetries) - oob_count) / len(telemetries)) * 100.0
            else:
                # Default values if farm.geofence is not available
                mo.out_of_bounds_count = 0
                mo.spatial_compliance_rate = 100.0

    def action_submit_for_approval(self):
        """Submit intervention for approval"""
        self.ensure_one()
        self.write({'approval_state': 'to_approve'})
        self.message_post(body=_("Intervention submitted for supervisor approval."))

    def action_approve(self):
        """Approve the intervention and confirm in base engine"""
        self.ensure_one()
        self.write({
            'approval_state': 'approved',
            'approver_id': self.env.user.id,
            'approval_date': fields.Datetime.now()
        })
        # Use Base Engine for confirmation
        self.action_confirm_base()
        self.message_post(body=_("Intervention approved by %s") % self.env.user.name)

    def action_reject(self):
        """Reject the intervention"""
        self.ensure_one()
        self.write({'approval_state': 'rejected'})
        self.message_post(body=_("Intervention rejected."))

    # ---------------------------------------------------------
    # Overridable Hooks (Bridge Pattern Implementation)
    # ---------------------------------------------------------

    def _hook_pre_confirm(self):
        """[US-041-02] Compliance Gating before confirmation"""
        super()._hook_pre_confirm()
        # Additional business-specific confirm logic if needed
        _logger.info("Farm Operation: Running pre-confirm hooks for %s", self.name)

    def _hook_pre_start(self):
        """[US-053-04] Weather & IoT Gating before starting"""
        super()._hook_pre_start()
        # Verify IoT status before allowing start
        if self.iot_status == 'critical':
            raise UserError(_("CRITICAL ALERT: IoT sensors report hazardous conditions. Cannot start intervention."))

    def _hook_pre_done(self):
        """[US-002-04] Harvest Grading and Audit before completion"""
        super()._hook_pre_done()
        _logger.info("Farm Operation: Running pre-done hooks for %s", self.name)

    def _hook_post_done(self):
        """[US-036-03] Labor recording and Cleanup after completion"""
        super()._hook_post_done()
        # Auto-record worklog if not already recorded
        if not self.is_working and self.date_start:
            self._create_auto_worklog_from_hook()

    def _create_auto_worklog_from_hook(self):
        """Helper to create worklog from completion hook"""
        if 'farm.worklog' in self.env:
            employee = self.env.user.employee_id
            self.env['farm.worklog'].create({
                'employee_id': employee.id if employee else False,
                'task_id': self.agri_task_id.id if self.agri_task_id else False,
                'date': fields.Date.today(),
                'work_type': self.intervention_type or 'harvesting',
                'quantity': 1.0,
                'notes': _('Auto-recorded from intervention hook: %s') % self.name
            })

    # ---------------------------------------------------------
    # UI Actions (Refactored to use Hooks)
    # ---------------------------------------------------------

    def action_start_work(self):
        """Start the actual work via Base Engine (which triggers hooks)"""
        self.ensure_one()
        self.action_start_base()
        self.write({'is_working': True})
        return True

    def action_stop_work(self):
        """Stop the actual work via Base Engine (which triggers hooks)"""
        self.ensure_one()
        if not self.date_start:
            return
        self.action_done_base()
        self.write({'is_working': False})
        return True

    def action_confirm(self):
        """扩展确认逻辑，通过基础引擎触发钩子"""
        self.filtered(lambda r: r.state == 'draft').action_confirm_base()
        return True

    def action_export_drone_kml(self):
        """Export drone route as KML for navigation - US-052-03, US-053-03"""
        """ US-052-03, US-053-03: 将地块边界与周边禁飞区导出为 KML """
        self.ensure_one()
        import base64
        # 1. 查找关联地块
        parcel = self.agri_task_id.land_parcel_id if self.agri_task_id else self.location_dest_id
        if not parcel or not hasattr(parcel, 'gps_coordinates') or not parcel.gps_coordinates:
            raise UserError(_("No GIS boundaries defined for the selected land parcel!"))

        # 2. 查找周边禁飞区围栏
        nearby_fences = self.env['farm.geofence'].search([
            ('fence_type', '=', 'no_fly'),
            ('active', '=', True)
        ])

        # 3. 生成 KML
        kml_header = """<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>Drone Mission: {name}</name>
    <Style id="workArea"><PolyStyle><color>4d00ff00</color></PolyStyle></Style>
    <Style id="noFly"><PolyStyle><color>4d0000ff</color></PolyStyle></Style>
""".format(name=self.name)

        # 核心作业区
        work_area = f"""    <Placemark>
      <name>Work Area: {parcel.name}</name>
      <styleUrl>#workArea</styleUrl>
      <Polygon><outerBoundaryIs><LinearRing><coordinates>{parcel.gps_coordinates.replace(';', ' ')}</coordinates></LinearRing></outerBoundaryIs></Polygon>
    </Placemark>"""

        # 禁飞区
        nf_areas = ""
        for nf in nearby_fences:
            if hasattr(nf, 'coordinates'):
                nf_areas += f"""    <Placemark>
      <name>NO-FLY: {nf.name}</name>
      <styleUrl>#noFly</styleUrl>
      <Polygon><outerBoundaryIs><LinearRing><coordinates>{nf.coordinates.replace(';', ' ')}</coordinates></LinearRing></outerBoundaryIs></Polygon>
    </Placemark>"""

        kml_footer = """  </Document>
</kml>"""

        full_kml = kml_header + work_area + nf_areas + kml_footer

        # 4. 创建附件
        attachment = self.env['ir.attachment'].create({
            'name': f"{self.name}_mission.kml",
            'type': 'binary',
            'datas': base64.b64encode(full_kml.encode('utf-8')),
            'mimetype': 'application/vnd.google-earth.kml+xml',
        })

        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }

    def button_mark_done(self):
        """扩展完成逻辑，通过基础引擎触发钩子"""
        for intervention in self:
            if intervention.state != 'done':
                intervention.action_done_base()

        # Call super method if available to handle other MRP production logic
        if hasattr(super(AgriInterventionMixin, self), 'button_mark_done'):
            return super(AgriInterventionMixin, self).button_mark_done()
        return True