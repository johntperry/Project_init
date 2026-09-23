"""
File defining any control classes used for robot function.
"""

from bisect import bisect_right
from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Waypoint:
    time: float
    position: np.ndarray[np.float64]


class Control:
    """
    Control class that should be inherited by classes describing a specific robot.
    """
    def __init__(self, waypoints: list[Waypoint], **kwargs):
        super().__init__(**kwargs)
        if not waypoints:
            raise ValueError("Trajectory requires at least one waypoint.")

        # Sort destinations chronologically
        self.waypoints = sorted(waypoints, key=lambda w: w.time)
        self.wptimes = [w.time for w in self.waypoints]

        # Flexibility of dimensionality
        self.dim = len(self.waypoints[0].position)
        for i, wp in enumerate(self.waypoints):
            if len(wp.position) != self.dim:
                raise ValueError(
                    f"""
                    Inconsistency of waypoint dimension at index {i}!\n
                    
                    Expected dimensionality {self.dim}D, but received {len(wp.position)}D!
                    """
                )

    def get_current_waypoint(self, current_time: float) -> Waypoint:
        """Returns the most recent waypoint whose time <= current_time."""
        idx = bisect_right(self.wptimes, current_time) - 1
        if idx <= -1:
            return None

        return self.waypoints[idx]


def create_1d_control_path(profile, limits, frequency, simulation_time):
    # Flexible control function that can quickly write complex control paths with little effort
    # Frequency in Hz

    waypoints = []
    precision = 100  # Waypoints per second

    avg = (limits[1] + limits[0]) / 2
    diff = abs(limits[1] - limits[0])
    position = 0

    for t in range(np.floor(simulation_time * precision)):
        if profile == "sinusoid":
            position = float(
                diff / 2 * np.sin(2 * np.pi * frequency * t / precision) + avg
            )
        elif profile == "sawtooth":
            position = limits[1] - (diff * frequency * t / precision) % diff
        if round(position, 3) > limits[1]:
            print("reached top!")
            position = limits[1]
        elif round(position, 3) < limits[0]:
            print("reached bottom!")
            position = limits[0]

        waypoints.append(Waypoint(time=t / precision, position=[0.0, position]))

    return waypoints
