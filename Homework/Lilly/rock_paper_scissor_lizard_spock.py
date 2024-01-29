import random

RULES = {'rps': {'rock': ['scissors', ],
                 'scissors': ['paper'],
                 'paper': ['rock'],
                 },
         'rpsls': {'rock': ['scissors', 'lizard'],
                   'scissors': ['paper', 'lizard'],
                   'paper': ['rock', 'spock'],
                   'lizard': ['paper', 'spock'],
                   'spock': ['scissors', 'paper'],
                   },
         }


class PlayerObject:
    """ A object representing something that a player may choose

        Class attributes
        ----------------
        rules: a dictionory of dictionaries giving the wins for the PlayerObjects. Default is 'rock paper scissors'
        allowable_objects: the types of object that the players may choose
        """

    rules = RULES['rps']
    allowable_objects = tuple(rules.keys())

    def __init__(self, name):
        """
        Constructs the attributes for the PlayerObject

        Parameter
        ---------
            name: str
                name of object - must be in allowable objects
        """

        self.name = name.lower()

    @classmethod
    def set_rules(cls, rules=None):
        """ Sets the victory rules for the PlayerObjects"""
        cls.rules = rules
        cls.allowable_objects = tuple(rules.keys())

    @classmethod
    def random_object(cls, rules=None):
        """
        Returns a random object from amongst the allowable objects
        """
        if rules:
            cls.set_rules(rules)
        return PlayerObject(random.choice(cls.allowable_objects))

    def __repr__(self):
        return f'PlayerObject({self.name})'

    def __str__(self):
        return self.name.title()

    def __gt__(self, other):
        return other.name in self.rules[self.name]

    def __eq__(self, other):
        return self.name == other.name


# The Player Class represents a player
class Player:
    """
    A class to represent a player of the game

    Attributes
    __________
        name: str
            Player name
        score: int
            Player score
        current_object: PlayerObject or None
            What the player's current object is None for not selected
    """

    def __init__(self, name=None):
        """
        Constructs the necessary attributes for the Player class
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
        """ Increases score by one """
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
    """
    A class representing the Rock, Paper Scissors Game
    Attributes
    __________
        allowable_objects (opt)
            list of allowable objects
        win_dict (opt)
            dict showing what objects the object in the key beats
        current_round: int
            the current round
        max_rounds: int
            the maximum rounds that can be played
        players
            A list of players
        round_result
            None (not played), draw or win
        round_winner
            the PlayerObject for the round winner (None if no winner)
    """

    def __init__(self, rules=None):
        if rules is None:
            rules= RULES['rps']
        # if win_dict is None:
        #     win_dict = RPSLS_WIN_DICT
        self.current_round = 0
        self.max_rounds = None
        self.players = []
        self.round_result = None
        # round_winner is the player who has won the round
        self.round_winner = None
        PlayerObject.set_rules(rules)

    def add_human_player(self, name=None):
        """ Add a human player with their name """
        player = HumanPlayer(name)
        self.players.append(player)
        return player

    def add_computer_player(self):
        """ Add a computer player (no name) """
        comp_player = ComputerPlayer()
        self.players.append(comp_player)
        return comp_player

    def set_max_rounds(self, mr):
        """ Set the maximum number of rounds """
        if not isinstance(mr, int):
            raise TypeError("Max rounds must be an integer")
        self.max_rounds = mr

    def find_winner(self):
        """ Finds the winner of the current round """
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

    def next_round(self):
        """ Resets game objects ready for a new round """
        self.round_result = None
        self.round_winner = None
        for player in self.players:
            player.reset_object()
        self.current_round += 1

    def is_finished(self):
        """ Checks if game is finished """
        return self.current_round >= self.max_rounds

    def reset(self):
        """ Resets the whole game, setting current round to 0 and player scores to 0"""
        self.current_round = 0
        self.round_result = None
        self.round_winner = None
        for player in self.players:
            player.score = 0
            player.reset_object()

    def report_round(self):
        """ returns a message reporting on what the players played and what the result of the round was """
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

    def report_score(self):
        """ Returns a string with the current scores """
        score_msg = f"After {self.current_round} rounds:\n"
        score_msg += "\n".join([f"{player.name} has scored {player.score}" for player in self.players])
        return score_msg

    def report_winner(self):
        """ Returns a message with the overall winner """
        if self.players[0].score > self.players[1].score:
            win_msg = f"{self.players[0].name} is the winner"
        elif self.players[0].score < self.players[1].score:
            win_msg = f"{self.players[1].name} is the winner"
        else:
            win_msg = "Game is drawn"
        return win_msg


if __name__ == "__main__":
    # PlayerObject.set_rules(RULES['rpsls'])
    # player = HumanPlayer('Andrew')
    # computer = ComputerPlayer()
    # player.choose_object('Rock')
    game = Game()