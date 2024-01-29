import tkinter as tk
import rps_backend


class GameApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.game = None
        self.frame = None
        self.max_rounds = tk.IntVar()
        self.player_1 = tk.StringVar()
        self.player_2 = tk.StringVar()
        self.name_1 = tk.StringVar()
        self.name_2 = tk.StringVar()
        self.game_mode = tk.StringVar()
        self.max_rounds.set(3)
        self.player_1.set("human")
        self.player_2.set("computer")
        self.game_mode.set("rps")
        self.name_1.set("Player1")
        self.name_2.set("Player2")
        self.title("rock paper scissors game")
        self.title_label = tk.Label(text="Rock🪨 Paper📄 Scissors✂️(Lizard🦎 Spock🖖)", font=("Arial", 12))
        self.title_label.pack()
        self.get_settings()

    def get_settings(self):
        if isinstance(self.frame, ResultsFrame):
            self.frame.pack_forget()
        self.frame = SetUpFrame(self)
        self.frame.pack()

    def start_game(self):
        self.game = rps_backend.Game("Game", self.game_mode.get())
        self.game.set_max_rounds(self.max_rounds.get() - 1)
        if self.player_1.get() == "human":
            self.game.add_human_player(self.name_1.get())
        else:
            self.game.add_computer_player()
            self.name_1.set("Computer")
        if self.player_2.get() == "human":
            self.game.add_human_player(self.name_2.get())
        else:
            self.game.add_computer_player()
            self.name_2.set("Computer")
        self.frame.pack_forget()
        self.frame = GameFrame(self)
        self.frame.pack()

    def end_game(self):
        self.frame.pack_forget()
        self.frame = ResultsFrame(self)
        self.frame.pack()


class SetUpFrame(tk.Frame):
    def __init__(self, master: GameApp):
        super().__init__()
        self.master: GameApp = master
        self.max_rounds_title = tk.Label(self, text="Maximum rounds:")
        self.player_1_title = tk.Label(self, text="Player 1:")
        self.player_2_title = tk.Label(self, text="Player 2:")
        self.mode_title = tk.Label(self, text="Mode")
        self.player_type1 = [tk.Radiobutton(self, text=typ,
                                            command=self.place_widgets,
                                            variable=self.master.player_1,
                                            value=typ)
                             for typ in ["computer", "human"]]
        self.player_type2 = [tk.Radiobutton(self, text=typ,
                                            variable=self.master.player_2,
                                            command=self.place_widgets,
                                            value=typ)
                             for typ in ["computer", "human"]]
        self.mode = [tk.Radiobutton(self, text=typ,
                                    variable=self.master.game_mode,
                                    value=typ)
                     for typ in ["rps", "rpsls"]]
        self.get_name_1 = tk.Entry(self, textvariable=self.master.name_1)
        self.get_name_2 = tk.Entry(self, textvariable=self.master.name_2)
        self.max_rounds = tk.Scale(self, from_=1, to=10, orient="horizontal", variable=self.master.max_rounds,
                                   length=200)
        self.play_button = tk.Button(self, text="Play!", bg="powder blue", command=self.master.start_game)
        self.place_widgets()

    def place_widgets(self):
        self.grid_forget()
        self.max_rounds_title.grid(row=0, column=0)
        self.max_rounds.grid(row=0, column=1, columnspan=3)
        self.player_1_title.grid(row=1, column=0)
        self.player_2_title.grid(row=2, column=0)
        self.mode_title.grid(row=3, column=0)
        for i in range(len(self.player_type1)):
            self.player_type1[i].grid(row=1, column=i + 1)
            self.player_type2[i].grid(row=2, column=i + 1)
        if self.master.player_1.get() == "human":
            self.get_name_1.grid(row=1, column=3, padx=5)
        else:
            self.get_name_1.grid_remove()
        if self.master.player_2.get() == "human":
            self.get_name_2.grid(row=2, column=3, padx=5)
        else:
            self.get_name_2.grid_remove()
        self.play_button.grid(row=3, column=3)
        for i in range(2):
            self.mode[i].grid(row=3, column=i + 1)


