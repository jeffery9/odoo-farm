"""
HTTP Service for the Industrial IoT Bridge
Handles communication with Odoo via HTTP webhooks
"""

import json
import logging
from typing import Dict, Any, Optional
import httpx
from httpx import TimeoutException, RequestError

from config.settings import settings

logger = logging.getLogger(__name__)


class HTTPService:
    """
    Service class for handling HTTP communication with Odoo
    """

    def __init__(self):
        # Create HTTP client with timeout
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(settings.HTTP_REQUEST_TIMEOUT, connect=settings.HTTP_REQUEST_TIMEOUT)
        )

    async def get_device_config(self, serial: str, token: str) -> Dict[str, Any]:
        """
        Request device configuration from Odoo

        Args:
            serial: Device serial number
            token: Configuration token

        Returns:
            Configuration response from Odoo
        """
        url = f"{settings.ODOO_BASE_URL}{settings.ODOO_CONFIG_ENDPOINT}"

        payload = {
            "serial": serial,
            "token": token
        }

        headers = {
            "Content-Type": "application/json"
        }

        if settings.ODOO_API_KEY:
            headers["Authorization"] = f"Bearer {settings.ODOO_API_KEY}"

        try:
            response = await self.client.post(url, json=payload, headers=headers)

            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to get device config: {response.status_code} - {response.text}")
                return {
                    "error": f"HTTP {response.status_code}: {response.text}",
                    "status": "error"
                }
        except TimeoutException:
            logger.error("Timeout while getting device config")
            return {
                "error": "Request timeout",
                "status": "error"
            }
        except RequestError as e:
            logger.error(f"Request error while getting device config: {str(e)}")
            return {
                "error": f"Request error: {str(e)}",
                "status": "error"
            }
        except Exception as e:
            logger.error(f"Error getting device config: {str(e)}")
            return {
                "error": str(e),
                "status": "error"
            }

    async def send_telemetry(self, device_id: str, topic: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send telemetry data to Odoo

        Args:
            device_id: Device identifier
            topic: MQTT topic where data was received
            payload: Telemetry data

        Returns:
            Response from Odoo
        """
        url = f"{settings.ODOO_BASE_URL}{settings.ODOO_WEBHOOK_ENDPOINT}/{device_id}"

        data = {
            "topic": topic,
            "payload": payload
        }

        headers = {
            "Content-Type": "application/json"
        }

        if settings.ODOO_API_KEY:
            headers["Authorization"] = f"Bearer {settings.ODOO_API_KEY}"

        try:
            response = await self.client.post(url, json=data, headers=headers)

            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to send telemetry: {response.status_code} - {response.text}")
                return {
                    "error": f"HTTP {response.status_code}: {response.text}",
                    "status": "error"
                }
        except TimeoutException:
            logger.error("Timeout while sending telemetry")
            return {
                "error": "Request timeout",
                "status": "error"
            }
        except RequestError as e:
            logger.error(f"Request error while sending telemetry: {str(e)}")
            return {
                "error": f"Request error: {str(e)}",
                "status": "error"
            }
        except Exception as e:
            logger.error(f"Error sending telemetry: {str(e)}")
            return {
                "error": str(e),
                "status": "error"
            }

    async def send_ota_status(self, device_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send OTA status update to Odoo

        Args:
            device_id: Device identifier
            payload: OTA status data

        Returns:
            Response from Odoo
        """
        url = f"{settings.ODOO_BASE_URL}{settings.ODOO_WEBHOOK_ENDPOINT}/{device_id}"

        data = {
            "topic": f"ota/{device_id}/status",
            "payload": payload
        }

        headers = {
            "Content-Type": "application/json"
        }

        if settings.ODOO_API_KEY:
            headers["Authorization"] = f"Bearer {settings.ODOO_API_KEY}"

        try:
            response = await self.client.post(url, json=data, headers=headers)

            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to send OTA status: {response.status_code} - {response.text}")
                return {
                    "error": f"HTTP {response.status_code}: {response.text}",
                    "status": "error"
                }
        except TimeoutException:
            logger.error("Timeout while sending OTA status")
            return {
                "error": "Request timeout",
                "status": "error"
            }
        except RequestError as e:
            logger.error(f"Request error while sending OTA status: {str(e)}")
            return {
                "error": f"Request error: {str(e)}",
                "status": "error"
            }
        except Exception as e:
            logger.error(f"Error sending OTA status: {str(e)}")
            return {
                "error": str(e),
                "status": "error"
            }

    async def send_command_to_device(self, device_id: str, action: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Send a command to a device through Odoo (for internal use)

        Args:
            device_id: Device identifier
            action: Command action
            params: Command parameters

        Returns:
            Response from Odoo
        """
        url = f"{settings.ODOO_BASE_URL}{settings.ODOO_COMMAND_ENDPOINT}/{device_id}"

        data = {
            "action": action,
            "params": params or {}
        }

        headers = {
            "Content-Type": "application/json"
        }

        if settings.ODOO_API_KEY:
            headers["Authorization"] = f"Bearer {settings.ODOO_API_KEY}"

        try:
            response = await self.client.post(url, json=data, headers=headers)

            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to send command: {response.status_code} - {response.text}")
                return {
                    "error": f"HTTP {response.status_code}: {response.text}",
                    "status": "error"
                }
        except TimeoutException:
            logger.error("Timeout while sending command")
            return {
                "error": "Request timeout",
                "status": "error"
            }
        except RequestError as e:
            logger.error(f"Request error while sending command: {str(e)}")
            return {
                "error": f"Request error: {str(e)}",
                "status": "error"
            }
        except Exception as e:
            logger.error(f"Error sending command: {str(e)}")
            return {
                "error": str(e),
                "status": "error"
            }

    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()