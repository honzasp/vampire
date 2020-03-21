from dataclasses import dataclass
from enum import Enum
from typing import Dict
import datetime

# Various types of blood (and blood products) that can be donated at transfusion centers.
BLOOD_TYPES = [
    "0+", "0-",
    "a+", "a-",
    "b+", "b-",
    "ab+", "ab-",
    "plasma",
]

# Possible states of storage of a particular type of blood at a transfusion center.
BLOOD_STATUSES = [
    # The center has very little amount of the blood type and urgently needs more.
    "urgent",
    # The center has some amount of the blood type, but it accepts further donations.
    "normal",
    # The center has sufficient amount of blood and does not accept donations.
    "full",
]

# Information about a transfusion center.
@dataclass
class SiteStatus:
    # UUID of the site at darujukrev.cz
    uuid: str
    # Short human-readable identifier of the site
    short_id: str
    # URL where the blood status is published.
    url: str
    # Full name of the institution.
    name: str
    # Mapping from BLOOD_TYPES to BLOOD_STATUSES. Some blood types may not be present if
    # the status is not known.
    blood_statuses: Dict[str, str]
