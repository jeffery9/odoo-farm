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
            # For production, you might want to specify ca_certs
            # self.client.tls_insecure_set(False)  # Only for testing with self-signed certificates

    def connect(self):
        """Connect to the MQTT broker"""
        try:
            self.client.connect(
                settings.MQTT_BROKER_HOST,
                settings.MQTT_BROKER_PORT,
                keepalive=60
            )
            self.connected = True
            logger.info(f"Connected to MQTT broker at {settings.MQTT_BROKER_HOST}:{settings.MQTT_BROKER_PORT}")
        except Exception as e:
            logger.error(f"Failed to connect to MQTT broker: {str(e)}")
            raise

    def disconnect(self):
        """Disconnect from the MQTT broker"""
        try:
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

        Args:
            topic: MQTT topic to publish to
            payload: Message payload as string
            qos: Quality of Service level (0, 1, or 2)
            retain: Whether to retain the message

        Returns:
            True if publish was successful, False otherwise
        """
        try:
            result = self.client.publish(topic, payload, qos=qos, retain=retain)

            # The result is a tuple (rc, mid) where rc is the result code
            # 0 means success
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                logger.debug(f"Published message to {topic}: {payload[:100]}...")
                return True
            else:
                logger.error(f"Failed to publish message to {topic}, result code: {result.rc}")
                return False
        except Exception as e:
            logger.error(f"Exception while publishing to {topic}: {str(e)}")
            return False

    def subscribe(self, topic: str, qos: int = 1) -> bool:
        """
        Subscribe to an MQTT topic

        Args:
            topic: MQTT topic to subscribe to
            qos: Quality of Service level

        Returns:
            True if subscription was successful, False otherwise
        """
        try:
            result = self.client.subscribe(topic, qos=qos)
            if result[0] == mqtt.MQTT_ERR_SUCCESS:
                logger.debug(f"Subscribed to topic: {topic}")
                return True
            else:
                logger.error(f"Failed to subscribe to {topic}, result code: {result[0]}")
                return False
        except Exception as e:
            logger.error(f"Exception while subscribing to {topic}: {str(e)}")
            return False

    def loop(self):
        """
        Process MQTT network traffic.
        This should be called regularly to handle incoming messages and maintain the connection.
        """
        try:
            self.client.loop(timeout=0.01)
        except Exception as e:
            logger.error(f"Error in MQTT loop: {str(e)}")
            self.connected = False

    def send_device_command(self, device_id: str, command: Dict[str, Any]) -> bool:
        """
        Send a command to a specific device

        Args:
            device_id: ID of the target device
            command: Command dictionary containing action and parameters

        Returns:
            True if command was sent successfully, False otherwise
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

        Args:
            device_id: ID of the target device
            ota_info: OTA information dictionary

        Returns:
            True if notification was sent successfully, False otherwise
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

        Args:
            device_id: ID of the target device
            command: OTA command dictionary

        Returns:
            True if command was sent successfully, False otherwise
        """
        try:
            topic = settings.MQTT_OTA_NOTIFY_TOPIC_TEMPLATE.format(device=device_id)  # OTA commands use notify topic
            payload = json.dumps(command)
            return self.publish(topic, payload)
        except Exception as e:
            logger.error(f"Error sending OTA command to device {device_id}: {str(e)}")
            return False