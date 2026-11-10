"""In-memory repositories. Store and return COPIES, like a real database would,
so a rejected change that was never saved can never leak into the store."""
from copy import deepcopy

from src.application.repositories import ReservationRepository, RoomRepository
from src.domain.reservation import Reservation
from src.domain.room import Room


class InMemoryReservationRepository(ReservationRepository):
    def __init__(self):
        self._store: dict[str, Reservation] = {}

    def get_by_id(self, reservation_id: str) -> Reservation | None:
        found = self._store.get(reservation_id)
        return deepcopy(found) if found else None

    def save(self, reservation: Reservation) -> None:
        self._store[reservation.reservation_id] = deepcopy(reservation)


class InMemoryRoomRepository(RoomRepository):
    def __init__(self):
        self._store: dict[str, Room] = {}

    def get_by_id(self, room_id: str) -> Room | None:
        found = self._store.get(room_id)
        return deepcopy(found) if found else None

    def save(self, room: Room) -> None:
        self._store[room.room_id] = deepcopy(room)
