This file uses cookiecutter to instantly generate a project folder in the format desired, generate from the command line in the folder desired using the command:
python -m cookiecutter https://github.com/johntperry/Project_init.git
and then input the names of desired arguments to finish the setup.

Future additions: (update latex init also)
- Have a hook that allows a pre-prompt to check if there are any properties which can be inherited as a daughter file to a larger project.
- This should read the 'project_defaults' json and reduce the number of questions that need to be answered each time a folder is copied.