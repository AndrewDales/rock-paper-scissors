import random
import pyinputplus

RULES = {"rps": {"rock": ("scissors",),
                 "scissors": ("paper",),
                 "paper": ("rock",),
                 },
         "rpsls": {"rock": ("scissors", "lizard"),
                   "scissors": ("paper", "lizard"),
                   "paper": ("rock", "spock"),
                   "lizard": ("paper", "spock"),
                   "spock": ("rock", "scissors"),
                   },
         }


class PlayerObject:
    def __init__(self, name, rules=None):
        if rules is None:
            rules = RULES["rps"]
        self.rules = rules
        if name.lower() in self.rules.keys():
            self.name = name.lower()

        else:
            self.name = None

    def __repr__(self):
        return f"PlayerObject({self.name})"

    def __gt__(self, other):
        return other.name in self.rules[self.name]

    def __eq__(self, other):
        return self.name == other.name

    def random_object(self):
        self.name = random.choice(list(self.rules.keys()))


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.current_object = None
        self.rules = RULES["rps"]

    def reset_object(self):
        self.current_object = None

    def win_round(self):
        self.score += 1

    def __repr__(self):
        return f"Player(Name: {self.name}, Score: {self.score}"


class HumanPlayer(Player):
    def choose_object(self, choice):
        self.current_object = PlayerObject(choice, self.rules)


class ComputerPlayer(Player):
    def __init__(self, name):
        super().__init__(name)
        self.name = "Computer"
        self.current_object = PlayerObject("Computer", self.rules)

    def choose_object(self):
        self.current_object.random_object()

    def reset_object(self):
        self.current_object = PlayerObject("Computer")


class Game:
    def __init__(self):
        self.current_round = 0
        self.max_rounds = 10
        self.players = []
        self.round_result = None
        self.round_winner = None
        self.rules = RULES["rps"]

    def add_human_player(self, name):
        self.players.append(HumanPlayer(name))

    def add_computer_player(self):
        self.players.append(ComputerPlayer("Computer"))

    def set_max_rounds(self, rounds):
        if isinstance(rounds, int):
            self.max_rounds = rounds

    def find_winner(self):
        player_1 = self.players[0]
        player_2 = self.players[1]
        if player_1.current_object is not None and player_2.current_object is not None:
            if player_1.current_object == player_2.current_object:
                self.round_result = "Draw"

            elif player_1.current_object > player_2.current_object:
                self.round_winner = player_1.name
                player_1.win_round()
                self.round_result = "Win"
            else:
                self.round_winner = player_2.name
                player_2.win_round()
                self.round_result = "Win"

    def next_round(self):
        self.current_round += 1
        self.round_result = None
        self.round_winner = None
        for player in self.players:
            player.reset_object()

    def is_finished(self):
        return self.current_round >= self.max_rounds

    def reset(self):
        self.current_round = 0
        for player in self.players:
            player.score = 0

    def report_round(self):
        player_1 = self.players[0]
        player_2 = self.players[1]
        message = (f"{player_1.name} chose {player_1.current_object.name}.\n"
                   f"{player_2.name} chose {player_2.current_object.name}.\n"
                   f"The round resulted in a {self.round_result}.\n")

        if self.round_winner == player_1.name:
            message += f"{player_1.name} won the round.\n"

        elif self.round_winner == player_2.name:
            message += f"{player_2.name} won the round.\n"

        return message

    def report_score(self):
        return (f"{self.players[0].name} has {self.players[0].score} points.\n"
                f"{self.players[1].name} has {self.players[1].score} points")

    def report_winner(self):
        if self.players[0].score == self.players[1].score:
            message = f"The game is a draw."

        elif self.players[0].score > self.players[1].score:
            message = f"{self.players[0].name} wins the game"

        else:
            message = f"{self.players[1].name} wins the game"

        return message

    def change_rules(self, rules):
        self.rules = RULES[rules]
        for player in self.players:
            player.rules = self.rules


class Clinterface:
    def __init__(self):
        self.game = Game()

    def set_up(self):
        print("Welcome to Rock, Paper, Scissors!")
        for i in range(2):
            user_choice = pyinputplus.inputChoice(["Computer", "Human"],
                                                  f"Would you like Player {i + 1} to be a computer or a human player?")
            if user_choice == "Human":
                player_name = pyinputplus.inputStr("Enter Name: ")
                self.game.add_human_player(player_name)

            else:
                self.game.add_computer_player()

        self.set_max_rounds()
        self.set_rules()

    def set_max_rounds(self):
        user_rounds = pyinputplus.inputNum("Input number of rounds: ", min=1)
        self.game.set_max_rounds(user_rounds)

    def set_rules(self):
        user_choice = pyinputplus.inputChoice(["RPS", "RPSLS"], "RPS rules or RPSLS rules: ")
        self.game.change_rules(user_choice.lower())

    def get_choices(self):
        for player in self.game.players:
            if isinstance(player, HumanPlayer):
                player_choice = pyinputplus.inputChoice(list(self.game.rules.keys()), f"{player.name} enter move: ")
                player.choose_object(player_choice)

            else:
                player.choose_object()

    def run_game(self):
        while not self.game.is_finished():
            self.get_choices()
            self.game.find_winner()
            print()
            print(self.game.report_round())
            print(self.game.report_score())
            self.game.next_round()

        print(self.game.report_winner())

    def run_sequence(self):
        self.set_up()
        user_quit = False
        while not user_quit:
            self.run_game()
            self.game.reset()
            user_choice = pyinputplus.inputChoice(["Y", "N"], "Do you want to quit Y/N: ")
            if user_choice == "Y":
                user_quit = True


if __name__ == "__main__":
    CLI = Clinterface()
    CLI.run_sequence()
