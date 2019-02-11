from dobot_gym.envs.real.straight import DobotStraightEnv

dobot_env = DobotStraightEnv()

dobot_env.reset()

random_action = dobot_env.action_space.sample()
print("Random action -- ", random_action)

for i in range(10):
    random_action = dobot_env.action_space.sample()
    obs, reward, done, _ = dobot_env.step(random_action)
