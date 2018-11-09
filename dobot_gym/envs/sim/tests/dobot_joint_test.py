import dobot_experiments.env.tests.joint_test_utils as utils
import mujoco_py

model = mujoco_py.load_model_from_path("../assets/dobot/reach.xml")

n_substeps = 20
sim = mujoco_py.MjSim(model, nsubsteps=n_substeps)
utils.dobot_env_setup(sim)
data = sim.data
print(data.qpos)
viewer = mujoco_py.MjViewer(sim)
initial_state = sim.get_state()
lp = len(initial_state.qpos)
lv = len(initial_state.qvel)
zero_state = utils.get_zero_state(initial_state)

# main joint test loop and useful params to change
speed = 1
num_steps = 50
step_flag = True
for i in range(0, lp):
    utils.qpos_incr(i, viewer, sim, num_steps, initial_state, speed, step_flag)
    print("done for qpos", i)
#
# for i in range(0, lv):
#     utils.qvel_incr(i, viewer, sim, num_steps, initial_state, speed, step_flag)
#     print("done for qvel ", i)
