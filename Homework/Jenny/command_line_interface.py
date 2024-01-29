import rps_backend


class CLInterface:
    def __init__(self):
        self.mode = rps_backend.inputMenu(["rps", "rpsls"], "rps or rpsls?\n")
        self.game = rps_backend.Game("Game", self.mode)

    def set_up(self):
        for i in range(2):
            typ = rps_backend.inputMenu(["computer", "human"], "Computer/human?\n")
            if typ == "human":
                name = input("Name: ")
                self.game.add_human_player(name)
            else:
                self.game.add_computer_player()
        self.set_max_rounds()

    def set_max_rounds(self):
        val = " "
        while not val.isdecimal():
            val = input("Maximum rounds: ")
        self.game.max_rounds = val

    def get_choices(self):
        for player in self.game.players:
            player.choose_object()

    def run_game(self):
        while not self.game.is_finished():
            self.game.next_round()
            self.get_choices()
            self.game.find_winner()
            self.game.report_round()
            self.game.report_score()
            print("------")
        print(f"{self.game.report_winner()} won")

    def run_sequence(self):
        while True:
            self.set_up()
            while not (input("Do you want to play again?").lower()[0] == "n"):
                self.run_game()
                self.game.reset()
            print("You have quit the game")


if __name__ == "__main__":
    cli_interface = CLInterface()
    cli_interface.run_sequence()
