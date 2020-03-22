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
    # UTC timestamp of the information (in ISO format)
    timestamp: str


SITE_STATUS_FIELDS = ["uuid","short_id","url","name"] + BLOOD_TYPES + ["timestamp"]

CZECH_BLOOD_STATUSES = {
    "urgent": "akutni",
    "normal": "potrebujeme",
    "full": "mame",
    "": "",
}

def site_status_to_fields(s: SiteStatus, status_kind="english") -> dict:
    res = {"uuid": s.uuid, "short_id": s.short_id, "url": s.url, "name": s.name}
    for blood_type in BLOOD_TYPES:
        blood_status = s.blood_statuses.get(blood_type, "")
        if status_kind == "english":
            status_text = blood_status
        elif status_kind == "czech":
            status_text = CZECH_BLOOD_STATUSES[blood_status]
        else:
            raise ArgumentError(f"Unknown value of status_kind: {status_kind!r}")
        res[blood_type] = status_text
    res["timestamp"] = s.timestamp
    return res

