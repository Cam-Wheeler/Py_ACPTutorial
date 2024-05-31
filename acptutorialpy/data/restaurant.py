# Standard Lib Imports:
from dataclasses import dataclass, field
from enum import Enum

# Local Imports:
from .lat_lng import LatLng
from .pizza import Pizza


class Weekday(Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

@dataclass
class Restaurant:
    name: str
    location: LatLng
    opening_days: list[Weekday]
    menu: list[Pizza]
