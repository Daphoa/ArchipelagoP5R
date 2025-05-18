import pkgutil

import orjson

from BaseClasses import Region, MultiWorld, CollectionState
from typing import NotRequired, Callable

LogicRequirement = Callable[[CollectionState, MultiWorld, int], bool]


class Connection:
    origin: str
    item_requirements: list[str] = []
    logic_requirements: list[LogicRequirement] = []


class PalaceChest:
    name: str
    id: int
    item_requirements: list[str] = []
    logic_requirements: list[LogicRequirement] = []


class PalaceRegion:
    name: str
    chests: list[PalaceChest] = []
    connections: list[Connection] = []


class Palace:
    name: str
    regions: list[PalaceRegion]


palaces: dict[str, Palace] = {}

if not palaces:
    from typing import TypedDict
    import worlds.p5r.logic as logic

    ChestData = TypedDict('ChestData', {'name': str, 'id': str, 'item_requirements': NotRequired[list[str]]})
    ConnectionData = TypedDict('ConnectionData', {'origin': str, 'item_requirements': NotRequired[list[str]],
                                                  'logic_requirements': NotRequired[list[str]]})
    RegionData = TypedDict('RegionData', {'name': str, 'chests': list[ChestData],
                                          'connections': NotRequired[list[ConnectionData]]})
    PalaceData = TypedDict('PalaceData', {'name': str, 'regions': list[RegionData]})

    # Initialize palaces once
    game_palaces_json: list[PalaceData] = orjson.loads(
        pkgutil.get_data(__name__, "data/palaces.json").decode("utf-8-sig"))

    palaces: dict[str, Palace] = {}

    for palace_data in game_palaces_json:
        palace: Palace = Palace()

        palace.name = palace_data["name"]
        palace.regions = []
        for region_data in palace_data["regions"]:
            region: PalaceRegion = PalaceRegion()
            region.name = region_data["name"]
            region.chests = []
            region.connections = []

            if "chests" in region_data:
                for chest_data in region_data["chests"]:
                    chest: PalaceChest = PalaceChest()
                    chest.name = chest_data["name"]
                    chest.id = int(chest_data["id"], 0)

                    if "item_requirements" in chest_data:
                        chest.item_requirements = chest_data["item_requirements"]

                    region.chests.append(chest)

            if "connections" in region_data:
                for connection_data in region_data["connections"]:
                    connection: Connection = Connection()

                    connection.origin = connection_data["origin"]
                    connection.item_requirements = []
                    if "item_requirements" in connection_data:
                        connection.item_requirements += connection_data["item_requirements"]
                    connection.logic_requirements = []
                    if "logic_requirements" in connection_data:
                        for logic_name in connection_data["logic_requirements"]:
                            logic_func: Callable[[CollectionState, MultiWorld, int], bool] = getattr(logic, logic_name)
                            connection.logic_requirements.append(logic_func)

                    region.connections.append(connection)

            palace.regions.append(region)
        palaces[palace.name] = palace


class P5RRegion(Region):
    game: str = "Persona 5 Royal"

    def __init__(self, name: str, player: int, multiworld: MultiWorld):
        super(P5RRegion, self).__init__(name, player, multiworld)
