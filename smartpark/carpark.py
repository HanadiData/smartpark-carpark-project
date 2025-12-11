# -*- coding: utf-8 -*-

from datetime import datetime
from config_parser import parse_config
from interfaces import CarparkSensorListener, CarparkDataProvider


class Car:
    """Represents a single car in the carpark."""

    def __init__(self, license_plate, time_in=None, make="", model=""):
        self.license_plate = license_plate
        self.time_in = time_in if time_in is not None else datetime.now()
        self.time_out = None
        self.make = make
        self.model = model

    def set_exit_time(self, time_out=None):
        """Set the time this car left the carpark."""
        self.time_out = time_out if time_out is not None else datetime.now()

    def __repr__(self):
        return (
            f"Car({self.license_plate}, in={self.time_in}, "
            f"out={self.time_out}, make={self.make}, model={self.model})"
        )


class CarparkManager(CarparkSensorListener, CarparkDataProvider):
    """Main carpark manager."""

    def __init__(self, config_file="carpark_config.txt", display_window=None, log_file=None):
        config = parse_config(config_file)
        self.capacity = int(config.get("capacity", 1000))
        self.location = config.get("location", "Unknown")
        self._available_spaces = self.capacity

        self._cars = {}
        self._temperature = 0.0

        self.log_file = log_file if log_file is not None else config.get(
            "log_file", "carpark_log.txt"
        )

        self.display_window = display_window

    @property
    def available_spaces(self):
        """Number of spaces currently free."""
        return self._available_spaces

    @property
    def temperature(self):
        """Current temperature value."""
        return self._temperature

    @property
    def current_time(self):
        """Current time as a string."""
        return datetime.now().strftime("%H:%M:%S")

    def is_empty(self):
        """True if all spaces are free."""
        return self._available_spaces == self.capacity

    def cars_currently_parked(self):
        """List of Car objects currently in the carpark."""
        return list(self._cars.values())

    def set_display(self, display_window):
        """Attach or update the display window."""
        self.display_window = display_window

    def log_event(self, message: str):
        """Write a line to the log file with a timestamp."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {message}\n")

    def _update_display(self):
        """Ask the display to refresh if it exists."""
        if self.display_window is not None:
            self.display_window.update_display()

    def car_arrives(self, license_plate=None, make: str = "", model: str = ""):
        """Handle a car entering the carpark."""
        if self._available_spaces <= 0:
            self.log_event(
                f"ENTRY DENIED: Carpark full. Car {license_plate or 'UNKNOWN'} refused."
            )
            return self._available_spaces

        if license_plate:
            if license_plate in self._cars:
                self.log_event(
                    f"ENTRY DENIED: Car {license_plate} already in carpark."
                )
                return self._available_spaces

            car = Car(license_plate=license_plate, make=make, model=model)
            self._cars[license_plate] = car
            self.log_event(f"ENTRY: Car {license_plate} entered at {car.time_in}.")
        else:
            self.log_event("ENTRY: Car with no license plate recorded entered.")

        self._available_spaces -= 1
        self._update_display()
        return self._available_spaces

    def car_leaves(self, license_plate=None):
        """Handle a car leaving the carpark."""
        if not license_plate and self._available_spaces == self.capacity:
            return self._available_spaces

        if license_plate:
            if license_plate not in self._cars:
                self.log_event(
                    f"EXIT DENIED: Car {license_plate} not found in carpark."
                )
                return self._available_spaces

            car = self._cars[license_plate]
            car.set_exit_time()
            self.log_event(f"EXIT: Car {license_plate} exited at {car.time_out}.")
            del self._cars[license_plate]
        else:
            self.log_event("EXIT: Car with no license plate recorded left.")

        if self._available_spaces < self.capacity:
            self._available_spaces += 1
        self._update_display()
        return self._available_spaces

    def incoming_car(self, license_plate):
        """Signal that a car has parked in a bay."""
        return self.car_arrives(license_plate)

    def outgoing_car(self, license_plate):
        """Signal that a car has left a bay."""
        return self.car_leaves(license_plate)

    def temperature_reading(self, reading):
        """Record a new temperature reading."""
        self._temperature = reading
        self.log_event(f"Temperature reading: {reading}")
        self._update_display()
