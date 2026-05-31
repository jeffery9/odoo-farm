"""
Persistence Manager for the Industrial IoT Bridge
Implements Store & Forward using SQLite
"""

import aiosqlite
import json
import logging
import os
from datetime import datetime
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class PersistenceManager:
    """
    Handles local storage of telemetry data when Odoo is unreachable
    """

    def __init__(self, db_path: str = "bridge_data.db"):
        self.db_path = db_path

    async def initialize(self):
        """Initialize the database and create tables if they don't exist"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS telemetry_queue (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    device_id TEXT,
                    topic TEXT,
                    payload TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    retry_count INTEGER DEFAULT 0
                )
            ''')
            await db.commit()
            logger.info(f"Persistence database initialized at {self.db_path}")

    async def store_telemetry(self, device_id: str, topic: str, payload: Dict[str, Any]):
        """Store telemetry for later forwarding"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    "INSERT INTO telemetry_queue (device_id, topic, payload) VALUES (?, ?, ?)",
                    (device_id, topic, json.dumps(payload))
                )
                await db.commit()
                logger.info(f"Stored telemetry for device {device_id} in local persistence")
        except Exception as e:
            logger.error(f"Failed to store telemetry: {str(e)}")

    async def get_queued_telemetry(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Retrieve queued telemetry records"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                async with db.execute(
                    "SELECT * FROM telemetry_queue ORDER BY id ASC LIMIT ?", 
                    (limit,)
                ) as cursor:
                    rows = await cursor.fetchall()
                    return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Failed to retrieve queued telemetry: {str(e)}")
            return []

    async def delete_telemetry(self, record_id: int):
        """Delete a telemetry record after successful forwarding"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("DELETE FROM telemetry_queue WHERE id = ?", (record_id,))
                await db.commit()
        except Exception as e:
            logger.error(f"Failed to delete telemetry record {record_id}: {str(e)}")

    async def increment_retry(self, record_id: int):
        """Increment the retry count for a record"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    "UPDATE telemetry_queue SET retry_count = retry_count + 1 WHERE id = ?", 
                    (record_id,)
                )
                await db.commit()
        except Exception as e:
            logger.error(f"Failed to increment retry count for record {record_id}: {str(e)}")
