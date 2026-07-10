This file uses cookiecutter to instantly generate a project folder in the format desired, generate from the command line in the folder desired using the command:
python -m cookiecutter https://github.com/johntperry/Project_init.git
and then input the names of desired arguments to finish the setup.

When (if) setting up MuJoCo:
- Make sure the latest stable release is installed from the official GitHub https://github.com/google-deepmind/mujoco/releases (or alternatively a specific version of the mujoco python package may be requested and that same version installed)
- 

Future additions: (update latex init also)
- Work on understanding how to initialise MuJoCo consistently, and have this work as a pre-set program with the 'robotics' project type.
- Have a hook that allows a pre-prompt to check if there are any properties which can be inherited as a daughter file to a larger project.
- This should read the 'project_defaults' json and reduce the number of questions that need to be answered each time a folder is copied.