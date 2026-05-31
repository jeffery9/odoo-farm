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
from services.subscription_manager import SubscriptionManager
from services.persistence_manager import PersistenceManager


class MQTTBridge:
    """
    Main MQTT Bridge class that manages the connection between MQTT and HTTP services
    """

    def __init__(self):
        self.mqtt_service = MQTTService()
        self.http_service = HTTPService()
        self.device_manager = DeviceManager()
        self.subscription_manager = SubscriptionManager()
        self.persistence_manager = PersistenceManager()
        self.app = FastAPI(
            title="Industrial IoT MQTT Bridge",
            description="Bridge between MQTT devices and Odoo HTTP webhooks",
            version="1.0.0"
        )
        self.loop = None  # To be captured on start
        self.setup_routes()
        self.setup_mqtt_callbacks()

    def setup_routes(self):
        """Setup FastAPI routes for the bridge"""

        @self.app.get("/")
        async def root():
            return {"message": "Industrial IoT MQTT Bridge", "status": "running"}

        @self.app.post("/api/v1/webhook")
        async def odoo_webhook_callback(data: Dict[str, Any]):
            """
            Unified callback endpoint for Odoo.
            Handles various events like command execution, configuration sync, etc.
            """
            event = data.get("event")
            payload = data.get("payload", {})
            
            logger.info(f"Received webhook event from Odoo: {event}")
            
            if event == "command":
                # Route to existing command logic
                device_id = payload.get("device_id")
                action = payload.get("action")
                params = payload.get("params", {})
                
                success = await self.mqtt_service.send_device_command(device_id, {"action": action, "params": params})
                return {"status": "success" if success else "error"}
            
            elif event == "subscribe":
                # Register a new webhook subscription from Odoo
                callback_url = payload.get("callback_url")
                events = payload.get("events", ["telemetry"])
                
                if not callback_url:
                    return {"status": "error", "message": "Missing callback_url"}
                
                for e in events:
                    await self.subscription_manager.register_subscription(e, callback_url)
                
                return {"status": "success", "message": f"Subscribed to {events}"}

            elif event == "ping":
                return {"status": "pong", "timestamp": datetime.utcnow().isoformat()}
                
            return {"status": "ignored", "message": f"Unknown event: {event}"}

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
                logger.debug(f"Received MQTT message on topic: {msg.topic}")

                if not self.loop:
                    logger.error("Event loop not yet captured, cannot handle message")
                    return

                # Parse the message payload
                try:
                    payload = json.loads(msg.payload.decode())
                except json.JSONDecodeError:
                    logger.error(f"Invalid JSON in message: {msg.payload}")
                    return

                # Route message based on topic using thread-safe async call
                coro = None
                if settings.MQTT_CONFIG_REQUEST_TOPIC in msg.topic:
                    coro = self.handle_config_request(payload)
                elif "telemetry" in msg.topic:
                    coro = self.handle_telemetry_data(msg.topic, payload)
                elif "ota" in msg.topic and "status" in msg.topic:
                    coro = self.handle_ota_status(msg.topic, payload)
                elif "command" in msg.topic and "response" in msg.topic:
                    coro = self.handle_command_response(msg.topic, payload)
                
                if coro:
                    asyncio.run_coroutine_threadsafe(coro, self.loop)
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
        """Handle telemetry data from device and forward to all subscribers"""
        try:
            # Extract device_id from topic
            topic_parts = topic.split('/')
            if len(topic_parts) >= 2:
                device_id = topic_parts[1]
            else:
                logger.error(f"Invalid topic format: {topic}")
                return

            logger.info(f"Processing telemetry for device: {device_id}")

            # Find all subscribers for 'telemetry' event
            subscribers = await self.subscription_manager.get_subscriptions('telemetry')
            
            # If no dynamic subscribers, use Odoo default
            if not subscribers:
                odoo_url = f"{settings.ODOO_BASE_URL}{settings.ODOO_WEBHOOK_ENDPOINT}/{device_id}"
                subscribers = [odoo_url]

            # Dispatch to all subscribers
            success = await self._dispatch_to_subscribers(subscribers, device_id, topic, payload)
            
            if not success:
                logger.warning(f"All webhook dispatches failed for {device_id}, storing in persistence")
                await self.persistence_manager.store_telemetry(device_id, topic, payload)

        except Exception as e:
            logger.error(f"Error handling telemetry data: {str(e)}")

    async def _dispatch_to_subscribers(self, subscribers: List[str], device_id: str, topic: str, payload: Dict) -> bool:
        """Helper to dispatch to multiple subscribers and return success if at least one succeeded"""
        dispatch_tasks = []
        for url in subscribers:
            dispatch_tasks.append(
                self.http_service.dispatch_webhook(url, device_id, topic, payload)
            )
        
        if not dispatch_tasks:
            return False
            
        results = await asyncio.gather(*dispatch_tasks)
        # Consider it success if at least one Odoo endpoint (or subscriber) acknowledged
        return any(r.get("status") == "success" for r in results if isinstance(r, dict))

    async def handle_ota_status(self, topic: str, payload: Dict):
        """Handle OTA status updates from device and forward to all subscribers"""
        try:
            # Extract device_id from topic
            topic_parts = topic.split('/')
            if len(topic_parts) >= 2:
                device_id = topic_parts[1]
            else:
                logger.error(f"Invalid topic format: {topic}")
                return

            logger.info(f"Processing OTA status for device: {device_id}")

            # Find all subscribers for 'ota_status' event
            subscribers = await self.subscription_manager.get_subscriptions('ota_status')
            
            if not subscribers:
                logger.warning(f"No subscribers for ota_status event from device {device_id}")
                return

            # Dispatch to all subscribers
            dispatch_tasks = []
            for url in subscribers:
                dispatch_tasks.append(
                    self.http_service.dispatch_webhook(url, device_id, f"ota/{device_id}/status", payload)
                )
            
            if dispatch_tasks:
                await asyncio.gather(*dispatch_tasks)

        except Exception as e:
            logger.error(f"Error handling OTA status: {str(e)}")

    async def handle_command_response(self, topic: str, payload: Dict):
        """Handle command responses from devices and notify subscribers (Loop Closure)"""
        try:
            # Extract device_id from topic
            topic_parts = topic.split('/')
            if len(topic_parts) >= 2:
                device_id = topic_parts[1]
            else:
                logger.error(f"Invalid topic format: {topic}")
                return

            logger.info(f"Processing command response from device: {device_id}")

            action = payload.get('action')
            status = payload.get('status', 'unknown')
            
            # Find all subscribers for 'command_ack' event
            subscribers = await self.subscription_manager.get_subscriptions('command_ack')
            
            # If no dynamic subscribers, try Odoo default
            if not subscribers:
                odoo_url = f"{settings.ODOO_BASE_URL}{settings.ODOO_WEBHOOK_ENDPOINT}/{device_id}"
                subscribers = [odoo_url]

            # Dispatch ACK to all subscribers
            ack_payload = {
                "event": "command_ack",
                "device_id": device_id,
                "action": action,
                "status": status,
                "raw_response": payload,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            await self._dispatch_to_subscribers(subscribers, device_id, f"command/{device_id}/response", ack_payload)

        except Exception as e:
            logger.error(f"Error handling command response: {str(e)}")

    async def heartbeat_loop(self):
        """Background task to keep the bridge registered with Odoo"""
        while True:
            try:
                await self.http_service.register_bridge()
            except Exception as e:
                logger.error(f"Heartbeat registration failed: {str(e)}")
            
            # Wait for 1 minute before next heartbeat
            await asyncio.sleep(60)

    async def persistence_forward_loop(self):
        """Background task to retry sending stored telemetries from local database"""
        while True:
            try:
                queued_records = await self.persistence_manager.get_queued_telemetry(limit=20)
                if queued_records:
                    logger.info(f"Persistence: Attempting to forward {len(queued_records)} queued records")
                    
                    for record in queued_records:
                        device_id = record['device_id']
                        topic = record['topic']
                        payload = json.loads(record['payload'])
                        
                        # Find all subscribers for 'telemetry' event
                        subscribers = await self.subscription_manager.get_subscriptions('telemetry')
                        
                        # If no dynamic subscribers, try Odoo default
                        if not subscribers:
                            odoo_url = f"{settings.ODOO_BASE_URL}{settings.ODOO_WEBHOOK_ENDPOINT}/{device_id}"
                            subscribers = [odoo_url]

                        success = await self._dispatch_to_subscribers(subscribers, device_id, topic, payload)
                        
                        if success:
                            await self.persistence_manager.delete_telemetry(record['id'])
                        else:
                            await self.persistence_manager.increment_retry(record['id'])
                            # If forwarding fails, wait a bit before next attempt
                            break 
            except Exception as e:
                logger.error(f"Error in persistence forward loop: {str(e)}")
            
            await asyncio.sleep(30)

    async def start(self):
        """Start the MQTT bridge"""
        try:
            # Capture the current event loop for thread-safe callbacks
            self.loop = asyncio.get_running_loop()

            # Initialize persistence database
            await self.persistence_manager.initialize()

            # 1. Fetch remote configuration from Odoo
            logger.info("Fetching bridge configuration from Odoo...")
            config_result = await self.http_service.fetch_gateway_config()
            
            mqtt_args = {}
            if config_result.get("status") == "success":
                mqtt_config = config_result.get("mqtt", {})
                mqtt_args = {
                    'host': mqtt_config.get('host'),
                    'port': mqtt_config.get('port'),
                    'username': mqtt_config.get('user'),
                    'password': mqtt_config.get('password'),
                    'use_tls': mqtt_config.get('use_tls'),
                }
                logger.info(f"Using remote MQTT config: {mqtt_args['host']}:{mqtt_args['port']}")
            else:
                logger.warning(f"Failed to fetch remote config, using local defaults: {config_result.get('error')}")

            # 2. Connect to MQTT broker (starts background threaded loop)
            self.mqtt_service.connect(**mqtt_args)

            # 3. Start heartbeat registration in the background
            asyncio.create_task(self.heartbeat_loop())

            # 4. Start persistence forwarder in the background
            asyncio.create_task(self.persistence_forward_loop())

            # Start the FastAPI app
            config = uvicorn.Config(
                self.app,
                host=settings.HOST,
                port=settings.PORT,
                log_level="info"
            )
            server = uvicorn.Server(config)
            
            logger.info(f"FastAPI server starting on {settings.HOST}:{settings.PORT}")
            await server.serve()

        except Exception as e:
            logger.error(f"Error starting MQTT bridge: {str(e)}")
            if self.mqtt_service.is_connected():
                self.mqtt_service.disconnect()
            raise


# Initialize the bridge
bridge = MQTTBridge()

if __name__ == "__main__":
    import asyncio

    async def main():
        await bridge.start()

    asyncio.run(main())