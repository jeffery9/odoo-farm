"""
FastAPI MQTT Bridge for Industrial IoT (IIoT) Integration

This module implements an MQTT bridge that connects MQTT devices to Odoo's HTTP webhooks,
facilitating device configuration download, telemetry data processing, command and control,
and OTA update management.

The bridge acts as an intermediary between MQTT brokers and Odoo, handling:
- Device configuration requests via HTTP webhook to Odoo
- Telemetry data forwarding from MQTT to Odoo
- Command routing from Odoo to MQTT devices
- OTA update notifications and status updates
"""

import asyncio
import json
import logging
import uuid
from datetime import datetime
from typing import Dict, Optional, Any

import httpx
import uvicorn
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
import paho.mqtt.client as mqtt

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import bridge components
from config.settings import settings
from models.message import DeviceConfigRequest, TelemetryData, CommandMessage, OTAStatus
from services.mqtt_service import MQTTService
from services.http_service import HTTPService
from services.device_manager import DeviceManager


class MQTTBridge:
    """
    Main MQTT Bridge class that manages the connection between MQTT and HTTP services
    """

    def __init__(self):
        self.mqtt_service = MQTTService()
        self.http_service = HTTPService()
        self.device_manager = DeviceManager()
        self.app = FastAPI(
            title="Industrial IoT MQTT Bridge",
            description="Bridge between MQTT devices and Odoo HTTP webhooks",
            version="1.0.0"
        )
        self.setup_routes()
        self.setup_mqtt_callbacks()

    def setup_routes(self):
        """Setup FastAPI routes for the bridge"""

        @self.app.get("/")
        async def root():
            return {"message": "Industrial IoT MQTT Bridge", "status": "running"}

        @self.app.get("/health")
        async def health_check():
            connected_devices = await self.device_manager.get_connected_devices()
            return {
                "status": "healthy",
                "mqtt_connected": self.mqtt_service.is_connected(),
                "active_connections": len(connected_devices),
                "timestamp": datetime.utcnow().isoformat()
            }

        @self.app.post("/api/v1/config/download")
        async def download_device_config(request: DeviceConfigRequest):
            """Handle device configuration download request"""
            try:
                # Forward request to Odoo
                config_response = await self.http_service.get_device_config(
                    request.serial, request.token
                )

                if config_response.get("status") == "success":
                    # Cache the configuration for the device
                    device_id = config_response.get("device_id")
                    if device_id:
                        await self.device_manager.set_device_config(
                            device_id, config_response
                        )

                    return config_response
                else:
                    return config_response

            except Exception as e:
                logger.error(f"Error getting device config: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.post("/api/v1/command/send")
        async def send_device_command(command: CommandMessage):
            """Send a command to a specific device"""
            try:
                device_id = command.device_id
                action = command.action
                params = command.params or {}

                logger.info(f"Sending command {action} to device {device_id}")

                # Check if device is configured
                device_config = await self.device_manager.get_device_config(device_id)
                if not device_config:
                    # Try to get device config from Odoo
                    logger.warning(f"No cached config for {device_id}, attempting to refresh")
                    # Note: In a real scenario, we might need to implement a way to refresh config
                    # For now, we'll proceed with the command assuming the device exists

                # Send command via MQTT
                command_payload = {
                    "action": action,
                    "params": params,
                    "timestamp": command.timestamp.isoformat()
                }

                success = await self.mqtt_service.send_device_command(device_id, command_payload)

                if success:
                    return {
                        "status": "success",
                        "message": f"Command {action} sent to device {device_id}",
                        "command_id": command.device_id
                    }
                else:
                    return {
                        "status": "error",
                        "error": f"Failed to send command {action} to device {device_id}"
                    }

            except Exception as e:
                logger.error(f"Error sending command: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/api/v1/device/{device_id}/status")
        async def get_device_status(device_id: str):
            """Get status of a specific device"""
            try:
                status = await self.device_manager.get_device_status(device_id)
                return status
            except Exception as e:
                logger.error(f"Error getting device status: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/api/v1/devices/status")
        async def get_all_device_statuses():
            """Get status of all known devices"""
            try:
                statuses = await self.device_manager.get_all_device_statuses()
                return {"devices": statuses}
            except Exception as e:
                logger.error(f"Error getting device statuses: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.post("/api/v1/ota/send")
        async def send_ota_command(ota_command: CommandMessage):
            """Send an OTA command to a specific device"""
            try:
                device_id = ota_command.device_id
                action = ota_command.action
                params = ota_command.params or {}

                logger.info(f"Sending OTA command {action} to device {device_id}")

                # Prepare OTA command payload
                ota_payload = {
                    "action": action,
                    "params": params,
                    "timestamp": ota_command.timestamp.isoformat(),
                    "command_type": "ota"
                }

                # Send OTA command via MQTT
                success = await self.mqtt_service.send_ota_command(device_id, ota_payload)

                if success:
                    return {
                        "status": "success",
                        "message": f"OTA command {action} sent to device {device_id}",
                        "command_id": ota_command.device_id
                    }
                else:
                    return {
                        "status": "error",
                        "error": f"Failed to send OTA command {action} to device {device_id}"
                    }

            except Exception as e:
                logger.error(f"Error sending OTA command: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))

    def setup_mqtt_callbacks(self):
        """Setup MQTT client callbacks"""

        def on_connect(client, userdata, flags, rc):
            """Handle MQTT connection"""
            if rc == 0:
                logger.info("Successfully connected to MQTT broker")

                # Subscribe to device configuration requests
                client.subscribe(settings.MQTT_CONFIG_REQUEST_TOPIC)

                # Subscribe to device telemetry data
                client.subscribe(settings.MQTT_TELEMETRY_TOPIC_TEMPLATE.format(device="+/+"))

                # Subscribe to OTA status updates
                client.subscribe(settings.MQTT_OTA_STATUS_TOPIC_TEMPLATE.format(device="+/+"))

                logger.info(f"Subscribed to topics: {settings.MQTT_CONFIG_REQUEST_TOPIC}, {settings.MQTT_TELEMETRY_TOPIC_TEMPLATE.format(device='+/+')}, {settings.MQTT_OTA_STATUS_TOPIC_TEMPLATE.format(device='+/+')}")
            else:
                logger.error(f"Failed to connect to MQTT broker, return code {rc}")

        def on_message(client, userdata, msg):
            """Handle incoming MQTT messages"""
            try:
                logger.info(f"Received MQTT message on topic: {msg.topic}")

                # Parse the message payload
                try:
                    payload = json.loads(msg.payload.decode())
                except json.JSONDecodeError:
                    logger.error(f"Invalid JSON in message: {msg.payload}")
                    return

                # Route message based on topic
                if settings.MQTT_CONFIG_REQUEST_TOPIC in msg.topic:
                    asyncio.create_task(self.handle_config_request(payload))
                elif "telemetry" in msg.topic:
                    asyncio.create_task(self.handle_telemetry_data(msg.topic, payload))
                elif "ota" in msg.topic and "status" in msg.topic:
                    asyncio.create_task(self.handle_ota_status(msg.topic, payload))
                elif "command" in msg.topic and "response" in msg.topic:
                    asyncio.create_task(self.handle_command_response(msg.topic, payload))
                else:
                    logger.warning(f"Unknown topic: {msg.topic}")

            except Exception as e:
                logger.error(f"Error handling MQTT message: {str(e)}")

        def on_disconnect(client, userdata, rc):
            """Handle MQTT disconnection"""
            logger.warning(f"Disconnected from MQTT broker, return code {rc}")
            if rc != 0:
                # Attempt to reconnect
                logger.info("Attempting to reconnect to MQTT broker...")
                try:
                    client.reconnect()
                except Exception as e:
                    logger.error(f"Failed to reconnect: {str(e)}")

        self.mqtt_service.client.on_connect = on_connect
        self.mqtt_service.client.on_message = on_message
        self.mqtt_service.client.on_disconnect = on_disconnect

    async def handle_config_request(self, payload: Dict):
        """Handle device configuration request from MQTT"""
        try:
            serial = payload.get('serial')
            token = payload.get('token')

            if not serial or not token:
                logger.error("Missing serial or token in config request")
                return

            logger.info(f"Processing config request for device: {serial}")

            # Request configuration from Odoo
            config_response = await self.http_service.get_device_config(serial, token)

            if config_response.get("status") == "success":
                device_id = config_response.get("device_id")
                mqtt_config = config_response.get("mqtt", {})
                topics = config_response.get("topics", {})

                # Send configuration back to device via MQTT
                config_topic = settings.MQTT_CONFIG_RESPONSE_TOPIC.format(device=device_id)

                device_config = {
                    "device_id": device_id,
                    "mqtt_config": mqtt_config,
                    "topics": topics,
                    "timestamp": datetime.utcnow().isoformat()
                }

                await self.mqtt_service.publish(config_topic, json.dumps(device_config))

                logger.info(f"Sent configuration to device: {device_id}")

                # Cache the configuration
                await self.device_manager.set_device_config(device_id, config_response)
            else:
                error_msg = {
                    "error": config_response.get("error", "Unknown error"),
                    "timestamp": datetime.utcnow().isoformat()
                }

                # Send error response (assuming we can get device_id from token lookup)
                # In a real scenario, might need to look up device_id from serial
                error_topic = settings.MQTT_CONFIG_RESPONSE_TOPIC.format(device=serial)
                await self.mqtt_service.publish(error_topic, json.dumps(error_msg))

        except Exception as e:
            logger.error(f"Error handling config request: {str(e)}")

    async def handle_telemetry_data(self, topic: str, payload: Dict):
        """Handle telemetry data from device and forward to Odoo"""
        try:
            # Extract device_id from topic
            # Assuming topic format like: telemetry/{device_id}/data
            topic_parts = topic.split('/')
            if len(topic_parts) >= 2:
                device_id = topic_parts[1]  # Extract device_id from topic
            else:
                logger.error(f"Invalid topic format: {topic}")
                return

            logger.info(f"Processing telemetry for device: {device_id}")

            # Forward telemetry to Odoo via webhook
            telemetry_response = await self.http_service.send_telemetry(
                device_id, topic, payload
            )

            if telemetry_response.get("status") == "success":
                logger.info(f"Telemetry forwarded successfully for device: {device_id}")
            else:
                logger.error(f"Failed to forward telemetry: {telemetry_response.get('error')}")

        except Exception as e:
            logger.error(f"Error handling telemetry data: {str(e)}")

    async def handle_ota_status(self, topic: str, payload: Dict):
        """Handle OTA status updates from device and forward to Odoo"""
        try:
            # Extract device_id from topic
            # Assuming topic format like: ota/{device_id}/status
            topic_parts = topic.split('/')
            if len(topic_parts) >= 2:
                device_id = topic_parts[1]  # Extract device_id from topic
            else:
                logger.error(f"Invalid topic format: {topic}")
                return

            logger.info(f"Processing OTA status for device: {device_id}")

            # Forward OTA status to Odoo via webhook
            ota_response = await self.http_service.send_ota_status(
                device_id, payload
            )

            if ota_response.get("status") == "success":
                logger.info(f"OTA status forwarded successfully for device: {device_id}")
            else:
                logger.error(f"Failed to forward OTA status: {ota_response.get('error')}")

        except Exception as e:
            logger.error(f"Error handling OTA status: {str(e)}")

    async def handle_command_response(self, topic: str, payload: Dict):
        """Handle command responses from devices"""
        try:
            # Extract device_id from topic
            # Assuming topic format like: command/{device_id}/response
            topic_parts = topic.split('/')
            if len(topic_parts) >= 2:
                device_id = topic_parts[1]  # Extract device_id from topic
            else:
                logger.error(f"Invalid topic format: {topic}")
                return

            logger.info(f"Processing command response from device: {device_id}")

            # Process the command response (e.g., update command status in Odoo)
            # This could involve notifying Odoo about the command result
            action = payload.get('action')
            status = payload.get('status', 'unknown')
            result = payload.get('result')

            logger.info(f"Command {action} response from {device_id}: {status}")

            # In a real implementation, you might want to send this status back to Odoo
            # For example, to update a command tracking record in Odoo
            # await self.http_service.update_command_status(device_id, action, status, result)

        except Exception as e:
            logger.error(f"Error handling command response: {str(e)}")

    async def start(self):
        """Start the MQTT bridge"""
        try:
            # Connect to MQTT broker
            self.mqtt_service.connect()

            # Start the FastAPI app
            config = uvicorn.Config(
                self.app,
                host=settings.HOST,
                port=settings.PORT,
                log_level="info"
            )
            server = uvicorn.Server(config)

            # Run the server in a separate task
            server_task = asyncio.create_task(server.serve())

            # Keep the MQTT client running
            while True:
                self.mqtt_service.loop()
                await asyncio.sleep(0.01)  # Small delay to prevent blocking

        except KeyboardInterrupt:
            logger.info("Shutting down MQTT bridge...")
            self.mqtt_service.disconnect()
        except Exception as e:
            logger.error(f"Error starting MQTT bridge: {str(e)}")
            raise


# Initialize the bridge
bridge = MQTTBridge()

if __name__ == "__main__":
    import asyncio

    async def main():
        await bridge.start()

    asyncio.run(main())