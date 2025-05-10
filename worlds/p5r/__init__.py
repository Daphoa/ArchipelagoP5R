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

    _num_locations = 26 + 12

    item_name_to_id = {
        "Grappling Hook": 0x2A3B + 0x3000000,
        "Hierophant: Coffee Basics": 0x34 + 0x2000000,
        "Coffee Basics": 0x34 + 0x2000000,
        "Hierophant: Leblanc Curry": 0x37 + 0x2000000,
        "Leblanc Curry": 0x37 + 0x2000000,
        "Chariot: Punk Talk": 0x4B + 0x2000000,
        "Punk Talk": 0x4B + 0x2000000,
        "Chariot: Follow Up": 0x49 + 0x2000000,
        "Chariot: Stealth Dash": 0x11B + 0x2000000,
        "Stealth Dash": 0x11B + 0x2000000,
        "Chariot: Harisen Recovery": 0x4A + 0x2000000,
        "Chariot: Insta-kill": 0x50 + 0x2000000,
        "Insta-kill": 0x50 + 0x2000000,
        "Chariot: Endure": 0x4D + 0x2000000,
        "Chariot: Protect": 0x4F + 0x2000000,
        # "Death: Rejuvenation": 0x83 + 0x2000000,
        # "Rejuvenation": 0x83 + 0x2000000,
        "Death: Sterilization": 0x85 + 0x2000000,
        "Sterilization": 0x85 + 0x2000000,
        "Death: Immunization": 0x89 + 0x2000000,
        "Immunization": 0x89 + 0x2000000,
        "Death: Discount": 0x87 + 0x2000000,
        "Death: Resuscitation": 0x8B + 0x2000000,
        "Resuscitation": 0x8B + 0x2000000,
    }
    location_name_to_id = {
        "Castle of Lust - West Building 1F Chest": 0x200001C2,
        "Castle of Lust - Old Castle 2F Chest 1": 0x200001D6,
        "Castle of Lust - Old Castle 2F Chest 2": 0x200001D5,
        "Castle of Lust - Old Castle 2F Chest 3": 0x200001C4,
        "Castle of Lust - Old Castle 2F Chest 4": 0x200001C5,
        "Castle of Lust - East Building 3F Chest 2": 0x200001D3,
        "Castle of Lust - Chapel Lower NW Chest": 0x200001D4,
        "Castle of Lust - Chapel Upper SE Chest": 0x200001CA,
        "Castle of Lust - Chapel Upper SW Chest": 0x200001C9,
        "Castle of Lust - East Building Annex Chest 4": 0x200001CB,
        "Castle of Lust - East Building Annex Chest 5": 0x200001D8,
        "Castle of Lust - Roof Chest": 0x200001CC,
        "Castle of Lust - Central Hall Chest 1": 0x200001C6,
        "Castle of Lust - Central Hall Chest 2": 0x200001C3,
        "Castle of Lust - Central Tower Chest 1": 0x200001D9,
        "Castle of Lust - Central Tower Chest 2": 0x200001C7,
        "Castle of Lust - Central Tower Chest 3": 0x200001CD,
        "Castle of Lust - Central Tower Chest 4": 0x200001D2,
        "Castle of Lust - Central Tower Chest 5": 0x200001CE,
        "Castle of Lust - Central Tower Chest 6": 0x200001C8,
        "Castle of Lust - Throne Room Chest 1": 0x200001D1,
        "Castle of Lust - Throne Room Chest 2": 0x200001CF,
        "Castle of Lust - Blue Lust Seed": 0x200013FD,
        "Castle of Lust - Red Lust Seed": 0x200013FB,
        "Castle of Lust - Green Lust Seed": 0x200013FC,

        "Hierophant Rank 2": 0x60000062,
        "Hierophant Rank 3": 0x60000063,
        "Hierophant Rank 4": 0x60000064,
        "Chariot Rank 2": 0x60000082,
        "Chariot Rank 3": 0x60000083,
        "Chariot Rank 4": 0x60000084,
        "Death Rank 2": 0x600000E2,
        "Death Rank 3": 0x600000E3,
        "Death Rank 4": 0x600000E4,
        "Death Rank 5": 0x600000E5,
        "Death Rank 6": 0x600000E6,
        "Death Rank 7": 0x600000E7,
    }

    def __init__(self, multiworld: "MultiWorld", player: int):
        self.item_name_to_id |= {name: game_items[categories][name] for categories in game_items
                                 for name in game_items[categories]}

        super(Persona5RoyalWorld, self).__init__(multiworld, player)

    def create_items(self):
        key_items: dict[str, int] = game_items[GameItemType.KEY_ITEM]

        progression_items: list[str] = ["Kamoshida's Medal",  "Red Lust Seed", "Green Lust Seed", "Blue Lust Seed",
                                        "Randy Right Eye", "Lustful Left Eye"]

        new_items: list[P5RItem] = [
            P5RItem("Grappling Hook", ItemClassification.progression, 0x2A3B + 0x3000000, self.player),
            P5RItem("Hierophant: Coffee Basics", ItemClassification.progression, 52 + 0x2000000, self.player),
            P5RItem("Hierophant: Leblanc Curry", ItemClassification.useful, 55 + 0x2000000, self.player),
            P5RItem("Chariot: Punk Talk", ItemClassification.useful, 0x4B + 0x2000000, self.player),
            P5RItem("Chariot: Follow Up", ItemClassification.useful, 0x49 + 0x2000000, self.player),
            P5RItem("Chariot: Stealth Dash", ItemClassification.useful, 0x11B + 0x2000000, self.player),
            P5RItem("Chariot: Harisen Recovery", ItemClassification.useful, 0x4A + 0x2000000, self.player),
            P5RItem("Chariot: Insta-kill", ItemClassification.useful, 0x50 + 0x2000000, self.player),
            P5RItem("Chariot: Endure", ItemClassification.useful, 0x4D + 0x2000000, self.player),
            P5RItem("Chariot: Protect", ItemClassification.useful, 0x4F + 0x2000000, self.player),
            P5RItem("Death: Sterilization", ItemClassification.useful, 0x85 + 0x2000000, self.player),
            P5RItem("Death: Immunization", ItemClassification.useful, 0x89 + 0x2000000, self.player),
            P5RItem("Death: Discount", ItemClassification.useful, 0x87 + 0x2000000, self.player),
            P5RItem("Death: Resuscitation", ItemClassification.useful, 0x8B + 0x2000000, self.player),
        ]

        # Progression items
        new_items += [P5RItem(name, ItemClassification.progression, key_items[name], self.player)
                      for name in progression_items]

        # Add filler
        new_items += generate_filler(num=self._num_locations - len(new_items), random=self.random, player=self.player)

        print([item.name for item in new_items])

        self.multiworld.itempool += new_items

    def create_regions(self):
        menu_region: P5RRegion = P5RRegion("Menu", self.player, self.multiworld)
        april: P5RRegion = P5RRegion("April", self.player, self.multiworld)
        castle_of_lust_beginning: P5RRegion = P5RRegion("Castle of Lust Beginning", self.player, self.multiworld)
        castle_of_lust_part_2: P5RRegion = P5RRegion("Castle of Lust Part 2", self.player, self.multiworld)
        castle_of_lust_part_3: P5RRegion = P5RRegion("Castle of Lust Part 3", self.player, self.multiworld)
        castle_of_lust_ending: P5RRegion = P5RRegion("Castle of Lust Ending", self.player, self.multiworld)
        castle_of_lust_infiltration: P5RRegion = P5RRegion("Castle of Lust Infiltration", self.player, self.multiworld)

        cmm_hierophant_start: P5RRegion = P5RRegion("Hierophant Confidant Start", self.player, self.multiworld)
        cmm_hierophant_part_2: P5RRegion = P5RRegion("Hierophant Confidant After Coffee", self.player, self.multiworld)
        cmm_hierophant_part_3: P5RRegion = P5RRegion("Hierophant Confidant After Pyramid of Wrath", self.player,
                                                     self.multiworld)
        cmm_hierophant_part_4: P5RRegion = P5RRegion("Hierophant Confidant After Kindness", self.player,
                                                     self.multiworld)
        cmm_hierophant_part_5: P5RRegion = P5RRegion("Hierophant Confidant After Request", self.player, self.multiworld)

        cmm_death_start: P5RRegion = P5RRegion("Death Confidant Start", self.player, self.multiworld)
        cmm_death_guts: P5RRegion = P5RRegion("Death Confidant Guts 2", self.player, self.multiworld)
        cmm_chariot_start: P5RRegion = P5RRegion("Chariot Confidant Start", self.player, self.multiworld)
        cmm_chariot_may: P5RRegion = P5RRegion("Chariot Confidant May", self.player, self.multiworld)

        menu_region.connect(april, name="Menu to April")
        april.connect(castle_of_lust_beginning, name="April Dungeon Connection")
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
            P5RLocation(self.player, "Castle of Lust - Red Lust Seed", 0x200013FB, castle_of_lust_part_3),
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

        menu_region.connect(cmm_hierophant_start, name="Menu to Hierophant")
        cmm_hierophant_start.connect(cmm_hierophant_part_2,
                                     rule=lambda state: can_make_coffee(state, self.multiworld, self.player))
        menu_region.connect(cmm_chariot_start, name="Menu to Chariot")
        menu_region.connect(cmm_death_start, name="Menu to Death")
        cmm_death_start.connect(cmm_death_guts, name="Death Guts 2",
                                rule=lambda state: has_guts_2(state, self.multiworld, self.player))

        cmm_hierophant_start.locations += [
            # P5RLocation(self.player, "Hierophant Rank 1", 0x60000061, cmm_hierophant_start),
            P5RLocation(self.player, "Hierophant Rank 2", 0x60000062, cmm_hierophant_start),
        ]

        cmm_hierophant_part_2.locations += [
            P5RLocation(self.player, "Hierophant Rank 3", 0x60000063, cmm_hierophant_part_2),
            P5RLocation(self.player, "Hierophant Rank 4", 0x60000064, cmm_hierophant_part_2),
        ]

        cmm_chariot_start.locations += [
            # P5RLocation(self.player, "Chariot Rank 1", 0x60000081, cmm_hierophant_start),
            P5RLocation(self.player, "Chariot Rank 2", 0x60000082, cmm_chariot_start),
            P5RLocation(self.player, "Chariot Rank 3", 0x60000083, cmm_chariot_start),
            P5RLocation(self.player, "Chariot Rank 4", 0x60000084, cmm_chariot_start),
        ]

        # cmm_death_start.locations += [
        #     P5RLocation(self.player, "Death Rank 1", 0x600000E1, cmm_death_start),
        # ]

        cmm_death_guts.locations += [
            P5RLocation(self.player, "Death Rank 2", 0x600000E2, cmm_death_guts),
            P5RLocation(self.player, "Death Rank 3", 0x600000E3, cmm_death_guts),
            P5RLocation(self.player, "Death Rank 4", 0x600000E4, cmm_death_guts),
            P5RLocation(self.player, "Death Rank 5", 0x600000E5, cmm_death_guts),
            P5RLocation(self.player, "Death Rank 6", 0x600000E6, cmm_death_guts),
            P5RLocation(self.player, "Death Rank 7", 0x600000E7, cmm_death_guts),
        ]

        self.multiworld.regions.append(menu_region)
