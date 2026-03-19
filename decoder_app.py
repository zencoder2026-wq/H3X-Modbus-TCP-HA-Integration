ative Python struct handling.

import struct
import logging

_LOGGER = logging.getLogger(__name__)

class ModbusDecoder:


    def __init__(self):
        pass

    @staticmethod
    def decode_uint16(registers):

        if not registers or len(registers) < 1:
            return None
        return registers[0]

    @staticmethod
    def decode_int16(registers):

        if not registers or len(registers) < 1:
            return None
        val = registers[0]

        if val > 32767:
            val -= 65536
        return val

    @staticmethod
    def decode_uint32(registers):

        if not registers or len(registers) < 2:
            return None

        return (registers[0] << 16) | registers[1]

    @staticmethod
    def decode_int32(registers):

        if not registers or len(registers) < 2:
            return None
        

        val = (registers[0] << 16) | registers[1]
        
   
        try:
            packed = struct.pack('>I', val)
            unpacked = struct.unpack('>i', packed)[0]
            return unpacked
        except Exception as e:
            _LOGGER.error(f"Error decoding int32: {e}")
            return None

    @staticmethod
    def decode_float32(registers):

        if not registers or len(registers) < 2:
            return None
        

        val = (registers[0] << 16) | registers[1]
        
        try:

            packed = struct.pack('>I', val)
            unpacked = struct.unpack('>f', packed)[0]
            return round(unpacked, 4)
        except Exception as e:
            _LOGGER.error(f"Error decoding float32: {e}")
            return None

    @staticmethod
    def decode_string(registers):

        if not registers:
            return None
        
        try:

            byte_string = b""
            for reg in registers:
                byte_string += struct.pack('>H', reg)
            

            decoded = byte_string.decode('utf-8', errors='ignore').replace('\x00', '').strip()
            return decoded
        except Exception as e:
            _LOGGER.error(f"Error decoding string: {e}")
            return "Error"