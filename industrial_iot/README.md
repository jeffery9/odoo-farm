# Industrial IoT (IIoT) Module Documentation

## Overview

The Industrial IoT (IIoT) module provides comprehensive integration between Odoo and MQTT-based IoT devices. This module enables device management, telemetry processing, command and control, and OTA firmware updates while maintaining Odoo as the central configuration and business logic engine.

## Architecture

The module follows an HTTP-to-MQTT bridge pattern where Odoo communicates with MQTT devices through an intermediary bridge application:

```
MQTT Devices ←→ MQTT Bridge (FastAPI) ←→ Odoo HTTP Webhooks
```

This architecture ensures reliability by avoiding direct MQTT connections from within Odoo, which could affect Odoo's stability.

## Components

### 1. Core Models

#### `iiot.device.profile`
- Device communication configuration templates
- MQTT topic templates for different device types
- Command message templates with Jinja2 support
- Validation for topic template syntax

#### `iiot.telemetry.rule`
- Declarative rules for mapping telemetry data to business objects
- JSONPath expressions for data extraction
- Target model and field mappings
- Domain filtering for specific business objects

#### `iiot.device`
- Individual device instances with lifecycle management
- Device identity (serial number and unique device ID)
- Business object binding for integration
- Configuration token system for secure pairing
- Connection status tracking
- Firmware version management

#### `iiot.firmware` and `iiot.update`
- Complete OTA firmware management system
- Version control and file management
- Update tracking and status monitoring
- Error handling and rollback support

### 2. HTTP Controllers

Located in `controllers/main.py`, these endpoints handle:

#### Device Configuration Download (`/iiot/config`)
- Secure one-time configuration token system
- Device pairing and authentication
- MQTT broker configuration generation
- Topic mapping for device-specific communications

#### Telemetry Webhook (`/iiot/webhook/<device_id>`)
- Receiving telemetry data from MQTT bridge
- Processing based on device profile rules
- Mapping telemetry to business objects
- OTA status update processing

#### Command Sending (`/iiot/command/<device_id>`)
- Internal API for sending commands to devices
- Integration with MQTT bridge
- Command queuing and delivery verification

### 3. User Interface

#### Views
- Device Profile Management (tree and form views)
- Telemetry Rule Configuration (tree and form views)
- Device Management (with config token generation and OTA update buttons)
- Firmware Management (version control and upload)
- OTA Update Tracking (status monitoring)

#### Menu Structure
- Industrial IoT (main menu)
  - Device Management
    - Device Configuration Templates
    - IIoT Devices
  - Telemetry Management
    - Telemetry Rules
  - OTA Management
    - Firmware Versions
    - OTA Update Records

### 4. MQTT Bridge

Located in `mqtt_bridge/`, the FastAPI-based bridge handles:

#### Core Functionality
- Connection to MQTT broker
- Bidirectional message routing between MQTT and HTTP
- Device configuration download handling
- Telemetry data forwarding to Odoo
- Command and control routing
- OTA update management

#### API Endpoints
- `/health` - Health status check
- `/api/v1/config/download` - Device configuration requests
- `/api/v1/command/send` - Send commands to devices
- `/api/v1/ota/send` - Initiate OTA updates
- `/api/v1/device/{id}/status` - Device status information

#### MQTT Topics
- `iiot/config/request` - Device configuration requests
- `iiot/config/{device}` - Configuration responses
- `telemetry/{device}/data` - Telemetry data from devices
- `command/{device}/action` - Commands to devices
- `command/{device}/response` - Command responses from devices
- `ota/{device}/notify` - OTA update notifications
- `ota/{device}/status` - OTA status updates

## Security Features

### Device Pairing
- One-time configuration tokens for secure device registration
- Token invalidation after first use
- Serial number validation

### Access Control
- Dedicated IIoT user and admin groups
- Granular permissions for each model
- Module category organization

## Business Integration

### Telemetry-to-Object Mapping
- JSONPath expressions for data extraction
- Flexible mapping to any Odoo model
- Domain-based filtering for specific objects
- Automatic data updates to business objects

### Command Templates
- Jinja2-based command templates for flexibility
- Device-specific command customization
- Parameterized command execution

## Configuration

### System Parameters
- `iiot.mqtt_host` - MQTT broker hostname
- `iiot.mqtt_port` - MQTT broker port
- `iiot.mqtt_use_tls` - TLS connection setting

### Device Profiles
- Template-based configuration for different device types
- Topic templates with `{device}` placeholders
- Command message templates with Jinja2 support
- Validation for template syntax

