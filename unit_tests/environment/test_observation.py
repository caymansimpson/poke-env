from unittest.mock import MagicMock

from poke_env.battle import DoubleBattle, Observation
from poke_env.battle.observation import Observation as ObservationDirect


def test_observation_importable_from_both_paths():
    assert Observation is ObservationDirect


def test_observation_has_events():
    obs = Observation()
    assert obs.events == []


def test_fresh_battle_has_empty_observations():
    battle = DoubleBattle("tag", "username", MagicMock(), gen=9)
    assert battle.observations == {}


def test_fresh_battle_has_current_observation():
    battle = DoubleBattle("tag", "username", MagicMock(), gen=9)
    assert isinstance(battle.current_observation, Observation)
    assert battle.current_observation.events == []


def test_parse_message_appends_to_current_observation():
    battle = DoubleBattle("tag", "username", MagicMock(), gen=9)
    battle.player_role = "p1"

    msg = ["", "move", "p1a: Incineroar", "Fake Out", "p2a: Landorus"]
    battle.parse_message(msg)

    assert msg in battle.current_observation.events


def test_turn_message_archives_observation_and_starts_fresh():
    # |turn|1 is the first real turn message; pre-turn events are stored at key 0
    battle = DoubleBattle("tag", "username", MagicMock(), gen=9)
    battle.player_role = "p1"
    battle.parse_message(["", "teamsize", "p1", 6])
    battle.parse_message(["", "teamsize", "p2", 6])

    move_msg = ["", "move", "p1a: Incineroar", "Fake Out", "p2a: Landorus"]
    battle.parse_message(move_msg)
    battle.parse_message(["", "turn", "1"])

    assert 0 in battle.observations
    assert move_msg in battle.observations[0].events
    assert isinstance(battle.current_observation, Observation)
    assert battle.current_observation.events == []


def test_observations_accumulate_across_turns():
    # Keys are self._turn at save time: 0 before |turn|1, 1 before |turn|2, etc.
    battle = DoubleBattle("tag", "username", MagicMock(), gen=9)
    battle.player_role = "p1"
    battle.parse_message(["", "teamsize", "p1", 6])
    battle.parse_message(["", "teamsize", "p2", 6])

    battle.parse_message(["", "move", "p1a: Incineroar", "Fake Out", "p2a: Landorus"])
    battle.parse_message(["", "turn", "1"])
    battle.parse_message(["", "move", "p2a: Landorus", "Rock Slide", "p1a: Incineroar"])
    battle.parse_message(["", "turn", "2"])

    assert 0 in battle.observations
    assert 1 in battle.observations