class GameFrame(tk.Frame):
    def __init__(self, master: GameApp):
        super().__init__()
        self.master: GameApp = master
        self.select_choice_txt = tk.StringVar()
        self.round_num = tk.IntVar()
        self.obj1 = tk.StringVar(value="Rock🪨")
        self.obj2 = tk.StringVar(value="Rock🪨")
        self.round_num.set(1)
        self.last_round = tk.Label(self, text="")
        self.player_1_title = tk.Label(self, text=self.master.name_1.get())
        self.player_2_title = tk.Label(self, text=self.master.name_2.get())
        self.choices = [obj for obj in self.master.game.player_object.allowed_objects]
        for i in range(len(self.choices)):
            if self.choices[i] == "rock":
                self.choices[i] = "Rock🪨"
            if self.choices[i] == "paper":
                self.choices[i] = "Paper📄"
            if self.choices[i] == "scissors":
                self.choices[i] = "Scissors✂"
            if self.choices[i] == "lizard":
                self.choices[i] = "Lizard🦎"
            if self.choices[i] == "spock":
                self.choices[i] = "Spock🖖"
        self.score = tk.Label(self, text="0:0")
        self.round_message = tk.Label(self, text=f"round {self.round_num.get()} of {self.master.max_rounds.get()}")
        self.submit = tk.Button(self, text="submit", bg="powder blue", command=self.next_round)
        if self.master.player_1.get() == "human":
            self.choice1 = tk.OptionMenu(self, self.obj1, *self.choices)
        else:
            self.choice1 = tk.Label(self, text="Computer choice")
        if self.master.player_2.get() == "human":
            self.choice2 = tk.OptionMenu(self, self.obj2, *self.choices)
        else:
            self.choice2 = tk.Label(self, text="Computer choice")
        self.place_widgets()

    def next_round(self):
        if self.master.game.is_finished():
            self.find_winner()
            self.master.end_game()
        else:
            self.find_winner()
            self.round_num.set(self.round_num.get() + 1)
            self.round_message = tk.Label(self, text=f"round {self.round_num.get()} of {self.master.max_rounds.get()}")
            self.last_round.destroy()
            self.last_round = tk.Label(self, text=f"last round: {self.master.game.players[0].current_object.name} vs."
                                                  f" {self.master.game.players[1].current_object.name}")
            self.score = tk.Label(self, text=f"{self.master.game.players[0].score}:{self.master.game.players[1].score}")
            self.master.game.next_round()
            self.place_widgets()

    def find_winner(self):
        if self.master.player_1.get() == "human":
            self.master.game.players[0].current_object = rps_backend.PlayerObject(self.obj1.get()[:-1],
                                                                                  rps_backend.RULES[
                                                                                      self.master.game_mode.get()])
        else:
            self.master.game.players[0].choose_object()
        if self.master.player_2.get() == "human":
            self.master.game.players[1].current_object = rps_backend.PlayerObject(self.obj2[:-1].get(),
                                                                                  rps_backend.RULES[
                                                                                      self.master.game_mode.get()])
        else:
            self.master.game.players[1].choose_object()
        self.master.game.find_winner()

    def place_widgets(self):
        self.player_1_title.grid(row=0, column=0)
        self.player_2_title.grid(row=0, column=2)
        self.score.grid(row=0, column=1)
        self.choice1.grid(row=1, column=0)
        tk.Label(self, text="vs.").grid(row=1, column=1)
        self.choice2.grid(row=1, column=2)
        self.submit.grid(row=2, column=1)
        self.round_message.grid(row=3, column=1)
        self.last_round.grid(row=4, column=0, columnspan=3)


class ResultsFrame(tk.Frame):
    def __init__(self, master: GameApp):
        super().__init__()
        self.master: GameApp = master
        self.last_round = tk.Label(self, text=f"final round: {self.master.game.players[0].current_object.name} vs."
                                              f" {self.master.game.players[1].current_object.name}")
        self.player_names = tk.Label(self, text=f"{self.master.name_1.get()} vs. {self.master.name_2.get()}")
        self.score = tk.Label(self,
                              text=f"{self.master.game.players[0].score}:{self.master.game.players[1].score}  "
                                   f"{self.master.game.report_winner()} won")
        self.play_again = tk.Label(self, text=f"Play again?")
        self.yes_button = tk.Button(self, text="yes", bg="powder blue", command=self.master.start_game)
        self.no_button = tk.Button(self, text="no", bg="powder blue", command=self.master.get_settings)
        self.place_widgets()

    def place_widgets(self):
        self.player_names.grid(row=0, column=0)
        self.score.grid(row=1, column=0)
        self.play_again.grid(row=2, column=0)
        self.yes_button.grid(row=2, column=1)
        self.no_button.grid(row=2, column=2)
        self.last_round.grid(row=3, column=0)


if __name__ == "__main__":
    app = GameApp()
    app.geometry("450x150")
    app.resizable(False, False)
    app.mainloop()
