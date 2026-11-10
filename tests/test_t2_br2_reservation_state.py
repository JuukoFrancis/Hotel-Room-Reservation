"""T2 - BR2: a Reservation starts PENDING; only PENDING may become CONFIRMED."""
import pytest

from src.domain.errors import InvalidReservationStateError
from src.domain.reservation import ReservationStatus


def test_t2_br2_new_reservation_is_pending(reservation):
    assert reservation.status is ReservationStatus.PENDING


def test_t2_br2_pending_can_be_confirmed(reservation):
    reservation.confirm()
    assert reservation.status is ReservationStatus.CONFIRMED


def test_t2_br2_confirming_twice_is_rejected(reservation):
    reservation.confirm()
    with pytest.raises(InvalidReservationStateError):
        reservation.confirm()
    assert reservation.status is ReservationStatus.CONFIRMED
