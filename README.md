This file uses cookiecutter to instantly generate a project folder in the format desired. 

## Initialisation

Generate this template from the command line in the folder desired using the command:

`
python -m cookiecutter https://github.com/johntperry/Project_init.git
`

then inputting the names of desired arguments to finish the setup.

To ensure modules install correctly, due to aggressive caching used by uv add the following exclusions from your antivirus software: (customise to the location of uv on your machine)
- C:\Users\user\AppData\Local\uv\cache\
- C:\Users\user\AppData\Roaming\uv\python\

## Running code within the directory

If running files within this directory, this is done via the command line and the following is run after cd-ing into the correct folder:

`
uv run python {file}.py
`

In Jupyter, to set up video properly, the ffmpeg path must be updated using the following (in a Jupyter notebook):

```
ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
media._config.ffmpeg_name_or_path = ffmpeg_path
```

When (if) setting up MuJoCo:
- Currently the MuJoCo version called is significantly older than the current best, due to ongoing issues with syncing across versions. If in future the version of MuJoCo (and Python) are wished to be updated, then refer to this issues log: https://github.com/google-deepmind/mujoco/issues/2275.

### Future additions: (update latex init also)
- Have a hook that allows a pre-prompt to check if there are any properties which can be inherited as a daughter file to a larger project.
    - This should read the 'project_defaults' json and reduce the number of questions that need to be answered each time a folder is copied.
- Add a hook to potentially append the .gitignore list to the __uv__ gitignore (in /.venv/), slightly cleaning up the appearance of the final production project.
    - Consider also having an exception of the .gitignore itself to still be synced via git by adding an exception to the /.venv/ directory, allowing .gitignore within .venv to be synced.
- Add different 'fundamental' python libraries/functions that would be valuable for different cases. For example:
    - A plotting.py file, which has a bunch of useful shortcuts to clean up some of the matplotlib mess into a more pleasant format. Specifically, this should target the ease of use to plot more complex behaviours in one or two lines.
    - Additionally to above, use python libraries to update the appearance of matplotlib, or have a '.mplstyle' file included with this project init.
    - _For MuJoCo_: A simple simulation file template, which makes it easier to simulate a basic scene without a lot of the complex set-up. It could come with a baked-in class structure it expects as an input, improving speed of iteration.