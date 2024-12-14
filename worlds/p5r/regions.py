from BaseClasses import Region, MultiWorld


class P5RRegion(Region):
    game: str = "Persona 5 Royal"

    def __init__(self, name: str, player: int, multiworld: MultiWorld):
        super(P5RRegion, self).__init__(name, player, multiworld)

