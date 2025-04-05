import csv

from BaseClasses import Tutorial, ItemClassification
from worlds.AutoWorld import WebWorld, World
from .items import P5RItem, GameItemType, game_items, generate_filler
from .locations import P5RLocation
from .regions import P5RRegion
from .logic import *


class P5RWeb(WebWorld):
    """
    Webhost info for Persona 5 Royal
    """

    theme = "partyTime"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Persona 5 Royal randomizer on your computer.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Daphoa"]
    )

    tutorials = [setup_en]


class Persona5RoyalWorld(World):
    """
    Persona 5 Royal is the definitive edition of the hit game in Atlus's Persona game series.
    """
    game = "Persona 5 Royal"
    web = P5RWeb()
    topology_present = True

    _num_locations = 25

    item_name_to_id = {
        # "Recov-R: 50 mg": 0x3002 + 0x010000 + 0x1000000,
        # "Dry Ice": 0x3029 + 0x010000 + 0x1000000,
        # "Rancid Gravy": 0x301D + 0x010000 + 0x1000000,
        "Grappling Hook": 0x2A3B + 0x3000000,
        # "Kamoshida's Medal": 0x0069 + 0x3000000,
        # "Lustful Left Eye": 0x0074 + 0x3000000,
        # "Randy Right Eye": 0x0075 + 0x3000000,
        "Coffee Basics": 52 + 0x2000000,
        "Leblanc Curry": 55 + 0x2000000,
    }
    location_name_to_id = {
        "Chapel Lower NW Chest": 0x200001D4,
        "Chapel Upper SE Chest": 0x200001CA,
        "Chapel Upper SW Chest": 0x200001C9,
    }

    def __init__(self, multiworld: "MultiWorld", player: int):
        self.item_name_to_id |= {name: game_items[categories][name] for categories in game_items
                                 for name in game_items[categories]}

        super(Persona5RoyalWorld, self).__init__(multiworld, player)

    def create_items(self):
        key_items: dict[str, int] = game_items[GameItemType.KEY_ITEM]

        progression_items: list[str] = ["Kamoshida's Medal", "Lustful Left Eye", "Randy Right Eye", "Red Lust Seed",
                                        "Green Lust Seed", "Blue Lust Seed"]

        new_items: list[P5RItem] = [
            P5RItem("Coffee Basics", ItemClassification.useful, 52 + 0x2000000, self.player),
            P5RItem("Leblanc Curry", ItemClassification.useful, 55 + 0x2000000, self.player),
            P5RItem("Grappling Hook", ItemClassification.progression, 0x2A3B + 0x3000000, self.player),
        ]

        # Progression items
        new_items += [P5RItem(name, ItemClassification.progression, key_items[name], self.player)
                      for name in progression_items]

        # Add filler
        new_items += generate_filler(num=self._num_locations - len(new_items), random=self.random, player=self.player)

        print(new_items)

        self.multiworld.itempool += new_items

    def create_regions(self):
        menu_region: P5RRegion = P5RRegion("Menu", self.player, self.multiworld)
        april: P5RRegion = P5RRegion("April", self.player, self.multiworld)
        castle_of_lust_beginning: P5RRegion = P5RRegion("Castle of Lust Beginning", self.player, self.multiworld)
        castle_of_lust_beginning_grapple_check: P5RRegion = P5RRegion("Castle of Lust Early Grapple Check", self.player,
                                                                      self.multiworld)
        castle_of_lust_part_2: P5RRegion = P5RRegion("Castle of Lust Part 2", self.player, self.multiworld)
        castle_of_lust_part_3: P5RRegion = P5RRegion("Castle of Lust Part 3", self.player, self.multiworld)
        castle_of_lust_ending: P5RRegion = P5RRegion("Castle of Lust Ending", self.player, self.multiworld)
        castle_of_lust_infiltration: P5RRegion = P5RRegion("Castle of Lust Infiltration", self.player, self.multiworld)

        menu_region.connect(april, name="Menu to April")
        april.connect(castle_of_lust_beginning, name="April Dungeon Connection")
        castle_of_lust_beginning.connect(castle_of_lust_beginning_grapple_check,
                                         rule=lambda state: has_grappling_hook(state, self.multiworld,
                                                                               self.player))
        castle_of_lust_beginning.connect(castle_of_lust_part_2,
                                         rule=lambda state: has_kamoshidas_medal(state, self.multiworld,
                                                                                 self.player))
        castle_of_lust_part_2.connect(castle_of_lust_part_3,
                                      rule=lambda state: has_grappling_hook(state, self.multiworld, self.player))
        castle_of_lust_part_3.connect(castle_of_lust_ending,
                                      rule=lambda state: has_both_eyes(state, self.multiworld, self.player))
        april.connect(castle_of_lust_infiltration,
                      rule=lambda state: can_infiltrate_lust(state, self.multiworld, self.player))

        lust_beginning_grapple_check = P5RLocation(self.player, "Castle of Lust - East Building 3F Chest 1",
                                                   0x20000173, castle_of_lust_beginning)
        lust_beginning_grapple_check.access_rule = lambda state: has_grappling_hook(state, self.multiworld, self.player)

        castle_of_lust_beginning.locations += [
            P5RLocation(self.player, "Castle of Lust - West Building 1F Chest", 0x200001C2, castle_of_lust_beginning),
            P5RLocation(self.player, "Castle of Lust - Old Castle 2F Chest 1", 0x200001D6, castle_of_lust_beginning),
            P5RLocation(self.player, "Castle of Lust - Old Castle 2F Chest 2", 0x200001D5, castle_of_lust_beginning),
            P5RLocation(self.player, "Castle of Lust - Old Castle 2F Chest 3", 0x200001C4, castle_of_lust_beginning),
            P5RLocation(self.player, "Castle of Lust - Old Castle 2F Chest 4", 0x200001C5, castle_of_lust_beginning),
            P5RLocation(self.player, "Castle of Lust - East Building 3F Chest 2", 0x200001D3, castle_of_lust_beginning),
            lust_beginning_grapple_check,
        ]

        castle_of_lust_beginning_grapple_check.locations += [
            P5RLocation(self.player, "Castle of Lust - East Building 3F Chest 1", 0x20000173,
                        castle_of_lust_beginning_grapple_check),
        ]

        castle_of_lust_part_2.locations += [
            P5RLocation(self.player, "Castle of Lust - Chapel Lower NW Chest", 0x200001D4, castle_of_lust_part_2),
            P5RLocation(self.player, "Castle of Lust - Chapel Upper SE Chest", 0x200001CA, castle_of_lust_part_2),
            P5RLocation(self.player, "Castle of Lust - Chapel Upper SW Chest", 0x200001C9, castle_of_lust_part_2),
            P5RLocation(self.player, "Castle of Lust - East Building Annex Chest 4", 0x200001CB,
                        castle_of_lust_part_2),
            P5RLocation(self.player, "Castle of Lust - East Building Annex Chest 5", 0x200001D8,
                        castle_of_lust_part_2),
        ]

        castle_of_lust_part_3.locations += [
            P5RLocation(self.player, "Castle of Lust - Roof Chest", 0x200001CC, castle_of_lust_part_3),
            P5RLocation(self.player, "Castle of Lust - Central Hall Chest 1", 0x200001C6, castle_of_lust_part_3),
            P5RLocation(self.player, "Castle of Lust - Central Hall Chest 2", 0x200001C3, castle_of_lust_part_3),
            P5RLocation(self.player, "Castle of Lust - Central Tower Chest 1", 0x200001D9, castle_of_lust_part_3),
            P5RLocation(self.player, "Castle of Lust - Central Tower Chest 2", 0x200001C7, castle_of_lust_part_3),
            P5RLocation(self.player, "Castle of Lust - Central Tower Chest 3", 0x200001CD, castle_of_lust_part_3),
            P5RLocation(self.player, "Castle of Lust - Blue Lust Seed", 0x200013FD, castle_of_lust_part_3),
            # P5RLocation(self.player, "Castle of Lust - Red Lust Seed", 0, castle_of_lust_part_3),
        ]

        castle_of_lust_ending.locations += [
            P5RLocation(self.player, "Castle of Lust - Central Tower Chest 4", 0x200001D2, castle_of_lust_ending),
            P5RLocation(self.player, "Castle of Lust - Central Tower Chest 5", 0x200001CE, castle_of_lust_ending),
            P5RLocation(self.player, "Castle of Lust - Central Tower Chest 6", 0x200001C8, castle_of_lust_ending),
            P5RLocation(self.player, "Castle of Lust - Throne Room Chest 1", 0x200001D1, castle_of_lust_ending),
            P5RLocation(self.player, "Castle of Lust - Throne Room Chest 2", 0x200001CF, castle_of_lust_ending),
            P5RLocation(self.player, "Castle of Lust - Green Lust Seed", 0x200013FC, castle_of_lust_ending),
        ]

        defeat_asmodeus_loc = P5RLocation(self.player, "Defeat Asmodeus", None, castle_of_lust_infiltration)
        defeat_asmodeus_loc.place_locked_item(
            P5RItem("Defeat Asmodeus", ItemClassification.progression, None, self.player))

        self.multiworld.regions.append(menu_region)
