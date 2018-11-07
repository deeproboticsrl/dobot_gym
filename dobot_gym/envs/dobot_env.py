import gym
from gym import utils
from glob import glob
from dobot_gym.utils.dobot_controller import DobotController
from dobot_gym.utils.vision import  Vision  ## gives centroid and rgb image and grey image
class DobotRealEnv(gym.Env,utils.EzPickle ):
    def __init__(self):
        self.ob= Vision() ## initialize camera
        available_ports = glob('/dev/tty*USB*')
        if len(available_ports) == 0:
            print('no port found for Dobot Magician')
            exit(1)
        def_port = available_ports[0]

        self.dobot = DobotController(port=def_port)

        ## initialize dobot

        pass
    def compute_reward(self):
        im,centroid =self.get_image(centroid=True)


    def step(self):
        pass

    def reset(self):
        ## return to home
        lastIndex = dType.SetHOMECmd(self.api, temp=0, isQueued=1)[0]

        dType.SetQueuedCmdStartExec(self.api)

        while lastIndex > dType.GetQueuedCmdCurrentIndex(self.api)[0]:
            dType.dSleep(500)
        dType.SetQueuedCmdStopExec(self.api)
        dType.SetQueuedCmdClear(self.api)


    def get_observation(self):
        im = self.get_image(centroid=False)
        poses = self.get_dobot_joint()
        return [im,poses]

    def get_image(self,centroid=False):
        if centroid:
        im,center= self.ob.get_obs_cam(centroid= centroid)
            return im,center
        else:
            im=self.ob.get_obs_cam(centroid=centroid)
            return im
    def get_dobot_joint(self):
        poses = self.dobot.GetPose(self.api)
        return  poses

    def close():
        self.dobot.disconnect()
        self.ob.cap2.release()


##TODOS
