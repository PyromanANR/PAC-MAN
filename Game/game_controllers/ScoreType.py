from enum import Enum

class ScoreType(Enum):
    """
    An enumeration representing the different types of scores in the game.

    COOKIE: Represents the score gained when the player collects a cookie. The value is 10.
    POWERUP: Represents the score gained when the player collects a power-up. The value is 50.
    GHOST: Represents the score gained when the player catches a ghost. The value is 400.
    """
    COOKIE = 10
    POWERUP = 50
    GHOST = 400