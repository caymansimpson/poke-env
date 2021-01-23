# -*- coding: utf-8 -*-
"""This module defines the SideCondition class, which represents a in-battle side
condition.
"""
# pyre-ignore-all-errors[45]
from enum import Enum, unique, auto

# This is an enum for all the Volatile Statuses you can have
@unique
class VolatileStatus(Enum):
    """Enumeration, represent a non null field in a battle."""
    OBSTRUCT = auto()
    OCTOLOCK = auto()
    LEECH_SEED = auto()
    MIRACLE_EYE = auto()
    MAX_GUARD = auto()
    PARTIALLY_TRAPPED = auto()
    FOCUS_ENERGY = auto()
    MAGNET_RISE = auto()
    TORMENT = auto()
    POWDER = auto()
    SPIKY_SHIELD = auto()
    POWER_TRICK = auto()
    ATTRACT = auto()
    SUBSTITUTE = auto()
    KINGS_SHIELD = auto()
    CURSE = auto()
    INGRAIN = auto()
    UPROAR = auto()
    ELECTRIFY = auto()
    NIGHTMARE = auto()
    FOLLOW_ME = auto()
    CHARGE = auto()
    STOCKPILE = auto()
    TAUNT = auto()
    LOCKED_MOVE = auto()
    CONFUSION = auto()
    FLINCH = auto()
    DESTINY_BOND = auto()
    MUST_RECHARGE = auto()
    EMBARGO = auto()
    TARSHOT = auto()
    RAGE_POWDER = auto()
    BANEFUL_BUNKER = auto()
    ROOST = auto()
    PROTECT = auto()
    SNATCH = auto()
    YAWN = auto()
    NO_RETREAT = auto()
    GASTRO_ACID = auto()
    TELEKINESIS = auto()
    LASER_FOCUS = auto()
    AQUA_RING = auto()
    GRUDGE = auto()
    MAGIC_COAT = auto()
    RAGE = auto()
    SMACK_DOWN = auto()
    HEAL_BLOCK = auto()
    HELPING_HAND = auto()
    FORESIGHT = auto()
    MINIMIZE = auto()
    DISABLE = auto()
    ENDURE = auto()
    IMPRISON = auto()
    DEFENSE_CURL = auto()
    BIDE = auto()
    SPOTLIGHT = auto()
    ENCORE = auto()

    def __str__(self) -> str:
        return f"{self.name} (field) object"
