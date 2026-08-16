from typing import Generic, Optional, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    """
    Standard API response for all successful requests.
    """

    success: bool = Field(
        default=True,
        description="Indicates whether the request was successful.",
    )

    message: str = Field(
        default="Request completed successfully.",
        description="Human-readable response message.",
    )

    data: Optional[T] = Field(
        default=None,
        description="Response payload.",
    )


class ErrorResponse(BaseModel):
    """
    Standard API response for errors.
    """

    success: bool = Field(
        default=False,
        description="Indicates whether the request failed.",
    )

    message: str = Field(
        ...,
        description="Error message.",
    )

    errors: Optional[dict] = Field(
        default=None,
        description="Additional validation or error details.",
    )


class PaginatedResponse(BaseModel, Generic[T]):
    """
    Standard paginated API response.
    """

    success: bool = True

    message: str = "Request completed successfully."

    items: list[T]

    total: int

    page: int

    page_size: int

    total_pages: int