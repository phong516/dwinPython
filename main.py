from hmi import MenuSelection
from mqtt import MQTT
import time
import re
import speech_recognition as sr

if __name__ == "__main__":

    self.recognizer = sr.Recognizer()

    mqtt = MQTT(client_id="hodangtu01", broker="a84370b326f84892bb2f62420fc9e5a5.s1.eu.hivemq.cloud")
    mqtt.set_credentials(username="hodangtu0601", password="Hodangtu!@3")
    mqtt.set_callback(on_message=True)
    mqtt.connect()
    mqtt.subscribe("test/topic")
    mqtt.loop_start()

    menu = MenuSelection(port="/dev/ttyUSB0", button_order=0x3000)
    menu.add_menu_item("khoai tây chiên", 0x5000, 15)
    menu.add_menu_item("gà rán", 0x5001, 30)
    menu.add_menu_item("bánh mì", 0x5002, 20)
    menu.add_menu_item("bánh báo", 0x5003, 20)

    menu.add_menu_item("nước lọc", 0x5004, 5)
    menu.add_menu_item("sữa", 0x5005, 10)
    menu.add_menu_item("nước ngọt", 0x5006, 10)
    menu.add_menu_item("kem", 0x5007, 10)


    while True:
        time.sleep(0.1)
        keyCode = menu.dwin.listenLastByte()
        if (keyCode == None):
            continue
        print(keyCode)
        match keyCode:
            case menu.button_order:
                print("manual order")
                bill = menu.ManualOrder()
                mqtt.publish("test/topic", bill)

            case menu.mic:
                print("voice order")
            