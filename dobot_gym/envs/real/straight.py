from glob import glob

import gym
import numpy as np
from dobot_gym.utils.dobot_controller import DobotController
from gym.spaces import MultiDiscrete, Box


class DobotStraightEnv(gym.Env, gym.utils.EzPickle):
    def __init__(self):
        super().__init__()
        available_ports = glob('/dev/tty*USB*')
        if len(available_ports) == 0:
            print('no port found for Dobot Magician')
            exit(1)
        def_port = available_ports[0]

        self.dobot = DobotController(port=def_port)
        # poses =[pose.x, pose.y, pose.z, pose.rHead, pose.joint1Angle,
        # pose.joint2Angle, pose.joint3Angle, pose.joint4Angle(gripper)]
        # ignore rhead and joint4angle
        self.poses_low = np.array([125, -165, -10, -50, -5, -5])
        self.poses_high = np.array([330, 190, 160, 55, 70, 75])
        self.observation_space = Box(low=self.poses_low, high=self.poses_high)

        # -1 0 1 actions - Incremental change in angles
        self.action_space = MultiDiscrete([3, 3, 3])
        self.timestep = 0

        self.max_timesteps = 400

    def compute_reward(self, poses):
        x, y, z = poses[:3]
        reward = -10 * y - 10 * z + x
        return reward

    def step(self, action):
        real_action = action - 1
        self.dobot.moveangleinc(*real_action, r=0, q=1)
        poses = self.dobot.get_dobot_joint()

        # [pose.x, pose.y, pose.z, pose.rHead, pose.joint1Angle, pose.joint2Angle, pose.joint3Angle, pose.joint4Angle]

        reward = self.compute_reward(poses)
        # TODO done condition using dobot limits
        done = False
        info = None
        if self.timestep > self.max_timesteps or not self.check_pose_limit(poses):
            done = True
        self.timestep += 1
        return poses, reward, done, info

    def check_pose_limit(self, poses):
        print("Poses ", poses,poses[4]<self.poses_low[3])
        if poses[0] > self.poses_high[0] or poses[0] < self.poses_low[0] or poses[1] < self.poses_low[1] or poses[1] > \
                self.poses_high[1] or poses[2] > self.poses_high[2] or poses[2] < self.poses_low[2] or poses[4] > \
                self.poses_high[3] or poses[4] < self.poses_low[3] or poses[5] > self.poses_high[4] or poses[5] < \
                self.poses_low[4] or poses[6] > self.poses_high[5] or poses[6] < self.poses_low[5]:
            # limit break
            return False
        else:
            return True

    def reset(self):
        self.timestep = 0
        self.dobot.movexyz(*self.dobot.DEFINED_HOME, q=1)
        poses = self.dobot.get_dobot_joint()
        return poses
