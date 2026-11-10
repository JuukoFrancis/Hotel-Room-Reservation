"""Entry point + composition root. Usage: python -m src.interface.cli R001"""
import sys
from datetime import datetime, timedelta

from src.application.confirm_reservation_service import ConfirmReservationService
from src.application.dtos import ConfirmReservationInput
from src.application.event_dispatcher import EventDispatcher
from src.application.handlers import ReservationConfirmedHandler
from src.domain.eligibility_service import ReservationEligibilityService
from src.domain.events import ReservationConfirmed
from src.domain.reservation import Reservation
from src.domain.room import Room
from src.domain.time_slot import TimeSlot
from src.infrastructure.in_memory_repositories import (InMemoryReservationRepository,
                                                       InMemoryRoomRepository)


def build_service(now=datetime.now):
    reservations = InMemoryReservationRepository()
    rooms = InMemoryRoomRepository()
    # demo data
    rooms.save(Room.create("RM001", now() + timedelta(days=1)))
    reservations.save(Reservation("R001", "M001", "RM001", TimeSlot("09:00")))
    # dependency injection
    dispatcher = EventDispatcher()
    dispatcher.register(ReservationConfirmed, ReservationConfirmedHandler(rooms))
    return ConfirmReservationService(reservations, rooms, ReservationEligibilityService(), dispatcher, now)


def main(argv=None) -> None:
    argv = sys.argv[1:] if argv is None else argv
    reservation_id = argv[0] if argv else "R001"
    out = build_service().execute(ConfirmReservationInput(reservation_id))
    print(f"{out.reservation_id}: {out.status} - {out.message}")


if __name__ == "__main__":
    main()
