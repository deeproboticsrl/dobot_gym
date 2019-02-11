## common class for only dobot with cam


import gym
from gym import utils
from glob import glob
from dobot_gym.utils.dobot_controller import DobotController
from gym.spaces import MultiDiscrete


class DobotRealEnv(gym.Env, utils.EzPickle):
    def __init__(self):
        super().__init__()
        # Find the port on which dobot is connected
        available_ports = glob('/dev/tty*USB*')
        if len(available_ports) == 0:
            print('no port found for Dobot Magician')
            exit(1)
        def_port = available_ports[0]

        self.dobot = DobotController(port=def_port)
        self.observation_space = None
        self.action_space = MultiDiscrete([3, 3, 3])

    def compute_reward(self):
        return 0

    def step(self, action):
        real_action = action - 1
        self.dobot.moveangleinc(*real_action, r=0, q=1)
        reward = self.compute_reward(image, centroid)
        poses = self.dobot.get_dobot_joint()
        done = False
        info =None

        return  poses,reward, done, info