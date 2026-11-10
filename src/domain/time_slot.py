"""BR1 - Value Object: a TimeSlot is one whole hour, 08:00 to 19:00 (HH:00)."""
import re
from dataclasses import dataclass

from src.domain.errors import InvalidTimeSlotError

FIRST_HOUR = 8     # 08:00-09:00
LAST_HOUR = 19     # 19:00-20:00
_PATTERN = re.compile(r"^(\d{2}):00$")


@dataclass(frozen=True)
class TimeSlot:
    value: str

    def __post_init__(self):
        match = _PATTERN.match(self.value) if isinstance(self.value, str) else None
        if match is None or not FIRST_HOUR <= int(match.group(1)) <= LAST_HOUR:
            raise InvalidTimeSlotError(f"Invalid time slot: {self.value!r}")

    @property
    def hour(self) -> int:
        return int(self.value[:2])

    def __str__(self) -> str:
        return self.value
