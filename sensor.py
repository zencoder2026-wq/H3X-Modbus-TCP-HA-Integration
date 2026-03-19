"""Sensor platform for Solar Hub."""
from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, SENSOR_TYPES

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    
    entities = []
    for sensor_def in SENSOR_TYPES:
        entities.append(SolarHubSensor(coordinator, sensor_def))
    
    # Add the Template Sensor replacement logic (Inverter State Text)
    entities.append(SolarInverterStateTextSensor(coordinator))

    async_add_entities(entities)


class SolarHubSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Solar Hub Sensor."""

    def __init__(self, coordinator, definition):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._def = definition
        self._attr_name = definition["name"]
        self._attr_unique_id = f"{DOMAIN}_{definition['id']}"
        self._attr_native_unit_of_measurement = definition["unit"]
        
        if definition["cls"]:
            self._attr_device_class = definition["cls"]
        if definition["state_cls"]:
            self._attr_state_class = definition["state_cls"]

    @property
    def native_value(self):
        """Return the state of the sensor."""
        raw_val = self.coordinator.data.get(self._def["id"])
        
        if raw_val is None:
            return None
            
        # Apply Scaling if numeric
        scale = self._def["scale"]
        if scale != 1 and isinstance(raw_val, (int, float)):
            return round(raw_val * scale, 2)
            
        return raw_val


class SolarInverterStateTextSensor(CoordinatorEntity, SensorEntity):
    """Additional sensor to map Raw State to Text (like the YAML template)."""

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Solar Inverter State"
        self._attr_unique_id = f"{DOMAIN}_solar_inverter_state_text"
        self._attr_icon = "mdi:information-outline"

    @property
    def native_value(self):
        """Calculate state based on raw sensor."""
        # Get raw value from coordinator data
        raw = self.coordinator.data.get("solar_inverter_state_raw")
        
        if raw is None:
            return "Unknown"
        
        try:
            val = int(raw)
            if val == 0:
                return "Wait"
            if val == 1:
                return "Normal"
            if val == 2:
                return "Fault"
            return "Unknown"
        except (ValueError, TypeError):
            return "Unknown"