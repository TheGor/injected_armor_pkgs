#!/usr/bin/env python


import rospy
from std_msgs.msg import Int16
import random
from random import randint

def talker():
#declares that your node is publishing to the chatter topic using the message type Int16. 
#Int16 here is actually the class #std_msgs.msg.Int16. 
    rospy.init_node('random_number')
    pub = rospy.Publisher('chatter', Int16, queue_size=10)
    rate = rospy.Rate(10) # 10hz
    #random number from 1 to 3 for three different scenes
    random_msg=random.randint(1,3)
    while not rospy.is_shutdown():
        rospy.loginfo(random_msg)
        pub.publish(random_msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass