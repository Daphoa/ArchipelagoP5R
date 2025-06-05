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
item_categories: dict[str, dict[str, int]] = {}
game_item_codes: dict[str, int] = {}

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
            max_count: int = 1
            if type_str in ["CONSUMABLE", "MATERIALS"]:
                max_count = 5

            for count in range(1, max_count + 1):
                item_code = data[item_name]
                sub_item_name: str
                if count > 1:
                    sub_item_name = str(count) + "x " + item_name
                else:
                    sub_item_name = item_name

                check_num = item_code + prefix_code + GAME_ITEM_HEX_PREFIX + count * GAME_ITEM_COUNT_PREFIX

                inner[sub_item_name] = check_num

        game_items[gameItemType] = inner

    game_item_codes = {name: game_items[categories][name] for categories in game_items
                       for name in game_items[categories]}

if not item_categories:
    item_categories = orjson.loads(
        pkgutil.get_data(__name__, "data/item_categories.json").decode("utf-8-sig"))

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


def generate_filler_list() -> list[str]:
    starting_filler_categories: list[str] = [
        "Consumables-HP",
        "Consumables-SP",
        "Consumables-HP-SP",
        "Consumables-Revival",
        "Consumables-Food",
        "Consumables-Battle-Recovery",
        "Consumables-Battle-Effect",
        # "Consumables-Tools",
        "Skill-Card-Physical",
        "Skill-Card-Magic",
        "Skill-Card-Recovery/Support",
        "Skill-Card-Passive",
        # "Transmute-Materials",
        "Material",
        "Treasure",
        # "Essentials-Incense",
        # "Essentials-Books",
        # "Essentials-DVDs",
        # "Essentials-Video-Games",
        # "Essentials-Decorations",
        # "Essentials-Gifts",
        # "Essentials-Other",
        # "Key-Items",
        # "Melee-Default",
        "Melee-Joker",
        "Melee-Skull",
        "Melee-Mona",
        "Melee-Panther",
        "Melee-Fox",
        "Melee-Queen",
        "Melee-Noir",
        "Melee-Crow",
        "Melee-Violet",
        # "Ranged-Default",
        "Ranged-Joker",
        "Ranged-Skull",
        "Ranged-Mona",
        "Ranged-Panther",
        "Ranged-Fox",
        "Ranged-Queen",
        "Ranged-Noir",
        "Ranged-Crow",
        "Ranged-Violet",
        "Armor-Laundry",
        # "Armor-Default",
        "Armor",
        # "Accessory-Default",
        "Accessory",
        # "Outfit-Default",
        # "Outfit",
    ]
    multiple_filler_categories = ["Consumables-HP", "Consumables-SP", "Consumables-Food", "Material"]

    filler_item_names: list[str] = []
    filler_item_names += [name
                          for category in starting_filler_categories
                          for name in item_categories[category]]
    filler_item_names += [str(n) + "x " + name
                          for n in range(2, 6)
                          for category in multiple_filler_categories
                          for name in item_categories[category]]

    return filler_item_names



