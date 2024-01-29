import random


RULESETS = {
    'default': {
        'rock': ['scissors'],
        'paper': ['rock'],
        'scissors': ['paper'],
    },
    'lizard spock': {
        'rock': ['scissors', 'lizard'],
        'paper': ['rock', 'spock'],
        'scissors': ['paper', 'lizard'],
        'lizard': ['paper', 'spock'],
        'spock': ['rock', 'scissors'],
    },
}


class Hand:
    ruleset_name = 'default'
    ruleset: dict[str, list[str]] = RULESETS[ruleset_name]
    allowable_hands: tuple[str] = tuple(ruleset.keys())

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f'Hand({self.name})'

    def __gt__(self, other):
        return other.name in self.ruleset[self.name]

    def __eq__(self, other):
        return self.name == other.name

    @classmethod
    def set_ruleset(cls, ruleset_name: str):
        if ruleset_name not in RULESETS.keys():
            raise ValueError(f'Provided ruleset name {ruleset_name} does not exist')

        cls.ruleset_name = ruleset_name
        cls.ruleset = RULESETS[ruleset_name]
        cls.allowable_hands = tuple(cls.ruleset.keys())


class Player:
    def __init__(self, name: str):
        self.name = name.title()
        self.score = 0
        self.current_hand: None | Hand = None

    def reset_hand(self):
        self.current_hand = None

    def reset_score(self):
        self.score = 0

    def win_round(self):
        self.score += 1

    def __repr__(self):
        return f'{self.__class__.__name__}(\'{self.name}\')'


class HumanPlayer(Player):
    def __init__(self, name: str):
        super().__init__(name)

    def choose_hand(self, choice: str):
        self.current_hand = Hand(choice)


class ComputerPlayer(Player):
    def __init__(self, name):
        super().__init__(name)

    def choose_hand(self):
        self.current_hand = Hand(random.choice(Hand.allowable_hands))


class Game:
    def __init__(self):
        self.current_round = 0
        self.max_rounds = 10
        self.players: list[HumanPlayer | ComputerPlayer] = []
        self.round_result: None | str = None
        self.round_winner: None | Player = None
        self.round_winner_index: int = -1

    def create_player(self, name: str, is_computer: bool = False):
        self.players.append(ComputerPlayer(name) if is_computer else HumanPlayer(name))

    def set_max_rounds(self, max_rounds: int):
        if not isinstance(max_rounds, int):
            raise TypeError('max_rounds must be an integer')
        self.max_rounds = max_rounds

    def find_round_winner(self):
        if self.players[0].current_hand == self.players[1].current_hand:
            self.round_result = 'draw'
        else:
            self.round_result = 'win'
            if self.players[0].current_hand > self.players[1].current_hand:
                self.round_winner_index = 0
            else:
                self.round_winner_index = 1
            self.players[self.round_winner_index].win_round()

    def next_round(self):
        self.current_round += 1
        self.round_result = None
        for player in self.players:
            player.reset_hand()

    def is_finished(self):
        return self.current_round >= self.max_rounds

    def reset(self):
        self.current_round = 0
        for player in self.players:
            player.reset_score()

    def report_round(self):
        message = f'Round {self.current_round + 1}: '
        message += f'{self.players[0].name} chose {self.players[0].current_hand.name} '
        message += f'and {self.players[1].name} chose {self.players[1].current_hand.name}. '
        if self.round_result == 'draw':
            message += 'Round was a draw.'
        else:
            message += f'{self.players[self.round_winner_index].name} won.'
        message += f'\n{self.players[0].name} has {self.players[0].score} points '
        message += f'and {self.players[1].name} has {self.players[1].score} points.'
        return message

    def report_winner(self):
        if self.players[0].score == self.players[1].score:
            return f'Both players drew with score {self.players[0].score}.'
        if self.players[0].score > self.players[1].score:
            return f'{self.players[0].name} won with a score of {self.players[0].score} vs {self.players[1].score}.'
        return f'{self.players[1].name} won with a score of {self.players[1].score} vs {self.players[0].score}.'
