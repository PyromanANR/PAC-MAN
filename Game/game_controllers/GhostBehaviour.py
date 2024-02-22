from enum import Enum


class GhostBehaviour(Enum):
    """
       An enumeration representing the behavior of a ghost in the game.

       PEACEFUL: Represents a state where the ghost is not actively chasing the player.
       AGGRESSIVE: Represents a state where the ghost is actively chasing the player.
    """
    PEACEFUL = 1
    AGGRESSIVE = 2