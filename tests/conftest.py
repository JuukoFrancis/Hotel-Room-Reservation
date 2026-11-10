"""Shared fixtures. The service is wired exactly like the CLI: dependencies injected from outside."""
from datetime import datetime

import pytest

from src.application.confirm_reservation_service import ConfirmReservationService
from src.application.event_dispatcher import EventDispatcher
from src.application.handlers import ReservationConfirmedHandler
from src.domain.eligibility_service import ReservationEligibilityService
from src.domain.events import ReservationConfirmed
from src.domain.reservation import Reservation
from src.domain.room import Room
from src.domain.time_slot import TimeSlot
from src.infrastructure.in_memory_repositories import (InMemoryReservationRepository,
                                                       InMemoryRoomRepository)

NOW = datetime(2026, 11, 10, 9, 0)          # fixed clock
FUTURE = datetime(2026, 11, 11, 8, 0)       # room day starts tomorrow


@pytest.fixture
def now():
    return NOW


@pytest.fixture
def room():
    return Room.create("RM001", FUTURE)


@pytest.fixture
def reservation():
    return Reservation("R001", "M001", "RM001", TimeSlot("09:00"))


@pytest.fixture
def world(room, reservation):
    reservations, rooms = InMemoryReservationRepository(), InMemoryRoomRepository()
    reservations.save(reservation)
    rooms.save(room)
    dispatcher = EventDispatcher()
    dispatcher.register(ReservationConfirmed, ReservationConfirmedHandler(rooms))
    service = ConfirmReservationService(reservations, rooms, ReservationEligibilityService(),
                                        dispatcher, lambda: NOW)
    return service, reservations, rooms
