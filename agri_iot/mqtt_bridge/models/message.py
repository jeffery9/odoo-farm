"""
Data models for MQTT Bridge messages
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class DeviceConfigRequest(BaseModel):
    """Request model for device configuration download"""
    serial: str = Field(..., description="Device serial number")
    token: str = Field(..., description="Configuration token for authentication")


class DeviceConfigResponse(BaseModel):
    """Response model for device configuration"""
    status: str = Field(..., description="Response status: success or error")
    device_id: Optional[str] = Field(None, description="Unique device identifier")
    mqtt: Optional[Dict[str, Any]] = Field(None, description="MQTT broker configuration")
    topics: Optional[Dict[str, str]] = Field(None, description="Topic mapping for the device")
    error: Optional[str] = Field(None, description="Error message if status is error")


class TelemetryData(BaseModel):
    """Model for telemetry data from devices"""
    device_id: str = Field(..., description="Device identifier")
    topic: str = Field(..., description="MQTT topic where data was received")
    payload: Dict[str, Any] = Field(..., description="Telemetry data payload")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of data receipt")


class CommandMessage(BaseModel):
    """Model for command messages to devices"""
    device_id: str = Field(..., description="Target device identifier")
    action: str = Field(..., description="Action/command to execute")
    params: Dict[str, Any] = Field(default={}, description="Command parameters")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of command")


class OTAStatus(BaseModel):
    """Model for OTA status updates from devices"""
    device_id: str = Field(..., description="Device identifier")
    update_id: str = Field(..., description="OTA update identifier")
    status: str = Field(..., description="Update status: pending, in_progress, success, failed")
    progress: Optional[int] = Field(None, description="Update progress percentage")
    error: Optional[str] = Field(None, description="Error message if update failed")


class BridgeHealthStatus(BaseModel):
    """Model for bridge health status"""
    status: str = Field(..., description="Overall bridge status")
    mqtt_connected: bool = Field(..., description="Whether MQTT is connected")
    http_available: bool = Field(..., description="Whether HTTP service is available")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Status timestamp")
    active_connections: int = Field(0, description="Number of active device connections")