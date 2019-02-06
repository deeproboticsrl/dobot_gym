from dobot_gym.envs import DobotCamRealEnv
from dobot_gym.utils.vision import Vision
# from dobot_gym.envs import LineReachEnvCam
# camera_obj = Vision(camera_port=1)
# print(camera_obj.get_obs_cam(centroid=True))
# camera_obj.show_image()
# camera_obj.show_image()
from dobot_gym.envs.real import DobotRealEnv
# env = LineReachEnvCam()

# env.reset()
# for i in range(100):
#     [image, centroid, poses], reward, done, real_action = env.step(env.action_space.sample())
#     env.render()
#     print(f'reward:{reward},centroid:{centroid},action:{real_action},done:{done}')
# from dobot_gym.utils.dobot_controller import DobotController

# cont = DobotController()
# while (1):
#     print(cont.get_dobot_joint())
# cont.moveangleinc(5,5,5,0)
# print(cont.get_dobot_joint())


env = DobotRealEnv()
print(env.action_space.sample())
print(env.observation_space.sample())
env.step(env.action_space.sample())




# lower_limit (doubletaped) = [125.49195861816406, 2.7253544330596924, -11.748306274414062, 1.2441176176071167,
#                                1.2441176176071167, 13.570417404174805, 76.56867218017578, 0.0]


# cartesian coordinates
#low_limit = [125,190, -10]
# hig_limit =[330, -165, 160]