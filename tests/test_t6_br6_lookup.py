"""T6 - BR6: the reservation must be retrieved from the repository before confirmation."""
from src.application.dtos import ConfirmReservationInput


def test_t6_br6_missing_reservation_is_rejected(world):
    service, _, _ = world
    out = service.execute(ConfirmReservationInput("R999"))
    assert out.success is False
    assert out.error == "ReservationNotFoundError"


def test_t6_br6_existing_reservation_proceeds(world):
    service, _, _ = world
    assert service.execute(ConfirmReservationInput("R001")).success is True


def test_t6_br6_repository_returns_none_for_unknown_id(world):
    _, reservations, rooms = world
    assert reservations.get_by_id("nope") is None
    assert rooms.get_by_id("nope") is None
