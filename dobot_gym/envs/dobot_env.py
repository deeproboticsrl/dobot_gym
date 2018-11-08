import gym
from gym import utils
from glob import glob
import dobot_gym.utils.DobotDllType as dType
from dobot_gym.utils.dobot_controller import DobotController
from dobot_gym.utils.vision import Vision  ## gives centroid and rgb image and grey image
from gym.spaces import MultiDiscrete, Discrete
import cv2

class DobotRealEnv(gym.Env, utils.EzPickle):
    def __init__(self, camera_port_left=1):
        self.camera_obj = Vision(camera_port_left=camera_port_left)  ## initialize camera
        available_ports = glob('/dev/tty*USB*')
        if len(available_ports) == 0:
            print('no port found for Dobot Magician')
            exit(1)
        def_port = available_ports[0]

        self.dobot = DobotController(port=def_port)
        self.observation_space = None
        self.action_space = MultiDiscrete([3, 3, 3])
        ## initialize dobot

    def compute_reward(self,image,centroid):
        return 0

    def step(self, action):
        obs = self.get_observation()
        real_action = action - 1
        self.dobot.movexyz(*real_action, r=0, q=1)
        image, centroid, poses = self.get_observation()
        self.image=image
        reward = self.compute_reward(image, centroid)
        done = False
        if not centroid:
            done = True
        return [image, centroid, poses], reward, done,real_action

    def reset(self):
        ## return to home
        lastIndex = dType.SetHOMECmd(self.dobot.api, temp=0, isQueued=0)[0]
        return lastIndex
        # dType.SetQueuedCmdStartExec(self.api)
        #
        # while lastIndex > dType.GetQueuedCmdCurrentIndex(self.api)[0]:
        #     dType.dSleep(500)
        # dType.SetQueuedCmdStopExec(self.api)
        # dType.SetQueuedCmdClear(self.api)

    def get_observation(self):
        im, centroid = self.get_image(centroid=True)
        poses = self.get_dobot_joint()
        return im, centroid, poses

    def get_image(self, centroid=False):

        if centroid:
            im, center = self.camera_obj.get_obs_cam(centroid=centroid)
            return [im, center]
        else:

            ima = self.camera_obj.get_obs_cam(centroid=centroid)
            return ima

    def get_dobot_joint(self):
        poses = dType.GetPose(self.dobot.api)
        return poses

    def render(self):
        # self.camera_obj.show_image(render_time=10)
        cv2.imshow('leftcam',self.image)
    def close():
        self.dobot.disconnect()
        self.ob.cap2.release()

##TODOS
