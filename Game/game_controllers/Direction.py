from enum import Enum


class Direction(Enum):
    """
    The `Direction` class is an enumeration that represents various directions in terms of angles.

    Each direction is associated with a specific angle in degrees, as follows:

    - `DOWN`: Represents the downward direction, associated with an angle of -90 degrees.
    - `RIGHT`: Represents the rightward direction, associated with an angle of 0 degrees.
    - `UP`: Represents the upward direction, associated with an angle of 90 degrees.
    - `LEFT`: Represents the leftward direction, associated with an angle of 180 degrees.
    - `NONE`: Represents no direction, associated with an angle of 360 degrees.

    """
    DOWN = -90
    RIGHT = 0
    UP = 90
    LEFT = 180
    NONE = 360