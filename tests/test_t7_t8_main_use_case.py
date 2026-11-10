"""T7 / T8 - the connected use cases: Confirm Reservation -> ReservationConfirmed -> Reserve Slot."""
from src.application.dtos import ConfirmReservationInput
from src.domain.reservation import ReservationStatus
from src.domain.room import SlotStatus
from src.domain.time_slot import TimeSlot

NINE = TimeSlot("09:00")


def test_t7_main_use_case_success(world):
    service, reservations, rooms = world
    out = service.execute(ConfirmReservationInput("R001"))
    assert out.success is True
    assert out.status == "CONFIRMED"
    assert out.message == "Reservation confirmed and slot reserved"
    assert reservations.get_by_id("R001").status is ReservationStatus.CONFIRMED     # Aggregate A saved
    room = rooms.get_by_id("RM001")                                                  # event was handled
    assert room.slot_status(NINE) is SlotStatus.RESERVED                             # Aggregate B changed
    assert room.slot_reserved_by(NINE) == "R001"


def test_t8_room_rejects_follow_up_when_slot_already_taken(world):
    service, reservations, rooms = world
    taken = rooms.get_by_id("RM001")
    taken.reserve_slot(NINE, "R999", "M999")            # another reservation already owns 09:00
    rooms.save(taken)

    out = service.execute(ConfirmReservationInput("R001"))

    assert out.success is False                                                      # returned outcome
    assert out.error == "SlotAlreadyReservedError"
    assert out.status == "PENDING"
    assert reservations.get_by_id("R001").status is ReservationStatus.PENDING        # nothing saved
    room = rooms.get_by_id("RM001")
    assert room.slot_reserved_by(NINE) == "R999"                                     # room unchanged
