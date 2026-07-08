This file uses cookiecutter to instantly generate a project folder in the format desired, generate from the command line in the folder desired using the command:
python -m cookiecutter https://github.com/johntperry/LaTeX_init.git
and then input the names of desired arguments to finish the setup.

For future, consider adding a setting with cookiecutter that allows for setting up multiple different formats with the same command, and the argument "What is the project name?" > robotics-1 etc. This also means that changes across the base packages (.sty files) and in the main document remain more reliably synced across all template formats.