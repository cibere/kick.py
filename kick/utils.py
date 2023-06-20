from __future__ import annotations

from functools import wraps
from typing import TYPE_CHECKING, Any, Callable, Type


def _cached_property(func: Callable):
    @wraps(func)
    def getter(parent: Type):
        cache = getattr(parent, "__cached_properties", {})
        if func.__name__ not in cache.keys():
            cache[func.__name__] = func(parent)
            parent.__cached_properties = cache
        return parent.__cached_properties[func.__name__]

    return property(getter)


if TYPE_CHECKING:
    from functools import cached_property as cached_property
else:
    cached_property = _cached_property

__all__ = ("MISSING", "cached_property")


class _MissingSentinel:
    __slots__ = ()

    def __eq__(self, other) -> bool:
        return False

    def __bool__(self) -> bool:
        return False

    def __hash__(self) -> int:
        return 0

    def __repr__(self):
        return "..."


MISSING: Any = _MissingSentinel()
