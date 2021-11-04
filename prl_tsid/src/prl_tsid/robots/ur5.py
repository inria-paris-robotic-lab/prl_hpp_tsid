# Do this first as prl_hpp.ur5 requires the node to be already started
import rospy
rospy.init_node("TSID", anonymous=True)

from prl_pinocchio.ur5 import robot

import tsid
from prl_tsid.tsid_commander import Commander

import numpy as np

tsid_robot = tsid.RobotWrapper(robot.pin_model, True, False)

q0 = np.zeros(tsid_robot.nq)
v0 = np.zeros(tsid_robot.nv)
a0 = np.zeros(tsid_robot.na)

formulation = tsid.InverseDynamicsFormulationAccForce("tsid", tsid_robot, False)
formulation.computeProblemData(0.0, q0, v0)

# ROS
commander_left_arm = Commander(robot, robot.left_arm_joints, "/left_arm/scaled_vel_joint_traj_controller/follow_joint_trajectory")
commander_right_arm = Commander(robot, robot.right_arm_joints, "/right_arm/scaled_vel_joint_traj_controller/follow_joint_trajectory")
