import csv
from functools import reduce
from typing import Callable

from BaseClasses import Tutorial, ItemClassification
from worlds.AutoWorld import WebWorld, World
from .items import P5RItem, GameItemType, game_items, generate_party_member_items, \
    party_member_to_code, game_item_codes, generate_filler_list
from .locations import P5RLocation
from .options import P5RGameOptions
from .regions import P5RRegion, palaces, LogicRequirement, confidants
from .logic import *


def create_confidant_location_name(confidant_name: str, level: int) -> str:
    return confidant_name + " Rank " + str(level)


def create_confidant_location_id(confidant_id: int, level: int) -> int:
    return 0x60000000 + (confidant_id * 0x10) + level


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

    return unique_items | game_item_codes | party_member_to_code


def create_location_to_code_map() -> dict[str, int]:
    confidant_locations: dict[str, int] = {create_confidant_location_name(confidant_name, level):
                                               create_confidant_location_id(confidants[confidant_name].id, level)
                                           for confidant_name in confidants
                                           for level in range(1, 11)}

    chest_items: dict[str, int] = {chest.name: chest.id
                                   for palace in palaces
                                   for region in palaces[palace].regions
                                   for chest in region.chests}

    chest_items_with_palace_name: dict[str, int] = {palaces[palace].name + ": " + chest.name: chest.id
                                                    for palace in palaces
                                                    for region in palaces[palace].regions
                                                    for chest in region.chests}

    return confidant_locations | chest_items | chest_items_with_palace_name


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
    rich_text_options_doc = True

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
    options_dataclass = P5RGameOptions
    options: P5RGameOptions

    item_name_to_id = create_item_label_to_code_map()
    location_name_to_id = create_location_to_code_map()

    p5r_regions: list[P5RRegion] = []
    num_locations: int = 0
    all_filler_items: list[str]

    def __init__(self, multiworld: "MultiWorld", player: int):
        super(Persona5RoyalWorld, self).__init__(multiworld, player)

    def create_items(self):
        self.all_filler_items = generate_filler_list()

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

        # Progression + useful items
        new_items += [P5RItem(name, ItemClassification.progression, key_items[name], self.player)
                      for name in progression_items]

        party_mem_items: dict[str, P5RItem] = generate_party_member_items(self.player)
        new_items += [party_mem_items[name] for name in party_mem_items]

        # Add filler
        new_items += self._generate_filler(num=self.num_locations - len(new_items))

        print([item.name for item in new_items])

        self.multiworld.itempool += new_items

    def create_regions(self):
        menu_region: P5RRegion = P5RRegion("Menu", self.player, self.multiworld)
        april: P5RRegion = P5RRegion("April", self.player, self.multiworld)

        # Adding regions to world
        self.p5r_regions.append(menu_region)
        self.p5r_regions.append(april)

        # Info from docs
        # TODO move this all into a method somewhere else
        castle_of_lust_data = palaces["Castle of Lust"]
        castle_of_lust_region = P5RRegion(castle_of_lust_data.name, self.player, self.multiworld)
        self.p5r_regions.append(castle_of_lust_region)
        region_map: dict[str, P5RRegion] = {region.name: P5RRegion(region.name, self.player, self.multiworld) for region
                                            in castle_of_lust_data.regions}
        for region_data in castle_of_lust_data.regions:
            print("Got region " + region_data.name)
            region = region_map[region_data.name]

            if region_data.connections:
                for connection in region_data.connections:
                    print("Connecting to " + connection.origin)
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
            self.num_locations += len(chest_locations)
            self.p5r_regions.append(region)

        menu_region.connect(april, name="Menu to April")
        april.connect(castle_of_lust_region, name="April Dungeon Connection")

        defeat_asmodeus_loc = P5RLocation(self.player, "Defeat Asmodeus", None,
                                          region_map["Castle of Lust Infiltration"])
        defeat_asmodeus_loc.place_locked_item(
            P5RItem("Defeat Asmodeus", ItemClassification.progression, None, self.player))
        region_map["Castle of Lust Infiltration"].locations += [defeat_asmodeus_loc]

        for confidant_name in confidants:
            confidant = confidants[confidant_name]

            confidant_region = P5RRegion(confidant_name + " Confidant", self.player, self.multiworld)
            # TODO Placeholder
            april.connect(confidant_region)

            sub_regions: list[P5RRegion] = [
                P5RRegion(confidant_name + " Confidant Part 1", self.player, self.multiworld)
            ]
            confidant_region.connect(sub_regions[0])
            for level in range(1, 11):
                if level in confidant.automatic:
                    # No location for automatic ranks
                    continue

                if level in confidant.logic_requirements:
                    region_name = confidant_name + " Confidant Part " + str(len(sub_regions) + 1)
                    new_region = P5RRegion(region_name, self.player, self.multiworld)
                    if logic.unimplemented in confidant.logic_requirements[level]:
                        break
                    rule_func = self.create_rule_func(confidant.logic_requirements[level])
                    sub_regions[-1].connect(new_region, rule=rule_func)
                    sub_regions.append(new_region)

                address: int = create_confidant_location_id(confidant.id, level)
                name: str = create_confidant_location_name(confidant.name, level)
                location: P5RLocation = P5RLocation(self.player, name, address, sub_regions[-1])
                sub_regions[-1].locations.append(location)
                self.num_locations += 1

            self.p5r_regions.append(confidant_region)
            self.p5r_regions += sub_regions

        self.multiworld.regions += self.p5r_regions

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

    def get_filler_item_name(self) -> str:
        """Called when the item pool needs to be filled with additional items to match location count."""
        return self.random.choice(tuple(self.all_filler_items))

    def _generate_filler(self, num: int) -> list[P5RItem]:
        # TODO enhance this algorithm, and add player options to modify it
        if not game_item_codes:
            return []

        item_names: list[str] = self.random.choices(self.all_filler_items, k=num)
        return [P5RItem(name=name, code=game_item_codes[name], classification=ItemClassification.filler,
                        player=self.player) for name in item_names]
