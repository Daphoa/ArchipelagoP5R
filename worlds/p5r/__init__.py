import csv
from functools import reduce
from typing import Callable

from BaseClasses import Tutorial, ItemClassification
from worlds.AutoWorld import WebWorld, World
from .items import P5RItem, GameItemType, game_items, generate_filler
from .locations import P5RLocation
from .regions import P5RRegion, palaces, LogicRequirement
from .logic import *


def create_item_label_to_code_map() -> dict[str, int]:
    unique_items = {
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

    game_item_codes = {name: game_items[categories][name] for categories in game_items
                       for name in game_items[categories]}

    return unique_items | game_item_codes


def create_location_to_code_map() -> dict[str, int]:
    confidant_items: dict[str, int] = {
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

    chest_items: dict[str, int] = {chest.name: chest.id
                                   for palace in palaces
                                   for region in palaces[palace].regions
                                   for chest in region.chests}

    chest_items_with_palace_name: dict[str, int] = {palaces[palace].name + ": " + chest.name: chest.id
                                                    for palace in palaces
                                                    for region in palaces[palace].regions
                                                    for chest in region.chests}

    return confidant_items | chest_items | chest_items_with_palace_name


def calc_num_items() -> int:
    april_confidant_locations = 1 + 2 + 3 + 6

    # TODO eventually only figure out actually in use chests
    all_chest_locations = len([chest
                               for palace_name in palaces
                               for region in palaces[palace_name].regions
                               for chest in region.chests])

    return april_confidant_locations + all_chest_locations


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

    item_name_to_id = create_item_label_to_code_map()
    location_name_to_id = create_location_to_code_map()

    def __init__(self, multiworld: "MultiWorld", player: int):
        super(Persona5RoyalWorld, self).__init__(multiworld, player)

    def create_items(self):
        key_items: dict[str, int] = game_items[GameItemType.KEY_ITEM]

        progression_items: list[str] = ["Kamoshida's Medal", "Red Lust Seed", "Green Lust Seed", "Blue Lust Seed",
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

        num_locations = calc_num_items()

        # Add filler
        new_items += generate_filler(num=num_locations - len(new_items), random=self.random, player=self.player)

        print([item.name for item in new_items])

        self.multiworld.itempool += new_items

    def create_regions(self):
        p5r_regions: list[P5RRegion] = []
        menu_region: P5RRegion = P5RRegion("Menu", self.player, self.multiworld)
        april: P5RRegion = P5RRegion("April", self.player, self.multiworld)
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

        # Adding regions to world
        p5r_regions.append(menu_region)
        p5r_regions.append(april)
        p5r_regions.append(cmm_hierophant_start)
        p5r_regions.append(cmm_hierophant_part_2)
        p5r_regions.append(cmm_death_start)
        p5r_regions.append(cmm_death_guts)
        p5r_regions.append(cmm_chariot_start)

        # Info from docs
        # TODO move this all into a method somewhere else
        castle_of_lust_data = palaces["Castle of Lust"]
        castle_of_lust_region = P5RRegion(castle_of_lust_data.name, self.player, self.multiworld)
        p5r_regions.append(castle_of_lust_region)
        region_map: dict[str, P5RRegion] = {region.name: P5RRegion(region.name, self.player, self.multiworld) for region
                                            in castle_of_lust_data.regions}
        for region_data in castle_of_lust_data.regions:
            region = region_map[region_data.name]

            if region_data.connections:
                for connection in region_data.connections:
                    connecting_region = region_map[connection.origin]
                    # TODO either implement item requirements, or remove it from the parser
                    rule_func = self.create_rule_func(connection.logic_requirements)
                    connecting_region.connect(region, rule=rule_func)
            else:
                castle_of_lust_region.connect(region)

            chest_locations = [P5RLocation(self.player, chest_data.name, chest_data.id, region,
                                           rule=self.create_rule_func(chest_data.logic_requirements))
                               for chest_data in region_data.chests]
            region.locations += chest_locations
            p5r_regions.append(region)

        menu_region.connect(april, name="Menu to April")
        april.connect(castle_of_lust_region, name="April Dungeon Connection")

        defeat_asmodeus_loc = P5RLocation(self.player, "Defeat Asmodeus", None,
                                          region_map["Castle of Lust Infiltration"])
        defeat_asmodeus_loc.place_locked_item(
            P5RItem("Defeat Asmodeus", ItemClassification.progression, None, self.player))
        region_map["Castle of Lust Infiltration"].locations += [defeat_asmodeus_loc]

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

        self.multiworld.regions += p5r_regions

        # TODO move this to a better point in logic
        self.multiworld.completion_condition[self.player] = \
            lambda state: logic.can_complete(state, self.multiworld, self.player)

    def create_rule_func(self, logic_requirements: list[LogicRequirement]) -> Callable[[CollectionState], bool] | None:
        rule_func = None
        if logic_requirements:
            logic_list: list[LogicRequirement] = [func for func in logic_requirements]
            rule_func = lambda state: reduce(
                (lambda val, logic_func: val and logic_func(state, self.multiworld, self.player)),
                logic_list, True)
        return rule_func
