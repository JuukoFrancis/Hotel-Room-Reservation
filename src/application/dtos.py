from dataclasses import dataclass


@dataclass(frozen=True)
class ConfirmReservationInput:
    reservation_id: str


@dataclass(frozen=True)
class ConfirmReservationOutput:
    reservation_id: str
    status: str | None
    success: bool
    message: str
    error: str | None = None
