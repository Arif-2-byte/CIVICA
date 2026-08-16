from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette import status


# ==========================================================
# Exception Handlers
# ==========================================================

async def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException,
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
        },
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "message": "Validation Error",
            "errors": exc.errors(),
        },
    )


async def generic_exception_handler(
    request: Request,
    exc: Exception,
):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "message": "Internal Server Error",
        },
    )


# ==========================================================
# Custom Exceptions
# ==========================================================

class CivicaException(HTTPException):
    """
    Base exception for all CIVICA-specific exceptions.
    """

    def __init__(
        self,
        status_code: int,
        message: str,
    ):
        super().__init__(
            status_code=status_code,
            detail=message,
        )


class BadRequestException(CivicaException):

    def __init__(self, message="Bad request."):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            message,
        )


class UnauthorizedException(CivicaException):

    def __init__(self, message="Unauthorized."):
        super().__init__(
            status.HTTP_401_UNAUTHORIZED,
            message,
        )


class ForbiddenException(CivicaException):

    def __init__(self, message="Permission denied."):
        super().__init__(
            status.HTTP_403_FORBIDDEN,
            message,
        )


class NotFoundException(CivicaException):

    def __init__(self, resource="Resource"):
        super().__init__(
            status.HTTP_404_NOT_FOUND,
            f"{resource} not found.",
        )


class ConflictException(CivicaException):

    def __init__(self, message="Resource already exists."):
        super().__init__(
            status.HTTP_409_CONFLICT,
            message,
        )


class ValidationException(CivicaException):

    def __init__(self, message="Validation failed."):
        super().__init__(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            message,
        )


class InternalServerException(CivicaException):

    def __init__(self, message="Internal server error."):
        super().__init__(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            message,
        )