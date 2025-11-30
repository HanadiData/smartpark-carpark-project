# -*- coding: utf-8 -*-
from config_parser import parse_config


class CarparkManager:
    """Very simple carpark manager.

    - Starts with a fixed number of spaces (capacity)
    - Each arriving car reduces the available spaces by 1
    - Each leaving car increases the available spaces by 1
    """

    def __init__(self, config_file="carpark_config.txt"):
        """Read initial settings from configuration file."""
        config = parse_config(config_file)
        self.capacity = int(config.get("capacity", 1000))
        self.location = config.get("location", "Unknown")
        self._available_spaces = self.capacity

    @property
    def available_spaces(self):
        """How many spaces are currently free."""
        return self._available_spaces

    def car_arrives(self):
        """A car enters the carpark and uses one space."""
        if self._available_spaces > 0:
            self._available_spaces -= 1
        return self._available_spaces

    def car_leaves(self):
        """A car leaves the carpark and frees one space."""
        if self._available_spaces < self.capacity:
            self._available_spaces += 1
        return self._available_spaces

    def is_empty(self):
        """Return True if the carpark has no cars (all spaces free)."""
        return self._available_spaces == self.capacity




