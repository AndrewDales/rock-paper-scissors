import tkinter as tk
import random

col_dict = {}


class GameApp(tk.Tk):
    def __init__(self):
        super().__init__()


class MenuFrame(tk.Frame):
    ...


class GameFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.master = master


class LizardSpock(GameFrame):
    def __init__(self, master):
        super().__init__(master)

        self.master = master
        self.options = ["rock", "paper", "scissors", "lizard", "spock"]


class HumanMoveFrame(tk.Frame):
    def __init__(self, master, player, options):
        super().__init__()

        self.master = master
        self.player = player
        self.buttons = None
        self.options = options
        self.choice = tk.StringVar()

        self.title = tk.Label(self, text=f"{player}'s turn")

    def create_options(self):
        self.buttons = [tk.Radiobutton(self,
                                       text=choice,
                                       value=choice,
                                       variable=self.choice,
                                       )
                        for choice in self.options]


class ComputerMoveFrame(tk.Frame):
    def __init__(self, master, player, options):
        super().__init__()

        self.master = master
        self.player = player
        self.options = options

        self.choice = random.choice(self.options)

        self.txt = tk.Label(self, text=f"{player} is thinking...")
