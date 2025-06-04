import json
import pkgutil
from enum import Enum
from random import Random
from typing import Optional

from orjson import orjson

from BaseClasses import Item, ItemClassification


class P5RItem(Item):
    game: str = "Persona 5 Royal"
    type: str

    def __init__(self, name: str, classification: ItemClassification, code: Optional[int], player: int):
        # Code placeholder

        super(P5RItem, self).__init__(name, classification, code, player)


class GameItemType(Enum):
    MELEE_ITEM = 0
    ARMOR = 1
    ACCESSORY = 2
    CONSUMABLE = 3
    KEY_ITEM = 4
    MATERIALS = 5
    SKILL_CARD = 6
    OUTFIT = 7
    RANGED_WEAPON = 8


GAME_ITEM_HEX_PREFIX = 0x1000000
GAME_ITEM_TYPE_PREFIX = 0x1000
GAME_ITEM_COUNT_PREFIX = 0x10000
PARTY_MEM_ITEM_HEX_PREFIX = 0x5000000

game_items: dict[GameItemType, dict[str, int]] = {}

if not game_items:
    # Initialize item once
    game_items_json: dict[str, dict[str, int]] = orjson.loads(
        pkgutil.get_data(__name__, "data/game_items.json").decode("utf-8-sig"))

    for type_str in game_items_json:
        gameItemType = getattr(GameItemType, type_str)
        data = game_items_json[type_str]

        prefix_code = GAME_ITEM_TYPE_PREFIX * gameItemType.value

        inner: dict[str, int] = {}

        for item_name in data:
            count = 1
            item_code = data[item_name]

            check_num = item_code + prefix_code + GAME_ITEM_HEX_PREFIX + count * GAME_ITEM_COUNT_PREFIX

            inner[item_name] = check_num

        game_items[gameItemType] = inner

party_member_to_code: dict[str, int] = {
    "Skull": 2 + PARTY_MEM_ITEM_HEX_PREFIX,
    "Mona": 3 + PARTY_MEM_ITEM_HEX_PREFIX,
    "Panther": 4 + PARTY_MEM_ITEM_HEX_PREFIX,
    "Fox": 5 + PARTY_MEM_ITEM_HEX_PREFIX,
    "Queen": 6 + PARTY_MEM_ITEM_HEX_PREFIX,
    "Noir": 7 + PARTY_MEM_ITEM_HEX_PREFIX,
    "Oracle": 8 + PARTY_MEM_ITEM_HEX_PREFIX,
    "Crow": 9 + PARTY_MEM_ITEM_HEX_PREFIX,
    "Violet": 10 + PARTY_MEM_ITEM_HEX_PREFIX,
}


def generate_party_member_items(player: int) -> dict[str, P5RItem]:
    return {
        mem_name: P5RItem(mem_name, ItemClassification.useful, party_member_to_code[mem_name], player)
        for mem_name in party_member_to_code}


def generate_filler(num: int, player: int, random: Random) -> list[P5RItem]:
    # TODO enhance this algorithm, and add player options to modify it
    if GameItemType.CONSUMABLE not in game_items:
        return []

    item_names: list[str] = random.choices([name for name in game_items[GameItemType.CONSUMABLE]], k=num)
    return [P5RItem(name=name, code=game_items[GameItemType.CONSUMABLE][name], classification=ItemClassification.filler,
                    player=player) for name in item_names]
