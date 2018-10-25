#!/usr/bin/env python

import rospy

from robonomics_liability.msg import Liability
from robonomics_liability.srv import *

from std_msgs.msg import String, Empty

class BlinkRedOrBlue:
    def __init__(self):
        rospy.init_node("blink_node")

        self.blink_red = rospy.Publisher('/blink_red', Empty, queue_size=10)
        self.blink_blue = rospy.Publisher('/blink_blue', Empty, queue_size=10)

        def newLiability(l):
            self.liability = l.address
            rospy.loginfo("Got new liability {}".format(l.address))

            prefix = '/liability/eth_' + self.liability
            rospy.Subscriber(prefix + '/blink', String, self.blink)

            rospy.wait_for_service("/liability/start")
            rospy.ServiceProxy('/liability/start', StartLiability)(StartLiabilityRequest(address=self.liability))
        rospy.Subscriber("/liability/ready", Liability, newliability)

        rospy.loginfo("Node is started!")

    def blink(self, data):
        if data.data == "blue":
            rospy.loginfo("Blinking blue...")
            self.blink_blue.publish(Empty())

        if data.data == "red":
            rospy.loginfo("Blinking red...")
            self.blink_red.publish(Empty())

        rospy.wait_for_service('/liability/finish')
        fin = rospy.ServiceProxy('/liability/finish', FinishLiability)
        fin(FinishLiabilityRequest(address=self.liability, success=True))
        rospy.loginfo("Finished")

    def spin(self):
        rospy.spin()

if __name__ == '__main__':
    BlinkRedOrBlue().spin()
