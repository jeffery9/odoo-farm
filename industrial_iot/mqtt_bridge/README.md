# Industrial IoT MQTT Bridge

The MQTT Bridge serves as an intermediary between MQTT devices and Odoo's HTTP webhooks, facilitating device configuration download, telemetry data processing, command and control, and OTA update management.

## Architecture Overview

The bridge connects to an MQTT broker and Odoo instance, handling communication in both directions:

- **Device Configuration**: Devices request configuration via MQTT, bridge forwards to Odoo and returns configuration
- **Telemetry Data**: Devices send telemetry via MQTT, bridge forwards to Odoo webhook
- **Command & Control**: Odoo sends commands via API, bridge forwards to devices via MQTT
- **OTA Updates**: Odoo initiates OTA updates via API, bridge forwards to devices via MQTT

## Configuration

The bridge can be configured using environment variables or a `.env` file:

```env
# MQTT Broker Configuration
MQTT_BROKER_HOST=mqtt.factory.com
MQTT_BROKER_PORT=8883
MQTT_BROKER_USERNAME=your_username
MQTT_BROKER_PASSWORD=your_password
MQTT_USE_TLS=True
MQTT_CLIENT_ID=iiot_bridge_001

# Odoo HTTP Webhook Configuration
ODOO_BASE_URL=http://localhost:8069
ODOO_API_KEY=your_odoo_api_key

# Topic Configuration
MQTT_CONFIG_REQUEST_TOPIC=iiot/config/request
MQTT_CONFIG_RESPONSE_TOPIC=iiot/config/{device}
MQTT_TELEMETRY_TOPIC_TEMPLATE=telemetry/{device}/data
MQTT_COMMAND_TOPIC_TEMPLATE=command/{device}/action
MQTT_OTA_NOTIFY_TOPIC_TEMPLATE=ota/{device}/notify
MQTT_OTA_STATUS_TOPIC_TEMPLATE=ota/{device}/status

# HTTP Server Configuration
HOST=0.0.0.0
PORT=8000
```

## API Endpoints

### Health Check
```
GET /
GET /health
```

### Device Configuration
```
POST /api/v1/config/download
{
  "serial": "device_serial",
  "token": "config_token"
}
```

### Command & Control
```
POST /api/v1/command/send
{
  "device_id": "device001",
  "action": "reset",
  "params": {
    "delay": 5
  }
}
```

### OTA Updates
```
POST /api/v1/ota/send
{
  "device_id": "device001",
  "action": "start_update",
  "params": {
    "url": "http://firmware.example.com/firmware.bin",
    "version": "2.1.0"
  }
}
```

### Device Status
```
GET /api/v1/device/{device_id}/status
GET /api/v1/devices/status
```

## MQTT Topics

The bridge subscribes to and publishes on the following MQTT topics:

- `iiot/config/request` - Device configuration requests
- `iiot/config/{device}` - Device configuration responses
- `telemetry/{device}/data` - Telemetry data from devices
- `command/{device}/action` - Commands to devices
- `command/{device}/response` - Command responses from devices
- `ota/{device}/notify` - OTA update notifications to devices
- `ota/{device}/status` - OTA status updates from devices

## Installation

1. Install required Python packages:
```bash
pip install fastapi uvicorn paho-mqtt httpx pydantic python-dotenv
```

2. Configure environment variables (see above)

3. Run the bridge:
```bash
uvicorn mqtt_bridge.main:bridge.app --host 0.0.0.0 --port 8000
```

Or run the standalone bridge:
```bash
python -m mqtt_bridge.main
```

## Security Considerations

- Use TLS for MQTT connections in production
- Secure the Odoo API with proper authentication
- Validate device tokens and serial numbers
- Implement rate limiting for API endpoints
- Use strong passwords for MQTT broker authentication

## Troubleshooting

- Check MQTT broker connectivity
- Verify topic names and permissions
- Check Odoo webhook endpoints
- Review bridge logs for error messages