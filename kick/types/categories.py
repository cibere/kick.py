from typing import List, TypedDict

class BaseCategoryFields(TypedDict):
    """Base fields shared between category types"""
    id: str
    name: str
    slug: str
    description: str | None


class InnerCategory(TypedDict):
    """Inner category data from regular API"""
    id: int
    name: str 
    slug: str
    icon: str


class Category(BaseCategoryFields):
    """Full category from regular API"""
    category_id: int
    tags: List[str]
    deleted_at: None  # TODO: Determine proper type
    category: InnerCategory


class CategorySearchDocument(BaseCategoryFields):
    """Category data from search API"""
    category_id: int
    is_live: bool
    is_mature: bool
    parent: str
    src: str
    srcset: str


class CategorySearchHighlight(TypedDict):
    """Search highlight information"""
    field: str
    matched_tokens: List[str]
    snippet: str


class CategorySearchHit(TypedDict):
    """Individual search result"""
    document: CategorySearchDocument
    highlight: dict
    highlights: List[CategorySearchHighlight]
    text_match: int
    text_match_info: dict


class CategorySearchResponse(TypedDict):
    """Full search response"""
    facet_counts: List[str]
    found: int
    hits: List[CategorySearchHit]
    out_of: int
    page: int
    request_params: dict
    search_cutoff: bool
    search_time_ms: int
