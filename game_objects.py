""" Module contains the class objects that control the underlying logic for rock-paper scissors game.
The module includes a command-line interface (CLI) for running the game."""

# rock-paper-scissors/game_objects

import random


# The Player Class represents a player - could be either human or a computer player
class Player:
    object_list = ("rock", "paper", "scissors")

    def __init__(self, name=None, object_list=None):
        if name:
            self.name = name
        else:
            self.name = ""
        if object_list:
            self.object_list = object_list
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


# A HumanPlayer subclasses Player
class HumanPlayer(Player):
    def choose_object(self, choice):
        choice = choice.lower()
        if choice not in self.object_list:
            object_list = tuple(f"'{obj}'" for obj in self.object_list)
            raise ValueError(f"Choice must be {', '.join(object_list[:-1])} or {object_list[-1]}")
        self.current_object = choice


# The ComputerPlayer Class is a subclass of Player
class ComputerPlayer(Player):
    def choose_object(self):
        self.current_object = random.choice(self.object_list)


class Game:
    def __init__(self):
        self.current_round = 0
        self.max_rounds = None
        self.players = []
        self.allowed_objects = ('rock', 'paper', 'scissors')
        # round_result is None - not played, draw or win
        self.round_result = None
        # round_winner is the player who has won the round
        self.round_winner = None

    def add_human_player(self, name=None):
        player = HumanPlayer(name, self.allowed_objects)
        self.players.append(player)
        return player

    def add_computer_player(self, name="Computer"):
        self.players.append(ComputerPlayer(name))

    def set_max_rounds(self, mr):
        if not isinstance(mr, int):
            raise TypeError("Max rounds must be an integer")
        self.max_rounds = mr

    def find_winner(self):
        choices = [player.current_object for player in self.players]
        # checks if all the player choices are non-empty values
        if not all(choices):
            raise TypeError("All choices must be non-empty")
        choice_diff = (self.allowed_objects.index(choices[0]) - self.allowed_objects.index(choices[1])) % 3
        if choice_diff == 0:
            self.round_result = "draw"
            self.round_winner = None
        else:
            self.round_result = "win"
            if choice_diff == 1:
                self.round_winner = self.players[0]
            elif choice_diff == 2:
                self.round_winner = self.players[1]
            self.round_winner.win_round()

    # Resets game objects ready for a new round
    def next_round(self):
        self.round_result = None
        self.round_winner = None
        for player in self.players:
            player.current_object = None
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
            player.current_object = None

    # returns a message reporting on what the players played and what the result of the round was
    def report_round(self):
        if self.round_result is None:
            report_msg = 'Round has not been played'
        else:
            report_msg = (
                f"{self.players[0].name} choose '{self.players[0].current_object}'.\n"
                f"{self.players[1].name} choose '{self.players[1].current_object}'.\n")

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


# Command Line Interface - runs the game from the Command line
class ClInterface:
    def __init__(self):
        self.game = Game()

    def set_up(self):
        wel_string = "Welcome to the Rock, Paper, Scissors Game"
        print(wel_string)
        print("-"*len(wel_string)+"\n")
        name = input("Enter Player's name: ")

        self.game.add_human_player(name)
        self.game.add_computer_player()
        self.input_max_rounds()

    def input_max_rounds(self):
        self.game.set_max_rounds(int(input("How many rounds will you play: ")))

    def get_choices(self):
        for player in self.game.players:
            while player.current_object is None:
                try:
                    if isinstance(player, ComputerPlayer):
                        player.choose_object()
                    elif isinstance(player, HumanPlayer):
                        current_choice = input("Please choose 'rock', 'paper', or 'scissors': ")
                        player.choose_object(current_choice)
                except ValueError:
                    pass

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
        print("-"*13)
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
