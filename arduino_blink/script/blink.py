#!/usr/bin/env python
import rospy
import serial

from std_msgs.msg import Empty

def blink(data):
    rospy.loginfo("Blinking...")
    ser = serial.Serial('/dev/ttyUSB0', 9600)
    ser.write(b"blink\n")

def main():
    rospy.init_node("blink_node")
    rospy.loginfo("Subscribing...")
    rospy.Subscriber("/blink", Empty, blink)
    rospy.spin()

if __name__ == '__main__':
    main()
