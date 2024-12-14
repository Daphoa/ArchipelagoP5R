from BaseClasses import Tutorial, ItemClassification
from worlds.AutoWorld import WebWorld, World
from .items import P5RItem
from .locations import P5RLocation
from .regions import P5RRegion


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

    item_name_to_id = {
        "Recov-R: 50 mg": 0x3002 + 0x010000 + 0x1000000,
        "Dry Ice": 0x3029 + 0x010000 + 0x1000000,
        "Rancid Gravy": 0x301D + 0x010000 + 0x1000000,
        "Coffee Basics": 52 + 0x2000000,
        "Leblanc Curry": 55 + 0x2000000,
    }
    location_name_to_id = {
        "Chapel Lower NW Chest": 0x200001D4,
        "Chapel Upper SE Chest": 0x200001CA,
        "Chapel Upper SW Chest": 0x200001C9,
    }

    def __init__(self, multiworld: "MultiWorld", player: int):
        super(Persona5RoyalWorld, self).__init__(multiworld, player)

    def create_items(self):
        new_items: list[P5RItem] = [
            # P5RItem("Recov-R: 50 mg", ItemClassification.filler, 0x3002 + 0x010000 + 0x1000000, self.player),
            # P5RItem("Dry Ice", ItemClassification.filler, 0x3029 + 0x010000 + 0x1000000, self.player),
            P5RItem("Rancid Gravy", ItemClassification.filler, 0x301D + 0x010000 + 0x1000000, self.player),
            P5RItem("Coffee Basics", ItemClassification.useful, 52 + 0x2000000, self.player),
            P5RItem("Leblanc Curry", ItemClassification.useful, 55 + 0x2000000, self.player),
        ]

        self.multiworld.itempool += new_items

    def create_regions(self):
        menu_region: P5RRegion = P5RRegion("Menu", self.player, self.multiworld)

        menu_region.locations += [
            P5RLocation(self.player, 'Chapel Lower NW Chest', 0x200001D4, menu_region),
            P5RLocation(self.player, 'Chapel Upper SE Chest', 0x200001CA, menu_region),
            P5RLocation(self.player, 'Chapel Upper SW Chest', 0x200001C9, menu_region),
        ]

        self.multiworld.regions.append(menu_region)


