from typing import Generic, TypeVar, List
from pydantic import BaseModel, Field
from math import ceil

T = TypeVar("T")

# ---------- Response models ----------
class PageMeta(BaseModel):
    page: int
    per_page: int
    total: int
    pages: int
    has_next: bool
    has_prev: bool

class Page(BaseModel, Generic[T]):
    items: List[T]
    meta: PageMeta

# ---------- Query params helper ----------
class PaginationParams(BaseModel):
    page: int = Field(1, ge=1)
    per_page: int = Field(20, ge=1, le=100)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.per_page

    def build_meta(self, total: int) -> PageMeta:
        pages = max(1, ceil(total / self.per_page)) if total else 1
        return PageMeta(
            page=self.page,
            per_page=self.per_page,
            total=total,
            pages=pages,
            has_next=self.page < pages,
            has_prev=self.page > 1,
        )