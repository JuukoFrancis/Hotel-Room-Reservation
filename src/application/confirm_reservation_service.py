"""Main use case. Coordinates only - every business rule lives in the Domain."""
from datetime import datetime
from typing import Callable

from src.application.dtos import ConfirmReservationInput, ConfirmReservationOutput
from src.application.event_dispatcher import EventDispatcher
from src.application.repositories import ReservationRepository, RoomRepository
from src.domain.eligibility_service import ReservationEligibilityService
from src.domain.errors import DomainError, ReservationNotFoundError, RoomNotFoundError


class ConfirmReservationService:
    def __init__(self, reservations: ReservationRepository, rooms: RoomRepository,
                 eligibility: ReservationEligibilityService, dispatcher: EventDispatcher,
                 clock: Callable[[], datetime]):
        self._reservations = reservations      # all collaborators injected from outside
        self._rooms = rooms
        self._eligibility = eligibility
        self._dispatcher = dispatcher
        self._clock = clock

    def execute(self, request: ConfirmReservationInput) -> ConfirmReservationOutput:
        original_status = None
        try:
            reservation = self._reservations.get_by_id(request.reservation_id)      # BR6
            if reservation is None:
                raise ReservationNotFoundError(f"Reservation {request.reservation_id} not found")
            original_status = reservation.status.value
            room = self._rooms.get_by_id(reservation.room_id)
            if room is None:
                raise RoomNotFoundError(f"Room {reservation.room_id} not found")
            self._eligibility.check(reservation, room, self._clock())               # BR4
            reservation.confirm()                                                   # BR2
            for event in reservation.pull_events():
                self._dispatcher.dispatch(event)                                    # BR5 -> Room (BR3)
            self._reservations.save(reservation)       # reached only if Room accepted
        except DomainError as error:
            return ConfirmReservationOutput(request.reservation_id, original_status, False,
                                            str(error), type(error).__name__)
        return ConfirmReservationOutput(reservation.reservation_id, reservation.status.value, True,
                                        "Reservation confirmed and slot reserved")
