from hmi import MenuSelection

from geometry_msgs.msg import PoseStamped # Pose with ref frame and timestamp
from rclpy.duration import Duration # Handles time for ROS 2
import rclpy # Python client library for ROS 2
 
from nav2_simple_commander.robot_navigator import BasicNavigator
from tf_transformations import quaternion_from_euler

import time

import re

if __name__ == "__main__":


#MENU--------------------------------------------------------------
    menu = MenuSelection(port="/dev/serial/by-path/platform-3f980000.usb-usb-0:1.1.3:1.0-port0")
    menu.add_menu_item("khoai tây chiên", 0x5000, 15)
    menu.add_menu_item("gà rán", 0x5001, 30)
    menu.add_menu_item("bánh mì", 0x5002, 20)
    menu.add_menu_item("bánh bao", 0x5003, 20)

    menu.add_menu_item("nước lọc", 0x5004, 5)
    menu.add_menu_item("sữa", 0x5005, 10)
    menu.add_menu_item("nước ngọt", 0x5006, 10)
    menu.add_menu_item("kem", 0x5007, 10)

#LOOP----------------------------------------------------------------
    while True:
        time.sleep(0.1)
        # print(keyCode)

        keyCode = menu.dwin.listenLastByte()
        match keyCode:
            case menu.button_order:
                print("manual order")
                bill = menu.order(UseMic=False)
                print(bill)

            case menu.button_mic:
                print("mic")
                bill = menu.order(UseMic=True)

    
