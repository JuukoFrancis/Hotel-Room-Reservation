"""BR5 - Domain Event. DomainEvent is the Layer Supertype for all events."""
from dataclasses import dataclass

from src.domain.time_slot import TimeSlot


@dataclass(frozen=True)
class DomainEvent:
    """Layer Supertype: every domain event is a DomainEvent."""


@dataclass(frozen=True)
class ReservationConfirmed(DomainEvent):
    reservation_id: str
    member_id: str
    room_id: str
    time_slot: TimeSlot
