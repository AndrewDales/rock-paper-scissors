import tkinter as tk
from tkinter import font

# Put these as class attributes within the app (neater than global attributes)
pad_settings = {"padx": "5px", "pady": "5px"}


def c_to_f(temp):
    return [(int(temp) * 9 / 5) + 32, u"\N{DEGREE FAHRENHEIT}"]


def f_to_c(temp):
    return [(int(temp) - 32) * 5 / 9, u"\N{DEGREE CELSIUS}"]


class TemperatureApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.bg_colours = ["#E6E6FF", "#E6EEFF", "#E6F7FF", "#E6FBFF", "#E6FFF7", "#F2FFE6", "#FFFFE6", "#FFF7E6", "#FFF2E6", "#FFEEE6", "#FFE6E6"]
        self.fg_colours = ["#cdcdff", "#cdddff", "#cdefff", "#cdf7ff", "#cdffef", "#e5ffcd", "#ffffcd", "#ffefcd", "#ffe5cd", "#ffddcd", "#ffcdcd"]
        self.units = {"C": c_to_f, "F": f_to_c}

        self.rowconfigure(0, weight=2, uniform="a")
        self.rowconfigure(1, weight=2, uniform="a")
        self.rowconfigure(2, weight=1, uniform="a")

        self.columnconfigure(0, weight=1, uniform="b")

        # Very nice splitting each part into a from on the tk.Tk subclass
        self.title("Temperature Converter")
        self.input_frame = TempInputFrame(self)
        self.unit_frame = PickUnitFrame(self)
        self.display_frame = DisplayFrame(self)

        self.input_frame.grid(row=0, column=0, sticky="news")
        self.unit_frame.grid(row=1, column=0, sticky="news")
        self.display_frame.grid(row=2, column=0, sticky="news", **pad_settings)

        self.config(bg="#f2fffd")

    def get_temp(self):
        return self.input_frame.edt.get()

    def convert_temp(self, from_unit):
        temp_input = self.get_temp()
        new_temp = self.units[from_unit](temp_input)
        if from_unit == "C":
            self.colour_index(temp_input)
        else:
            self.colour_index(new_temp[0])
        self.display_frame.txt.config(text="Converted Temperature:{:.2F}{}".format(*new_temp))

    def colour_index(self, c_temp):
        temp_index = int(c_temp // 10)
        if temp_index < 0:
            temp_index = 0
        elif temp_index > 10:
            temp_index = 10
        new_col = self.bg_colours[temp_index]
        new_col2 = self.fg_colours[temp_index]
        self.change_cols(new_col, new_col2)

    def change_cols(self, colour, colour2):
        self.config(bg=colour)
        self.unit_frame.config(bg=colour)
        self.input_frame.config(bg=colour)
        self.input_frame.txt.config(bg=colour)
        self.input_frame.edt.config(bg=colour2)
        self.display_frame.txt.config(bg=colour2)


class TempInputFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Do you need the uniform option? Experiment with and without it.
        self.rowconfigure(0, weight=1, uniform="a")
        self.rowconfigure(1, weight=1, uniform="a")

        self.columnconfigure(0, weight=1, uniform="b")

        # Consider using color names - or creating a dictionary with colour names (for readability)
        self.txt = tk.Label(self,
                            text="Enter temperature:",
                            font=('', 14),
                            bg="#f2fffd",
                            fg="#004761")
        self.edt = tk.Entry(self,
                            font=("", 16),
                            bg="#e6f2f0",
                            fg="#004761")
        self.place_input()
        self.config(bg="#f2fffd")

    def place_input(self):
        self.txt.grid(row=0, column=0, sticky="news", **pad_settings)
        self.edt.grid(row=0, column=1, sticky="ew", **pad_settings)


class PickUnitFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.master = master

        self.temp = self.master.get_temp()

        self.grid_columnconfigure(0, weight=1, uniform='a')
        self.grid_columnconfigure(1, weight=1, uniform='a')

        self.c_btn = tk.Button(self,
                               text="Convert to celsius",
                               font=("Ariel", 16),
                               bg="#fff2f5",
                               fg="#004761",
                               command=lambda: self.master.convert_temp("F")
                               )

        self.f_btn = tk.Button(self,
                               text="Convert to fahrenheit",
                               font=("Ariel", 16),
                               bg="#fff2f5",
                               fg="#004761",
                               command=lambda: self.master.convert_temp("C"),
                               )

        self.place_buttons()
        self.config(bg="#f2fffd")

    def place_buttons(self):
        self.c_btn.grid(row=0, column=0, sticky="news", **pad_settings)
        self.f_btn.grid(row=0, column=1, sticky="news", **pad_settings)


class DisplayFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.master = master

        self.txt = tk.Label(self,
                            text="Converted temperature:",
                            font=("", 15),
                            bg="#e6f2f0",
                            fg="#004761")

        self.place_output()

    def place_output(self):
        self.txt.pack(side=tk.LEFT, fill="both", expand=True)


if __name__ == '__main__':
    app = TemperatureApp()
    app.mainloop()
