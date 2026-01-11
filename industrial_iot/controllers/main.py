# -*- coding: utf-8 -*-
import json
import logging
from odoo import http, _
from odoo.http import request
from odoo.exceptions import ValidationError
import werkzeug
from datetime import datetime

_logger = logging.getLogger(__name__)


class IndustrialIotController(http.Controller):
    """HTTP controllers for IIoT module"""

    @http.route('/iiot/config', type='json', auth='public', methods=['POST'], csrf=False)
    def device_config(self, **post):
        """
        Device configuration download endpoint
        Expected payload: {"serial": "SN123", "token": "tk_abc"}
        """
        try:
            # Get request data
            data = request.jsonrequest or {}
            serial = data.get('serial')
            token = data.get('token')

            if not serial or not token:
                return {
                    'error': 'Missing serial or token',
                    'status': 'error'
                }

            # Find device by serial and token
            device = request.env['iiot.device'].sudo().search([
                ('serial_number', '=', serial),
                ('config_token', '=', token)
            ], limit=1)

            if not device:
                return {
                    'error': 'Invalid serial or token',
                    'status': 'error'
                }

            # Generate MQTT configuration
            mqtt_config = self._generate_mqtt_config(device)

            # Return configuration and invalidate token
            result = {
                'status': 'success',
                'device_id': device.device_id,
                'mqtt': mqtt_config,
                'topics': device.get_topic_map()
            }

            # Invalidate the token after successful config download
            device.sudo().write({'config_token': False})

            _logger.info(f"Device configuration downloaded for {device.serial_number}")
            return result

        except Exception as e:
            _logger.error(f"Error in device config endpoint: {str(e)}")
            return {
                'error': str(e),
                'status': 'error'
            }

    def _generate_mqtt_config(self, device):
        """Generate MQTT configuration for device"""
        # Get MQTT broker settings from system parameters
        mqtt_host = request.env['ir.config_parameter'].sudo().get_param('iiot.mqtt_host', 'mqtt.factory.com')
        mqtt_port = int(request.env['ir.config_parameter'].sudo().get_param('iiot.mqtt_port', '8883'))
        use_tls = request.env['ir.config_parameter'].sudo().get_param('iiot.mqtt_use_tls', 'True').lower() == 'true'

        return {
            'host': mqtt_host,
            'port': mqtt_port,
            'use_tls': use_tls,
            'client_id': device.device_id,
            'username': device.device_id,
            'password': device.config_token or device.device_id  # Use token if available, otherwise device_id
        }

    @http.route('/iiot/webhook/<string:device_id>', type='json', auth='public', methods=['POST'], csrf=False)
    def telemetry_webhook(self, device_id, **post):
        """
        Webhook endpoint for telemetry data from MQTT bridge
        Expected payload: {"topic": "telemetry/device001/data", "payload": {...}}
        """
        try:
            # Get request data
            data = request.jsonrequest or {}
            topic = data.get('topic', '')
            payload = data.get('payload', {})

            if not isinstance(payload, dict):
                return {
                    'error': 'Payload must be a JSON object',
                    'status': 'error'
                }

            # Find device by device_id
            device = request.env['iiot.device'].sudo().search([
                ('device_id', '=', device_id)
            ], limit=1)

            if not device:
                _logger.warning(f"Webhook received for unknown device: {device_id}")
                return {
                    'error': f'Unknown device: {device_id}',
                    'status': 'error'
                }

            # Process telemetry data based on topic
            if 'telemetry' in topic:
                device.process_telemetry_data(payload)
            elif 'ota' in topic and 'status' in topic:
                self._process_ota_status(device, payload)

            _logger.info(f"Telemetry received for device {device_id}: {topic}")
            return {'status': 'success'}

        except Exception as e:
            _logger.error(f"Error in telemetry webhook: {str(e)}")
            return {
                'error': str(e),
                'status': 'error'
            }

    def _process_ota_status(self, device, payload):
        """Process OTA status updates from device"""
        update_id = payload.get('update_id')
        status = payload.get('status')
        progress = payload.get('progress')
        error_message = payload.get('error')

        if not update_id:
            _logger.warning(f"OTA status update missing update_id for device {device.device_id}")
            return

        # Find the update record
        update = request.env['iiot.update'].sudo().search([
            ('update_id', '=', update_id),
            ('device_id', '=', device.id)
        ], limit=1)

        if not update:
            _logger.warning(f"OTA update not found: {update_id} for device {device.device_id}")
            return

        # Update the status
        update.update_status_from_device(status, progress, error_message)

    @http.route('/iiot/command/<string:device_id>', type='json', auth='user', methods=['POST'], csrf=False)
    def send_command(self, device_id, **post):
        """
        Endpoint for sending commands to devices (for internal use)
        Expected payload: {"action": "reset", "params": {...}}
        """
        try:
            # Get request data
            data = request.jsonrequest or {}
            action = data.get('action')
            params = data.get('params', {})

            if not action:
                return {
                    'error': 'Action is required',
                    'status': 'error'
                }

            # Find device by device_id
            device = request.env['iiot.device'].search([
                ('device_id', '=', device_id)
            ], limit=1)

            if not device:
                return {
                    'error': f'Device not found: {device_id}',
                    'status': 'error'
                }

            # Send command to device
            device.send_command(action, **params)

            return {
                'status': 'success',
                'message': f'Command {action} sent to {device_id}'
            }

        except Exception as e:
            _logger.error(f"Error sending command: {str(e)}")
            return {
                'error': str(e),
                'status': 'error'
            }