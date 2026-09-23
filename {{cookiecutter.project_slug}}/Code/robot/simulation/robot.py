"""
File containing the hopper classes used in the simulation.
"""

import os
import string

import mujoco as mj
import numpy as np

from Code.robot.constants import *
from Code.robot.control import Control, Waypoint


class Robot:
    """
    Robot class that defines the different functions that the robot should be able to have, and should be a sub-class of any final robot class.
    """
    def __init__(self, xml_file: string, filename: string, **kwargs):
        """
        Initialise a hopper with:
        - xml: Which describes the type of hopper to be generated, using the xml filename designated at the beginning.
        - control: An undetermined array describing (in some way) the path that the leg must take.

        'init' as a function argument depends on if that function is being run on initialisation or not.
        """
        super().__init__(**kwargs)
        self.xml = xml_file

        self._init_model()

    def _init_model(self):
        # Initialise model and data using the xml path from file.

        dirname = os.path.dirname(__file__)
        abspath = os.path.join(dirname + "/xml_config/" + self.xml + ".xml")

        # Update xml model and instate self.model, self.data
        self.model = self._update_xml_file(abspath)
        self.data = mj.MjData(self.model)

        self.update_simulation(True)

    def update_simulation(self, init=False):
        self.update_robot_geom(init)
        self.update_robot_mass(init)
        self.update_robot_control(init)
        self.update_robot_constants(init)

    def _update_xml_file(self, abspath):
        # Update the xml file before parsing model - this function should not be called after initialisation.
        model = mj.MjModel.from_xml_path(abspath)
        return model

    def update_robot_geom(self, init):
        return

    def update_robot_mass(self, init):
        return

    def update_robot_control(self, init):
        return

    def update_robot_constants(self, init):
        # This function is intended to update the physical constants that control the behaviour of the hopper, such as series elasticity/damping etc.
        return


def update_model_geom(
    model: mj._structs.MjModel, name: str, size=None, pos=None, **kwargs
) -> mj._structs.MjModel:
    # Update desired parameters for a given geometry in a model
    geom_view = model.geom(name)

    if size != None:
        geom_view.size = size
    if pos != None:
        geom_view.pos = pos

    for attr_name, attr_value in kwargs.items():
        if hasattr(geom_view, attr_name):
            setattr(geom_view, attr_name, attr_value)
        else:
            raise AttributeError(f"MjModelGeomViews has no attribute '{attr_name}'.")

    return model


def update_model_body(
    model: mj._structs.MjModel, name: str, size=None, pos=None, **kwargs
) -> mj._structs.MjModel:
    # Update desired parameters for a given body in a model
    body_view = model.body(name)

    if size != None:
        body_view.size = size
    if pos != None:
        body_view.pos = pos

    for attr_name, attr_value in kwargs.items():
        if hasattr(body_view, attr_name):
            setattr(body_view, attr_name, attr_value)
        else:
            raise AttributeError(f"MjModelBodyViews has no attribute '{attr_name}'.")

    return model


def update_model_joint(
    model: mj._structs.MjModel, name: str, damping=None, stiffness=None, **kwargs
) -> mj._structs.MjModel:
    # Update desired parameters for a given joint in a model
    joint_view = model.joint(name)

    if damping != None:
        joint_view.damping = damping
    if stiffness != None:
        joint_view.stiffness = stiffness

    for attr_name, attr_value in kwargs.items():
        if hasattr(joint_view, attr_name):
            setattr(joint_view, attr_name, attr_value)
        else:
            raise AttributeError(f"MjModelJointViews has no attribute '{attr_name}'.")

    return model


def update_model_actuator(
    model: mj._structs.MjModel,
    data: mj._structs.MjData,
    name: str,
    ctrl_length=None,
    kp=None,
    **kwargs,
) -> tuple[mj._structs.MjModel, mj._structs.MjData]:
    # Stub function that should enable the actuator/motor within a model to be adjusted flexibly.
    actuator_id = mj.mj_name2id(model, mj.mjtObj.mjOBJ_ACTUATOR, name)
    actuator_view = model.actuator(name)

    if ctrl_length != None:
        data.ctrl[actuator_id] = ctrl_length
    if kp != None:
        actuator_view.gainprm = kp
        actuator_view.biasprm = -kp

    for attr_name, attr_value in kwargs.items():
        if hasattr(actuator_view, attr_name):
            setattr(actuator_view, attr_name, attr_value)
        else:
            raise AttributeError(
                f"MjModelActuatorViews has no attribute '{attr_name}'."
            )

    return model, data
