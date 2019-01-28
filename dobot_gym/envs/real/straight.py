import gym
from gym import utils
from glob import glob
from dobot_gym.utils.dobot_controller import DobotController
from gym.spaces import MultiDiscrete


class DobotRealEnv(gym.Env, utils.EzPickle):
    def __init__(self):
        super().__init__()
        available_ports = glob('/dev/tty*USB*')
        if len(available_ports) == 0:
            print('no port found for Dobot Magician')
            exit(1)
        def_port = available_ports[0]

        self.dobot = DobotController(port=def_port)
        self.observation_space = None
        # -1 0 1 actions
        self.action_space = MultiDiscrete([3, 3, 3])
        self.timestep = 0

    def compute_reward(self,poses):
        x,y,z =poses[:3]
        reward = -10*y-10*z+x
        return reward

    def step(self, action):
        real_action = action - 1
        self.dobot.moveangleinc(*real_action, r=0, q=1)
        poses = self.dobot.get_dobot_joint()

        reward = self.compute_reward(poses)
        done = False
        info = None
        if self.timestep > 400 or poses[0] > 331 or poses[0]<110:
            done = True
        self.timestep += 1
        return poses, reward, done, info

    def reset(self):
        self.timestep = 0
        self.dobot.movexyz(*self.dobot.DEFINED_HOME, q=1)
        poses = self.dobot.get_dobot_joint()
        return poses
