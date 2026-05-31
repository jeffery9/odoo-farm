"""
MQTT Service for the Industrial IoT Bridge
"""

import json
import ssl
import logging
from typing import Optional, Dict, Any
import paho.mqtt.client as mqtt

from config.settings import settings

logger = logging.getLogger(__name__)


class MQTTService:
    """
    Service class for handling MQTT connections and operations
    """

    def __init__(self):
        self.client = mqtt.Client(client_id=settings.MQTT_CLIENT_ID)
        self.connected = False

        # Set up authentication if credentials are provided
        if settings.MQTT_BROKER_USERNAME and settings.MQTT_BROKER_PASSWORD:
            self.client.username_pw_set(settings.MQTT_BROKER_USERNAME, settings.MQTT_BROKER_PASSWORD)

        # Configure TLS if required
        if settings.MQTT_USE_TLS:
            self.client.tls_set(
                cert_reqs=ssl.CERT_REQUIRED,
                tls_version=ssl.PROTOCOL_TLS,
            )

    def connect(self, host: Optional[str] = None, port: Optional[int] = None, username: Optional[str] = None, password: Optional[str] = None, use_tls: Optional[bool] = None):
        """Connect to the MQTT broker and start the background loop"""
        target_host = host or settings.MQTT_BROKER_HOST
        target_port = port or settings.MQTT_BROKER_PORT
        target_user = username or settings.MQTT_BROKER_USERNAME
        target_pass = password or settings.MQTT_BROKER_PASSWORD
        target_tls = use_tls if use_tls is not None else settings.MQTT_USE_TLS

        try:
            # Re-configure client if credentials provided
            if target_user and target_pass:
                self.client.username_pw_set(target_user, target_pass)

            if target_tls:
                try:
                    self.client.tls_set(
                        cert_reqs=ssl.CERT_REQUIRED,
                        tls_version=ssl.PROTOCOL_TLS,
                    )
                except:
                    # If already configured, ignore
                    pass

            self.client.connect(
                target_host,
                target_port,
                keepalive=60
            )
            self.client.loop_start()  # Start the multi-threaded loop
            self.connected = True
            logger.info(f"Connected to MQTT broker at {target_host}:{target_port}")
        except Exception as e:
            logger.error(f"Failed to connect to MQTT broker: {str(e)}")
            raise

    def disconnect(self):
        """Disconnect from the MQTT broker and stop the background loop"""
        try:
            self.client.loop_stop()  # Stop the multi-threaded loop
            self.client.disconnect()
            self.connected = False
            logger.info("Disconnected from MQTT broker")
        except Exception as e:
            logger.error(f"Error disconnecting from MQTT broker: {str(e)}")

    def is_connected(self) -> bool:
        """Check if the MQTT client is connected"""
        return self.connected

    def publish(self, topic: str, payload: str, qos: int = 1, retain: bool = False) -> bool:
        """
        Publish a message to an MQTT topic
        """
        try:
            result = self.client.publish(topic, payload, qos=qos, retain=retain)
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                logger.debug(f"Published message to {topic}")
                return True
            else:
                logger.error(f"Failed to publish to {topic}, rc: {result.rc}")
                return False
        except Exception as e:
            logger.error(f"Exception publishing to {topic}: {str(e)}")
            return False

    def subscribe(self, topic: str, qos: int = 1) -> bool:
        """
        Subscribe to an MQTT topic
        """
        try:
            result = self.client.subscribe(topic, qos=qos)
            if result[0] == mqtt.MQTT_ERR_SUCCESS:
                logger.debug(f"Subscribed to topic: {topic}")
                return True
            else:
                logger.error(f"Failed to subscribe to {topic}, rc: {result[0]}")
                return False
        except Exception as e:
            logger.error(f"Exception subscribing to {topic}: {str(e)}")
            return False

    def send_device_command(self, device_id: str, command: Dict[str, Any]) -> bool:
        """
        Send a command to a specific device
        """
        try:
            topic = settings.MQTT_COMMAND_TOPIC_TEMPLATE.format(device=device_id)
            payload = json.dumps(command)
            return self.publish(topic, payload)
        except Exception as e:
            logger.error(f"Error sending command to device {device_id}: {str(e)}")
            return False

    def send_ota_notification(self, device_id: str, ota_info: Dict[str, Any]) -> bool:
        """
        Send an OTA notification to a specific device
        """
        try:
            topic = settings.MQTT_OTA_NOTIFY_TOPIC_TEMPLATE.format(device=device_id)
            payload = json.dumps(ota_info)
            return self.publish(topic, payload)
        except Exception as e:
            logger.error(f"Error sending OTA notification to device {device_id}: {str(e)}")
            return False

    def send_ota_command(self, device_id: str, command: Dict[str, Any]) -> bool:
        """
        Send an OTA command to a specific device
        """
        try:
            topic = settings.MQTT_OTA_NOTIFY_TOPIC_TEMPLATE.format(device=device_id)
            payload = json.dumps(command)
            return self.publish(topic, payload)
        except Exception as e:
            logger.error(f"Error sending OTA command to device {device_id}: {str(e)}")
            return False
