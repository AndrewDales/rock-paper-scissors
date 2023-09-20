from game_objects import PlayerObject, HumanPlayer, ComputerPlayer, Game, RPSLS_OBJECTS
import random
import pytest


class TestParametrized:
    win_list = [('rock', ['scissors', 'lizard']),
                ('scissors', ['paper', 'lizard']),
                ('paper', ['rock', 'spock']),
                ('lizard', ['paper', 'spock']),
                ('spock', ['rock', 'scissors']),
                ]

    @pytest.mark.parametrize("obj, obj_beats", win_list)
    def test_wins(self, obj, obj_beats):
        assert PlayerObject(obj) > PlayerObject(obj_beats[0])
        assert PlayerObject(obj) > PlayerObject(obj_beats[1])


class TestObjects:
    @pytest.fixture
    def my_objects(self):
        return {obj: PlayerObject(obj) for obj in RPSLS_OBJECTS}

    def test_random_object(self):
        rand_obj = PlayerObject.random_object()
        assert rand_obj.name in PlayerObject.allowable_objects

    def test_rankings(self, my_objects):
        assert my_objects["spock"] > my_objects["rock"] and my_objects["spock"] > my_objects["scissors"]
        assert my_objects["rock"] > my_objects["scissors"] and my_objects["rock"] > my_objects["lizard"]
        assert my_objects["paper"] > my_objects["rock"] and my_objects["paper"] > my_objects["spock"]
        assert my_objects["scissors"] > my_objects["paper"] and my_objects["scissors"] > my_objects["lizard"]
        assert my_objects["lizard"] > my_objects["paper"] and my_objects["lizard"] > my_objects["spock"]


class TestPlayers:
    @pytest.fixture
    def human_player(self):
        return HumanPlayer("Andrew")

    @pytest.fixture
    def computer_player(self):
        return ComputerPlayer()

    def test_set_name(self, human_player):
        assert human_player.name == "Andrew"
        human_player.set_name("Bob")
        assert human_player.name == "Bob"

    def test_choose_object(self, human_player):
        human_player.choose_object('rock')
        assert human_player.current_object == PlayerObject("rock")

    def test_reset_object(self, human_player):
        human_player.choose_object('scissors')
        human_player.reset_object()
        assert human_player.current_object is None

    def test_win_round(self, human_player):
        human_player.win_round()
        human_player.win_round()
        assert human_player.score == 2

    def test_choose_computer_object(self, computer_player):
        random.seed(5)
        assert computer_player.current_object is None
        computer_player.choose_object()
        assert computer_player.current_object == PlayerObject('spock')
        computer_player.choose_object()
        assert computer_player.current_object == PlayerObject('scissors')


class TestGame:
    @pytest.fixture
    def my_game(self):
        random.seed(8)
        game = Game()
        game.add_human_player("Bob")
        game.add_computer_player()
        game.set_max_rounds(2)
        game.players[0].choose_object("spock")
        game.players[1].choose_object()
        return game

    @pytest.fixture()
    def finished_game(self, my_game):
        my_game.find_winner()
        my_game.next_round()
        my_game.players[0].choose_object("lizard")
        my_game.players[1].choose_object()
        my_game.find_winner()
        my_game.next_round()
        return my_game  #

    def test_find_winner(self, my_game):
        assert my_game.players[0].current_object == PlayerObject("spock")
        assert my_game.players[1].current_object == PlayerObject("paper")
        my_game.find_winner()
        assert my_game.round_result == "win"
        assert my_game.round_winner is my_game.players[1]

    def test_next_round(self, my_game):
        my_game.next_round()
        assert my_game.round_result is None
        assert my_game.round_winner is None
        assert my_game.players[0].current_object is None
        assert my_game.players[1].current_object is None
        assert my_game.current_round == 1

    def test_is_finished(self, finished_game):
        assert finished_game.is_finished()

    def test_reset(self, my_game):
        my_game.reset()
        assert my_game.current_round == 0
        assert my_game.round_result is None
        assert my_game.round_winner is None

    def test_report_round(self, my_game):
        my_game.find_winner()
        assert (my_game.report_round() ==
                "Bob choose 'spock'.\nComputer choose 'paper'.\nComputer won this round"
                )

    def test_report_score(self, finished_game):
        assert (finished_game.report_score() ==
                "After 2 rounds:\nBob has scored 0\nComputer has scored 2")

    def test_report_winner(self, finished_game):
        assert (finished_game.report_winner() == "Computer is the winner")
