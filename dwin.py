import serial

class dwin:
    def __init__(self, port:str="/dev/ttyAMA0", baudrate:int=115200):
        self.dwinSerial = serial.Serial(
                port=port,
                baudrate=baudrate,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1
                )
        self.dwinSerial.open()

    #call in loop
    def listenLastByte(self):
       data = self.dwinSerial.read(size=1).hex()
       if (data != 0x5A):
           return
       data = self.dwinSerial.read(size=2).hex()
       data = self.dwinSerial.read(size=data[1]).hex()
       self.dwinSerial.reset_intput_buffer()
       keyCode = data[-1]
       return keyCode

   def setDataVP(self, address:int, data:int):
       sendBuffer = [0x5A, 0xA5, len(data)+3, 0x82, (address>>8)&&0xF, address&&0xF]
       dataList = list(data)
       for value in dataList:
            sendBuffer.append(ord(value))
            self.dwinSerial.write(bytes(sendBuffer))
    
    def readDataVP(self, address:int):
            sendBuffer = [0x5A, 0xA5, 0x04, 0x83, (address>>8)&&0xF, address&&0xF, 0x01]
            dwinSerial.write(bytes(sendBuffer))
            return listenLastByte()
        
