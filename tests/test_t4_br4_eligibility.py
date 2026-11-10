"""T4 - BR4: eligible only if the room day has not started AND the member holds < 4 slots there."""
from datetime import timedelta

import pytest

from src.domain.eligibility_service import ReservationEligibilityService
from src.domain.errors import ReservationNotEligibleError
from src.domain.room import Room
from src.domain.time_slot import TimeSlot

service = ReservationEligibilityService()


def _hold(room, member, hours):
    for i, h in enumerate(hours):
        room.reserve_slot(TimeSlot(f"{h:02d}:00"), f"X{member}{i}", member)


def test_t4_br4_below_limit_is_eligible(room, reservation, now):
    _hold(room, "M001", [10, 11, 12])                      # 3 held
    service.check(reservation, room, now)                  # no error


def test_t4_br4_boundary_exactly_four_is_rejected(room, reservation, now):
    _hold(room, "M001", [10, 11, 12, 13])                  # 4 held -> limit reached
    with pytest.raises(ReservationNotEligibleError):
        service.check(reservation, room, now)


def test_t4_br4_started_room_day_is_rejected(room, reservation):
    with pytest.raises(ReservationNotEligibleError):
        service.check(reservation, room, room.start_time + timedelta(minutes=1))


def test_t4_br4_boundary_exactly_at_start_time_is_rejected(room, reservation):
    with pytest.raises(ReservationNotEligibleError):
        service.check(reservation, room, room.start_time)


def test_t4_br4_other_member_or_other_room_do_not_count(room, reservation, now):
    _hold(room, "M999", [10, 11, 12, 13])                  # someone else holds 4
    other = Room.create("RM002", room.start_time)
    _hold(other, "M001", [10, 11, 12, 13])                 # same member, other room
    service.check(reservation, room, now)                  # still eligible
