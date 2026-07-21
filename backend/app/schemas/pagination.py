from math import ceil
from typing import Generic, List, TypeVar

from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar("T")


class PaginatedResponse(GenericModel, Generic[T]):
    items: List[T]

    total: int

    page: int

    page_size: int

    total_pages: int

    @classmethod
    def create(
        cls,
        *,
        items,
        total,
        page,
        page_size,
    ):
        return cls(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=ceil(total / page_size)
            if total
            else 0,
        )