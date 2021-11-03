from prl_hpp.robot import Robot
from prl_hpp.planner import Planner
from prl_hpp.commander import Commander

"""
 Create instances of Robot, Planner and Commander classes, dedicated for the Double-UR5 robot.
"""

class UR5_Robot(Robot):
    left_gripper_name = "l_gripper"
    right_gripper_name = "r_gripper"

    def __init__(self, compositeName, robotName, robot_description_param_prefix, joint_state_topic):
        Robot.__init__(self, compositeName, robotName, robot_description_param_prefix, joint_state_topic)

        # Init joints group
        joints = self.get_joint_names(with_prefix = False)
        self.gripper_joints = list(filter(lambda joint: joint.lower().find("gripper") != -1, joints))

        # joints = set(joints) - set(self.gripper_joints) # Remove grippers joints from list
        self.left_arm_joints  = list(filter(lambda joint: joint.lower().find("left")  != -1 and joint.lower().find("gripper") == -1, joints))
        self.right_arm_joints = list(filter(lambda joint: joint.lower().find("right") != -1 and joint.lower().find("gripper") == -1, joints))

class UR5_Planner(Planner):
    def __init__(self, robot):
        Planner.__init__(self, robot)

    def lock_grippers(self):
        return self.lock_joints(self.robot.gripper_joints)

    def lock_left_arm(self):
        return self.lock_joints(self.robot.left_arm_joints)

    def lock_right_arm(self):
        return self.lock_joints(self.robot.right_arm_joints)

    def left_gripper_at_pose(self, position, orientation, start_configuration = None):
        return self.tool_at_pose("/left_gripper_grasp_frame", position, orientation, start_configuration)

    def right_gripper_at_pose(self, position, orientation, start_configuration = None):
        return self.tool_at_pose("/right_gripper_grasp_frame", position, orientation, start_configuration)

ur5_robot = UR5_Robot("prl_ur5_robot", "dbl_ur5", "prl_ur5_description", "joint_states")
ur5_robot.MAX_JOINT_SPEED = 3.1415926 / 1.0 # 180°/s
ur5_robot.MAX_JOINT_ACC = 3.1415926 / 1.0 # 180°/s^2

ur5_planner = UR5_Planner(ur5_robot)

ur5_commander_left_arm = Commander(ur5_robot, ur5_robot.left_arm_joints, "/left_arm/scaled_vel_joint_traj_controller/follow_joint_trajectory")
ur5_commander_right_arm = Commander(ur5_robot, ur5_robot.right_arm_joints, "/right_arm/scaled_vel_joint_traj_controller/follow_joint_trajectory")
