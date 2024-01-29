import pyinputplus
from main import Game, HumanPlayer, Hand, RULESETS


class Clinterface:
    def __init__(self):
        self.game = Game()
        self.run_sequence()

    def set_up(self):
        for _ in range(2):
            name = pyinputplus.inputStr('Enter player name: ')
            is_computer = pyinputplus.inputChoice(
                ('human', 'computer'),
                'Do you want this player to be a human or computer? '
            ) == 'computer'
            self.game.create_player(name, is_computer)
        if pyinputplus.inputYesNo(
            f'The current max rounds is set to {self.game.max_rounds}. Would you like to change it? '
        ) == 'yes':
            max_rounds = pyinputplus.inputInt('How many rounds should be in a game? ', min=1, max=100)
            self.game.set_max_rounds(max_rounds)
        if pyinputplus.inputYesNo(
                f'The current ruleset is set to {Hand.ruleset_name}. Would you like to change it? '
        ) == 'yes':
            Hand.set_ruleset(pyinputplus.inputChoice(
                tuple(RULESETS.keys()),
                f'Choose a ruleset from {", ".join(RULESETS.keys())}: '
            ))

    def get_choices(self):
        for player in self.game.players:
            if isinstance(player, HumanPlayer):
                choice = pyinputplus.inputChoice(
                    Hand.allowable_hands,
                    f'{player.name}, choose one of {", ".join(Hand.allowable_hands)}: '
                )
                player.choose_hand(choice)
            else:
                player.choose_hand()

    def run_game(self):
        while not self.game.is_finished():
            self.get_choices()
            self.game.find_round_winner()
            print(self.game.report_round())
            self.game.next_round()
        print(self.game.report_winner())
        self.game.reset()

    def run_sequence(self):
        self.set_up()
        self.run_game()
        while pyinputplus.inputYesNo('Want to play again? ') == 'yes':
            self.run_game()
        print('Goodbye!')


if __name__ == '__main__':
    Clinterface()
