'Generates different project profiles based on expected tasks'

import shutil
import subprocess
from pathlib import Path

PROJECT_TYPE = "{{ cookiecutter.project_type }}"
USE_JUPYTER = "{{ cookiecutter.use_jupyter }}" == "yes"


# Common tools
base = [
    "numpy",
]


# Scientific computing
scientific = [
    "scipy",
    "matplotlib",
    "PySide6", # Required to display the pop-ups that appear in matplotlib
    "pandas",
]


# Robotics / simulation
robotics = [
    "mujoco",
    "mediapy",
    "imageio-ffmpeg",
]

# Teaching / demonstration tools
teaching = [
    "manim",
]

# Development tools
dev = [
    "pytest",
]

ai = [
    "torch",    # https://pytorch.org/
]

# Construct profiles
profiles = {
    "minimal": [
        *base,
        *dev,
    ],
    "scientific": [
        *base,
        *scientific,
        *dev,
    ],
    "AI": [
        *base,
        *scientific,
        *dev,
        *ai,
    ],
    "robotics": [
        *base,
        *scientific,
        *robotics,
        *dev,
    ],
    "demonstration": [
        *base,
        *scientific,
        *teaching,
        *dev,
    ]
}

packages = profiles[PROJECT_TYPE]

if USE_JUPYTER:
    packages += [
        "jupyterlab",
        "ipykernel",
    ]

subprocess.run(["uv", "venv"], check=True)


try:
    if packages:
        subprocess.run(
            ["uv", "add", *packages], 
            check=True
        )
except subprocess.CalledProcessError:
    print(
        """
        uv failed while installing dependencies.

        Try running:
            uv sync

        manually after fixing the issue
        """
    )

# Remove robotics files if robotics preset not used

if PROJECT_TYPE != "robotics":
    robot_dir = Path.cwd() / "Code/robot"
    if robot_dir.exists():
        shutil.rmtree(robot_dir)
    

# Check if the user wants to use the vscode preferences

INCLUDE_VSCODE = "{{ cookiecutter.include_vscode }}".lower()

if INCLUDE_VSCODE != "yes":
    vscode_dir = Path.cwd() / ".vscode"
    if vscode_dir.exists():
        shutil.rmtree(vscode_dir)

print("Project ready!")