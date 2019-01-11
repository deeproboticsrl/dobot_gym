import dobot_gym.envs.sim.tests.joint_test_utils as utils
import mujoco_py

model = mujoco_py.load_model_from_path("../assets/dobot/reach.xml")

n_substeps = 20
sim = mujoco_py.MjSim(model, nsubsteps=n_substeps)
viewer = mujoco_py.MjViewer(sim)

body_id = sim.model.body_name2id('robot0:gripper_link')
lookat = sim.data.body_xpos[body_id]
for idx, value in enumerate(lookat):
    viewer.cam.lookat[idx] = value
viewer.cam.distance = 2.5
viewer.cam.azimuth = -90.
viewer.cam.elevation = 0.

utils.dobot_env_setup(sim)

data = sim.data
print(data.qpos)
initial_state = sim.get_state()
lp = len(initial_state.qpos)
lv = len(initial_state.qvel)
zero_state = utils.get_zero_state(initial_state)

# main joint test loop and useful params to change
speed = 0
num_steps = 5000
step_flag = 0
for i in range(0, lp):
    utils.qpos_incr(i, viewer, sim, num_steps, initial_state, speed, step_flag)
    print("done for qpos", i)
#
# for i in range(0, lv):
#     utils.qvel_incr(i, viewer, sim, num_steps, initial_state, speed, step_flag)
#     print("done for qvel ", i)
