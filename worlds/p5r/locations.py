from typing import (Optional)

from BaseClasses import Location, Region


class P5RLocation(Location):
    game: str = 'Persona 5 Royal'

    def __init__(self, player: int, name: str = '', address: Optional[int] = None, parent: Optional[Region] = None):
        super(P5RLocation, self).__init__(player, name, address, parent)

