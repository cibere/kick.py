
from __future__ import annotations

from typing import TYPE_CHECKING, List

from .object import BaseDataclass

if TYPE_CHECKING:
    from .types.categories import Category as CategoryPayload
    from .types.categories import InnerCategory, CategorySearchResponse, CategorySearchHit

__all__ = ("Category", "CategorySearch")


class Category(BaseDataclass["CategoryPayload"]):
    """
    A dataclass which represents a Category on kick

    Attributes
    -----------
    id: int
        The category's id
    name: str
        The category's name
    slug: str
        The category's slug
    description: str | None
        The category's description if any
    category_id: int
        The category's internal ID
    tags: List[str]
        List of tags associated with the category
    inner_category: InnerCategory
        The inner category data containing id, name, slug and icon
    """

    def __init__(self, *, data: CategoryPayload) -> None:
        super().__init__(data=data)

    @property
    def id(self) -> int:
        return self._data["id"] if isinstance(self._data["id"], int) else int(self._data["id"])

    @property
    def name(self) -> str:
        return self._data["name"]

    @property
    def slug(self) -> str:
        return self._data["slug"]

    @property
    def description(self) -> str | None:
        return self._data.get("description")

    @property
    def category_id(self) -> int:
        return self._data["category_id"]

    @property
    def tags(self) -> List[str]:
        return self._data.get("tags", [])

    @property
    def inner_category(self) -> InnerCategory:
        return self._data["category"]

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"<Category id={self.id!r} name={self.name!r}>"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Category) and other.id == self.id


class CategorySearch(BaseDataclass["CategorySearchResponse"]):
    """
    A dataclass which represents a Category Search Response from kick

    Attributes
    -----------
    facet_counts: List[str]
        The facet counts from the search
    found: int
        Number of results found
    hits: List[CategorySearchHit]
        The search results
    out_of: int
        Total number of results available
    page: int
        Current page number
    search_cutoff: bool
        Whether the search was cut off
    search_time_ms: int
        Time taken for the search in milliseconds
    """

    def __init__(self, *, data: CategorySearchResponse) -> None:
        super().__init__(data=data)

    @property
    def facet_counts(self) -> List[str]:
        return self._data["facet_counts"]

    @property
    def found(self) -> int:
        return self._data["found"]

    @property
    def hits(self) -> List[CategorySearchHit]:
        return self._data["hits"]

    @property
    def out_of(self) -> int:
        return self._data["out_of"]

    @property
    def page(self) -> int:
        return self._data["page"]

    @property
    def search_cutoff(self) -> bool:
        return self._data["search_cutoff"]

    @property
    def search_time_ms(self) -> int:
        return self._data["search_time_ms"]

    def __repr__(self) -> str:
        return f"<CategorySearch found={self.found!r} page={self.page!r}>"
