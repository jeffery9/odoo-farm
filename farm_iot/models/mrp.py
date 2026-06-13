# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    def _hook_post_start(self):
        """[US-IOT-05] Activate IoT Monitoring upon start"""
        super()._hook_post_start()
        # If devices are linked, put them in high-frequency monitoring mode
        if hasattr(self, 'iot_device_ids') and self.iot_device_ids:
            for device in self.iot_device_ids:
                if hasattr(device, 'action_activate_monitoring'):
                    device.action_activate_monitoring(context={'intervention_id': self.id})
            
            # Check connectivity
            all_connected = all(d.connection_state == 'connected' for d in self.iot_device_ids)
            self.write({'iot_status': 'connected' if all_connected else 'offline'})
            self.message_post(body=_("IOT SYNC: Monitoring activated for %s devices.") % len(self.iot_device_ids))
        else:
            self.write({'iot_status': 'none'})

    def _hook_pre_done(self):
        """[US-IOT-06] Deactivate IoT Monitoring before completion"""
        super()._hook_pre_done()
        if hasattr(self, 'iot_device_ids') and self.iot_device_ids:
            for device in self.iot_device_ids:
                if hasattr(device, 'action_deactivate_monitoring'):
                    device.action_deactivate_monitoring()
            self.message_post(body=_("IOT SYNC: Monitoring deactivated."))
            self.write({'iot_status': 'none'})
