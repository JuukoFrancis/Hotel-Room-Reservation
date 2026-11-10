"""Repository abstractions (ports) - needed by the use case, so they live in Application."""
from abc import ABC, abstractmethod

from src.domain.reservation import Reservation
from src.domain.room import Room


class ReservationRepository(ABC):
    @abstractmethod
    def get_by_id(self, reservation_id: str) -> Reservation | None: ...

    @abstractmethod
    def save(self, reservation: Reservation) -> None: ...


class RoomRepository(ABC):
    @abstractmethod
    def get_by_id(self, room_id: str) -> Room | None: ...

    @abstractmethod
    def save(self, room: Room) -> None: ...
