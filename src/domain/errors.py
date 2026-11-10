"""Domain errors: one per business-rule violation."""


class DomainError(Exception):
    """Base class for every business-rule violation."""


class InvalidTimeSlotError(DomainError):            # BR1
    pass


class InvalidReservationStateError(DomainError):    # BR2
    pass


class SlotAlreadyReservedError(DomainError):        # BR3
    pass


class ReservationNotEligibleError(DomainError):     # BR4
    pass


class ReservationNotFoundError(DomainError):        # BR6
    pass


class RoomNotFoundError(DomainError):               # BR6 (follow-up lookup)
    pass