## Usage Workflow

### Device Onboarding
1. Create device profile template with topic configurations
2. Add telemetry rules for data mapping (optional)
3. Create device instance with serial number
4. Generate configuration token
5. Device requests configuration using serial and token
6. Configuration downloaded and token invalidated

### Telemetry Processing
1. Device sends telemetry data via MQTT
2. MQTT bridge forwards to Odoo webhook
3. Telemetry rules applied to map data to business objects
4. Business objects updated with telemetry values

### Command Execution
1. User initiates command from Odoo interface
2. Odoo sends command to MQTT bridge via API
3. MQTT bridge publishes command to device via MQTT
4. Device executes command and optionally responds

### OTA Updates
1. Upload firmware version in Odoo
2. Create update record for specific device
3. Initiate update from Odoo interface
4. MQTT bridge sends OTA command to device
5. Device downloads and installs firmware
6. Status updates sent back to Odoo

## Error Handling

- Comprehensive logging throughout the module
- Graceful error handling for network issues
- Device status tracking for connection monitoring
- Retry mechanisms for transient failures
- Detailed error messages for troubleshooting

## Performance Considerations

- Efficient caching of device configurations
- Asynchronous processing where possible
- Connection pooling for HTTP requests
- Efficient database queries with proper indexing
- Scalable MQTT topic design

## Usage

### Device Management
1. **Create Device Profile**:
   - Navigate to Industrial IoT > Device Management > Device Configuration Templates
   - Create a new profile with appropriate topic templates
   - Configure command message templates using Jinja2 syntax

2. **Configure Telemetry Rules** (optional):
   - Go to Industrial IoT > Telemetry Management > Telemetry Rules
   - Define JSONPath expressions to map telemetry data to business objects
   - Set target models and field fields for data mapping

3. **Register New Device**:
   - Access Industrial IoT > Device Management > IIoT Devices
   - Create a new device record with serial number
   - Assign appropriate device profile
   - Generate configuration token using "生成配置令牌" button

4. **Device Configuration**:
   - Device uses serial number and configuration token to download setup
   - Configuration includes MQTT broker settings and topic mappings
   - Token is invalidated after first successful download

### Command and Control
1. **Send Commands**:
   - From device form view, use "发送重置指令" or custom command buttons
   - Commands are sent via MQTT bridge to target devices
   - Command status can be tracked in device records

### OTA Updates
1. **Upload Firmware**:
   - Navigate to Industrial IoT > OTA Management > Firmware Versions
   - Create new firmware entry with version, URL, and checksum
   - Upload firmware file or specify download URL

2. **Initiate Update**:
   - From device form view, use "OTA升级" button
   - Or create OTA update record manually
   - Monitor update progress and status

### Monitoring
1. **Device Status**:
   - Check connection status in device list view
   - View last telemetry timestamp
   - Monitor command history

2. **System Health**:
   - Use MQTT bridge health endpoints
   - Monitor logs for error conditions
   - Track telemetry processing rates

## MQTT Bridge Deployment

### Prerequisites
- Python 3.8+ installed
- MQTT broker (e.g., Mosquitto, AWS IoT, Azure IoT Hub)
- Network connectivity between MQTT broker, Odoo instance, and MQTT bridge
- Python dependencies from requirements.txt

### Local Development Setup
1. **Install Dependencies**:
   ```bash
   cd mqtt_bridge
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables**:
   Create a `.env` file in the `mqtt_bridge` directory:
   ```env
   # MQTT Broker Configuration
   MQTT_BROKER_HOST=your-mqtt-broker.com
   MQTT_BROKER_PORT=8883
   MQTT_BROKER_USERNAME=your_username
   MQTT_BROKER_PASSWORD=your_password
   MQTT_USE_TLS=True

   # Odoo HTTP Webhook Configuration
   ODOO_BASE_URL=http://your-odoo-instance:8069
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

