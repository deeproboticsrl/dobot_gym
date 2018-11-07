from dobot_gym.envs import DobotRealEnv
from dobot_gym.utils.vision import Vision
# camera_obj = Vision(camera_port=1)
# print(camera_obj.get_obs_cam(centroid=True))
# camera_obj.show_image()
# camera_obj.show_image()

env = DobotRealEnv()

# env.reset()
for i in range(100):
    ob,r,d,a = env.step(env.action_space.sample())

    print(r,d,a,ob[1])