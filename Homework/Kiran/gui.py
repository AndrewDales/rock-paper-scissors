import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as tk_messagebox
from functools import partial
from main import Game, Hand, RULESETS, HumanPlayer


class GameApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.game = Game()
        self.title('Rock Paper Scissors')
        self.resizable(False, False)

        self.frames = {
            'setup_frame': SetupFrame(self),
            'choose_frame': ChooseFrame(self),
        }
        self.show_frame('setup_frame')

    def show_frame(self, current_frame: str):
        widgets = self.winfo_children()
        for widget in widgets:
            if widget.winfo_class() == 'Frame':
                widget.pack_forget()
        frame_to_show = self.frames[current_frame]
        frame_to_show.pack(expand=True, fill=tk.BOTH)
        frame_to_show.set_up()

    def end_of_round(self):
        """
        Shows a frame that reports the result of a round, and begin the next round if the game is not finished.
        If the game is finished, shows a frame that asks the player whether they want to play again.
        """
        self.game.find_round_winner()
        tk_messagebox.showinfo(f'Round {self.game.current_round+1}', self.game.report_round(), parent=self)
        self.game.next_round()
        if self.game.is_finished():
            # report winner ask if user wants to play again
            response = tk_messagebox.askyesnocancel(
                'Game over',
                f'{self.game.report_winner()}\nWould you like to play again with the same options?',
                detail='Press No to change the settings and Cancel to quit.',
                parent=self,
            )
            if response is None:
                self.destroy()
            elif response:
                # reset game and restart
                self.game.reset()
                self.show_frame('choose_frame')
            else:
                self.game = Game()
                self.show_frame('setup_frame')
        else:
            self.show_frame('choose_frame')


class SetupFrame(tk.Frame):
    def __init__(self, parent: GameApp):
        super().__init__()
        self.parent = parent

        # player one
        self.player_one_label = tk.Label(self, text='Player 1', font=('', 15))
        self.player_one_name_label = tk.Label(self, text='Name:')
        self.player_one_name_entry = tk.Entry(self)
        self.player_one_is_computer = tk.BooleanVar(None, False)
        self.player_one_human_radiobutton = ttk.Radiobutton(
            self, text='Human', variable=self.player_one_is_computer, value=False,
        )
        self.player_one_computer_radiobutton = ttk.Radiobutton(
            self, text='Computer', variable=self.player_one_is_computer, value=True,
        )

        # player two
        self.player_two_label = tk.Label(self, text='Player 2', font=('', 15))
        self.player_two_name_label = tk.Label(self, text='Name:')
        self.player_two_name_entry = tk.Entry(self)
        self.player_two_is_computer = tk.BooleanVar(None, True)
        self.player_two_human_radiobutton = ttk.Radiobutton(
            self, text='Human', variable=self.player_two_is_computer, value=False,
        )
        self.player_two_computer_radiobutton = ttk.Radiobutton(
            self, text='Computer', variable=self.player_two_is_computer, value=True,
        )

        # game
        self.game_label = tk.Label(self, text='Game', font=('', 15))
        self.max_rounds_label = tk.Label(self, text='Max rounds:')
        self.max_rounds_entry = ttk.LabeledScale(self, from_=1, to=20)
        self.ruleset_label = tk.Label(self, text='Ruleset:')
        self.ruleset_combobox = ttk.Combobox(self, state='readonly', values=list(RULESETS.keys()))
        self.ruleset_combobox.current(0)

        self.go_button = tk.Button(self, text='Go', font=('', 15), command=self.create_game)

        self.place_widgets()

    def place_widgets(self):
        padding = {
            'padx': 5,
            'pady': 10,
        }
        self.player_one_label.grid(row=0, column=0, **padding)
        self.player_one_name_label.grid(row=1, column=0, sticky='e', **padding)
        self.player_one_name_entry.grid(row=1, column=1, sticky='w', **padding)
        self.player_one_human_radiobutton.grid(row=2, column=0, **padding)
        self.player_one_computer_radiobutton.grid(row=2, column=1, **padding)

        self.player_two_label.grid(row=3, column=0, **padding)
        self.player_two_name_label.grid(row=4, column=0, sticky='e', **padding)
        self.player_two_name_entry.grid(row=4, column=1, sticky='w', **padding)
        self.player_two_human_radiobutton.grid(row=5, column=0, **padding)
        self.player_two_computer_radiobutton.grid(row=5, column=1, **padding)

        self.game_label.grid(row=6, column=0, **padding)
        self.max_rounds_label.grid(row=7, column=0, sticky='e', **padding)
        self.max_rounds_entry.grid(row=7, column=1, sticky='w', **padding)
        self.ruleset_label.grid(row=8, column=0, sticky='e', **padding)
        self.ruleset_combobox.grid(row=8, column=1, sticky='w', **padding)

        self.go_button.grid(row=9, column=0, **padding)

    def set_up(self):
        pass
        # variables can go here

    def create_game(self):
        # use inputs from tk form to add players / change ruleset etc.

        # create players
        player_one_name = self.player_one_name_entry.get() or 'Player One'
        player_one_computer = self.player_one_is_computer.get()
        self.parent.game.create_player(player_one_name, player_one_computer)

        player_two_name = self.player_two_name_entry.get() or 'Player Two'
        player_two_computer = self.player_two_is_computer.get()
        self.parent.game.create_player(player_two_name, player_two_computer)

        # set max rounds
        max_rounds = self.max_rounds_entry.value
        self.parent.game.set_max_rounds(max_rounds)

        # set ruleset
        ruleset = self.ruleset_combobox.get()
        Hand.set_ruleset(ruleset)

        self.parent.show_frame('choose_frame')


class ChooseFrame(tk.Frame):
    def __init__(self, parent: GameApp):
        super().__init__()
        self.parent = parent
        self.current_player: HumanPlayer | None = None
        self.waiting = tk.BooleanVar()

        self.label = tk.Label(self)
        self.buttons = [tk.Button(
            self,
            text=option,
            command=partial(self.make_choice, option),
        ) for option in Hand.allowable_hands]

        self.place_widgets()

    def place_widgets(self):
        padding = {
            'padx': 5,
            'pady': 10,
        }
        self.label.grid(row=0, column=0, columnspan=3, **padding)
        for index, button in enumerate(self.buttons):
            button.grid(row=1, column=index, **padding)

    def set_up(self):
        for player in self.parent.game.players:
            if isinstance(player, HumanPlayer):
                self.current_player = player
                self.label.config(text=f'{player.name}, choose your hand: ')
                self.waiting.set(True)
                self.wait_variable(self.waiting)  # wait for button to be pressed
            else:
                player.choose_hand()
        self.parent.end_of_round()

    def make_choice(self, choice: str):
        self.current_player.choose_hand(choice)
        self.waiting.set(False)


class Results(tk.Frame):
    # this frame will be shown once user selects an option
    def __init__(self, parent: GameApp):
        super().__init__()
        self.parent = parent

        self.header = tk.Label(self, text=f'Round {self.parent.game.current_round}', font=('', 15))

        # insert results and score here once game is functional



if __name__ == '__main__':
    # root = tk.Tk()
    # root.title('Rock Paper Scissors')
    # f = ChooseFrame(root)
    # f.pack()
    # root.mainloop()

    app = GameApp()
    app.mainloop()

