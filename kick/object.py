from __future__ import annotations

from typing import TYPE_CHECKING, Generic, TypeVar

DataT = TypeVar("DataT")

if TYPE_CHECKING:
    from .http import HTTPClient


__all__ = ("BaseDataclass", "HTTPDataclass")


class BaseDataclass(Generic[DataT]):
    def __init__(self, *, data: DataT) -> None:
        self._data = data

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"


class HTTPDataclass(Generic[DataT]):
    def __init__(self, *, data: DataT, http: HTTPClient) -> None:
        self._data = data
        self.http = http

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"
