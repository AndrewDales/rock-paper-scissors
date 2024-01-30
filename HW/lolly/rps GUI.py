import tkinter as tk
from rock_paper_scissors import PlayerObject


class GameApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.settings = {'padx': 10, 'pady': 10}
        self.title("Rock Paper Scissors")
        self.menu_frame = Menu(self)
        self.game_frame = Game(self)

        self.pack_frames()

    def pack_frames(self):
        self.menu_frame.grid()

    def play(self):
        self.menu_frame.grid_forget()
        self.game_frame.grid()
    def back_to_menu(self):
         self.game_frame.grid_forget()
         self.menu_frame.grid()

class Menu(tk.Frame):
    def __init__(self, game_app):
        super().__init__()

        self.settings = {'padx': 10, 'pady': 10}
        self.game_app = game_app

        self.rps_btn = tk.Button(self, text="rock paper scissors", command=self.rps_selected)
        self.rpsls_btn = tk.Button(self, text="rock paper scissors lizard spock", command=self.rpsls_selected)

        self.num_rounds = tk.StringVar()
        self.rounds_entry = tk.Entry(self, width=25, textvariable=self.num_rounds)

        self.player1_name = tk.StringVar()
        self.player1_name_entry = tk.Entry(self, width=25, textvariable=self.player1_name)

        self.player2_name = tk.StringVar()
        self.player2_name_entry = tk.Entry(self, width=25, textvariable=self.player2_name)

        self.human_player1_btn = tk.Button(self, text="Human", command=self.human_player1)
        self.computer_player1_btn = tk.Button(self, text="computer", command=self.computer_player1)

        self.human_player2_btn = tk.Button(self, text="Human", command=self.human_player2)
        self.computer_player2_btn = tk.Button(self, text="computer", command=self.human_player2)

        self.name_label = tk.Label(self, text="opponent name:")

        self.play_btn = tk.Button(self, text="PLAY!", command=self.game_app.play)
        self.play_btn.config(bg="green")

        text = ["game type", "number of rounds", "player 1","player 2" ]
        x = 0
        for item in text:
            self.response_txt = tk.Label(self, text=item)
            self.response_txt.configure(font=("Calibri", 12))
            self.response_txt.grid(row=x, column=0, sticky="W", **self.settings)
            x += 1

        self.place_widgets()

    def place_widgets(self):
        global settings
        self.rps_btn.grid(row=0, column=1, **self.settings)
        self.rpsls_btn.grid(row=0, column=2, **self.settings)
        self.rounds_entry.grid(row=1, column=1, **self.settings)
        self.human_player1_btn.grid(row=2, column=1, **self.settings)
        self.computer_player1_btn.grid(row=2, column=2, **self.settings)
        self.human_player2_btn.grid(row=3, column=1, **self.settings)
        self.computer_player2_btn.grid(row=3, column=2, **self.settings)
        self.play_btn.grid(row=4, column=1, **self.settings)

    def rpsls_selected(self):
        self.game_app.game_frame.lizard_btn.grid(row=1, column=3, **self.settings)
        self.game_app.game_frame.spock_btn.grid(row=1, column=4, **self.settings)

    def rps_selected(self):
        self.game_app.game_frame.lizard_btn.grid_remove()
        self.game_app.game_frame.spock_btn.grid_remove()

    def human_player1(self):
        self.player1_name.grid(row=2, column=3, **self.settings)
        self.player1_name_entry.grid(row=2, column=4, **self.settings)

    def computer_player1(self):
        self.player1_name.grid_forget()
        self.player1_name_entry.grid_forget()


    def human_player2(self):
        self.player2_name.grid(row=3, column=3, **self.settings)
        self.player2_name_entry.grid(row=3, column=4, **self.settings)

    def computer_player2(self):
        self.player2_name.grid_forget()
        self.player2_name_entry.grid_forget()

class Game(tk.Frame):
    def __init__(self, game_app):
        super().__init__()
        self.game_app = game_app
        self.settings = {'padx': 10, 'pady': 10}

        self.score = tk.Label(self, text="0:0")

        self.back_btn = tk.Button(self, text="back to menu", command=self.game_app.back_to_menu)
        self.back_btn.config(bg="green")

        self.rock_btn = tk.Button(self, text="ROCK")
        self.rock_btn.config(bg="grey")

        self.paper_btn = tk.Button(self, text="PAPER")
        self.paper_btn.config(bg="white")

        self.scissors_btn = tk.Button(self, text="SCISSORS")
        self.scissors_btn.config(bg="red")

        self.lizard_btn = tk.Button(self, text="LIZARD")
        self.lizard_btn.config(bg="green")

        self.spock_btn = tk.Button(self, text="SPOCK")
        self.spock_btn.config(bg="gold")

        self.place_game_widgets()

    def place_game_widgets(self):
        self.score.grid(row=0, column=0, **self.settings)
        self.rock_btn.grid(row=1, column=0, **self.settings)
        self.paper_btn.grid(row=1, column=1, **self.settings)
        self.scissors_btn.grid(row=1, column=2, **self.settings)
        self.back_btn.grid(row=2, column=0, **self.settings)


if __name__ == '__main__':
    app = GameApp()
    app.mainloop()
