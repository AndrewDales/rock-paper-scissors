from random import choice
from pyinputplus import inputMenu

RULES = {"rps": {"rock": ["scissors"],
                 "paper": ["rock"],
                 "scissors": ["paper"],
                 },
         "rpsls": {"rock": ["scissors", "lizard"],
                   "paper": ["rock", "spock"],
                   "scissors": ["paper", "lizard"],
                   "lizard": ["paper", "spock"],
                   "spock": ["rock", "scissors"], }}


class PlayerObject:
    def __init__(self, name, rules=None):
        if rules is None:
            rules = RULES["rps"]
        self.name = name.lower()
        self.rules = rules
        self.allowed_objects = [objct for objct in rules.keys()]

    def __repr__(self):
        return f"PlayerObject({self.name})"

    def __gt__(self, other):
        return other.name in self.rules[self.name]

    def __eq__(self, other):
        return self.name == other.name

    def random_object(self):
        return choice(self.allowed_objects)


class Player:
    def __init__(self, name, player_object: PlayerObject):
        self.name = name.capitalize()
        self.score = 0
        self.current_object = name
        self.player_object = player_object

    def reset_object(self):
        self.current_object = None

    def win_round(self):
        self.score += 1

    def __repr__(self):
        return f"Player({self.name}, {self.score}, {self.current_object})"


class HumanPlayer(Player):
    def __init__(self, name, player_object: PlayerObject):
        super().__init__(name, player_object)

    def choose_object(self):
        self.current_object = PlayerObject(inputMenu(self.player_object.allowed_objects, "choice: \n"), RULES["rpsls"])


class ComputerPlayer(Player):
    def __init__(self, player_object: PlayerObject):
        super().__init__("Computer", player_object)

    def choose_object(self):
        self.current_object = PlayerObject(self.player_object.random_object(), RULES["rpsls"])


class Game:
    def __init__(self, name, rules):
        self.current_round = 1
        self.max_rounds = 3
        self.players = []
        self.round_result = None
        self.round_winner = None
        self.player_object = PlayerObject(name, RULES[rules])

    def add_human_player(self, name):
        x = HumanPlayer(name, self.player_object)
        self.players.append(x)

    def add_computer_player(self):
        x = ComputerPlayer(self.player_object)
        self.players.append(x)

    def set_max_rounds(self, val):
        if isinstance(val, int):
            self.max_rounds = val
        else:
            print("must be an integer")

    def find_winner(self):
        if self.players[0].current_object is not None and self.players[1].current_object is not None:
            if self.players[0].current_object == self.players[1].current_object:
                self.round_result = "Draw"
            elif self.players[0].current_object > self.players[1].current_object:
                self.round_result = "Win"
                self.round_winner = self.players[0].name
                self.players[0].win_round()
            else:
                self.round_result = "Win"
                self.round_winner = self.players[1].name
                self.players[1].win_round()

    def next_round(self):
        self.current_round += 1
        self.round_result, self.round_winner = None, None
        for player in self.players:
            player.reset_object()

    def is_finished(self):
        if self.current_round > int(self.max_rounds):
            return True
        else:
            return False

    def reset(self):
        self.current_round = 1
        for player in self.players:
            player.score = 0

    def report_round(self):
        for player in self.players:
            print(f"{player.name} chose {player.current_object.name}")
        if self.round_result == "Draw":
            print("It was a draw")
        else:
            print(f"{self.round_winner} won")

    def report_score(self):
        for player in self.players:
            print(f"{player.name} has {player.score} points")

    def report_winner(self):
        if self.players[0].score == self.players[1].score:
            return "neither"
        elif self.players[0].score > self.players[1].score:
            return self.players[0].name
        else:
            return self.players[1].name

