from __future__ import annotations

from typing import TYPE_CHECKING

from .assets import Asset
from .object import HTTPDataclass, BaseDataclass
from .utils import cached_property

if TYPE_CHECKING:
    from .types.categories import (
        Category as CategoryPayload,
        InnerCategory as ParentCategoryPayload,
        CategoryDocument,
        CategorySearchResponse,
        TextHighlight as TextHighlightPayload,
        SearchHighlight as SearchHighlightPayload,
        TextMatchInfo as TextMatchInfoPayload,
        CategorySearchHit as CategorySearchHitPayload,
    )

__all__ = ("Category", "ParentCategory", "SearchCategory",
           "CategorySearchResult", "TextHighlight", "SearchHighlight",
           "TextMatchInfo", "CategorySearchHit")


class TextHighlight(BaseDataclass["TextHighlightPayload"]):
    """
    A dataclass representing text highlighting information

    Attributes
    -----------
    matched_tokens: list[str]
        List of tokens that matched
    snippet: str
        The highlighted text snippet
    """

    @property
    def matched_tokens(self) -> list[str]:
        return self._data["matched_tokens"]

    @property
    def snippet(self) -> str:
        return self._data["snippet"]

    def __repr__(self) -> str:
        return f"<TextHighlight matched_tokens={self.matched_tokens!r} snippet={self.snippet!r}>"


class SearchHighlight(BaseDataclass["SearchHighlightPayload"]):
    """
    A dataclass representing search highlight information

    Attributes
    -----------
    field: str
        The field that was highlighted
    matched_tokens: list[str]
        List of tokens that matched
    snippet: str
        The highlighted text snippet
    """

    @property
    def field(self) -> str:
        return self._data["field"]

    @property
    def matched_tokens(self) -> list[str]:
        return self._data["matched_tokens"]

    @property
    def snippet(self) -> str:
        return self._data["snippet"]

    def __repr__(self) -> str:
        return f"<SearchHighlight field={self.field!r} matched_tokens={self.matched_tokens!r} snippet={self.snippet!r}>"


class TextMatchInfo(BaseDataclass["TextMatchInfoPayload"]):
    """
    A dataclass representing text match scoring information

    Attributes
    -----------
    best_field_score: str
        Score of the best matching field
    best_field_weight: int
        Weight of the best matching field
    fields_matched: int
        Number of fields that matched
    num_tokens_dropped: int
        Number of tokens that were dropped
    score: str
        Overall match score
    tokens_matched: int
        Number of tokens that matched
    typo_prefix_score: int
        Score for typo/prefix matches
    """

    @property
    def best_field_score(self) -> str:
        return self._data["best_field_score"]

    @property
    def best_field_weight(self) -> int:
        return self._data["best_field_weight"]

    @property
    def fields_matched(self) -> int:
        return self._data["fields_matched"]

    @property
    def num_tokens_dropped(self) -> int:
        return self._data["num_tokens_dropped"]

    @property
    def score(self) -> str:
        return self._data["score"]

    @property
    def tokens_matched(self) -> int:
        return self._data["tokens_matched"]

    @property
    def typo_prefix_score(self) -> int:
        return self._data["typo_prefix_score"]

    def __repr__(self) -> str:
        return f"<TextMatchInfo score={self.score!r} tokens_matched={self.tokens_matched} fields_matched={self.fields_matched}>"


class CategorySearchHit(BaseDataclass["CategorySearchHitPayload"]):
    """
    A dataclass representing a category search hit result

    Attributes
    -----------
    document: SearchCategory
        The matching category document
    highlight: dict[str, TextHighlight]
        Highlights for each field
    highlights: list[SearchHighlight]
        List of all highlights
    text_match: int
        Text match score
    text_match_info: TextMatchInfo
        Detailed text match information
    """

    @cached_property
    def document(self) -> SearchCategory:
        return SearchCategory(data=self._data["document"])

    @cached_property
    def highlight(self) -> dict[str, TextHighlight]:
        return {k: TextHighlight(data=v) for k, v in self._data["highlight"].items()}

    @cached_property
    def highlights(self) -> list[SearchHighlight]:
        return [SearchHighlight(data=h) for h in self._data["highlights"]]

    @property
    def text_match(self) -> int:
        return self._data["text_match"]

    @cached_property
    def text_match_info(self) -> TextMatchInfo:
        return TextMatchInfo(data=self._data["text_match_info"])

    def __repr__(self) -> str:
        return f"<CategorySearchHit document={self.document!r} text_match={self.text_match}>"


class ParentCategory(HTTPDataclass["ParentCategoryPayload"]):
    """
    A dataclass which represents one of kick's main categories

    Attributes
    -----------
    id: int
        The categorie's ID
    name: str
        The categorie's name
    slug: str
        The categorie's slug
    icon: `Asset`
        The categorie's icon
    """

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

    @cached_property
    def icon(self) -> Asset:
        """
        The categorie's icon
        """

        return Asset(url=self._data["icon"], http=self.http)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and other.id == self.id

    def __repr__(self) -> str:
        return f"<ParentCategory id={self.id!r} name={self.name!r} icon={self.icon!r}>"

class SearchCategory(BaseDataclass["CategoryDocument"]):
    """
    A dataclass which represents a searchable category on kick

    Attributes
    -----------
    category_id: int
        The category's ID
    name: str
        The category's name
    slug: str
        The category's slug
    description: str
        The category's description
    is_live: bool
        Whether the category is live
    is_mature: bool
        Whether the category is marked as mature
    src: str
        The category's banner image URL
    srcset: str
        The category's responsive image srcset
    """

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
    def description(self) -> str:
        return self._data["description"]

    @property
    def is_live(self) -> bool:
        return self._data["is_live"]

    @property
    def is_mature(self) -> bool:
        return self._data["is_mature"]

    @property
    def src(self) -> str:
        return self._data["src"]

    @property
    def srcset(self) -> str:
        return self._data["srcset"]

    def __repr__(self) -> str:
        return f"<SearchCategory name={self.name!r} slug={self.slug!r} is_live={self.is_live}>"


class CategorySearchResult(BaseDataclass["CategorySearchResponse"]):
    """
    A dataclass which represents a category search response

    Attributes
    -----------
    found: int
        Total number of results found
    hits: list[SearchCategory]
        List of matching categories
    page: int
        Current page number
    """

    @property
    def found(self) -> int:
        return self._data["found"]

    @property
    def page(self) -> int:
        return self._data["page"]

    @cached_property
    def hits(self) -> list[CategorySearchHit]:
        return [CategorySearchHit(data=hit) for hit in self._data["hits"]]

    def __repr__(self) -> str:
        return f"<CategorySearchResult found={self.found} page={self.page} hits={len(self.hits)}>"



class Category(HTTPDataclass["CategoryPayload"]):
    """
    A dataclass which represents one of kick's sub categories

    Attributes
    -----------
    id: int
        The categorie's ID?
    category_id: str
        The categorie's ID?
    slug: str
        The categorie's slug
    name: str
        The categorie's name
    tags: list[str]
        A list of the categorie's tags
    description: str | None
        The categorie's description, if any
    parent: `ParentCategory`
        The categorie's parent category.
    """

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

    @cached_property
    def parent(self) -> ParentCategory:
        """
        The categorie's parent category.
        """

        return ParentCategory(data=self._data["category"], http=self.http)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and other.id == self.id

    def __repr__(self) -> str:
        return f"<Category id={self.id!r} name={self.name!r} category_id={self.category_id!r}> tags={self.tags!r} description={self.description!r} parent={self.parent!r}"
