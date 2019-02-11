from dobot_gym.envs.real.straight import DobotStraightEnv
import numpy as np

dobot_env = DobotStraightEnv()

dobot_env.reset()

random_action = dobot_env.action_space.sample()
print("Random action -- ", random_action)

fixed_action = np.array([0, 1, 1])
for i in range(55):
    random_action = dobot_env.action_space.sample()
    # obs, reward, done, _ = dobot_env.step(random_action)
    obs, reward, done, _ = dobot_env.step(fixed_action)
    print(done)
