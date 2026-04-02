
import logging
import asyncio
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, SENSOR_TYPES
from .decoder_app import ModbusDecoder
from .custom_modbus_client import AsyncCustomModbusClient

_LOGGER = logging.getLogger(__name__)

class SolarHubCoordinator(DataUpdateCoordinator):


    def __init__(self, hass: HomeAssistant, host: str, port: int, scan_interval: int):
    
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            # Set the update interval based on user config
            update_interval=timedelta(seconds=scan_interval),
        )
        self.host = host
        self.port = port
        self.client = AsyncCustomModbusClient(host, port)
        self.decoder = ModbusDecoder()

    async def _async_update_data(self):
       
        data = {}
        
        if not self.client.is_connected():
            connected = await self.client.connect()
            if not connected:
                raise UpdateFailed(f"Could not connect to {self.host}")

        for sensor in SENSOR_TYPES:
            uid = sensor["id"]
            slave = sensor["slave"]
            address = sensor["addr"]
            data_type = sensor["type"]
            count = sensor.get("count", 1)

            if data_type in ["int32", "uint32", "float32"] and count == 1:
                count = 2

            try:
                # _LOGGER.debug(f"Reading {uid}: Slave={slave}, Addr={address}")
                
                registers = await self.client.read_holding_registers(slave, address, count)

                if registers is None:
                    # _LOGGER.error(f"Error reading {uid}")
                    data[uid] = None
                    continue

                val = None
                if data_type == "uint16":
                    val = self.decoder.decode_uint16(registers)
                elif data_type == "int16":
                    val = self.decoder.decode_int16(registers)
                elif data_type == "uint32":
                    val = self.decoder.decode_uint32(registers)
                elif data_type == "int32":
                    val = self.decoder.decode_int32(registers)
                elif data_type == "float32":
                    val = self.decoder.decode_float32(registers)
                elif data_type == "string":
                    val = self.decoder.decode_string(registers)

                data[uid] = val

            except Exception as e:
                _LOGGER.error(f"Exception reading {uid}: {e}")
                data[uid] = None
        
        return data