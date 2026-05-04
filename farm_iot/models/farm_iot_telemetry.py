from odoo import models, fields, api, _

class FarmIotTelemetry(models.Model):
    """
    Farm-specific business logic extensions for Agri IoT Telemetry.
    Adds linkages to farm operations, assets, and geofencing.
    """
    _inherit = 'iiot.telemetry'

    # 关联资产与任务
    production_id = fields.Many2one('project.task', string="Production Task")
    drone_id = fields.Many2one('maintenance.equipment', string="Drone", domain="[('is_drone', '=', True)]")

    # 关联地块
    land_parcel_id = fields.Many2one('farm.location', string="Land Parcel/Pond")

    # US-066-01: Adoption Linkage
    adopted_lot_id = fields.Many2one('stock.lot', string="Adopted Asset", help="If the sensor is attached to a specific adopted tree/animal")

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            # 1. 自动化规则触发
            rules = self.env['farm.automation.rule'].search([
                ('active', '=', True),
                ('sensor_type', '=', record.sensor_type)
            ])
            for rule in rules:
                rule.check_and_trigger(record)

            # 2. 地理围栏越界判定 [US-053-02, US-053-06]
            if record.device_id and record.device_id.geofence_id and record.gps_lat and record.gps_lng:
                fence = record.device_id.geofence_id
                is_inside = fence.is_point_inside(record.gps_lng, record.gps_lat)

                if not is_inside:
                    # 触发越界告警
                    self._trigger_geofence_alarm(record, fence)

            # 3. 认养推送逻辑 [US-066-01]
            if record.adopted_lot_id:
                # Find active subscriptions for this lot
                subs = self.env['farm.csa.subscription'].search([
                    ('adopted_lot_id', '=', record.adopted_lot_id.id),
                    ('state', '=', 'active')
                ])
                for sub in subs:
                    # Post message to customer
                    sub.message_post(body=_("STATUS UPDATE: Your adopted asset %s sent a new reading: %s %s at %s.") % (
                        record.adopted_lot_id.name, record.value, record.sensor_type, record.timestamp
                    ))
        return records

    def _trigger_geofence_alarm(self, telemetry, fence):
        """ 创建越界告警活动与消息推送 """
        msg_body = _("GEOFENCE ALERT: Device %s has LEFT the assigned fence '%s' at [%s, %s]!") % (
            telemetry.device_id.name, fence.name, telemetry.gps_lat, telemetry.gps_lng
        )

        # 记录消息到设备和围栏
        telemetry.device_id.message_post(body=msg_body, message_type='notification', subtype_xmlid='mail.mt_comment')
        fence.message_post(body=msg_body, message_type='notification', subtype_xmlid='mail.mt_comment')

        # 创建待办活动
        self.env['mail.activity'].create({
            'res_id': telemetry.device_id.id,
            'res_model_id': self.env['ir.model']._get('iiot.device').id,
            'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
            'summary': _('BOUNDARY BREACH: %s') % telemetry.device_id.name,
            'note': msg_body,
            'user_id': telemetry.device_id.create_uid.id or self.env.user.id,
        })
