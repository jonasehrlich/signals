from __future__ import annotations

from collections.abc import Callable
from typing import Any, Generic, TypeVar

T = TypeVar("T")
SourceT = TypeVar("SourceT")
ComputedT = TypeVar("ComputedT")


class Signal(Generic[T]):
    def __init__(self, value: T) -> None:
        self._value = value
        self._is_dirty = False
        self._sinks: set[Signal[Any] | _ComputedSignal[Any, Any]] = set()

    def __str__(self) -> str:
        return str(self.get())

    def get(self) -> T:
        return self._value

    def set(self, value: T) -> None:
        self._is_dirty = True
        self._value = value
        for sink in self._sinks:
            sink.mark_as_dirty()

    def computed(self, func: Callable[[T], ComputedT]) -> _ComputedSignal[T, ComputedT]:
        sink = _ComputedSignal(self, func)
        self._sinks.add(sink)
        return sink

    def mark_as_dirty(self) -> None:
        self._is_dirty = True
        for sink in self._sinks:
            sink.mark_as_dirty()


class _ComputedSignal(Generic[SourceT, T]):
    def __init__(self, source: Signal[SourceT] | _ComputedSignal[Any, SourceT], func: Callable[[SourceT], T]) -> None:
        self._source = source
        self._func = func

        self._value = None
        self._is_dirty = True
        self._sinks: set[Signal[Any] | _ComputedSignal[Any, Any]] = set()

    def __str__(self) -> str:
        return str(self.get())

    def get(self) -> T:
        if self._is_dirty or self._value is None:
            self._value = self._func(self._source.get())
            self._is_dirty = False
        return self._value

    def computed(self, func: Callable[[T], ComputedT]) -> _ComputedSignal[T, ComputedT]:
        return _ComputedSignal(self, func)

    def mark_as_dirty(self) -> None:
        self._is_dirty = True
        for sink in self._sinks:
            sink.mark_as_dirty()
