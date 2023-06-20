from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .object import BaseDataclass
from .utils import cached_property

if TYPE_CHECKING:
    from .types.user import Category as CategoryPayload
    from .types.user import InnerCategory as ParentCategoryPayload

__all__ = ("Category", "ParentCategory")


class ParentCategory(BaseDataclass["ParentCategoryPayload"]):
    @property
    def id(self) -> int:
        return self._data["id"]

    @property
    def name(self) -> str:
        return self._data["name"]

    @property
    def slug(self) -> str:
        return self._data["slug"]

    @property
    def icon(self) -> str:
        return self._data["icon"]


class Category(BaseDataclass["CategoryPayload"]):
    @property
    def id(self) -> int:
        return self._data["id"]

    @property
    def category_id(self) -> int:
        return self._data["category_id"]

    @property
    def name(self) -> str:
        return self._data["name"]

    @property
    def slug(self) -> str:
        return self._data["slug"]

    @property
    def tags(self) -> list[str]:
        return self._data["tags"]

    @property
    def description(self) -> str | None:
        return self._data["description"]

    @property
    def deleted_at(self) -> Any:
        """THIS IS RAW DATA, UNKNOWN ON WHAT IT RETURNS"""
        return self._data["deleted_at"]

    @cached_property
    def parent(self) -> ParentCategory:
        return ParentCategory(data=self._data["category"])
