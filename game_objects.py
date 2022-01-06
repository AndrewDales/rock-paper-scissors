""" Module contains the class objects that control the underlying logic for rock-paper scissors game.
The module includes a command-line interface (CLI) for running the game."""

# rock-paper-scissors/game_objects

import random


# PlayerObject represents an object that a player could choose
class PlayerObject:
    allowable_objects = ('rock', 'paper', 'scissors', 'lizard', 'spock')
    win_dict = {'rock': ['scissors', 'lizard'],
                'scissors': ['paper', 'lizard'],
                'paper': ['rock', 'spock'],
                'lizard': ['paper', 'spock'],
                'spock': ['rock', 'scissors'],
                }

    def __init__(self, name):
        if name.lower() in self.allowable_objects:
            self.name = name.lower()
        else:
            raise ValueError(f"Choice must be in {', '.join(self.allowable_objects)}")

    @classmethod
    def random_object(cls):
        return PlayerObject(random.choice(cls.allowable_objects))

    @classmethod
    def set_object_rules(cls, allowable_objects=None, win_dict=None):
        if allowable_objects:
            cls.allowable_objects = allowable_objects
        if win_dict:
            if set(win_dict.keys()) == set(allowable_objects):
                cls.win_dict = win_dict
            else:
                raise ValueError("Keys of win_dict must be the allowable objects")

    def __eq__(self, other):
        return self.name == other.name

    def __gt__(self, other):
        return other.name in self.win_dict[self.name]

    def __repr__(self):
        return f'<{self.name.title()}>'


# The Player Class represents a player
class Player:
    def __init__(self, name=None):
        if name:
            self.name = name
        else:
            self.name = ""
        self.score = 0
        self.current_object = None

    def set_name(self, name):
        self.name = name

    def reset_object(self):
        self.current_object = None

    def win_round(self):
        self.score += 1

    def __repr__(self):
        check_object_chosen = bool(self.current_object)
        return f'Player: {self.name}\nScore: {self.score}\nObject chosen: {check_object_chosen}'


# The HumanPlayer Class is a subclass of Player representing a human player
class HumanPlayer(Player):
    def choose_object(self, choice):
        self.current_object = PlayerObject(choice)


# The ComputerPlayer Class is a subclass of Player representing a Computer player
class ComputerPlayer(Player):
    def __init__(self):
        super().__init__('Computer')

    def choose_object(self):
        self.current_object = PlayerObject.random_object()


# The Game class contains the instructions for running the game
class Game:

    def __init__(self, allowable_objects=None, win_dict=None):
        if allowable_objects is None:
            allowable_objects = ('rock', 'paper', 'scissors', 'lizard', 'spock')
        if win_dict is None:
            win_dict = {'rock': ['scissors', 'lizard'],
                        'scissors': ['paper', 'lizard'],
                        'paper': ['rock', 'spock'],
                        'lizard': ['paper', 'spock'],
                        'spock': ['rock', 'scissors'],
                        }
        self.allowable_objects = allowable_objects
        self.win_dict = win_dict
        self.current_round = 0
        self.max_rounds = None
        self.players = []
        # round_result is None - not played, draw or win
        self.round_result = None
        # round_winner is the player who has won the round
        self.round_winner = None
        PlayerObject.set_object_rules(self.allowable_objects, self.win_dict)

    # Add a human player with their name
    def add_human_player(self, name=None):
        player = HumanPlayer(name)
        self.players.append(player)
        return player

    # Add a computer player (no name)
    def add_computer_player(self):
        comp_player = ComputerPlayer()
        self.players.append(comp_player)
        return comp_player

    def set_max_rounds(self, mr):
        if not isinstance(mr, int):
            raise TypeError("Max rounds must be an integer")
        self.max_rounds = mr

    def find_winner(self):
        choices = [player.current_object for player in self.players]
        # checks if all the player choices are non-empty values
        if not all(choices):
            raise TypeError("All choices must be non-empty")
        if choices[0] == choices[1]:
            self.round_result = "draw"
            self.round_winner = None
        else:
            self.round_result = "win"
            if choices[0] > choices[1]:
                self.round_winner = self.players[0]
            else:
                self.round_winner = self.players[1]
            self.round_winner.win_round()

    # Resets game objects ready for a new round
    def next_round(self):
        self.round_result = None
        self.round_winner = None
        for player in self.players:
            player.reset_object()
        self.current_round += 1

    # Checks if game is finished
    def is_finished(self):
        return self.current_round >= self.max_rounds

    # Resets the games setting current round to 0 and player scores to 0
    def reset(self):
        self.current_round = 0
        self.round_result = None
        self.round_winner = None
        for player in self.players:
            player.score = 0
            player.reset_object()

    # returns a message reporting on what the players played and what the result of the round was
    def report_round(self):
        if self.round_result is None:
            report_msg = 'Round has not been played'
        else:
            report_msg = (
                f"{self.players[0].name} choose '{self.players[0].current_object.name}'.\n"
                f"{self.players[1].name} choose '{self.players[1].current_object.name}'.\n")

            if self.round_result == "draw":
                report_msg += "Round was a draw"
            elif self.round_result == "win":
                report_msg += f'{self.round_winner.name} won this round'
        return report_msg

    # Returns a string with the current scores
    def report_score(self):
        score_msg = f"After {self.current_round} rounds:\n"
        score_msg += "\n".join([f"{player.name} has scored {player.score}" for player in self.players])
        return score_msg

    # Returns a message with the overall winner
    def report_winner(self):
        if self.players[0].score > self.players[1].score:
            win_msg = f"{self.players[0].name} is the winner"
        elif self.players[0].score < self.players[1].score:
            win_msg = f"{self.players[1].name} is the winner"
        else:
            win_msg = "Game is drawn"
        return win_msg


