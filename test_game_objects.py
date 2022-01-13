from game_objects import PlayerObject
import pytest


@pytest.fixture
def my_rock():
    return PlayerObject("rock")


@pytest.fixture
def my_spock():
    return PlayerObject("spock")


def test_random_object():
    rand_obj = PlayerObject.random_object()
    assert rand_obj.name in PlayerObject.allowable_objects


def test_set_object_rules(my_rock, my_spock):
    assert my_spock > my_rock
