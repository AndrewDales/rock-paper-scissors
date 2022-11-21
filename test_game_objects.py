from game_objects import PlayerObject, HumanPlayer, ComputerPlayer
import random
import pytest


@pytest.fixture
def my_rock():
    return PlayerObject("rock")


@pytest.fixture
def my_spock():
    return PlayerObject("spock")


@pytest.fixture()
def human_player():
    return HumanPlayer("Andrew")


@pytest.fixture()
def computer_player():
    return ComputerPlayer()


def test_random_object():
    rand_obj = PlayerObject.random_object()
    assert rand_obj.name in PlayerObject.allowable_objects


def test_set_object_rules(my_rock, my_spock):
    assert my_spock > my_rock


def test_set_name(human_player):
    assert human_player.name == "Andrew"
    human_player.set_name("Bob")
    assert human_player.name == "Bob"


def test_choose_object(human_player):
    human_player.choose_object('rock')
    assert human_player.current_object == PlayerObject("rock")


def test_reset_object(human_player):
    human_player.choose_object('scissors')
    human_player.reset_object()
    assert human_player.current_object is None


def test_win_round(human_player):
    human_player.win_round()
    human_player.win_round()
    assert human_player.score == 2


def test_choose_computer_object(computer_player):
    random.seed(5)
    assert computer_player.current_object is None
    computer_player.choose_object()
    assert computer_player.current_object == PlayerObject('spock')
    computer_player.choose_object()
    assert computer_player.current_object == PlayerObject('scissors')
