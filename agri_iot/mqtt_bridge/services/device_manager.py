"""
Device Manager for the Industrial IoT Bridge
Handles device state management and caching
"""

import asyncio
import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class DeviceManager:
    """
    Service class for managing device state, caching, and metadata
    """

    def __init__(self):
        self.device_configs = {}  # Cache for device configurations
        self.device_connections = {}  # Track connected devices
        self.device_last_seen = {}  # Track last activity
        self.command_queue = {}  # Queue for pending commands
        self._lock = asyncio.Lock()  # Thread-safe operations

    async def set_device_config(self, device_id: str, config: Dict[str, Any]):
        """
        Cache device configuration

        Args:
            device_id: Device identifier
            config: Configuration data from Odoo
        """
        async with self._lock:
            self.device_configs[device_id] = {
                'config': config,
                'timestamp': datetime.utcnow(),
                'mqtt_config': config.get('mqtt', {}),
                'topics': config.get('topics', {})
            }
            logger.info(f"Stored configuration for device: {device_id}")

    async def get_device_config(self, device_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve cached device configuration

        Args:
            device_id: Device identifier

        Returns:
            Device configuration if available, None otherwise
        """
        async with self._lock:
            if device_id in self.device_configs:
                config = self.device_configs[device_id]
                # Check if config is still valid (not expired)
                if datetime.utcnow() < config['timestamp'] + timedelta(hours=1):  # 1 hour TTL
                    return config
                else:
                    # Remove expired config
                    del self.device_configs[device_id]
                    logger.info(f"Removed expired configuration for device: {device_id}")
            return None

    async def register_device_connection(self, device_id: str):
        """
        Register a device connection

        Args:
            device_id: Device identifier
        """
        async with self._lock:
            self.device_connections[device_id] = datetime.utcnow()
            self.device_last_seen[device_id] = datetime.utcnow()
            logger.info(f"Device connected: {device_id}")

    async def unregister_device_connection(self, device_id: str):
        """
        Unregister a device connection

        Args:
            device_id: Device identifier
        """
        async with self._lock:
            if device_id in self.device_connections:
                del self.device_connections[device_id]
            logger.info(f"Device disconnected: {device_id}")

    async def update_device_last_seen(self, device_id: str):
        """
        Update the last seen timestamp for a device

        Args:
            device_id: Device identifier
        """
        async with self._lock:
            self.device_last_seen[device_id] = datetime.utcnow()

    async def get_connected_devices(self) -> Dict[str, datetime]:
        """
        Get all currently connected devices

        Returns:
            Dictionary mapping device IDs to connection timestamps
        """
        async with self._lock:
            return self.device_connections.copy()

    async def is_device_connected(self, device_id: str) -> bool:
        """
        Check if a device is currently connected

        Args:
            device_id: Device identifier

        Returns:
            True if device is connected, False otherwise
        """
        async with self._lock:
            return device_id in self.device_connections

    async def queue_command(self, device_id: str, command: Dict[str, Any]):
        """
        Queue a command for a device

        Args:
            device_id: Device identifier
            command: Command to queue
        """
        async with self._lock:
            if device_id not in self.command_queue:
                self.command_queue[device_id] = []
            self.command_queue[device_id].append({
                'command': command,
                'timestamp': datetime.utcnow(),
                'id': f"cmd_{datetime.utcnow().timestamp()}"
            })
            logger.info(f"Queued command for device {device_id}: {command.get('action')}")

    async def get_pending_commands(self, device_id: str) -> list:
        """
        Get pending commands for a device

        Args:
            device_id: Device identifier

        Returns:
            List of pending commands
        """
        async with self._lock:
            return self.command_queue.get(device_id, [])

    async def clear_commands(self, device_id: str):
        """
        Clear all pending commands for a device

        Args:
            device_id: Device identifier
        """
        async with self._lock:
            if device_id in self.command_queue:
                del self.command_queue[device_id]
                logger.info(f"Cleared command queue for device: {device_id}")

    async def cleanup_expired_configs(self):
        """
        Remove expired configurations from cache
        """
        async with self._lock:
            expired_devices = []
            now = datetime.utcnow()

            for device_id, config in self.device_configs.items():
                if now > config['timestamp'] + timedelta(hours=1):  # 1 hour TTL
                    expired_devices.append(device_id)

            for device_id in expired_devices:
                del self.device_configs[device_id]
                logger.info(f"Cleaned up expired config for device: {device_id}")

    async def get_device_status(self, device_id: str) -> Dict[str, Any]:
        """
        Get complete status for a specific device

        Args:
            device_id: Device identifier

        Returns:
            Device status information
        """
        async with self._lock:
            is_connected = await self.is_device_connected(device_id)
            config = await self.get_device_config(device_id)
            last_seen = self.device_last_seen.get(device_id)
            pending_commands = len(await self.get_pending_commands(device_id))

            status = {
                "device_id": device_id,
                "connected": is_connected,
                "has_config": config is not None,
                "last_seen": last_seen.isoformat() if last_seen else None,
                "pending_commands": pending_commands
            }

            if config:
                status["mqtt_client_id"] = config['mqtt_config'].get('client_id')
                status["firmware_version"] = config.get('firmware_version')

            return status

    async def get_all_device_statuses(self) -> Dict[str, Dict[str, Any]]:
        """
        Get status for all registered devices

        Returns:
            Dictionary mapping device IDs to their status information
        """
        async with self._lock:
            all_connected = await self.get_connected_devices()
            statuses = {}

            # Add status for connected devices
            for device_id in all_connected:
                statuses[device_id] = await self.get_device_status(device_id)

            # Add status for devices with cached configs but not connected
            for device_id in self.device_configs:
                if device_id not in statuses:
                    statuses[device_id] = await self.get_device_status(device_id)

            return statuses