from typing import (Optional, Callable)

from BaseClasses import Location, Region, CollectionState


class P5RLocation(Location):
    game: str = 'Persona 5 Royal'

    def __init__(self, player: int, name: str = '', address: Optional[int] = None, parent: Optional[Region] = None,
                 rule: Optional[Callable[[CollectionState], bool]] = None):
        super(P5RLocation, self).__init__(player, name, address, parent)
        if rule:
            self.access_rule = rule
