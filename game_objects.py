""" Module contains the class objects that control the underlying logic for rock-paper scissors game.
The module includes a command-line interface (CLI) for running the game."""

# rock-paper-scissors/game_objects

import random

# constants
RPSLS_OBJECTS = ('rock', 'paper', 'scissors', 'lizard', 'spock')
RPSLS_WIN_DICT = {'rock': ['scissors', 'lizard'],
                  'scissors': ['paper', 'lizard'],
                  'paper': ['rock', 'spock'],
                  'lizard': ['paper', 'spock'],
                  'spock': ['rock', 'scissors'],
                  }
RPS_OBJECTS = ('rock', 'paper', 'scissors')
RPS_WIN_DICT = {'rock': ['scissors'],
                'scissors': ['paper'],
                'paper': ['rock'],
                }


# PlayerObject represents an object that a player could choose
class PlayerObject:
    """
    A class to represent a playable object
    ...
    Attributes
    ----------
    name: str
        name of the object
    allowable_objects: tuple (class attribute)
        list of allowable objects
    win_dict: dict
        keys are allowable objects, values is list of what keys will beat
    Methods
    -------
    random_objects (class method)
        returns a PlayerObject randomly chosen from the allowable objects
    set_object_rules (class method)
        sets the allowable objects and the win_dict for what the object can beat
    """

    # Set default objects for the class
    allowable_objects = RPSLS_OBJECTS
    win_dict = RPSLS_WIN_DICT

    def __init__(self, name):
        """
        Constructs the attributes for the PlayerObject

        Parameters
        ----------
            name: str
                name of object - must be in allowable objects
        """
        if name.lower() in self.allowable_objects:
            self.name = name.lower()
        else:
            raise ValueError(f"Choice must be in {', '.join(self.allowable_objects)}")

    @classmethod
    def random_object(cls):
        """
        Returns a random object from amongst the allowable objects
        """
        return PlayerObject(random.choice(cls.allowable_objects))

    @classmethod
    def set_object_rules(cls, allowable_objects=None, win_dict=None):
        """
        Sets the allowable objects and the win_dict for the class
        """
        if allowable_objects:
            cls.allowable_objects = allowable_objects
        if win_dict:
            if set(win_dict.keys()) == set(allowable_objects):
                cls.win_dict = win_dict
            else:
                raise ValueError("Keys of win_dict must be the allowable objects")

    def __eq__(self, other):
        """
        Checks if two objects are the same
        """
        return self.name == other.name

    def __gt__(self, other):
        """
        Checks if the current object (self) beats the passed object (other)
        """
        return other.name in self.win_dict[self.name]

    def __repr__(self):
        """
        Representation of the object
        """
        return f'PlayerObject({self.name})'


# The Player Class represents a player
class Player:
    """
    A class to represent a player of the game
    """
    def __init__(self, name=None):
        """
        Constructs the necessary attributes for the Player class

        Attributes
        __________
            name: str
                Player name
            score: int
                Player score
            current_object: PlayerObject or None
                What the player's current object is None for not selected
        """
        if name:
            self.name = name
        else:
            self.name = ""
        self.score = 0
        self.current_object = None

    def set_name(self, name):
        """ Sets name attribute to name """
        self.name = name

    def reset_object(self):
        """ Sets the current_object to None - not selected"""
        self.current_object = None

    def win_round(self):
        """ Increases score by one"""
        self.score += 1

    def __repr__(self):
        """ Representation of the object """
        check_object_chosen = bool(self.current_object)
        return f'Player: {self.name}\nScore: {self.score}\nObject chosen: {check_object_chosen}'


# The HumanPlayer Class is a subclass of Player representing a human player
class HumanPlayer(Player):
    """ Subclass of Player representing a human player (PC) """
    def choose_object(self, choice):
        """ Chooses a PlayerObject for the player"""
        self.current_object = PlayerObject(choice)


# The ComputerPlayer Class is a subclass of Player representing a Computer player
class ComputerPlayer(Player):
    """ Subclass of Player representing a Computer player (NPC) """
    def __init__(self):
        """ Constructs super Player object with name "Computer """
        super().__init__('Computer')

    def choose_object(self):
        """ Computer chooses a random PlayerObject """
        self.current_object = PlayerObject.random_object()


# The Game class contains the instructions for running the game
class Game:
    """ """
    def __init__(self, allowable_objects=None, win_dict=None):
        if allowable_objects is None:
            allowable_objects = RPSLS_OBJECTS
        if win_dict is None:
            win_dict = RPSLS_WIN_DICT
        self.current_round = 0
        self.max_rounds = None
        self.players = []
        # round_result is None - not played, draw or win
        self.round_result = None
        # round_winner is the player who has won the round
        self.round_winner = None
        PlayerObject.set_object_rules(allowable_objects, win_dict)

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
