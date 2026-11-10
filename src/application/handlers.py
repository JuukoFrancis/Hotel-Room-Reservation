"""BR5 handler: asks Aggregate B (Room) to reserve the slot. Contains no rule itself."""
from src.application.repositories import RoomRepository
from src.domain.errors import RoomNotFoundError
from src.domain.events import ReservationConfirmed


class ReservationConfirmedHandler:
    def __init__(self, room_repository: RoomRepository):
        self._rooms = room_repository

    def __call__(self, event: ReservationConfirmed) -> None:
        room = self._rooms.get_by_id(event.room_id)
        if room is None:
            raise RoomNotFoundError(f"Room {event.room_id} not found")
        room.reserve_slot(event.time_slot, event.reservation_id, event.member_id)   # BR3 enforced by Room
        self._rooms.save(room)
