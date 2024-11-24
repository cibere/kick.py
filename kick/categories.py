from __future__ import annotations

from typing import TYPE_CHECKING, List, Dict

from .object import BaseDataclass

if TYPE_CHECKING:
    from .types.categories import Category as CategoryPayload
    from .types.categories import (
        InnerCategory, 
        CategorySearchResponse, 
        CategorySearchHit as CategorySearchHitPayload,
        CategorySearchDocument as CategorySearchDocumentPayload,
        CategorySearchHighlight as CategorySearchHighlightPayload
    )

__all__ = ("Category", "CategorySearch", "CategorySearchDocument", "CategorySearchHighlight", "CategorySearchHit")

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
        return [CategorySearchHit(data=hit) for hit in self._data["hits"]]

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


class CategorySearchDocument(BaseDataclass["CategorySearchDocumentPayload"]):
    """
    A dataclass which represents Category data from search API

    Attributes
    id: str
        The category's ID
    name: str
        The category's name
    slug: str
        The category's slug
    description: str
        The category's description
    -----------
    category_id: int
        The category's internal ID
    is_live: bool
        Whether the category is currently live
    is_mature: bool
        Whether the category is marked as mature
    parent: str
        The parent category name
    src: str
        The source URL for category image
    srcset: str
        The source set for responsive images
    """

    def __init__(self, *, data: CategorySearchDocumentPayload) -> None:
        super().__init__(data=data)

    def id(self) -> str:
        return self._data["id"]

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
    def is_live(self) -> bool:
        return self._data["is_live"]

    @property
    def is_mature(self) -> bool:
        return self._data["is_mature"]

    @property
    def parent(self) -> str:
        return self._data["parent"]

    @property
    def src(self) -> str:
        return self._data["src"]

    @property
    def srcset(self) -> str:
        return self._data["srcset"]

    def __repr__(self) -> str:
        return f"<CategorySearchDocument id={self.category_id!r}>"


class CategorySearchHighlight(BaseDataclass["CategorySearchHighlightPayload"]):
    """
    A dataclass which represents search highlight information

    Attributes
    -----------
    field: str
        The field that was matched
    matched_tokens: List[str]
        List of tokens that matched the search
    snippet: str
        A snippet of the matched text
    """

    def __init__(self, *, data: CategorySearchHighlightPayload) -> None:
        super().__init__(data=data)

    @property
    def field(self) -> str:
        return self._data["field"]

    @property
    def matched_tokens(self) -> List[str]:
        return self._data["matched_tokens"]

    @property
    def snippet(self) -> str:
        return self._data["snippet"]

    def __repr__(self) -> str:
        return f"<CategorySearchHighlight field={self.field!r}>"


class CategorySearchHit(BaseDataclass["CategorySearchHitPayload"]):
    """
    A dataclass which represents an individual search result

    Attributes
    -----------
    document: CategorySearchDocument
        The category document data
    highlight: Dict
        Raw highlight information
    highlights: List[CategorySearchHighlight]
        Processed highlight information
    text_match: int
        Text match score
    text_match_info: Dict
        Additional text match information
    """

    def __init__(self, *, data: CategorySearchHitPayload) -> None:
        super().__init__(data=data)

    @property
    def document(self) -> CategorySearchDocument:
        return CategorySearchDocument(data=self._data["document"])

    @property
    def highlight(self) -> Dict:
        return self._data["highlight"]

    @property
    def highlights(self) -> List[CategorySearchHighlight]:
        return [CategorySearchHighlight(data=h) for h in self._data["highlights"]]

    @property
    def text_match(self) -> int:
        return self._data["text_match"]

    @property
    def text_match_info(self) -> Dict:
        return self._data["text_match_info"]

    def __repr__(self) -> str:
        return f"<CategorySearchHit document={self.document!r}>"
