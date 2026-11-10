"""Aggregate A - Reservation (BR2). Raises ReservationConfirmed (BR5)."""
from enum import Enum

from src.domain.errors import InvalidReservationStateError
from src.domain.events import DomainEvent, ReservationConfirmed
from src.domain.time_slot import TimeSlot


class ReservationStatus(Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"


class Reservation:
    def __init__(self, reservation_id: str, member_id: str, room_id: str,
                 time_slot: TimeSlot, status: ReservationStatus = ReservationStatus.PENDING):
        self.reservation_id = reservation_id      # identity (BR2)
        self.member_id = member_id
        self.room_id = room_id
        self.time_slot = time_slot                # Value Object (BR1)
        self.status = status
        self._events: list[DomainEvent] = []

    def confirm(self) -> None:
        """BR2: only a PENDING reservation may become CONFIRMED."""
        if self.status is not ReservationStatus.PENDING:
            raise InvalidReservationStateError(
                f"Reservation {self.reservation_id} is {self.status.value}; only PENDING can be confirmed")
        self.status = ReservationStatus.CONFIRMED
        self._events.append(ReservationConfirmed(
            self.reservation_id, self.member_id, self.room_id, self.time_slot))

    def pull_events(self) -> list[DomainEvent]:
        events, self._events = self._events, []
        return events
