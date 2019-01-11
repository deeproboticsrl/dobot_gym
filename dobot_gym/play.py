from dobot_gym.envs import DobotCamRealEnv
from dobot_gym.utils.vision import Vision
from dobot_gym.envs import LineReachEnvCam
# camera_obj = Vision(camera_port=1)
# print(camera_obj.get_obs_cam(centroid=True))
# camera_obj.show_image()
# camera_obj.show_image()

env = LineReachEnvCam()

# env.reset()
for i in range(100):
    [image, centroid, poses], reward, done, real_action = env.step(env.action_space.sample())
    env.render()
    print(f'reward:{reward},centroid:{centroid},action:{real_action},done:{done}')