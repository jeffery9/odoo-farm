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

    @http.route('/iiot/gateway/register', type='json', auth='public', methods=['POST'], csrf=False)
    def gateway_register(self, **post):
        """
        Automatic registration endpoint for IoT Gateways
        Expected payload: {"gateway_id": "bridge-01", "name": "Main Bridge", "url": "http://192.168.1.100:8000"}
        """
        try:
            data = request.jsonrequest or {}
            gateway_id = data.get('gateway_id')
            name = data.get('name', gateway_id)
            url = data.get('url')

            if not gateway_id:
                return {'error': 'Missing gateway_id', 'status': 'error'}

            gateway = request.env['iiot.gateway'].sudo().search([('gateway_id', '=', gateway_id)], limit=1)
            vals = {
                'name': name,
                'url': url,
                'state': 'online',
                'last_seen': datetime.now(),
            }

            if gateway:
                gateway.sudo().write(vals)
            else:
                gateway = request.env['iiot.gateway'].sudo().create({
                    'gateway_id': gateway_id,
                    **vals
                })

            _logger.info(f"IoT Gateway registered: {gateway_id} at {url}")
            return {'status': 'success'}

        except Exception as e:
            _logger.error(f"Error in gateway registration: {str(e)}")
            return {'error': str(e), 'status': 'error'}

    @http.route('/iiot/gateway/config', type='json', auth='public', methods=['POST'], csrf=False)
    def gateway_config(self, **post):
        """
        Endpoint for IoT Gateways to download their configuration
        Expected payload: {"gateway_id": "bridge-01"}
        """
        try:
            data = request.jsonrequest or {}
            gateway_id = data.get('gateway_id')

            if not gateway_id:
                return {'error': 'Missing gateway_id', 'status': 'error'}

            gateway = request.env['iiot.gateway'].sudo().search([('gateway_id', '=', gateway_id)], limit=1)
            
            if not gateway:
                return {'error': 'Gateway not found', 'status': 'error'}

            # Collect managed device profiles for topic patterns
            managed_devices = gateway.device_ids
            topics = {
                'config_request': request.env['ir.config_parameter'].sudo().get_param('iiot.mqtt_config_request_topic', 'iiot/config/request'),
            }

            return {
                'status': 'success',
                'mqtt': {
                    'host': gateway.mqtt_host or request.env['ir.config_parameter'].sudo().get_param('iiot.mqtt_host', 'mqtt.factory.com'),
                    'port': gateway.mqtt_port or int(request.env['ir.config_parameter'].sudo().get_param('iiot.mqtt_port', '8883')),
                    'user': gateway.mqtt_user,
                    'password': gateway.mqtt_password,
                    'use_tls': gateway.mqtt_use_tls,
                },
                'topics': topics
            }

        except Exception as e:
            _logger.error(f"Error in gateway config: {str(e)}")
            return {'error': str(e), 'status': 'error'}

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
            payload_type = payload.get('event', 'telemetry')
            
            if payload_type == 'telemetry' or 'telemetry' in topic:
                device.process_telemetry_data(payload)
            elif payload_type == 'command_ack':
                self._process_command_ack(device, payload)
            elif 'ota' in topic and 'status' in topic:
                self._process_ota_status(device, payload)

            _logger.info(f"IoT Event received for device {device_id}: {payload_type}")
            return {'status': 'success'}

        except Exception as e:
            _logger.error(f"Error in telemetry webhook: {str(e)}")
            return {
                'error': str(e),
                'status': 'error'
            }

    def _process_command_ack(self, device, payload):
        """Process command acknowledgement from device"""
        action = payload.get('action')
        status = payload.get('status')
        
        # Find the most recent dispatched command for this device and action
        command_log = request.env['farm.command.log'].sudo().search([
            ('device_id', '=', device.id),
            ('command', '=', action),
            ('status', '=', 'dispatched')
        ], order='create_date desc', limit=1)
        
        if command_log:
            vals = {
                'status': 'success' if status in ['ok', 'success', 'ACK'] else 'failed',
                'ack_timestamp': datetime.now(),
            }
            if status == 'failed':
                vals['error_log'] = json.dumps(payload.get('raw_response', {}))
            command_log.write(vals)
            _logger.info(f"Command {action} ACK received for log {command_log.id}")

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