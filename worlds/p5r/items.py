from BaseClasses import Item, ItemClassification


class P5RItem(Item):
    game: str = "Persona 5 Royal"
    type: str

    def __init__(self, name: str, classification: ItemClassification, code: int, player: int):
        # Code placeholder
        # code = None

        super(P5RItem, self).__init__(name, classification, code, player)
