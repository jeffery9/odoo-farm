"""
Subscription Manager for the Industrial IoT Bridge
Handles dynamic webhook registrations from Odoo
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class SubscriptionManager:
    """
    Service class for managing dynamic webhook subscriptions from Odoo
    """

    def __init__(self):
        # Dictionary mapping event types to lists of callback URLs
        # Example: {"telemetry": ["http://odoo:8069/iiot/webhook"], "ota_status": [...]}
        self.subscriptions: Dict[str, List[str]] = {}
        self._lock = asyncio.Lock()

    async def register_subscription(self, event: str, callback_url: str):
        """
        Register a new webhook subscription for an event type

        Args:
            event: Event type (e.g., 'telemetry', 'ota_status')
            callback_url: Full URL to POST the event data to
        """
        async with self._lock:
            if event not in self.subscriptions:
                self.subscriptions[event] = []
            
            if callback_url not in self.subscriptions[event]:
                self.subscriptions[event].append(callback_url)
                logger.info(f"Registered new subscription for event '{event}': {callback_url}")

    async def unregister_subscription(self, event: str, callback_url: str):
        """
        Remove a webhook subscription
        """
        async with self._lock:
            if event in self.subscriptions and callback_url in self.subscriptions[event]:
                self.subscriptions[event].remove(callback_url)
                logger.info(f"Unregistered subscription for event '{event}': {callback_url}")

    async def get_subscriptions(self, event: str) -> List[str]:
        """
        Get all callback URLs for a specific event type
        """
        async with self._lock:
            return self.subscriptions.get(event, []).copy()

    async def get_all_subscriptions(self) -> Dict[str, List[str]]:
        """
        Get all active subscriptions
        """
        async with self._lock:
            return {event: urls.copy() for event, urls in self.subscriptions.items()}
