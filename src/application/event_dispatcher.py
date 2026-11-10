"""Simple in-process event delivery."""
from collections import defaultdict
from typing import Callable

from src.domain.events import DomainEvent


class EventDispatcher:
    def __init__(self):
        self._handlers: dict[type, list[Callable]] = defaultdict(list)

    def register(self, event_type: type, handler: Callable) -> None:
        self._handlers[event_type].append(handler)

    def dispatch(self, event: DomainEvent) -> None:
        for handler in self._handlers[type(event)]:
            handler(event)
