import serial
import time

class dwin:
    def __init__(self, port:str="/dev/ttyAMA0", baudrate:int=115200):
        self.dwinSerial = serial.Serial(
                port=port,
                baudrate=baudrate,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=0.1
                )
        # self.dwinSerial.open()

    #call in loop
    def listenLastByte(self):
        first_byte = self.dwinSerial.read(size=1)
        if first_byte != b'\x5a':
            self.dwinSerial.reset_input_buffer()
            return None
        data_size = self.dwinSerial.read(size=2)
        size = int.from_bytes(data_size, byteorder='little')
        data = self.dwinSerial.read(size=size)
        hex_data = data.hex()
        keyCode = int(hex_data[-4:], 16)
        return keyCode

    def setDataVP(self, address:int, data:int):
        sendBuffer = [0x5A, 0xA5, 0x05, 0x82, (address>>8)&0xFF, address&0xFF, (data>>8)&0xFF, data&0xFF]
        self.dwinSerial.write(bytes(sendBuffer))
        time.sleep(0.1)
        self.dwinSerial.reset_input_buffer()

    
    def readDataVP(self, address:int):
        sendBuffer = [0x5A, 0xA5, 0x04, 0x83, (address>>8)&0xFF, address&0xFF, 0x01]
        self.dwinSerial.write(bytes(sendBuffer))
        return self.listenLastByte()
        
    def setTextVP(self, address:int, text:str):
        textLen = len(text)
        textList = list(text)
        sendBuffer = [0x5A, 0xA5, textLen+5, 0x82, (address>>8)&0xFF, address&0xFF]
        for value in textList:
            sendBuffer.append(ord(value))
        sendBuffer.append(0xFF)
        sendBuffer.append(0xFF)
        self.dwinSerial.write(bytes(sendBuffer))

    def switchPage(self, pageID:int):
        sendBuffer = [0x5A, 0xA5, 0x07, 0x82, 0x00, 0x84, 0x5A, 0x01, (pageID>>8)&0xFF, pageID&0xFF]
        self.dwinSerial.write(bytes(sendBuffer))