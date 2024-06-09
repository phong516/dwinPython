#! /usr/bin/env python3
# Copyright 2021 Samsung Research America
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Modified by AutomaticAddison.com
 
import time  # Time library
 
from geometry_msgs.msg import PoseStamped # Pose with ref frame and timestamp
from rclpy.duration import Duration # Handles time for ROS 2
import rclpy # Python client library for ROS 2
 
from nav2_simple_commander.robot_navigator import BasicNavigator
from tf_transformations import quaternion_from_euler

'''
Navigates a robot from an initial pose to a goal pose.
'''

def main():
 
  # Start the ROS 2 Python Client Library
  rclpy.init()
 
  # Launch the ROS 2 Navigation Stack
  navigator = BasicNavigator()
 
  # Wait for navigation to fully activate. Use this line if autostart is set to true.
  # navigator.waitUntilNav2Active()

  cmd = input("Enter the goal pose (x#y#yaw#: ")
  goal_pose = PoseStamped()
  goal_pose.header.frame_id = "map"
  goal_pose.header.stamp = navigator.get_clock().now().to_msg()
  goal_pose.pose.position.x = float(cmd.split("x")[1].split("y")[0])
  goal_pose.pose.position.y = float(cmd.split("y")[1].split("yaw")[0])
  goal_pose.pose.position.z = 0.0

  yaw_goal = float(cmd.split("yaw")[1])
  q = quaternion_from_euler(0, 0, yaw_goal)

  goal_pose.pose.orientation.x = q[0]
  goal_pose.pose.orientation.y = q[1]
  goal_pose.pose.orientation.z = q[2]
  goal_pose.pose.orientation.w = q[3]

  navigator.goToPose(goal_pose)

 
if __name__ == '__main__':
    #get the x, y, yaw from user input
    # # is the value
    main()
    
