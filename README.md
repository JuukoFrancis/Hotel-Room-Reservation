## Hotel Room Reservation

Domain-Driven Design, Test-Driven Development and Clean Architecture.

## Domain

Hotel Room Reservation: a guest (`member_id`) reserves a one-hour time slot in a hotel room (for example a day-use or conference room) for a booking day.

## Project Scope

The project focuses on confirming an existing room reservation and reserving the corresponding time slot in a specific room.

## Main Use Case

Confirm a Room Reservation.

## Connected Follow-Up Use Case

Reserve the corresponding slot in the Room after the Reservation is confirmed.

## Business Rules

BR1 (Value rule) - A TimeSlot is one whole hour written `HH:00`, from 08:00 to 19:00.

BR2 (Identity/state rule) - A Reservation starts as PENDING and may only transition to CONFIRMED from PENDING.

BR3 (Invariant rule) - Within one Room, a RoomSlot may be allocated to at most one Reservation.

BR4 (Cross-concept rule) - A Reservation is eligible only when the Room's booking day has not started and the member holds fewer than four slots in that Room.

BR5 (Follow-up rule) - When a Reservation is confirmed, a `ReservationConfirmed` domain event requests the Room to reserve the TimeSlot.

BR6 (Lookup rule) - A Reservation must already exist before confirmation can proceed.

## Where each business rule lives

| Rule | Enforced by                                                                                                           | Test   |
| ---- | --------------------------------------------------------------------------------------------------------------------- | ------ |
| BR1  | `src/domain/time_slot.py` - `TimeSlot` validates in its own constructor                                               | T1     |
| BR2  | `src/domain/reservation.py` - `Reservation.confirm()`                                                                 | T2     |
| BR3  | `src/domain/room.py` - `Room.reserve_slot()`; `RoomSlot._reserve()` is aggregate-internal                             | T3     |
| BR4  | `src/domain/eligibility_service.py` - `ReservationEligibilityService.check()`                                         | T4     |
| BR5  | `src/domain/events.py`, dispatched by `src/application/event_dispatcher.py`, handled by `src/application/handlers.py` | T5, T7 |
| BR6  | `src/application/confirm_reservation_service.py` - the lookup happens before anything else                            | T6     |

Main use case: T7 (success). Follow-up rejected by the Room: T8.

## Aggregates

- **Reservation (Aggregate A)** - Aggregate Root. Owns BR2 and raises the BR5 event.
- **Room (Aggregate B)** - Aggregate Root. Owns the slot map and BR3.

They are separate aggregates because they have separate lifecycles and separate invariants, and they are not updated in one atomic step here. They never hold a reference to each other: the only thing that crosses the boundary is the BR5 domain event, which carries plain data only.

## Architecture

The project uses four Clean Architecture layers:

- Domain
- Application
- Infrastructure
- Interface

The Domain layer contains the business rules and domain model.

The Application layer coordinates use cases using DTOs, repositories and application services.

The Infrastructure layer provides in-memory repository implementations.

The Interface layer provides a simple CLI entry point.

`python scripts/check_dependencies.py` verifies that no import points outward from a layer, and fails if one does.

```
Interface -> Application -> Domain
Interface -> Infrastructure -> Application -> Domain
```

## Design decisions

**Repository interfaces sit in the Application layer.** They are ports used by use cases rather than part of the domain model, so they are declared where they are used and implemented in Infrastructure. The Domain layer depends on neither, and it is given no repository at all: BR4 is decided from the `Reservation` and `Room` aggregates alone, and `Room.confirmed_slot_count_for()` answers "how many slots does this member hold in this room?" from state the Room already owns.

**Domain Service for BR4.** The rule spans two aggregates plus the current time, so it cannot live inside either one. `ReservationEligibilityService` is therefore a Domain Service, and it is stateless and holds no collaborators.

**Factory for Room.** `Room.create()` builds the entire slot map, because "every hour from 08:00 to 19:00 exists and every slot starts AVAILABLE" is a construction rule rather than something each caller should assemble by hand. No other Factory is needed: a `Reservation` is fully described by its constructor.

**Layer Supertype for events.** `DomainEvent` is the supertype of every domain event, so the dispatcher and any future subscriber program against the abstraction instead of a growing list of concrete event classes.

**Aggregate-internal mutation.** Only the Aggregate Root changes its own entities: `RoomSlot._reserve()` is called only by `Room`, and `Reservation.pull_events()` is the only way to read back the recorded events.

**Failures are returned, not leaked.** The application service catches domain errors and returns `ConfirmReservationOutput(success=False, error=<error name>)`, so callers read one DTO and never need to know domain exceptions.

**Repositories store copies.** The in-memory repositories store and return deep copies, as a database would, so a change rejected by the Room and never saved cannot leak into the stored Reservation (T8).

## Testing

The project uses pytest.

Install requirements:

```bash
pip install -r requirements.txt
```

Run all tests:

```bash
python -m pytest -v
```

Expected: `29 passed` (8 required test ids, T1-T8, in the test names, e.g. `test_t4_br4_...`).

`pytest.ini` puts the project root on `sys.path`, so the tests import `src` whether pytest is started as `pytest` or as `python -m pytest`.

## Running the project

Run the main use case from the command line:

```bash
python -m src.interface.cli R001      # R001: CONFIRMED - Reservation confirmed and slot reserved
python -m src.interface.cli R999      # BR6: Reservation R999 not found
```

Check the layer dependencies:

```bash
python scripts/check_dependencies.py
```

## Evidence

`evidence/` contains the TDD cycle for T1 (BR1) and the full test run:

- `tdd_1_red.txt` - test written first, fails against an empty `TimeSlot`
- `tdd_2_green.txt` - passes after the validation is added
- `tdd_3_refactor.txt` - still passes after the regex/constants refactor
- `test_run_output.txt` - all tests

## AI Usage Statement

AI tool used: CHATGPT - helped with brainstorming and code assistance. We remained responsible for the final design, implementation and testing of the project.
