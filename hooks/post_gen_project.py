'Generates different project profiles based on expected tasks'

from pathlib import Path
import subprocess

PROJECT_TYPE = "{{ cookiecutter.project_type }}"
USE_JUPYTER = "{{ cookiecutter.use_jupyter }}" == "yes"

profiles = {
    "base": [
        "numpy",
    ],
    "scientific": [
        "scipy",
        "matplotlib",
        "pandas",
    ],
    "robotics": [
        "mujoco",
    ],
}

packages = profiles[PROJECT_TYPE]

if USE_JUPYTER:
    packages += [
        "jupyterlab",
        "ipykernel",
    ]

subprocess.run(["uv", "venv"], check=True)

if packages:
    subprocess.run(["uv", "add", *packages], check=True)

print("Project ready!")