3. **Run the MQTT Bridge**:
   ```bash
   # Option 1: Direct Python execution
   python main.py

   # Option 2: Using Uvicorn
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

### Production Deployment

#### Docker Deployment
1. **Create Dockerfile**:
   ```Dockerfile
   FROM python:3.9-slim

   WORKDIR /app

   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   COPY . .

   EXPOSE 8000

   CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
   ```

2. **Create Docker Compose File** (recommended for production):
   ```yaml
   version: '3.8'

   services:
     mqtt-bridge:
       build: .
       container_name: iiot-mqtt-bridge
       ports:
         - "8000:8000"
       environment:
         - MQTT_BROKER_HOST=${MQTT_BROKER_HOST}
         - MQTT_BROKER_PORT=${MQTT_BROKER_PORT}
         - MQTT_BROKER_USERNAME=${MQTT_BROKER_USERNAME}
         - MQTT_BROKER_PASSWORD=${MQTT_BROKER_PASSWORD}
         - ODOO_BASE_URL=${ODOO_BASE_URL}
         - ODOO_API_KEY=${ODOO_API_KEY}
         - MQTT_USE_TLS=${MQTT_USE_TLS:-True}
       env_file:
         - .env
       restart: unless-stopped
       networks:
         - iiot_network
       healthcheck:
         test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
         interval: 30s
         timeout: 10s
         retries: 3
         start_period: 40s

   networks:
     iiot_network:
       driver: bridge
   ```

3. **Deploy with Docker Compose**:
   ```bash
   # Build and start the service
   docker-compose up -d

   # Monitor logs
   docker-compose logs -f mqtt-bridge
   ```

#### Systemd Service (Linux) - Alternative Production Method
1. **Create service file**: Create `/etc/systemd/system/iiot-mqtt-bridge.service`:
   ```ini
   [Unit]
   Description=Industrial IoT MQTT Bridge
   After=network.target
   StartLimitIntervalSec=0

   [Service]
   Type=simple
   Restart=always
   RestartSec=1
   User=iiot-bridge
   WorkingDirectory=/path/to/industrial_iot/mqtt_bridge
   ExecStart=/usr/local/bin/python3 /path/to/industrial_iot/mqtt_bridge/main.py
   EnvironmentFile=/path/to/industrial_iot/mqtt_bridge/.env
   StandardOutput=journal
   StandardError=journal

   [Install]
   WantedBy=multi-user.target
   ```

2. **Enable and start the service**:
   ```bash
   # Create user for running the service
   sudo useradd -r -s /bin/false iiot-bridge

   # Set proper permissions
   sudo chown -R iiot-bridge:iiot-bridge /path/to/industrial_iot/mqtt_bridge

   # Copy service file and enable
   sudo cp iiot-mqtt-bridge.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable iiot-mqtt-bridge
   sudo systemctl start iiot-mqtt-bridge

   # Check status
   sudo systemctl status iiot-mqtt-bridge
   ```

### MQTT Broker Setup

#### Mosquitto (Open Source)
1. **Install Mosquitto**:
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install mosquitto mosquitto-clients

   # Or with Docker
   docker run -d -p 1883:1883 -p 8883:8883 --name mqtt-broker eclipse-mosquitto:latest
   ```

2. **Configure Authentication** (mosquitto.conf):
   ```
   listener 1883
   listener 8883
   protocol mqtt

   allow_anonymous false
   password_file /etc/mosquitto/passwd
   ```

3. **Create User**:
   ```bash
   sudo mosquitto_passwd -c /etc/mosquitto/passwd your_username
   sudo systemctl restart mosquitto
   ```

#### Security Considerations
- Always use TLS/SSL for production MQTT connections (port 8883)
- Implement proper authentication and authorization
- Use strong passwords for MQTT broker access
- Configure firewall rules to restrict access to MQTT ports
- Consider using client certificates for additional security

### Odoo Module Installation

1. **Prerequisites**:
   - Odoo 17.0+ installed and running
   - The industrial_iot module directory in your addons path

2. **Installation Steps**:
   ```bash
   # Add module directory to Odoo addons path in configuration
   # Restart Odoo server
   # Go to Apps > Industrial IoT (IIoT) Integration and install
   ```

3. **Configure System Parameters** (optional):
   - Navigate to Settings > Technical > Parameters > System Parameters
   - Set the following if needed:
     - `iiot.mqtt_host`: Your MQTT broker hostname
     - `iiot.mqtt_port`: Your MQTT broker port (default: 8883)
     - `iiot.mqtt_use_tls`: Enable TLS (default: True)

### Network Configuration

#### Required Network Access
- MQTT bridge must be able to connect to MQTT broker
- MQTT bridge must be able to reach Odoo HTTP endpoints
- Devices must be able to connect to MQTT broker
- Firewall rules should allow:
  - Port 1883/8883 (MQTT, depending on TLS usage)
  - Port 8000 (MQTT bridge API)
  - Odoo server port (typically 8069)

