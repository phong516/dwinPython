import dwin
import time

hmi = dwin.dwin()

button_1 = 0x3000

data_1 = 0x5000

while(1):
	time.sleep(0.1)
	keyCode = hmi.listenLastByte()
	if (keyCode == None):
		continue
	print(keyCode)
	match keyCode:
		case button_1:
			hmi.setDataVP(data_1, 10)
	
