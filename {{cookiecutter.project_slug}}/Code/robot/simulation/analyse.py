"""
File to analyse the simulation results of sim.py, informing robot design accordingly
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Bool to determine if the most recently created file should be opened for analysis (almost always True)
LOAD_RECENT = True

# Alternatively, load a chosen file from Path
LOAD_ALTERNATE = "general/sim_run_20260716_161534.parquet"

MODEL_FOLDER = "hopper_5_bar_linkage"  # Give the model folder name

# Point to simulation data folder:
DATA_DIR = (
    Path("simulation_data") / MODEL_FOLDER / "general"
)  # Comment out 'general' where desired

# List all parquet files in chosen directory
parquet_files = list(DATA_DIR.glob("*.parquet"))
print(parquet_files)
# If files exist, load the most recent
if parquet_files:
    if LOAD_RECENT:
        # Sort by latest
        latest_file = sorted(parquet_files, key=lambda p: p.stat().st_mtime)[-1]

        print(f"Loading latest run: {latest_file.name}")
        df = pd.read_parquet(latest_file)
    elif not LOAD_RECENT:
        print(f"Loading chosen run: {LOAD_ALTERNATE}")
        df = pd.read_parquet(LOAD_RECENT)
    else:
        print("Choose whether to load the most recent file!")
else:
    raise FileNotFoundError("No parquet files found in the chosen directory!")

### ---------- DATA ANALYSIS ---------- ###

if MODEL_FOLDER == "blank":
    # Calculate the parameters desired

### ---------- PLOTTING --------------- ###

if MODEL_FOLDER == "blank":
    # Customised plotting for the specific file
