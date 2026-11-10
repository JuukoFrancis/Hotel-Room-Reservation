"""T5 - BR5: confirming raises ReservationConfirmed; the handler asks the Room to reserve the slot."""
import pytest

from src.application.handlers import ReservationConfirmedHandler
from src.domain.errors import InvalidReservationStateError
from src.domain.events import ReservationConfirmed
from src.domain.room import SlotStatus
from src.domain.time_slot import TimeSlot
from src.infrastructure.in_memory_repositories import InMemoryRoomRepository


def test_t5_br5_confirm_raises_event_with_correct_data(reservation):
    reservation.confirm()
    events = reservation.pull_events()
    assert events == [ReservationConfirmed("R001", "M001", "RM001", TimeSlot("09:00"))]


def test_t5_br5_no_event_when_confirmation_is_rejected(reservation):
    reservation.confirm()
    reservation.pull_events()
    with pytest.raises(InvalidReservationStateError):
        reservation.confirm()
    assert reservation.pull_events() == []


def test_t5_br5_handler_reserves_the_slot(room):
    rooms = InMemoryRoomRepository()
    rooms.save(room)
    ReservationConfirmedHandler(rooms)(ReservationConfirmed("R001", "M001", "RM001", TimeSlot("09:00")))
    assert rooms.get_by_id("RM001").slot_status(TimeSlot("09:00")) is SlotStatus.RESERVED
