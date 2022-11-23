from game_objects import PlayerObject, \
    HumanPlayer, ComputerPlayer, Game
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


@pytest.fixture()
def my_game():
    random.seed(8)
    game = Game()
    game.add_human_player("Bob")
    game.add_computer_player()
    game.set_max_rounds(2)
    game.players[0].choose_object("spock")
    game.players[1].choose_object()
    return game


@pytest.fixture()
def finished_game(my_game):
    my_game.find_winner()
    my_game.next_round()
    my_game.players[0].choose_object("lizard")
    my_game.players[1].choose_object()
    my_game.find_winner()
    my_game.next_round()
    return my_game


def test_random_object():
    rand_obj = PlayerObject.random_object()
    assert rand_obj.name in PlayerObject.allowable_objects


def test___gt__(my_rock, my_spock):
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


def test_find_winner(my_game):
    assert my_game.players[0].current_object == PlayerObject("spock")
    assert my_game.players[1].current_object == PlayerObject("paper")
    my_game.find_winner()
    assert my_game.round_result == "win"
    assert my_game.round_winner is my_game.players[1]


def test_next_round(my_game):
    my_game.next_round()
    assert my_game.round_result is None
    assert my_game.round_winner is None
    assert my_game.players[0].current_object is None
    assert my_game.players[1].current_object is None
    assert my_game.current_round == 1


def test_is_finished(finished_game):
    assert finished_game.is_finished()


def test_reset(my_game):
    my_game.reset()
    assert my_game.current_round == 0
    assert my_game.round_result is None
    assert my_game.round_winner is None


def test_report_round(my_game):
    my_game.find_winner()
    assert (my_game.report_round() ==
            "Bob choose 'spock'.\nComputer choose 'paper'.\nComputer won this round"
            )


def test_report_score(finished_game):
    assert (finished_game.report_score() ==
            "After 2 rounds:\nBob has scored 0\nComputer has scored 2")


def test_report_winner(finished_game):
    assert (finished_game.report_winner() == "Computer is the winner")
