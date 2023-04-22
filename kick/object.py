from typing import Generic, TypeVar

DataT = TypeVar("DataT")

__all__ = ("BaseDataclass",)


class BaseDataclass(Generic[DataT]):
    def __init__(self, *, data: DataT) -> None:
        self.__data = data

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"
