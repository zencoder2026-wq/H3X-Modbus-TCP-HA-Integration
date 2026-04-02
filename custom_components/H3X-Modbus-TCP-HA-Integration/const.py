"""Constants for the Solar Hub integration."""
from typing import Final

DOMAIN: Final = "solar_hub"
DEFAULT_NAME: Final = "Solar Hub"
DEFAULT_PORT: Final = 502
DEFAULT_SCAN_INTERVAL: Final = 10  # Default to 10s if not set
CONF_SCAN_INTERVAL: Final = "scan_interval"

# Sensor Definitions mapped from YAML
SENSOR_TYPES = [
    # SLAVE 1: BATTERY
    {"name": "Solar Battery Status", "id": "solar_ess_status", "slave": 1, "addr": 5120, "type": "uint16", "scale": 1, "unit": None, "cls": None, "state_cls": None},
    {"name": "Solar Battery Voltage", "id": "solar_ess_voltage", "slave": 1, "addr": 5123, "type": "uint16", "scale": 0.1, "unit": "V", "cls": "voltage", "state_cls": "measurement"},
    {"name": "Solar Battery Current", "id": "solar_ess_current", "slave": 1, "addr": 5124, "type": "int32", "scale": 0.01, "unit": "A", "cls": "current", "state_cls": "measurement"},
    {"name": "Solar Battery Temperature", "id": "solar_ess_temp", "slave": 1, "addr": 5126, "type": "int16", "scale": 0.1, "unit": "°C", "cls": "temperature", "state_cls": "measurement"},
    {"name": "Solar Battery SOC", "id": "solar_ess_soc", "slave": 1, "addr": 5127, "type": "uint16", "scale": 1, "unit": "%", "cls": "battery", "state_cls": "measurement"},

    # SLAVE 2: DEVICE INFO
    {"name": "Solar Manufacturer", "id": "solar_manufacturer", "slave": 2, "addr": 30010, "type": "string", "count": 8, "scale": 1, "unit": None, "cls": None, "state_cls": None},
    {"name": "Solar Model", "id": "solar_model", "slave": 2, "addr": 30018, "type": "string", "count": 8, "scale": 1, "unit": None, "cls": None, "state_cls": None},
    {"name": "Solar Serial Number", "id": "solar_serial", "slave": 2, "addr": 30026, "type": "string", "count": 8, "scale": 1, "unit": None, "cls": None, "state_cls": None},

    # SLAVE 2: AC & GRID
    {"name": "Solar AC Output Power", "id": "solar_ac_total_p", "slave": 2, "addr": 30100, "type": "int32", "scale": 1, "unit": "W", "cls": "power", "state_cls": "measurement"},
    {"name": "Solar Grid Power", "id": "solar_grid_total_p", "slave": 2, "addr": 30108, "type": "int32", "scale": 1, "unit": "W", "cls": "power", "state_cls": "measurement"},
    {"name": "Solar Meter Power", "id": "solar_meter_p", "slave": 2, "addr": 30110, "type": "uint32", "scale": 1, "unit": "W", "cls": "power", "state_cls": "measurement"},
    {"name": "Solar Inverter State Raw", "id": "solar_inverter_state_raw", "slave": 2, "addr": 30115, "type": "uint16", "scale": 1, "unit": None, "cls": None, "state_cls": None},

    # SLAVE 2: PV DATA
    {"name": "Solar PV1 Voltage", "id": "solar_pv1_v", "slave": 2, "addr": 30119, "type": "uint16", "scale": 0.1, "unit": "V", "cls": "voltage", "state_cls": "measurement"},
    {"name": "Solar PV1 Current", "id": "solar_pv1_a", "slave": 2, "addr": 30120, "type": "uint16", "scale": 0.1, "unit": "A", "cls": "current", "state_cls": "measurement"},
    {"name": "Solar PV2 Voltage", "id": "solar_pv2_v", "slave": 2, "addr": 30121, "type": "uint16", "scale": 0.1, "unit": "V", "cls": "voltage", "state_cls": "measurement"},
    {"name": "Solar PV2 Current", "id": "solar_pv2_a", "slave": 2, "addr": 30122, "type": "uint16", "scale": 0.1, "unit": "A", "cls": "current", "state_cls": "measurement"},
    {"name": "Solar PV3 Voltage", "id": "solar_pv3_v", "slave": 2, "addr": 30123, "type": "uint16", "scale": 0.1, "unit": "V", "cls": "voltage", "state_cls": "measurement"},
    {"name": "Solar PV3 Current", "id": "solar_pv3_a", "slave": 2, "addr": 30124, "type": "uint16", "scale": 0.1, "unit": "A", "cls": "current", "state_cls": "measurement"},
    {"name": "Solar PV Total Power", "id": "solar_pv_total_p", "slave": 2, "addr": 30127, "type": "int32", "scale": 1, "unit": "W", "cls": "power", "state_cls": "measurement"},
    {"name": "Solar PV Total Energy", "id": "solar_pv_total_e", "slave": 2, "addr": 30129, "type": "float32", "scale": 1, "unit": "kWh", "cls": "energy", "state_cls": "total_increasing"},

    # SLAVE 2: AC PHASES
    {"name": "Solar AC Frequency", "id": "solar_ac_freq", "slave": 2, "addr": 30140, "type": "uint16", "scale": 0.01, "unit": "Hz", "cls": "frequency", "state_cls": "measurement"},
    {"name": "Solar Bus Voltage", "id": "solar_bus_volt", "slave": 2, "addr": 30141, "type": "uint16", "scale": 0.1, "unit": "V", "cls": "voltage", "state_cls": "measurement"},
    {"name": "Solar AC Output Energy Total", "id": "solar_ac_out_e_total", "slave": 2, "addr": 30154, "type": "float32", "scale": 1, "unit": "kWh", "cls": "energy", "state_cls": "total_increasing"},
    {"name": "Grid Import Energy Total", "id": "grid_import_e_total", "slave": 2, "addr": 30156, "type": "float32", "scale": 1, "unit": "kWh", "cls": "energy", "state_cls": "total_increasing"},
]