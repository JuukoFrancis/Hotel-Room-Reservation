"""T1 - BR1: a TimeSlot is one whole hour from 08:00 to 19:00 (format HH:00)."""
import pytest

from src.domain.errors import InvalidTimeSlotError
from src.domain.time_slot import TimeSlot


def test_t1_br1_accepts_valid_time_slots():
    assert TimeSlot("09:00").value == "09:00"
    assert TimeSlot("13:00").hour == 13


def test_t1_br1_accepts_boundary_time_slots():
    assert TimeSlot("08:00").hour == 8      # first valid slot
    assert TimeSlot("19:00").hour == 19     # last valid slot


@pytest.mark.parametrize("bad", ["07:00", "20:00", "9:00", "09:30", "", "A10", "24:00"])
def test_t1_br1_rejects_invalid_time_slots(bad):
    with pytest.raises(InvalidTimeSlotError):
        TimeSlot(bad)


def test_t1_br1_equality_is_by_value():
    assert TimeSlot("10:00") == TimeSlot("10:00")
    assert TimeSlot("10:00") != TimeSlot("11:00")