#### Example Network Topology
```
Device Network ←→ MQTT Broker ←→ MQTT Bridge ←→ Odoo Server
(10.0.1.x)        (10.0.2.x)    (10.0.3.x)     (10.0.4.x)
```

### Testing and Validation

1. **Verify MQTT Bridge Health**:
   ```bash
   curl http://bridge-host:8000/health
   ```

2. **Check Available Endpoints**:
   ```bash
   curl http://bridge-host:8000
   ```

3. **Test MQTT Connection**:
   - Subscribe to test topic: `mosquitto_sub -h broker -t test/topic -u user -P pass`
   - Verify bridge subscribes to configured topics

4. **Test Odoo Integration**:
   - Create a test device in Odoo
   - Attempt to retrieve device status via bridge API
   - Verify webhooks are received by Odoo

### Troubleshooting

#### Common Issues and Solutions

1. **MQTT Connection Issues**:
   - Verify broker connectivity: `telnet mqtt-broker.com 8883`
   - Check TLS certificate validity
   - Confirm authentication credentials
   - Review MQTT topic permissions

2. **Odoo Communication Issues**:
   - Verify Odoo instance is accessible from bridge
   - Check webhook endpoint URLs
   - Confirm API keys are valid
   - Examine Odoo logs for incoming webhook requests

3. **Device Registration Issues**:
   - Ensure configuration tokens are valid and not expired
   - Verify device serial numbers match Odoo records
   - Check MQTT topic permissions for device-specific topics

4. **Telemetry Processing Issues**:
   - Verify telemetry rules have correct JSONPath expressions
   - Check device topic mappings in profiles
   - Confirm JSONPath syntax is valid using test tools

#### Monitoring and Logging
- Enable detailed logging in bridge settings
- Monitor both MQTT bridge and Odoo logs
- Track metric collection for performance monitoring
- Use health check endpoints for automated monitoring

### Command Construction

#### Overview
The Industrial IoT module uses Jinja2 templating to construct command messages that are sent to devices via MQTT. Commands are defined at the device profile level and can be parameterized for different actions.

#### Command Template Structure
Commands are defined using Jinja2 templates in the device profile's "Command Template" field. The template has access to two variables:
- `action`: The specific action to perform
- `params`: A dictionary of parameters for the action

**Default Template:**
```json
{"action": "{{ action }}", "params": {{ params | tojson }}}
```

This template generates command messages like:
```json
{"action": "reset", "params": {"delay": 5}}
```

#### Creating Custom Command Templates
1. **Navigate to Device Profiles**: Go to Industrial IoT > Device Management > Device Configuration Templates
2. **Edit a Profile**: Select or create a device profile
3. **Modify Command Template**: Update the "Command Template" field with your custom Jinja2 template

**Note on Multiple Command Templates:** The current implementation supports a single command template per device profile. To support different command formats for different actions, use conditional logic in your template:

**Multiple Command Types in Single Template:**
```json
{%- if action == 'reset' -%}
{"command": "device_reset", "delay": {{ params.delay | default(0) }}}
{%- elif action == 'configure' -%}
{"command": "device_config", "settings": {{ params | tojson }}}
{%- elif action == 'ota_update' -%}
{"command": "firmware_update", "url": "{{ params.url }}", "version": "{{ params.version }}"}
{%- else -%}
{"command": "{{ action }}", "params": {{ params | tojson }}}
{%- endif -%}
```

**Example Custom Templates:**

**Simple Command Format:**
```json
{"cmd": "{{ action }}", "args": {{ params | tojson }}}
```

**Device-Specific Format:**
```json
{
  "device_id": "{{ device_id }}",
  "command": "{{ action }}",
  "timestamp": "{{ now() }}",
  "parameters": {{ params | tojson }}
}
```

**Advanced Template with Conditional Logic:**
```json
{
  "type": "command",
  "action": "{{ action }}",
  {% if params.priority %}"priority": {{ params.priority }},{% endif %}
  "data": {{ params | tojson }}
}
```

#### Using Parameters
Parameters can be passed to commands when they are sent from the Odoo interface:

**Common Parameter Examples:**
- `{"delay": 10}` - Delay in seconds
- `{"threshold": 25.5}` - Threshold value
- `{"mode": "auto"}` - Operating mode
- `{"duration": 300}` - Duration in seconds

#### Sending Commands from Odoo
1. **From Device Form**: Use the "Send Command" button or custom command buttons
2. **Programmatically**: Call the device's `send_command()` method
3. **Via MQTT Bridge**: Commands are forwarded through the MQTT bridge to the device

