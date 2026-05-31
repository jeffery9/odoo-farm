"""
Simulation script for FastAPI MQTT Bridge integration testing.
This script simulates Odoo interactions and MQTT device events.
"""

import asyncio
import json
import httpx
import time
from datetime import datetime

BRIDGE_URL = "http://localhost:8000"
ODOO_MOCK_PORT = 8069

async def simulate_bridge_workflow():
    print("--- Starting Bridge Simulation ---")
    
    async with httpx.AsyncClient() as client:
        # 1. Test Health Check
        try:
            resp = await client.get(f"{BRIDGE_URL}/health")
            print(f"Health Check: {resp.status_code} - {resp.json()}")
        except Exception as e:
            print(f"Bridge not running at {BRIDGE_URL}. Please start it first. Error: {e}")
            return

        # 2. Simulate Odoo Subscribing to Webhooks
        print("\n2. Simulating Odoo subscription...")
        sub_payload = {
            "event": "subscribe",
            "payload": {
                "callback_url": f"http://localhost:{ODOO_MOCK_PORT}/iiot/webhook",
                "events": ["telemetry", "command_ack"]
            }
        }
        resp = await client.post(f"{BRIDGE_URL}/api/v1/webhook", json=sub_payload)
        print(f"Subscription Response: {resp.json()}")

        # 3. Simulate Device Configuration Download
        print("\n3. Simulating Device Config Request...")
        config_req = {
            "serial": "SN-TEST-999",
            "token": "initial-token-123"
        }
        # This will fail unless Odoo is actually running or mocked, 
        # but we can test the bridge's routing logic
        try:
            resp = await client.post(f"{BRIDGE_URL}/api/v1/config/download", json=config_req)
            print(f"Config Download Status: {resp.status_code}")
        except Exception as e:
            print(f"Config Download Failed (Expected if Odoo offline): {e}")

        # 4. Test Internal Command Routing
        print("\n4. Simulating Internal Command...")
        cmd_payload = {
            "event": "command",
            "payload": {
                "device_id": "test_dev_01",
                "action": "reset",
                "params": {"force": True}
            }
        }
        resp = await client.post(f"{BRIDGE_URL}/api/v1/webhook", json=cmd_payload)
        print(f"Command Routing Response: {resp.json()}")

    print("\n--- Simulation Complete ---")

if __name__ == "__main__":
    asyncio.run(simulate_bridge_workflow())
