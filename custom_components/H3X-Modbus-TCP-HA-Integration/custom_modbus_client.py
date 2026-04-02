
import asyncio
import struct
import logging

_LOGGER = logging.getLogger(__name__)

class AsyncCustomModbusClient:


    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self._reader = None
        self._writer = None

        self._transaction_id = 0  

    async def connect(self):
     
        try:
            _LOGGER.debug(f"Connecting to {self.host}:{self.port}...")
            self._reader, self._writer = await asyncio.open_connection(self.host, self.port)
            _LOGGER.debug("Connected successfully.")
            return True
        except Exception as e:
            _LOGGER.error(f"Connection failed: {e}")
            return False

    def is_connected(self):
       
        return self._writer is not None and not self._writer.is_closing()

    async def close(self):
        
        if self._writer:
            self._writer.close()
            try:
                await self._writer.wait_closed()
            except Exception:
                pass
            self._writer = None
            self._reader = None

    async def read_holding_registers(self, slave_id, start_address, count):
  
        if not self.is_connected():
            await self.connect()

        self._transaction_id = (self._transaction_id + 1) & 0xFFFF
        tx_id = self._transaction_id

        proto_id = 0x0000

        length = 6

        unit_id = slave_id

        func_code = 0x03


        packet = struct.pack(
            '>HHHBBHH',     
            tx_id,          
            proto_id,       
            length,         
            unit_id,        
            func_code,      
            start_address,  
            count           
        )

        _LOGGER.debug(f"TX RAW ({self.host}): {packet.hex().upper()}")

        try:
            
            self._writer.write(packet)
            await self._writer.drain()

            header_data = await self._reader.readexactly(7)
            
            rx_tx_id, rx_proto, rx_len, rx_unit = struct.unpack('>HHHB', header_data)
            

            if rx_tx_id != tx_id:
                _LOGGER.warning(f"Transaction ID mismatch! Sent: {tx_id}, Recv: {rx_tx_id}")


            if rx_proto != 0x0000:
                _LOGGER.warning(f"Invalid Protocol ID: {rx_proto}")

            if rx_unit != unit_id:
                _LOGGER.error(f"Unit ID mismatch. Expected {unit_id}, got {rx_unit}")
                return None


            remaining_bytes = rx_len - 1
            
            pdu_data = await self._reader.readexactly(remaining_bytes)
            
            full_response = header_data + pdu_data
            _LOGGER.debug(f"RX RAW ({self.host}): {full_response.hex().upper()}")

            rx_func_code = pdu_data[0]
            rx_byte_count = pdu_data[1]
            rx_payload = pdu_data[2:]


            if rx_func_code != func_code:
                if rx_func_code == (func_code + 0x80):
                    _LOGGER.error(f"Modbus Exception Response: Code {rx_payload[0]}")
                else:
                    _LOGGER.error(f"Function code mismatch. Sent: {func_code}, Recv: {rx_func_code}")
                return None


            if len(rx_payload) != rx_byte_count:
                _LOGGER.warning(f"Payload length mismatch. Header said {rx_byte_count}, got {len(rx_payload)}")


            registers = []
            for i in range(0, len(rx_payload), 2):
                if i + 2 > len(rx_payload):
                    break

                reg = struct.unpack('>H', rx_payload[i:i+2])[0]
                registers.append(reg)

            return registers

        except asyncio.IncompleteReadError:
            _LOGGER.error("Incomplete Read - Device closed connection.")
            await self.close()
            return None
        except Exception as e:
            _LOGGER.error(f"Socket Error: {e}")
            await self.close()
            return None