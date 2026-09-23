"""
MuJoCo simulation file obtained unlicensed from https://github.com/pab47/pab47.github.io/blob/master/mujoco/python/template_mujoco_python.zip and heavily modified.

It contains the simulation files for a given robot, accessed via an imported class from simulation.robot.
"""

import datetime as dt
from pathlib import Path

import mujoco as mj
import numpy as np
import pandas as pd
from constants import *
from control import create_1d_control_path
from mujoco.glfw import glfw
from simulation.robot import RobotClassToImport
from simulation.lib import data_out, init_names

### ---------- PROPERTIES TO CHANGE ------------ ###

xml_file = "blank"  # xml file (assumes this is in the same folder as this file) (don't include .xml)
simend = 100  # simulation time

print_camera_config = 0  # set to 1 to print camera config

default_camera = None  # Set to the name of the camera you wish to start the view with
data_filename = None  # 'Physical_Design_Informed_hopper' # Provide the filename for the location of the data from simulation

if xml_file == "blank":
    robot = RobotClassToImport(
        xml_file, filename=data_filename, waypoints=waypoints_hopper
    )
else:
    raise NotImplementedError(f"File {xml_file} is not implemented yet!")


# For callback functions
button_left = False
button_middle = False
button_right = False
lastx = 0
lasty = 0


def init_controller(model, data):
    # initialize the controller here. This function is called once, in the beginning
    pass


def controller(model, data):
    # put the controller here. This function is called inside the simulation.
    pass


def keyboard(window, key, scancode, act, mods):
    if act == glfw.PRESS and key == glfw.KEY_BACKSPACE:
        mj.mj_resetData(robot.model, robot.data)
        mj.mj_forward(robot.model, robot.data)


def mouse_button(window, button, act, mods):
    # update button state
    global button_left
    global button_middle
    global button_right

    button_left = glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_LEFT) == glfw.PRESS
    button_middle = (
        glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_MIDDLE) == glfw.PRESS
    )
    button_right = glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_RIGHT) == glfw.PRESS

    # update mouse position
    glfw.get_cursor_pos(window)


def mouse_move(window, xpos, ypos):
    # compute mouse displacement, save
    global lastx
    global lasty
    global button_left
    global button_middle
    global button_right

    dx = xpos - lastx
    dy = ypos - lasty
    lastx = xpos
    lasty = ypos

    # no buttons down: nothing to do
    if (not button_left) and (not button_middle) and (not button_right):
        return

    # get current window size
    width, height = glfw.get_window_size(window)

    # get shift key state
    PRESS_LEFT_SHIFT = glfw.get_key(window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS
    PRESS_RIGHT_SHIFT = glfw.get_key(window, glfw.KEY_RIGHT_SHIFT) == glfw.PRESS
    mod_shift = PRESS_LEFT_SHIFT or PRESS_RIGHT_SHIFT

    # determine action based on mouse button
    if button_right:
        if mod_shift:
            action = mj.mjtMouse.mjMOUSE_MOVE_H
        else:
            action = mj.mjtMouse.mjMOUSE_MOVE_V
    elif button_left:
        if mod_shift:
            action = mj.mjtMouse.mjMOUSE_ROTATE_H
        else:
            action = mj.mjtMouse.mjMOUSE_ROTATE_V
    else:
        action = mj.mjtMouse.mjMOUSE_ZOOM

    mj.mjv_moveCamera(robot.model, action, dx / height, dy / height, cam)


def scroll(window, xoffset, yoffset):
    action = mj.mjtMouse.mjMOUSE_ZOOM
    mj.mjv_moveCamera(robot.model, action, 0.0, -0.05 * yoffset, cam)


def xml_to_mjv_camera(default_camera, model):
    # cam_id = model.camera(default_camera).id

    cam_id = mj.mj_name2id(model, mj.mjtObj.mjOBJ_CAMERA, default_camera)

    # XML camera pose
    pos = model.cam_pos[cam_id].copy()

    return cam


cam = mj.MjvCamera()
opt = mj.MjvOption()  # visualization options

# Init GLFW, create window, make OpenGL context current, request v-sync
glfw.init()
window = glfw.create_window(1200, 900, "Demo", None, None)
glfw.make_context_current(window)
glfw.swap_interval(1)

# initialize visualization data structures
mj.mjv_defaultCamera(cam)
mj.mjv_defaultOption(opt)
scene = mj.MjvScene(robot.model, maxgeom=10000)
context = mj.MjrContext(robot.model, mj.mjtFontScale.mjFONTSCALE_150.value)

# install GLFW mouse and keyboard callbacks
glfw.set_key_callback(window, keyboard)
glfw.set_cursor_pos_callback(window, mouse_move)
glfw.set_mouse_button_callback(window, mouse_button)
glfw.set_scroll_callback(window, scroll)

### ----------- CAMERA CONFIG --------------- ###

# Camera configuration
# cam.azimuth = 45
cam.elevation = -20
cam.distance = 4
cam.lookat = np.array([0.0, 0.0, 0.6])

### ----------------------------------------- ###

cam.type = mj.mjtCamera.mjCAMERA_TRACKING
cam.trackbodyid = robot.model.body(
    "hopper"
).id  # Set the camera to track the top-level body element, this will be different for different codebases.

if default_camera != None:
    cam = xml_to_mjv_camera(default_camera, robot.model)

# initialize the controller
init_controller(robot.model, robot.data)

# set the controller
mj.set_mjcb_control(controller)

# Prepare list to hold timeseries data
simulation_records = []
names = init_names(robot.model)

while not glfw.window_should_close(window):
    time_prev = robot.data.time

    while robot.data.time - time_prev < 1.0 / 60.0:
        mj.mj_step(robot.model, robot.data)

    # Get data out from the simulation
    step_data = data_out(robot.data, names)
    simulation_records.append(step_data)

    if robot.data.time >= simend:
        break

    # get framebuffer viewport
    viewport_width, viewport_height = glfw.get_framebuffer_size(window)
    viewport = mj.MjrRect(0, 0, viewport_width, viewport_height)

    # print camera configuration (help to initialize the view)
    if print_camera_config == 1:
        print(
            "cam.azimuth =",
            cam.azimuth,
            ";",
            "cam.elevation =",
            cam.elevation,
            ";",
            "cam.distance = ",
            cam.distance,
        )
        print(
            "cam.lookat =np.array([",
            cam.lookat[0],
            ",",
            cam.lookat[1],
            ",",
            cam.lookat[2],
            "])",
        )

    # Update the model / control
    robot.update_simulation()

    # Update scene and render
    mj.mjv_updateScene(
        robot.model, robot.data, opt, None, cam, mj.mjtCatBit.mjCAT_ALL.value, scene
    )
    mj.mjr_render(viewport, scene, context)

    # swap OpenGL buffers (blocking call due to v-sync)
    glfw.swap_buffers(window)

    # process pending GUI events, call GLFW callbacks
    glfw.poll_events()

glfw.terminate()

# Convert data out into pandas DataFrame for nice data analysis
df = pd.DataFrame(simulation_records)
print(df.columns.values)

timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")

# Format a data file and save to drive
if data_filename == None:
    DATA_DIR = Path(f"simulation/simulation_data/{xml_file}/general/")
    filename = f"sim_run_{timestamp}.parquet"
else:
    DATA_DIR = Path(f"simulation/simulation_data/{xml_file}/")
    filename = f"{data_filename}_{timestamp}.parquet"

DATA_DIR.mkdir(parents=True, exist_ok=True)
data_path = DATA_DIR / filename

df.to_parquet(data_path, index=False)
print(f"Successfully saved data to: {data_path}")
