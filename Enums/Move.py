from enum import Enum


class Move(Enum):
    NONE = -1
    UP = 1
    DOWN = 2
    BACKWARD = 3
    FORWARD = 4
    START = 5
    STOP = 6
    LEFT = 7
    RIGHT = 8
    LAND = 9
    FOLLOW = 10
    TURN_LEFT = 11
    TURN_RIGHT = 12
