from hmi import MenuSelection
from mqtt import MQTT

from geometry_msgs.msg import PoseStamped # Pose with ref frame and timestamp
from rclpy.duration import Duration # Handles time for ROS 2
import rclpy # Python client library for ROS 2
 
from nav2_simple_commander.robot_navigator import BasicNavigator
from tf_transformations import quaternion_from_euler

import time

import re

from enum import Enum

UNNAVIGATED = 0
RUNNING = 1
ORDERING = 2
ORDERED = 3

def setGoalPose(x:float, y:float, yaw:float)->None:
    goal_pose = PoseStamped()
    goal_pose.header.frame_id = "map"
    goal_pose.header.stamp = navigator.get_clock().now().to_msg()

    goal_pose.pose.position.x = x
    goal_pose.pose.position.y = y
    goal_pose.pose.position.z = 0.0

    orientation = quaternion_from_euler(0, 0, yaw)
    goal_pose.pose.orientation.x = orientation[0]
    goal_pose.pose.orientation.y = orientation[1]
    goal_pose.pose.orientation.z = orientation[2]
    goal_pose.pose.orientation.w = orientation[3]

    navigator.goToPose(goal_pose)


if __name__ == "__main__":

#NAV2-------------------------------------------------------------
    rclpy.init()
    navigator = BasicNavigator()
    
#MQTT-----------------------------------------------------------
    mqtt = MQTT(client_id="hodangtu01", broker="e94ecb09544d4cd39ee5231c33b0f001.s2.eu.hivemq.cloud")
    mqtt.set_credentials(username="hodangtu0601", password="Hodangtu!@3")
    mqtt.set_callback(on_message=True, on_connect=True)
    mqtt.connect()
    mqtt.subscribe("manager/order")
    mqtt.subscribe("manager/deliver")
    mqtt.loop_start()

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
    bill:str = ""
    tablePoses = [
        [1.0, 0.0, -1.57],
        [2.0, 0.0, -1.57],
        [3.0, 0.0, -1.57]
    ]

    tableReceived: dict = {}
    trayReceived: dict = {}
    isWaiting: bool = False

    while True:
        time.sleep(0.1)
        # print(keyCode)

        if isWaiting:
            keyCode = menu.dwin.listenLastByte()
            match keyCode:
                case menu.button_order:
                    print("manual order")
                    bill = menu.order(UseMic=False)
                    print(bill)

                case menu.button_mic:
                    print("mic")
                    bill = menu.order(UseMic=True)

                case menu.button_yes:
                    print("yes")
                    for table in tableReceived:
                        if tableReceived[table] == ORDERING:
                            bill = "Bàn %d\n %s" % (table, bill)
                    mqtt.publish(topic="client/bill", payload=bill)
                    bill = ""
                    isWaiting = False

                case menu.button_deliveried:
                    print("delivered")
                    isWaiting = False

                

        if mqtt.message_received == True:
            mqtt.message_received = False
            isWaiting = False
            match mqtt.message.topic:
                case 'manager/order':
                    tables = re.findall(r'\d+', mqtt.message.payload.decode("utf-8"))
                    for table in tables:
                        if int(table) < len(tablePoses):
                            tableReceived[int(table)] = UNNAVIGATED

                case 'manager/deliver':
                    tables = re.findall(r'(\d+)\/(\d+)', mqtt.message.payload.decode("utf-8"))
                    for table in tables:
                        if int(table[0]) < len(tablePoses):
                            tableReceived[int(table[0])] = UNNAVIGATED
                            trayReceived[int(table[0])] = table[1]


        for table in tableReceived:
            if tableReceived[table] == UNNAVIGATED:
                setGoalPose(tablePoses[table][0], tablePoses[table][1], tablePoses[table][2])
                tableReceived[table] = RUNNING
                time.sleep(5)
                menu.resetOrder()
                break

            if tableReceived[table] == RUNNING:
                if navigator.isTaskComplete():
                    tableReceived[table] = ORDERING
                    isWaiting = True
                    if trayReceived == {}:
                        menu.startOrder()
                    else:
                        menu.deliver(int(trayReceived[table]))
                    print("ordering")

                break

            if tableReceived[table] == ORDERING:
                if isWaiting == False:
                    print("next table")
                    tableReceived[table] = ORDERED
                break

            if tableReceived[table] == ORDERED:
                #if tableReceived reached the end of the list
                if table == list(tableReceived.keys())[-1]:
                    tableReceived = {}
                    trayReceived = {}
                    setGoalPose(0.0, 0.0, 0.0)
                    time.sleep(5)
                    menu.resetOrder()
