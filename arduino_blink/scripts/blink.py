#!/usr/bin/env python

import rospy

from robonomics_liability.msg import Liability
from robonomics_liability.srv import *

from std_msgs.msg import Empty

class BlinkLED:
    def __init__(self):
        rospy.init_node('blink_node')

        self.blink_led = rospy.Publisher('/blink_led', Empty, queue_size=10)

        def newliability(l):
            self.liability = l.address
            rospy.loginfo("Got new liability {}".format(self.liability))

            prefix = "/liability/eth_" + self.liability
            rospy.Subscriber(prefix + '/blink', Empty, self.blink)

            rospy.wait_for_service("/liability/start")
            rospy.ServiceProxy('/liability/start', StartLiability)(StartLiabilityRequest(address=self.liability))
        rospy.Subscriber("/liability/ready", Liability, newliability)

        rospy.loginfo("Node is started!")

    def blink(self, data):
        self.blink_led.publish(Empty())

        rospy.wait_for_service('/liability/finish')
        fin = rospy.ServiceProxy('/liability/finish', FinishLiability)
        fin(FinishLiabilityRequest(address=self.liability, success=True))
        rospy.loginfo("finished")

    def spin(self):
        rospy.spin()

if __name__ == '__main__':
    BlinkLED().spin()
