import random

RULES = {'rps': {'rock': ['scissors'],
                 'paper': ['rock'],
                 'scissors': ['paper']
                 },

         'rpsls': {'rock': ['scissors', 'lizard'],
                   'paper': ['rock', 'spock'],
                   'scissors': ['paper', 'lizard'],
                   'lizard': ['paper', 'spock'],
                   'spock': ['scissors', 'paper']
                   },
         }


class PlayerObject:
    rules = RULES['rps']
    allowable_objects = list(rules.keys())

    # data structures not in constuctor are class atribtes and are the same for every instance
    def __init__(self, name):
        # if rules is None:
        #     rules = RULES['rps']
        # PlayerObject.set_rules(rules)
        # self.rules=rules
        name = name.lower()
        if name not in self.rules.keys():
            raise ValueError("name must be valid object")
        else:
            self.name = name

    @classmethod
    def random_object(cls):
        object_name = random.choice(cls.allowable_objects)
        return PlayerObject(object_name)

    @classmethod
    def set_rules(cls, choice='rpsls'):
        cls.rules = RULES[choice]
        cls.allowable_objects = list(cls.rules.keys())

    def __repr__(self):
        return f'PlayerObject({self.name})'

    def __gt__(self, other):  # gt sets greater than: return true if in the list of objects it can beat
        return other.name in self.rules[self.name]

    def __eq__(self, other):
        return self.name == other.name


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.current_object = None

    def reset_object(self):
        self.current_object = None

    def win_round(self):
        self.score += 1

    def __repr__(self):
        return f'name: {self.name}\nscore: {self.score}\ncurrent object: {self.current_object}'


class HumanPlayer(Player):
    def choose_object(self, choice):
        self.current_object = PlayerObject(choice)


class ComputerPlayer(Player):
    def __init__(self):
        super().__init__("Computer")

    def choose_object(self):
        self.current_object = PlayerObject.random_object()


class Game:

    def __init__(self):
        self.current_round = 0
        self.round_result = None
        self.round_winner = None
        self.players = []
        self.max_rounds = 0

    def add_human_player(self, name):
        self.players.append(HumanPlayer(name))

    def add_computer_player(self):
        computer = ComputerPlayer()
        self.players.append(computer)

    def set_max_rounds(self, num):
        if isinstance(num, int):
            self.max_rounds = num
        else:
            raise ValueError("max rounds must be an integer")

    def find_winner(self):
        if self.players[0].current_object > self.players[1].current_object:
            self.round_result = "WON"
            self.round_winner = self.players[0]
            self.players[0].score += 1
        elif self.players[1].current_object > self.players[0].current_object:
            self.round_result = "WON"
            self.round_winner = self.players[1]
            self.players[1].score += 1
        else:
            self.round_result = "DRAW"


    def next_round(self):
        self.current_round += 1
        self.round_result = None
        self.round_winner = None
        for player in self.players:
            player.reset_object()

    def is_finished(self):
        if self.current_round >= self.max_rounds:
            return True

    def reset(self):
        self.current_round = 0
        for player in self.players:
            player.score = 0

    def report_round(self):
        message = (f"{self.players[0].name} chose {self.players[0].current_object.name} \n{self.players[1].name} chose "
                   f"{self.players[1].current_object.name} \n")
        if self.round_result == 'WON':
            message1 = f'round won by {self.round_winner.name}'
        else:
            message1 = 'round is a draw'
        return message + message1

    def report_score(self):
        return f'{self.players[0].name}: {self.players[0].score} {self.players[1].name}: {self.players[1].score}'

    def report_winner(self):
        if self.players[0].score > self.players[1].score:
            return f'{self.players[0].name} won overall'
        elif self.players[1].score > self.players[0].score:
            return f'{self.players[1].name} won overall'
        else:
            return 'draw overall'


if __name__ == "__main__":
    game = Game()
    game.set_max_rounds(3)
    game.add_human_player('lolly1')
    game.players[0].choose_object('scissors')
    game.add_human_player('lolly2')
    game.players[1].choose_object('paper')
    game.find_winner()

