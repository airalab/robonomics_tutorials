#!/usr/bin/env python
import rospy
import serial

from std_srvs.srv import Empty
from std_msgs.msg import String

def blink(data):
    ser = serial.Serial('/dev/ttyUSB0', 9600)

    if data.data == "blue":
        rospy.loginfo("Blinking blue...")
        ser.write(b"blue\n")

    if data.data == "red":
        rospy.loginfo("Blinking red...")
        ser.write(b"red\n")
    
    ser.flush()
    ser.close()

    rospy.wait_for_service("liability/finish")
    fin = rospy.ServiceProxy("liability/finish", Empty)
    rospy.loginfo("finishing...")
    fin()

def main():
    rospy.init_node("blink_node")
    rospy.loginfo("Subscribing...")
    rospy.Subscriber("/blink", String, blink)
    rospy.spin()

if __name__ == '__main__':
    main()
