"""BR4 - Domain Service: needs the Reservation, the Room and the current time."""
from datetime import datetime

from src.domain.errors import ReservationNotEligibleError
from src.domain.reservation import Reservation
from src.domain.room import Room

MAX_SLOTS_PER_MEMBER = 4


class ReservationEligibilityService:
    """Stateless, no collaborators. Eligible only if the Room's booking day has not
    started AND the member has fewer than 4 confirmed slots in that Room."""

    def check(self, reservation: Reservation, room: Room, current_time: datetime) -> None:
        if room.has_started(current_time):
            raise ReservationNotEligibleError(f"Room {room.room_id} booking day has already started")
        if room.confirmed_slot_count_for(reservation.member_id) >= MAX_SLOTS_PER_MEMBER:
            raise ReservationNotEligibleError(
                f"Member {reservation.member_id} already holds {MAX_SLOTS_PER_MEMBER} slots in this room")
