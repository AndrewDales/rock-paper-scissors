import pytest
from rpc_back import PlayerObject, Game, RULES, HumanPlayer, ComputerPlayer
import random


class TestPlayerObjects:
    @pytest.fixture()
    def rock(self):
        return PlayerObject("rock", RULES["rpsls"])

    @pytest.fixture()
    def paper(self):
        return PlayerObject("paper", RULES["rpsls"])

    @pytest.fixture()
    def scissors(self):
        return PlayerObject("scissors", RULES["rpsls"])

    @pytest.fixture()
    def lizard(self):
        return PlayerObject("lizard", RULES["rpsls"])

    @pytest.fixture()
    def spock(self):
        return PlayerObject("spock", RULES["rpsls"])

    @pytest.fixture()
    def random_object(self):
        random.seed(5)
        ran_obj = PlayerObject("random", RULES["rpsls"])
        ran_obj.random_object()
        return ran_obj

    def test_objects(self, random_object, rock, paper, scissors, lizard, spock):
        assert rock > scissors
        assert rock > lizard
        assert scissors > paper
        assert scissors > lizard
        assert paper > rock
        assert paper > spock
        assert lizard > paper
        assert lizard > spock
        assert spock > rock
        assert spock > scissors
        assert random_object == spock
        assert random_object > scissors
        assert random_object > rock


class TestGame:
    @pytest.fixture()
    def game_fix_norm(self):
        random.seed(8)
        game = Game()
        game.change_rules("rps")
        game.add_human_player("Albert")
        game.add_computer_player()
        game.set_max_rounds(2)
        game.players[0].choose_object("rock")
        game.players[1].choose_object()
        game.find_winner()
        return game

    @pytest.fixture()
    def game_fix_sp(self):
        random.seed(10)
        game = Game()
        game.change_rules("rpsls")
        game.add_computer_player()
        game.add_human_player("Albert")
        game.set_max_rounds(5)
        game.players[0].choose_object()
        game.players[1].choose_object("lizard")
        game.find_winner()
        return game

    @pytest.fixture()
    def game_fix_nxt(self):
        game = Game()
        game.add_computer_player()
        game.add_human_player("Ben")
        game.set_max_rounds(5)
        game.players[0].choose_object()
        game.players[1].choose_object("rock")
        game.find_winner()
        game.next_round()
        return game

    @pytest.fixture()
    def game_fix_fn(self):
        game = Game()
        random.seed(8)
        game.add_human_player("Ben")
        game.add_computer_player()
        game.set_max_rounds(2)
        game.players[0].choose_object("paper")
        game.players[1].choose_object()
        game.find_winner()
        game.next_round()
        random.seed(8)
        game.players[0].choose_object("paper")
        game.players[1].choose_object()
        game.find_winner()
        game.next_round()
        return game

    def test_game_norm(self, game_fix_norm):
        assert game_fix_norm.max_rounds == 2
        assert game_fix_norm.players[0].name == "Albert"
        assert game_fix_norm.players[1].name == "Computer"
        assert isinstance(game_fix_norm.players[0], HumanPlayer)
        assert isinstance(game_fix_norm.players[1], ComputerPlayer)
        assert game_fix_norm.round_winner is None
        assert game_fix_norm.round_result == "Draw"

    def test_game_sp(self, game_fix_sp):
        assert game_fix_sp.max_rounds == 5
        assert game_fix_sp.players[0].name == "Computer"
        assert game_fix_sp.players[1].name == "Albert"
        assert isinstance(game_fix_sp.players[0], ComputerPlayer)
        assert isinstance(game_fix_sp.players[1], HumanPlayer)
        assert game_fix_sp.round_winner == "Albert"
        assert game_fix_sp.round_result == "Win"

    def test_game_nxt(self, game_fix_nxt):
        assert game_fix_nxt.current_round == 1
        assert game_fix_nxt.max_rounds == 5
        assert game_fix_nxt.players[0].current_object.name is None
        assert game_fix_nxt.players[1].current_object is None
        assert game_fix_nxt.round_result is None
        assert game_fix_nxt.round_winner is None

    def test_game_fn(self, game_fix_fn):
        assert game_fix_fn.is_finished()
        assert game_fix_fn.players[0].score == 2
        assert game_fix_fn.players[1].score == 0
