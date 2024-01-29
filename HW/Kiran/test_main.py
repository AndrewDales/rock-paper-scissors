from main import Hand, Player, HumanPlayer, ComputerPlayer, Game
import pytest, random


@pytest.fixture
def rock():
    Hand.set_ruleset('lizard spock')
    return Hand('rock')


@pytest.fixture
def spock():
    Hand.set_ruleset('lizard spock')
    return Hand('spock')


@pytest.fixture
def player():
    player = Player('clara')
    return player


@pytest.fixture
def human():
    return HumanPlayer('joan')


@pytest.fixture
def computer():
    random.seed(0)
    return ComputerPlayer('computer')


@pytest.fixture
def game():
    random.seed(0)
    game = Game()
    game.create_player('jack')
    game.create_player('jill', True)
    game.set_max_rounds(2)
    game.players[0].choose_hand('spock')
    game.players[1].choose_hand()
    game.find_round_winner()
    return game


@pytest.fixture
def finished_game(game):
    game.find_round_winner()
    game.next_round()
    game.players[0].choose_hand('lizard')
    game.players[1].choose_hand()
    game.find_round_winner()


def test_hand(spock, rock):
    assert spock > rock
    assert spock == Hand('spock')
    Hand.set_ruleset('default')
    assert Hand.ruleset_name == 'default'


def test_player(player, spock):
    player.win_round()
    assert player.score == 1

    player.reset_score()
    assert player.score == 0

    player.current_hand = spock
    player.reset_hand()
    assert player.current_hand is None


def test_human_player(human, spock):
    human.choose_hand('spock')
    assert human.current_hand == spock


def test_computer_player(computer):
    computer.choose_hand()
    assert computer.current_hand == Hand('lizard')


def test_game(game):
    assert game.players[0].score == 0
    assert game.players[1].score == 1
    game.next_round()
    game.players[0].choose_hand('lizard')
    game.players[1].choose_hand()  # lizard
    game.find_round_winner()
    assert game.players[0].score == 0
    assert game.players[1].score == 1
    assert f'{game.players[1].name} won' in game.report_winner()
