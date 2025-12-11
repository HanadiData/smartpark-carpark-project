# -*- coding: utf-8 -*-

import threading
import time
import tkinter as tk
from typing import Iterable

from carpark import CarparkManager


DISPLAY_INIT = " - - "
SEP = " : "


class WindowedDisplay:

    def __init__(self, root, title: str, display_fields: Iterable[str], manager: CarparkManager):
        self.root = root
        self.manager = manager
        self.display_fields = list(display_fields)

        self.root.title(title)
        self.root.geometry("500x250")
        self.root.resizable(False, False)

        self.gui_elements = {}
        self._create_widgets()
        self.update_display()

    def _create_widgets(self):
        for i, field_name in enumerate(self.display_fields):
            lbl_field = tk.Label(self.root, text=field_name + SEP, font=("Arial", 16))
            lbl_field.grid(row=i, column=0, sticky="w", padx=10, pady=5)

            lbl_value = tk.Label(self.root, text=DISPLAY_INIT, font=("Arial", 16))
            lbl_value.grid(row=i, column=1, sticky="w", padx=10, pady=5)

            self.gui_elements[field_name] = lbl_value

        tk.Label(self.root, text="License plate:", font=("Arial", 14)).grid(
            row=len(self.display_fields), column=0, sticky="w", padx=10, pady=10
        )
        self.plate_entry = tk.Entry(self.root, font=("Arial", 14))
        self.plate_entry.grid(
            row=len(self.display_fields), column=1, sticky="w", padx=10, pady=10
        )

        btn_in = tk.Button(self.root, text="Car IN", font=("Arial", 14),
                           command=self._btn_car_in)
        btn_in.grid(row=len(self.display_fields) + 1, column=0, padx=10, pady=10)

        btn_out = tk.Button(self.root, text="Car OUT", font=("Arial", 14),
                            command=self._btn_car_out)
        btn_out.grid(row=len(self.display_fields) + 1, column=1, padx=10, pady=10)

    def _btn_car_in(self):
        plate = self.plate_entry.get().strip()
        if plate:
            self.manager.incoming_car(plate)
        else:
            self.manager.car_arrives()
        self.update_display()

    def _btn_car_out(self):
        plate = self.plate_entry.get().strip()
        if plate:
            self.manager.outgoing_car(plate)
        else:
            self.manager.car_leaves()
        self.update_display()

    def update_display(self):
        spaces = self.manager.available_spaces
        temp = self.manager.temperature
        now = self.manager.current_time

        if "Available spaces" in self.gui_elements:
            self.gui_elements["Available spaces"]["text"] = str(spaces)
        if "Temperature" in self.gui_elements:
            self.gui_elements["Temperature"]["text"] = f"{temp:.1f} °C"
        if "Current time" in self.gui_elements:
            self.gui_elements["Current time"]["text"] = now

        self.root.update_idletasks()


def temperature_thread(manager: CarparkManager):
    t = 20.0
    while True:
        t += 0.5
        if t > 25:
            t = 18.0
        manager.temperature_reading(t)
        time.sleep(3)


def main():
    root = tk.Tk()
    manager = CarparkManager()
    display = WindowedDisplay(
        root,
        title="SmartPark Carpark",
        display_fields=["Available spaces", "Temperature", "Current time"],
        manager=manager,
    )

    manager.set_display(display)

    thread = threading.Thread(target=temperature_thread, args=(manager,), daemon=True)
    thread.start()

    root.mainloop()


if __name__ == "__main__":
    main()
