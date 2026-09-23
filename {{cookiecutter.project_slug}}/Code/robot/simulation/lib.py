"File containing auxiliary functions to assist in rendering a MuJoCo instance."

import mujoco as mj


def init_names(model):
    # Initialise names of points where simulation data would be desired, general to each model. If not named, give label 'joint_i, etc.'
    joint_names = [
        mj.mj_id2name(model, mj.mjtObj.mjOBJ_JOINT, i) or f"joint_{i}"
        for i in range(model.nq)
    ]
    actuator_names = [
        mj.mj_id2name(model, mj.mjtObj.mjOBJ_ACTUATOR, i) or f"actuator_{i}"
        for i in range(model.nu)
    ]
    body_names = [
        mj.mj_id2name(model, mj.mjtObj.mjOBJ_BODY, i) or f"body_{i}"
        for i in range(model.nbody)
    ]
    geom_names = [
        mj.mj_id2name(model, mj.mjtObj.mjOBJ_GEOM, i) or f"body_{i}"
        for i in range(model.ngeom)
    ]

    names = {
        "joints": {
            "properties": [
                "qpos",
                "qvel",
                "qfrc_inverse",  # This is represents the total internal joint forces
                "qfrc_constraint",  # Value that represents constraint force which can be used to determine FEA simulation parameters
            ],
            "names": joint_names,
        },
        "actuators": {
            "properties": [
                "ctrl",
                "actuator_force",
                "actuator_velocity",
            ],
            "names": actuator_names,
        },
        "bodies": {
            "properties": [
                "qpos",
                "qvel",
            ],
            "names": body_names,
        },
        "geometries": {
            "properties": [
                "qpos",
                "qvel",
            ],
            "names": geom_names,
        },
    }

    return names


def data_out(data, names):
    # Forms a data struct to be appended to the data at current time-step, given the names desired
    # 'names' is a dict of descriptor-names

    # Provide a time-step data point
    step_data = {
        "time": data.time,
    }

    # Loop dynamically over the names structure
    for metadata in names.values():
        names = metadata["names"]
        properties = metadata["properties"]

        for prop in properties:
            # Dynamically grab array from mjData and copy (to prevent overwrite)
            values = getattr(data, prop).copy()

            # Map values to respective names and property type
            for name, val in zip(names, values):
                step_data[f"{prop}_{name}"] = val

    return step_data


def audit_properties(object):
    # A function to quickly invoke an audit on the different possible attributes for a different action
    return [attr for attr in dir(object) if not attr.startswith("_")]
