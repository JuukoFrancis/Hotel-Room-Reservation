"""Aggregate B - Room (root) with RoomSlot children (BR3). Factory: Room.create()."""
from datetime import datetime
from enum import Enum

from src.domain.errors import InvalidTimeSlotError, SlotAlreadyReservedError
from src.domain.time_slot import FIRST_HOUR, LAST_HOUR, TimeSlot


class SlotStatus(Enum):
    AVAILABLE = "AVAILABLE"
    RESERVED = "RESERVED"


class RoomSlot:
    """Child entity: identified by its TimeSlot *within one Room*."""

    def __init__(self, time_slot: TimeSlot):
        self.time_slot = time_slot
        self.status = SlotStatus.AVAILABLE
        self.reserved_by: str | None = None      # reservation_id
        self.member_id: str | None = None

    def _reserve(self, reservation_id: str, member_id: str) -> None:   # only Room calls this
        if self.status is SlotStatus.RESERVED:
            raise SlotAlreadyReservedError(
                f"Slot {self.time_slot} is already reserved by {self.reserved_by}")
        self.status = SlotStatus.RESERVED
        self.reserved_by = reservation_id
        self.member_id = member_id


class Room:
    def __init__(self, room_id: str, start_time: datetime, slots: dict[TimeSlot, RoomSlot]):
        self.room_id = room_id
        self.start_time = start_time
        self._slots = slots

    @classmethod
    def create(cls, room_id: str, start_time: datetime) -> "Room":
        """Factory: builds the slot map (08:00..19:00) with every slot AVAILABLE."""
        slots = {}
        for hour in range(FIRST_HOUR, LAST_HOUR + 1):
            ts = TimeSlot(f"{hour:02d}:00")
            slots[ts] = RoomSlot(ts)
        return cls(room_id, start_time, slots)

    def reserve_slot(self, time_slot: TimeSlot, reservation_id: str, member_id: str) -> None:
        """BR3: a slot may be allocated to at most one reservation."""
        slot = self._slots.get(time_slot)
        if slot is None:
            raise InvalidTimeSlotError(f"Room {self.room_id} has no slot {time_slot}")
        slot._reserve(reservation_id, member_id)

    def slot_status(self, time_slot: TimeSlot) -> SlotStatus:
        return self._slots[time_slot].status

    def slot_reserved_by(self, time_slot: TimeSlot) -> str | None:
        return self._slots[time_slot].reserved_by

    def confirmed_slot_count_for(self, member_id: str) -> int:
        return sum(1 for s in self._slots.values() if s.member_id == member_id)

    def has_started(self, now: datetime) -> bool:
        return now >= self.start_time
