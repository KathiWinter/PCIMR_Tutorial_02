#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from sensor_msgs.msg import LaserScan 
from numpy import mean

vel_msg = Twist()


class VelocityNode:
  

    def __init__(self):

        self.sub_cmd_vel = rospy.Subscriber("/cmd_vel", Twist, self.cmd_vel_callback)
        self.sub_scan = rospy.Subscriber("/scan", LaserScan, self.scan_callback)
        self.pub = rospy.Publisher('/pioneer/cmd_vel', Twist, queue_size=10)
    
        
        
    def cmd_vel_callback(self, data):
        global vel_msg
 
        vel_msg.linear.x = data.linear.x
        vel_msg.linear.y = data.linear.y
        vel_msg.linear.z = data.linear.z
        vel_msg.angular.x = data.angular.x
        vel_msg.angular.y = data.angular.y
        vel_msg.angular.z = data.angular.z
       

    def scan_callback(self, data):
        global vel_msg 

        range_left = data.ranges[0:int(len(data.ranges)/5)]
        range_right = data.ranges[int(len(data.ranges)/5*3):int(len(data.ranges))]
        range_diagonal_left = data.ranges[int(len(data.ranges)/5):int(len(data.ranges)/5*2)]
        range_diagonal_right = data.ranges[int(len(data.ranges)/5*3):int(len(data.ranges)/5*4)]
        range_forward = data.ranges[int(len(data.ranges)/5*2):int(len(data.ranges)/5*3)]
    
        
        if(self.average(range_forward) < 3 and self.average(range_forward) > 0):
                if(self.average(range_forward)/3-1/3 > 0):
                    vel_msg.linear.x  = self.average(range_forward)/3
                else: 
                    vel_msg.linear.x = 0.0
                vel_msg.linear.y = vel_msg.linear.x
                vel_msg.linear.z = vel_msg.linear.z
                vel_msg.angular.x = 0.0
                vel_msg.angular.y = 0.0
                vel_msg.angular.z = 0.0
        elif(self.average(range_diagonal_left) < 3 and self.average(range_diagonal_left) > 0):
                if(self.average(range_diagonal_left)/3-1/3 > 0):
                    vel_msg.linear.x  = self.average(range_diagonal_left)/3
                else: 
                    vel_msg.linear.x = 0.0
                vel_msg.linear.y = vel_msg.linear.x
                vel_msg.linear.z = vel_msg.linear.z
                vel_msg.angular.x = 0.0
                vel_msg.angular.y = 0.0
                vel_msg.angular.z = 0.0
           
        elif(self.average(range_diagonal_right) < 3 and self.average(range_diagonal_right) > 0):
                if(self.average(range_diagonal_right)/3-1/3 > 0):
                    vel_msg.linear.x  = self.average(range_diagonal_right)/3
                else: 
                    vel_msg.linear.x = 0.0
                vel_msg.linear.y = vel_msg.linear.x
                vel_msg.linear.z = vel_msg.linear.z
                vel_msg.angular.x = 0.0
                vel_msg.angular.y = 0.0
                vel_msg.angular.z = 0.0
           
        print(vel_msg)
        self.pub.publish(vel_msg)

    def average(self,tuple):
         return(sum(tuple) / len(tuple))

    def run(self, rate: float = 1):
   
        while not rospy.is_shutdown():
            if rate:
                rospy.sleep(1/rate)


if __name__ == '__main__':
    rospy.init_node('velocity_node')
    velocity_node = VelocityNode()
    velocity_node.run(rate=1)