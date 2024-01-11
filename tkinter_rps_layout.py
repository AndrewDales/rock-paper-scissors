import tkinter as tk
from Dales_RPS.game_objects import Game, PlayerObject
from functools import partial


class GameApp(tk.Tk):
    """ GameApp initialises a game and a Tk instance (window)
    The window includes a title and sets up frames with the different views on the game
    The show_frame method unpacks all the frames except for the one that needs to be shown """

    def __init__(self):
        super().__init__()
#         self.game = create_game()
        title_string = ", ".join(obj.title() for obj in PlayerObject.allowable_objects) + " Game"

        # Set the window title
        self.title(title_string)
        self.resizable(False, False)

        # Create an overall title and pack it into the top of the container
        title_label = tk.Label(self,
                               text=title_string,
                               bg="red", fg="white",
                               width=40,
                               font=("Arial", 20))
        title_label.pack(side=tk.TOP)

        # Create a dictionary of frames. The key identifies the frame and the value is an instance of the
        # frame object
        self.frames = {
            "game_frame_one": GameFrameOne(self),
            "game_frame_two": GameFrameTwo(self)}

        # Show the GameOptionsGUI frame
        self.show_frame("game_frame_one")

    # Function to show the desired game class, which is a subclass of tk.Frame
    def show_frame(self, current_frame: str):
        widgets = self.winfo_children()
        # Forget all the existing frames
        for w in widgets:
            if w.winfo_class() == "Frame":
                w.pack_forget()

        # Find and pack the current_frame
        frame_to_show = self.frames[current_frame]
        frame_to_show.pack(expand=True, fill=tk.BOTH)
        frame_to_show.set_up()


class GameFrameOne(tk.Frame):
    def __init__(self, controller: GameApp):
        super().__init__()
        self.controller = controller
        self.round_number = tk.StringVar()
        self.config(background="pink")
        # This spreads out two columns in the available space with equal weight given to both columns
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        title_label = tk.Label(self, text="Frame 1")
        num_rounds_label = tk.Label(self, text="Round Number")
        num_rounds_value = tk.Label(self, textvariable=self.round_number)
        self.next_frame_button = tk.Button(self, text="Next Frame", command=self.next_frame)

        title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        num_rounds_label.grid(row=1, column=0, padx=10, pady=10)
        num_rounds_value.grid(row=1, column=1, padx=10, pady=10)
        self.next_frame_button.grid(row=2, column=1, padx=10, pady=10)

    def set_up(self):
        # Add code to set up variables for this frame. Note this refers to the game object stored on
        # the main app (the controller)
        self.round_number.set(self.controller.game.current_round)

    def next_frame(self):
        self.controller.show_frame("game_frame_two")


class GameFrameTwo(tk.Frame):
    def __init__(self, controller: GameApp):
        super().__init__()
        self.controller = controller
        self.config(background="ivory")
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        title_label = tk.Label(self, text="Frame 2")
        self.next_frame_button = tk.Button(self, text="Next Frame",
                                           command=self.next_frame)
        self.option_buttons = (tk.Button(self, text="Option 1", command=partial(self.option_button, "Option 1")),
                               tk.Button(self, text="Option 2", command=partial(self.option_button, "Option 2")),
                               tk.Button(self, text="Option 3", command=partial(self.option_button, "Option 3")),
                               )

        title_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
        for i, btn in enumerate(self.option_buttons):
            btn.grid(row=1, column=i, padx=10, pady=10)
        self.next_frame_button.grid(row=2, column=2, padx=10, pady=10)

    def set_up(self):
        # Add code to set up variables for this frame
        ...

    def option_button(self, option):
        print(f'You choose {option}')

    def next_frame(self):
        self.controller.show_frame("game_frame_one")


def create_game():
    game = Game()
    game.player = game.add_human_player()
    game.add_computer_player()
    return game


if __name__ == "__main__":
    app = GameApp()
    app.mainloop()
