from dobot_gym.envs import DobotSimGoalEnv

initial_qpos = {
    'robot0:slide0': 0.0,
    'robot0:slide1': 0.0,
    'robot0:slide2': 0.0,
}
env = DobotSimGoalEnv(model_path='../assets/dobot/reach.xml', n_actions=4, n_substeps=20,
                      distance_threshold=0.01, initial_qpos=0)
