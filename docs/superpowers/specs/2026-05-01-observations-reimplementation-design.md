# Observations Reimplementation Design

**Date:** 2026-05-01  
**Scope:** Restore `battle.observations` and `battle.current_observation` to the poke-env fork after upstream removed them in commit `d9781e5`.

## Background

Upstream poke-env removed the observation system in "Move observation feature to examples/ (#872)". This deleted `observation.py`, `observed_pokemon.py`, and all population logic from `abstract_battle.py`. EliteFurretAI depends on `battle.observations` in several places (Embedder transition features, speed/item inference, battle data ETL, diagnostics).

## What We Are Building

A minimal, always-on event log attached to every battle. Each turn's protocol messages are collected into an `Observation` object (just an `events` list). At turn end, the completed observation is filed into `battle.observations[turn]`. A fresh `Observation` starts accumulating for the next turn.

## Scope Decision

**Events only.** The original also snapshotted full battle state per turn (active pokemon, team, weather, fields via `ObservedPokemon`). EliteFurretAI callers only access `observation.events` — no snapshot data is consumed anywhere. Restoring snapshots would add per-turn copy overhead for no benefit.

**Always on.** No `log_observations` flag. Overhead is one list append per protocol message, which is negligible.

## Components

### `src/poke_env/battle/observation.py` (new file)

```python
from dataclasses import dataclass, field
from typing import List

@dataclass
class Observation:
    events: List[List[str]] = field(default_factory=list)
```

No other fields. No `ObservedPokemon`.

### `src/poke_env/battle/abstract_battle.py` (modified)

1. Import `Observation` at top of file.
2. In `__init__`: add `self._observations: Dict[int, Observation] = {}` and `self._current_observation: Observation = Observation()`.
3. In `parse_message`: prepend `self._current_observation.events.append(split_message)` (before the existing dispatch logic, same as the original).
4. On `|turn|` message handling: before `end_turn()`, save `self._observations[self.turn] = self._current_observation` then set `self._current_observation = Observation()`.
5. Add two read-only properties:
   - `observations -> Dict[int, Observation]`: returns `self._observations`
   - `current_observation -> Observation`: returns `self._current_observation`

### `src/poke_env/battle/__init__.py` (modified)

Add `Observation` to the exports so both import styles work:
- `from poke_env.battle import Observation`
- `from poke_env.battle.observation import Observation`

## What Does Not Change

- `double_battle.py` — no changes needed
- `battle.py` — no changes needed
- `observed_pokemon.py` — not restored; not needed
- All EliteFurretAI code — zero changes required; existing call sites already use the exact API being restored

## Testing

The upstream repo had `unit_tests/environment/test_observation.py` which was deleted with the feature. We will add a minimal test that:
1. Runs a few protocol lines through a `DoubleBattle`
2. Asserts `battle.observations` has the right turn keys
3. Asserts `observation.events` contains the expected messages
4. Asserts `battle.current_observation` is a fresh `Observation` after a `|turn|` message
