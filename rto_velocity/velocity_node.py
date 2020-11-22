#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from sensor_msgs.msg import LaserScan 
from numpy import mean


class VelocityNode:

    def __init__(self):

        self.sub_cmd_vel = rospy.Subscriber("/cmd_vel", Twist, self.cmd_vel_callback)
        self.sub_scan = rospy.Subscriber("/scan", LaserScan, self.scan_callback)
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    
        
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
        vel_msg_pub = vel_msg

        #Partition the sensor range into five smaller ranges
        #range_left = data.ranges[0:int(len(data.ranges)/5)]
        #range_right = data.ranges[int(len(data.ranges)/5*3):int(len(data.ranges))]
        range_diagonal_left = data.ranges[int(len(data.ranges)/5):int(len(data.ranges)/5*2)]
        range_diagonal_right = data.ranges[int(len(data.ranges)/5*3):int(len(data.ranges)/5*4)]
        range_forward = data.ranges[int(len(data.ranges)/5*2):int(len(data.ranges)/5*3)]
      
        #Let the robot go backwards, when we want so
        if(vel_msg.linear.x < 0):
            vel_msg_pub.linear.x = vel_msg.linear.x
        #If closer to an object than distance 3, but further away than 0.33, proportionally reduce speed
        elif(self.average(range_forward) < attention_distance and self.average(range_forward) > 0):
            if(self.average(range_forward)/3-stop_distance > 0):
                #If the input is slower than the required speed, listen to the input
                vel_msg_pub.linear.x  = min(vel_msg.linear.x, self.average(range_forward)/3)

            else: 
                vel_msg_pub.linear.x = 0.0
                vel_msg_pub.linear.z = 0.0
             
        elif(self.average(range_diagonal_left) < attention_distance and self.average(range_diagonal_left) > 0):
            if(self.average(range_diagonal_left)/3-stop_distance > 0):
                vel_msg_pub.linear.x  = min(vel_msg.linear.x, self.average(range_diagonal_left)/3)
               

            else: 
                vel_msg_pub.linear.x = 0.0
                vel_msg_pub.linear.z = 0.0
           
        elif(self.average(range_diagonal_right) < attention_distance and self.average(range_diagonal_right) > 0):

            if(self.average(range_diagonal_right)/3-stop_distance > 0):
                vel_msg_pub.linear.x  = min(vel_msg.linear.x, self.average(range_diagonal_right)/3)
                
            else: 
                vel_msg_pub.linear.x = 0.0
                vel_msg_pub.linear.z = 0.0
          
        #If no attention_distance is invaded, drive es input says
        else: 
            vel_msg_pub.linear.x = vel_msg.linear.x  
            vel_msg_pub.linear.y = vel_msg.linear.y
            vel_msg_pub.linear.z = vel_msg.linear.z
        vel_msg_pub.angular.x = vel_msg.angular.x
        vel_msg_pub.angular.y = vel_msg.angular.y
        vel_msg_pub.angular.z = vel_msg.angular.z
        self.pub.publish(vel_msg_pub)

    def average(self,tuple):
         return(sum(tuple) / len(tuple))

    def run(self, rate: float = 1):

        while not rospy.is_shutdown():
            if rate:
                rospy.sleep(1/rate)


if __name__ == '__main__':
    
    rospy.init_node('rto_velocity')
    velocity_node = VelocityNode()

    vel_msg = Twist()
    stop_distance = rospy.get_param('~stop_distance')
    attention_distance = rospy.get_param('~attention_distance')

    velocity_node.run(rate=1)