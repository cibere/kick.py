from typing import Any, Optional
from typing_extensions import TypedDict

class InnerCategory(TypedDict):
    id: int
    name: str
    slug: str
    icon: str

class CategoryDocument(TypedDict):
    category_id: int
    description: str
    id: str
    is_live: bool
    is_mature: bool
    name: str
    parent: str
    slug: str
    src: str
    srcset: str

class TextHighlight(TypedDict):
    matched_tokens: list[str]
    snippet: str

class SearchHighlight(TypedDict):
    field: str
    matched_tokens: list[str]
    snippet: str

class TextMatchInfo(TypedDict):
    best_field_score: str
    best_field_weight: int
    fields_matched: int
    num_tokens_dropped: int
    score: str
    tokens_matched: int
    typo_prefix_score: int

class CategorySearchHit(TypedDict):
    document: CategoryDocument
    highlight: dict[str, TextHighlight]
    highlights: list[SearchHighlight]
    text_match: int
    text_match_info: TextMatchInfo

class CategorySearchResponse(TypedDict):
    facet_counts: list[Any]
    found: int
    hits: list[CategorySearchHit]
    out_of: int
    page: int
    request_params: dict[str, Any]
    search_cutoff: bool
    search_time_ms: int

class Category(TypedDict):
    id: int
    category_id: int
    name: str
    slug: str
    tags: list[str]
    description: Optional[str]
    deleted_at: None
    category: InnerCategory