**Example Programmatic Usage:**
```python
# In a custom method or action
device = self.env['iiot.device'].browse(device_id)
device.send_command('reset', delay=5)

# With multiple parameters
device.send_command('configure', threshold=25.5, mode='auto', duration=300)
```

#### Command Processing Flow
1. **Command Initiation**: Command is initiated from Odoo UI or API
2. **Template Rendering**: Jinja2 template is rendered with action and parameters
3. **MQTT Forwarding**: Command is sent to MQTT bridge via HTTP API
4. **Device Publication**: MQTT bridge publishes command to device's command topic
5. **Device Execution**: Device receives and processes the command
6. **Status Update**: Device may send response back through telemetry/OTA status topics

#### Best Practices
- **Template Validation**: Always test command templates with sample data
- **Parameter Validation**: Ensure parameters are properly validated before sending
- **Error Handling**: Implement proper error handling for command failures
- **Security**: Validate and sanitize command parameters to prevent injection attacks
- **Documentation**: Document command formats and expected parameters for each device type
- **Logging**: Enable logging to track command sending and responses

#### Troubleshooting Commands
1. **Check Template Syntax**: Verify Jinja2 syntax in the command template
2. **Validate Parameters**: Ensure parameters are compatible with the template
3. **MQTT Connection**: Verify the MQTT bridge and device connections
4. **Topic Permissions**: Check that the device has permission to subscribe to command topics
5. **Device Status**: Ensure the target device is online and connected

#### Security Considerations
- **Input Validation**: Always validate command parameters to prevent malicious input
- **Access Control**: Use appropriate permissions to restrict who can send commands
- **Command Auditing**: Log all command requests for security auditing
- **Template Safety**: Avoid using unsafe Jinja2 filters or extensions

#### Command Examples by Use Case

**Device Reset Command:**
```
Action: reset
Params: {"delay": 10}
Template: {"action": "{{ action }}", "params": {{ params | tojson }}}
Result: {"action": "reset", "params": {"delay": 10}}
```

**Configuration Update Command:**
```
Action: configure
Params: {"temperature_threshold": 25.5, "humidity_limit": 60}
Result: {"action": "configure", "params": {"temperature_threshold": 25.5, "humidity_limit": 60}}
```

**OTA Update Command:**
```
Action: ota_update
Params: {"url": "http://firmware.example.com/v2.1.bin", "version": "2.1.0"}
Result: {"action": "ota_update", "params": {"url": "http://firmware.example.com/v2.1.bin", "version": "2.1.0"}}
```

#### Multiple Command Templates Support

**Current Implementation:**
The Industrial IoT module currently supports a single command template per device profile. However, you can implement conditional logic within a single template to handle different command types, as shown in the "Multiple Command Types in Single Template" example above.

**Extending the Module (Advanced):**
To implement true multiple command templates, you would need to extend the module with additional fields and logic. Consider creating a custom model to manage multiple templates:

```python
class IiotCommandTemplate(models.Model):
    _name = 'iiot.command.template'
    _description = 'IIoT Command Template'

    name = fields.Char('Name', required=True)
    code = fields.Char('Code', required=True)  # e.g., 'reset', 'configure', 'ota'
    template = fields.Text('Template', required=True)
    profile_id = fields.Many2one('iiot.device.profile', 'Device Profile')
    is_active = fields.Boolean('Active', default=True)
```

#### Automatic Command Triggering

**Current Capabilities:**
The standard Industrial IoT module supports manual command triggering through:
- Device form views with command buttons
- Programmatic calls to `device.send_command()` method
- MQTT bridge API endpoints

**Automatic Command Triggering (Advanced):**
Automatic command triggering is not directly built into the module, but can be implemented through various approaches:

**1. Scheduled Actions (Cron Jobs):**
Use Odoo's automated actions to trigger commands based on schedules or conditions:

```python
# In a custom method that could be called by a scheduled action
def trigger_scheduled_commands(self):
    devices = self.env['iiot.device'].search([('is_active', '=', True)])
    for device in devices:
        # Check if the device needs a specific command based on conditions
        if self.should_send_command(device):
            device.send_command('status_check', interval=300)
```

**2. Business Rule Integration:**
Link commands to business object changes using Odoo's automation features:

