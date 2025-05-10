from BaseClasses import CollectionState, MultiWorld


def has_grappling_hook(state: CollectionState, world: MultiWorld, player: int) -> bool:
    return state.has("Grappling Hook", player)


def has_guts_2(state: CollectionState, world: MultiWorld, player: int) -> bool:
    # For now its assumed the player will be able to grind out social stats
    return True


def can_make_coffee(state: CollectionState, world: MultiWorld, player: int) -> bool:
    # Some odd behaviour - needs to be investigated manually to implement.
    return state.has("Hierophant: Coffee Basics", player)


def has_kamoshidas_medal(state: CollectionState, world: MultiWorld, player: int) -> bool:
    return state.has("Kamoshida's Medal", player)


def has_both_eyes(state: CollectionState, world: MultiWorld, player: int) -> bool:
    return state.has_all(["Lustful Left Eye", "Randy Right Eye"], player)


def can_infiltrate_lust(state: CollectionState, world: MultiWorld, player: int) -> bool:
    return state.has_all([], player)
