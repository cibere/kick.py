from typing_extensions import TypedDict


class InnerCategory(TypedDict):
    id: int
    name: str
    slug: str
    icon: str


class Category(TypedDict):
    id: int
    category_id: int
    name: str
    slug: str
    tags: list[str]
    description: str | None
    deleted_at: None  # NEED TO FIGURE THIS OUT
    category: InnerCategory
