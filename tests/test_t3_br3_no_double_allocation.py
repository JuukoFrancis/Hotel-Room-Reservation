"""T3 - BR3: inside one Room a slot may be allocated to at most one Reservation."""
import pytest

from src.domain.errors import SlotAlreadyReservedError
from src.domain.room import Room, SlotStatus
from src.domain.time_slot import TimeSlot

NINE = TimeSlot("09:00")


def test_t3_br3_available_slot_can_be_reserved_once(room):
    assert room.slot_status(NINE) is SlotStatus.AVAILABLE
    room.reserve_slot(NINE, "R001", "M001")
    assert room.slot_status(NINE) is SlotStatus.RESERVED
    assert room.slot_reserved_by(NINE) == "R001"


def test_t3_br3_same_slot_twice_is_rejected(room):
    room.reserve_slot(NINE, "R001", "M001")
    with pytest.raises(SlotAlreadyReservedError):
        room.reserve_slot(NINE, "R002", "M002")
    assert room.slot_reserved_by(NINE) == "R001"          # first owner keeps it


def test_t3_br3_other_slot_and_other_room_are_independent(room, now):
    room.reserve_slot(NINE, "R001", "M001")
    room.reserve_slot(TimeSlot("10:00"), "R002", "M002")                   # other slot: fine
    other_room = Room.create("RM002", room.start_time)
    other_room.reserve_slot(NINE, "R003", "M003")                          # same slot, other room: fine
