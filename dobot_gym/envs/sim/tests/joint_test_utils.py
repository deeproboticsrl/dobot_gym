import copy

import mujoco_py
from gym.envs.robotics import utils


def get_zero_state(initial_state):
    lp = len(initial_state.qpos)
    lv = len(initial_state.qvel)
    zero_state = copy.deepcopy(initial_state)
    for i in range(lp):
        zero_state.qpos[i] = 0
    for i in range(lv):
        zero_state.qvel[i] = 0
    return zero_state


def qpos_incr(i, viewer, sim, num_steps, initial_state, speed, step_flag):
    zero_state = get_zero_state(initial_state)

    # delta state has speed in "i"th dimension and 0 in all others
    delta_state = copy.deepcopy(zero_state)
    delta_state.qpos[i] = speed
    for j in range(0, num_steps):
        viewer.render()
        old_state = sim.get_state()
        new_state = mujoco_py.MjSimState(old_state.time, old_state.qpos + delta_state.qpos, old_state.qvel,
                                         old_state.act, old_state.udd_state)
        sim.set_state(new_state)
        sim.forward()
        if step_flag:
            sim.step()
    # print(new_state.qpos)
    sim.set_state(initial_state)
    sim.forward()
    viewer.render()


def qvel_incr(i, viewer, sim, num_steps, initial_state, speed, step_flag):
    zero_state = get_zero_state(initial_state)
    delta_state = copy.deepcopy(zero_state)
    delta_state.qvel[i] = speed
    for j in range(0, num_steps):
        viewer.render()
        old_state = sim.get_state()
        new_state = mujoco_py.MjSimState(old_state.time, old_state.qpos, old_state.qvel + delta_state.qvel,
                                         old_state.act, old_state.udd_state)
        sim.set_state(new_state)
        sim.forward()
        if step_flag:
            sim.step()
    # print(new_state.qvel)
    sim.set_state(initial_state)
    sim.forward()
    viewer.render()


def dobot_env_setup(sim):
    initial_qpos = {
        'robot0:slide0': 0.8,
        'robot0:slide1': 1.2,
        'robot0:slide2': -0.04,
    }
    gripper_extra_height = 0.2
    for name, value in initial_qpos.items():
        sim.data.set_joint_qpos(name, value)
    utils.reset_mocap_welds(sim)
    sim.forward()

    # gripper_target = np.array([0.8, 1.0, 0.37 + gripper_extra_height]) + sim.data.get_site_xpos('robot0:grip')
    # gripper_rotation = np.array([1., 0., 1., 0.])
    # sim.data.set_mocap_pos('robot0:mocap', gripper_target)
    # sim.data.set_mocap_quat('robot0:mocap', gripper_rotation)
    for _ in range(10):
        sim.step()

    initial_gripper_xpos = sim.data.get_site_xpos('robot0:grip').copy()
