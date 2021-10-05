import tkinter as tk


class TestGUI(tk.Frame):
    """ TestGUI is a simple single frame tkinter app demonstrating setting up a button and binding a key press"""
    def __init__(self, parent):
        super().__init__(parent)

        self.edit_text = tk.StringVar()

        self.intro_label = tk.Label(self, text="Try Moving the slider",
                                    background='red')
        self.hello_button = tk.Button(self, text='Say Hello (H)')
        self.goodbye_button = tk.Button(self, text='Say Goodbye (G)')
        self.slider = tk.Scale(self, from_=0, to_=10, orient=tk.HORIZONTAL,
                               command=self.scale_callback)
        self.text_area = tk.Label(self, textvariable=self.edit_text, width=20, height=5)

        self.intro_label.grid(row=0, column=0, columnspan=2, sticky='nsew')
        self.hello_button.grid(row=1, column=0, padx=10, pady=10)
        self.goodbye_button.grid(row=1, column=1, padx=10, pady=10)
        self.slider.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        self.text_area.grid(row=3, column=0, columnspan=2, padx=10, pady=(5, 10))

    def scale_callback(self, val):
        txt = self.edit_text.get()
        # val is by default the value that the slider is set to.
        txt += '\n' + str(val)
        self.edit_text.set(txt)


if __name__ == "__main__":
    root = tk.Tk()
    TestGUI(root).pack()
    root.mainloop()
