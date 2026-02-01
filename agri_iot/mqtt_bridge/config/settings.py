"""
Configuration settings for the MQTT Bridge
"""

import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    # MQTT Broker Configuration
    MQTT_BROKER_HOST: str = os.getenv("MQTT_BROKER_HOST", "mqtt.factory.com")
    MQTT_BROKER_PORT: int = int(os.getenv("MQTT_BROKER_PORT", "8883"))
    MQTT_BROKER_USERNAME: str = os.getenv("MQTT_BROKER_USERNAME", "")
    MQTT_BROKER_PASSWORD: str = os.getenv("MQTT_BROKER_PASSWORD", "")
    MQTT_USE_TLS: bool = os.getenv("MQTT_USE_TLS", "True").lower() == "true"
    MQTT_CLIENT_ID: str = os.getenv("MQTT_CLIENT_ID", f"iiot_bridge_{os.getpid()}")

    # Odoo HTTP Webhook Configuration
    ODOO_BASE_URL: str = os.getenv("ODOO_BASE_URL", "http://localhost:8069")
    ODOO_CONFIG_ENDPOINT: str = os.getenv("ODOO_CONFIG_ENDPOINT", "/iiot/config")
    ODOO_WEBHOOK_ENDPOINT: str = os.getenv("ODOO_WEBHOOK_ENDPOINT", "/iiot/webhook")
    ODOO_COMMAND_ENDPOINT: str = os.getenv("ODOO_COMMAND_ENDPOINT", "/iiot/command")

    # Topic Configuration
    MQTT_CONFIG_REQUEST_TOPIC: str = os.getenv("MQTT_CONFIG_REQUEST_TOPIC", "iiot/config/request")
    MQTT_CONFIG_RESPONSE_TOPIC: str = os.getenv("MQTT_CONFIG_RESPONSE_TOPIC", "iiot/config/{device}")
    MQTT_TELEMETRY_TOPIC_TEMPLATE: str = os.getenv("MQTT_TELEMETRY_TOPIC_TEMPLATE", "telemetry/{device}/data")
    MQTT_COMMAND_TOPIC_TEMPLATE: str = os.getenv("MQTT_COMMAND_TOPIC_TEMPLATE", "command/{device}/action")
    MQTT_OTA_NOTIFY_TOPIC_TEMPLATE: str = os.getenv("MQTT_OTA_NOTIFY_TOPIC_TEMPLATE", "ota/{device}/notify")
    MQTT_OTA_STATUS_TOPIC_TEMPLATE: str = os.getenv("MQTT_OTA_STATUS_TOPIC_TEMPLATE", "ota/{device}/status")

    # HTTP Server Configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))

    # API Keys and Security
    ODOO_API_KEY: str = os.getenv("ODOO_API_KEY", "")
    BRIDGE_API_KEY: str = os.getenv("BRIDGE_API_KEY", "")

    # Connection and Retry Settings
    MQTT_CONNECT_RETRY_INTERVAL: int = int(os.getenv("MQTT_CONNECT_RETRY_INTERVAL", "5"))
    HTTP_REQUEST_TIMEOUT: int = int(os.getenv("HTTP_REQUEST_TIMEOUT", "30"))
    HTTP_RETRY_COUNT: int = int(os.getenv("HTTP_RETRY_COUNT", "3"))
    HTTP_RETRY_DELAY: float = float(os.getenv("HTTP_RETRY_DELAY", "1.0"))

    # Device Management
    DEVICE_CACHE_TTL: int = int(os.getenv("DEVICE_CACHE_TTL", "3600"))  # 1 hour
    MAX_DEVICE_CONNECTIONS: int = int(os.getenv("MAX_DEVICE_CONNECTIONS", "1000"))

    class Config:
        env_file = ".env"
        case_sensitive = True


# Initialize settings
settings = Settings()