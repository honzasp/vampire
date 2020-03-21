from dataclasses import dataclass
from enum import Enum
from typing import Dict
import datetime

BLOOD_TYPES = [
    "0+", "0-",
    "a+", "a-",
    "b+", "b-",
    "ab+", "ab-",
    "plasma",
]

BLOOD_STATUSES = [
    "urgent",
    "normal",
    "full",
]

@dataclass
class SiteStatus:
    url: str
    name: str
    blood_statuses: Dict[str, str]
