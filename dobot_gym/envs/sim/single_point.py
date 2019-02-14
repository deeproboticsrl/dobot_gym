import gym


class SinglePointEnv(gym.Env, gym.utils.EzPickle):

    def __init__(self, initial_state, goal_state):
        super().__init__()
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.reached_state = None

    def step(self, action):
        reward = (action - self.goal_state) ** 2
        self.reached_state = action
        return None, reward, True, None

    def render(self, mode="human"):
        print("State reached = ", self.reached_state)

    def reset(self):
        self.reached_state = None
        return None, None, False, None
