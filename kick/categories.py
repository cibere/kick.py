from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .object import BaseDataclass
from .utils import cached_property

if TYPE_CHECKING:
    from .types.categories import Category as CategoryPayload
    from .types.categories import InnerCategory as ParentCategoryPayload

__all__ = ("Category", "ParentCategory")


class ParentCategory(BaseDataclass["ParentCategoryPayload"]):
    @property
    def id(self) -> int:
        """
        The categorie's ID
        """

        return self._data["id"]

    @property
    def name(self) -> str:
        """
        The categorie's name
        """

        return self._data["name"]

    @property
    def slug(self) -> str:
        """
        The categorie's slug
        """

        return self._data["slug"]

    @property
    def icon(self) -> str:
        """
        The categorie's icon url
        """

        return self._data["icon"]

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, ParentCategory) and other.id == self.id


class Category(BaseDataclass["CategoryPayload"]):
    @property
    def id(self) -> int:
        """
        The categorie's ID?

        Unknown on the difference between this and `Category.category_id`
        """

        return self._data["id"]

    @property
    def category_id(self) -> int:
        """
        The categorie's ID?

        Unknown on the difference between this and `Category.id`
        """

        return self._data["category_id"]

    @property
    def name(self) -> str:
        """
        The categorie's name
        """

        return self._data["name"]

    @property
    def slug(self) -> str:
        """
        The categorie's slug
        """

        return self._data["slug"]

    @property
    def tags(self) -> list[str]:
        """
        A list of the categorie's tags
        """

        return self._data["tags"]

    @property
    def description(self) -> str | None:
        """
        The categorie's description, if any
        """

        return self._data["description"]

    @property
    def deleted_at(self) -> Any:
        """THIS IS RAW DATA, UNKNOWN ON WHAT IT RETURNS"""

        return self._data["deleted_at"]

    @cached_property
    def parent(self) -> ParentCategory:
        """
        The categorie's parent category.
        """

        return ParentCategory(data=self._data["category"])

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, ParentCategory) and other.id == self.id
