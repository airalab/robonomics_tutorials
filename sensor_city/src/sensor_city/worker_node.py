#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Standart, System and Third party

# ROS
import rospy
import rosbag
from std_msgs.msg import String

# Web3
from web3 import Web3
from eth_account.messages import defunct_hash_message
from eth_account.account import Account
from base58 import b58decode

# AIRA
from robonomics_msgs.msg import Demand, Result

import ipfsapi
from tempfile import NamedTemporaryFile

class WorkerNode:
    # TODO: need an objective messages collector and empty objective (by new liability) starter
    def __init__(self):
        rospy.init_node('worker')
        rospy.loginfo('Launching worker node...')

        self.ipfs = ipfsapi.connect()

        rospy.Subscriber('/liability/infochan/incoming/demand', Demand, self.process)
        rospy.Subscriber('/measurements', String, self.update_measurements)

        self.pub = rospy.Publisher('/liability/infochan/signing/result', Result, queue_size=128)

        rospy.loginfo('Worker node launched.')

    def update_measurements(self, msg):
        self.measurements = msg.data.split(' ')

    def demandhash(self, msg):
        types = ['bytes',
                 'bytes',
                 'address',
                 'uint256',
                 'address',
                 'uint256',
                 'uint256',
                 'bytes32']
        return Web3.soliditySha3(types, [b58decode(msg.model),
                                         b58decode(msg.objective),
                                         msg.token,
                                         msg.cost,
                                         msg.validator,
                                         msg.validatorFee,
                                         msg.deadline,
                                         msg.nonce])

    def process(self, incoming_demand):
        rospy.loginfo('Incoming ask %s...', str(incoming_demand))
        if (incoming_demand.model == rospy.get_param('~model') and
            incoming_demand.token == rospy.get_param('~token') and
            incoming_demand.cost == 0):

            rospy.loginfo('Starting process...')

            with NamedTemporaryFile(delete=False) as tmpfile:
                recorder = rosbag.Bag(tmpfile.name, 'w')

                output = 'St.Petersburg: {{"DUST": {}, "CO": {}, "LPG": {}, "METHANE": {}, "SMOKE": {}, "HYDROGEN": {}}}'.format(*self.measurements)
                recorder.write('/worker/data', String(data=output))
                recorder.close()

                # recover account of sender
                msg_hash = defunct_hash_message(self.demandhash(incoming_demand))
                sender_account = Account.recoverHash(msg_hash, signature=incoming_demand.signature)

                ipfs_response = self.ipfs.add(tmpfile.name)

                res = Result()
                res.liability = sender_account
                res.result = ipfs_response
                res.success = True

                self.pub.publish(res)

            rospy.loginfo('Process complete.')

    def spin(self):
        rospy.spin()

