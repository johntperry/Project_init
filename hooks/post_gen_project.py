'Generates different project profiles based on expected tasks'

from pathlib import Path
import subprocess


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
    "pandas",
]


# Robotics / simulation
robotics = [
    "mujoco==3.2.5",
    "mediapy",
    "imageio-ffmpeg",
]


# Development tools
dev = [
    "pytest",
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
    "robotics": [
        *base,
        *scientific,
        *robotics,
        *dev,
    ],
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

print("Project ready!")