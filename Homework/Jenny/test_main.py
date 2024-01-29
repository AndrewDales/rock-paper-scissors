import rps_backend
import random
import pytest
# Fixtures are objects that can be used in subsequent tests
@pytest.fixture
def my_rock():
    return rps_backend.PlayerObject("rock", rps_backend.RULES["rpsls"])
@pytest.fixture
def my_spock():
    return rps_backend.PlayerObject("spock", rps_backend.RULES["rpsls"])
@pytest.fixture
def my_paper():
    return rps_backend.PlayerObject("paper", rps_backend.RULES["rps"])
@pytest.fixture()
def human_player():
    player = rps_backend.HumanPlayer("Andrew", rps_backend.PlayerObject("", rps_backend.RULES["rpsls"]))
    player.current_object = "spock"
    return player
@pytest.fixture()
def computer_player():
    obj = rps_backend.PlayerObject("", rps_backend.RULES["rpsls"])
    return rps_backend.ComputerPlayer(obj)
@pytest.fixture()
def my_game():
    random.seed(8)
    game = rps_backend.Game("Game", "rpsls")
    game.add_human_player("Bob")
    game.add_computer_player()
    game.set_max_rounds(2)
    game.players[1].choose_object()
    return game
@pytest.fixture()
def finished_game(my_game):
    my_game.next_round()
    my_game.players[0].current_object = rps_backend.PlayerObject("lizard", rps_backend.RULES["rpsls"])
    my_game.players[1].choose_object()
    my_game.find_winner()
    my_game.next_round()
    return my_game
def test_player_object(my_rock, my_spock, my_paper):
    assert my_rock.name == "rock"
    assert my_spock > my_rock
    assert my_paper > my_rock
def test_human_player(human_player):
    assert human_player.name == "Andrew"
    assert human_player.current_object == "spock"
    human_player.reset_object()
    assert human_player.current_object is None
def test_computer_player(computer_player):
    assert computer_player.name == "Computer"
    computer_player.win_round()
    assert computer_player.score == 1
def test_game(my_game, finished_game):
    assert my_game.max_rounds == 2
    assert finished_game.players[0].name == "Bob"
    assert finished_game.is_finished()
    assert finished_game.current_round == 3
