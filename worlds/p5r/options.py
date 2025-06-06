from dataclasses import dataclass

from Options import Toggle, Range, Choice, PerGameCommonOptions, NamedRange, Visibility


class OracleRandomized(Choice):
    """How to randomize Oracle in your party."""
    display_name = "Randomize Oracle"
    option_start_with = 0
    option_randomize = 1
    option_no_oracle = 2
    default = 0


class StartingParty(NamedRange):
    """How many party members do you start with (note: Oracle isn't included here)"""
    display_name = "Starting Party Member Count"
    range_start = 0
    range_end = 7
    special_range_names = {
        "none": 0,
        "all": 7,
    }
    default = 2


@dataclass
class P5RGameOptions(PerGameCommonOptions):
    oracle_randomized: OracleRandomized
    starting_party: StartingParty