# Command Line Interface - gives prompts to run the game from the Command line
class ClInterface:
    def __init__(self):
        self.game = Game()
        # Convert to plain Rock, Paper, Scissors by uncommenting next 3 lines
        # ToDo Give the user an option to choose this
        # allowable_objects = ('rock', 'paper', 'scissors')
        # win_dict = {'rock': ['scissors'], 'scissors': ['paper'], 'paper': ['rock']}
        # self.game = Game(allowable_objects, win_dict)

    def set_up(self):
        objects = self.game.allowable_objects
        wel_string = f"Welcome to the {', '.join([obj.title() for obj in objects])} Game"
        print(wel_string)
        print("-" * len(wel_string))

        for i in range(2):
            player_type_chosen = False
            while not player_type_chosen:
                player_type = input(f"\nWill player {i} be a human (h) or the computer (c): ")
                if player_type[0].lower() == "h":
                    name = input("\nEnter Player's name: ")
                    self.game.add_human_player(name)
                    player_type_chosen = True
                elif player_type[0].lower() == "c":
                    self.game.add_computer_player()
                    player_type_chosen = True
                else:
                    print("Error - please enter 'h' or 'c'")
        self.input_max_rounds()

    def input_max_rounds(self):
        self.game.set_max_rounds(int(input("How many rounds will you play: ")))

    def get_choices(self):
        for player in self.game.players:
            while player.current_object is None:
                try:
                    if isinstance(player, ComputerPlayer):
                        player.choose_object()
                    else:
                        object_list = [f"'{obj}'" for obj in PlayerObject.allowable_objects]
                        choice = input(f"{player.name} please choose "
                                       f"{', '.join(object_list[:-1])} or {object_list[-1]}: ")
                        player.choose_object(choice)
                except ValueError as e:
                    print(e)

    def run_game(self):

        while not self.game.is_finished():
            self.game.next_round()
            self.get_choices()
            self.game.find_winner()
            print()
            print(self.game.report_round())
            print()
            print(self.game.report_score())
            print()

        print("Final Results")
        print("-" * 13)
        print(self.game.report_score())
        print()
        print(self.game.report_winner())

    def run_sequence(self):
        self.set_up()
        cont_seq = True
        while cont_seq:
            self.run_game()
            print("Would you like to play again (y/n)? ")
            play_again = input()
            if play_again[0].lower() == "y":
                self.input_max_rounds()
                self.game.reset()
            else:
                cont_seq = False
        print("Goodbye!")


if __name__ == "__main__":
    cli = ClInterface()
    cli.run_sequence()