**Option A: Custom Method with Automated Actions**
```python
# Example: Send command when maintenance equipment status changes
@api.model
def create(self, vals):
    record = super().create(vals)
    if 'state' in vals and vals['state'] == 'maintenance':
        # Find associated IIoT device
        iiot_device = self.env['iiot.device'].search([('business_ref', '=', f'maintenance.equipment,{record.id}')])
        if iiot_device:
            iiot_device.send_command('enter_maintenance_mode', equipment_id=record.id)
    return record
```

**Option B: Using Odoo's Built-in Automated Actions**
1. Go to **Settings > Technical > Automation > Automated Actions**
2. Create a new automated action:
   - **Model**: Select the model you want to monitor (e.g., `maintenance.equipment`)
   - **Trigger**: Choose when to trigger (On Creation, On Update, etc.)
   - **Filter Domain**: Define conditions (e.g., `[('state', '=', 'maintenance')]`)
   - **Python Code**: Use Python code to send commands:
```python
# In automated action Python code
for record in records:
    # Find associated IIoT device
    iiot_device = env['iiot.device'].search([('business_ref', '=', f'maintenance.equipment,{record.id}')])
    if iiot_device:
        iiot_device.send_command('enter_maintenance_mode', equipment_id=record.id)
```

**Option C: Scheduled Automated Actions**
1. Create a scheduled automated action:
   - **Model**: `iiot.device` or any relevant model
   - **Trigger**: On Time Condition
   - **Schedule Interval**: Define how often to run
   - **Python Code**:
```python
# Send periodic status check commands
for device in records:
    if device.is_active and device.connection_status == 'online':
        device.send_command('status_check', interval=300)
```

**Option D: Complex Conditions with Server Actions**
You can also create more complex automation rules:
- **Record Rules**: Trigger based on complex domain conditions
- **Field Triggers**: Trigger when specific fields change
- **Related Field Changes**: Trigger based on related record changes

Example for automated action that triggers on field change:
```python
# Trigger when a specific field reaches a threshold
for record in records:
    if record.field_name > record.threshold_value:
        # Find associated IIoT device
        iiot_device = env['iiot.device'].search([('business_ref', '=', f'{record._name},{record.id}')])
        if iiot_device:
            iiot_device.send_command('alert_threshold_reached',
                                   field=record.field_name,
                                   value=record.field_name,
                                   threshold=record.threshold_value)
```

**3. Telemetry-Based Triggers:**
Trigger commands based on incoming telemetry data:

```python
# In the device's process_telemetry_data method
def process_telemetry_data(self, telemetry_data):
    # Process telemetry data first
    super().process_telemetry_data(telemetry_data)

    # Then check if any commands should be triggered based on the data
    for key, value in telemetry_data.items():
        if key == 'temperature' and value > 80:
            # Send cooling command
            self.send_command('activate_cooling', target_temp=70)
        elif key == 'vibration' and value > 5.0:
            # Send inspection command
            self.send_command('enter_inspection_mode')
```

**4. Custom Automation Rules:**
Create custom automation rules that can trigger commands based on various conditions:

```python
class IiotAutomationRule(models.Model):
    _name = 'iiot.automation.rule'
    _description = 'IIoT Automation Rule'

    name = fields.Char('Name', required=True)
    model_id = fields.Many2one('ir.model', 'Model')
    domain = fields.Char('Domain', default='[]')
    command_action = fields.Char('Command Action', required=True)
    command_params = fields.Text('Command Parameters')
    condition_field = fields.Char('Condition Field')
    condition_value = fields.Float('Condition Value')
    trigger_on_create = fields.Boolean('Trigger on Create')
    trigger_on_write = fields.Boolean('Trigger on Update')
    is_active = fields.Boolean('Active', default=True)
```

**Best Practices for Automatic Command Triggering:**
- **Throttling**: Implement rate limiting to prevent command flooding
- **Conditions**: Use appropriate conditions to avoid unnecessary commands
- **Error Handling**: Implement proper error handling for failed commands
- **Logging**: Maintain logs of automatically triggered commands for auditing
- **Safety**: Include safety checks to prevent dangerous command sequences
- **Testing**: Thoroughly test automatic triggers in non-production environments

### Scaling Considerations

1. **High Availability**:
   - Deploy multiple MQTT bridge instances
   - Use load balancer for bridge API endpoints
   - Implement distributed MQTT broker setup

2. **Performance**:
   - Monitor bridge resource usage
   - Scale bridge instances based on device count
   - Optimize database queries in Odoo module

3. **Load Distribution**:
   - Consider MQTT broker clustering for large deployments
   - Implement queue-based processing for high-volume telemetry
   - Use MQTT topic partitioning for scalability