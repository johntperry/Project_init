This file uses cookiecutter to instantly generate a project folder in the format desired, generate from the command line in the folder desired using the command:
python -m cookiecutter https://github.com/johntperry/Project_init.git
and then input the names of desired arguments to finish the setup.

To ensure modules install correctly, due to aggressive caching used by uv add the following exclusions from your antivirus software:
- Customise to wherever uv is installed on your machine.
- C:\Users\{user}\AppData\Local\uv\cache\
- C:\Users\{user}\AppData\Roaming\uv\python\

When (if) setting up MuJoCo:
- Currently the MuJoCo version called is significantly older than the current best, due to ongoing issues with syncing across versions. If in future the version of MuJoCo (and Python) are wished to be updated, then refer to this issues log: https://github.com/google-deepmind/mujoco/issues/2275.

Future additions: (update latex init also)
- Have a hook that allows a pre-prompt to check if there are any properties which can be inherited as a daughter file to a larger project.
- This should read the 'project_defaults' json and reduce the number of questions that need to be answered each time a folder is copied.