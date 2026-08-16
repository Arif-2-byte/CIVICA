from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ==========================================================
# User Registration
# ==========================================================

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    full_name: str
    password: str = Field(min_length=8)
    exams: list[str]


class UserLogin(BaseModel):
    username: str
    password: str


# ==========================================================
# User Response
# ==========================================================

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: str | None
    exams: str
    role: str
    is_active: bool
    is_verified: bool
    is_premium: bool

    model_config = ConfigDict(
        from_attributes=True,
    )


# ==========================================================
# Admin Update Schemas
# ==========================================================

class UserRoleUpdate(BaseModel):
    role: str = Field(
        pattern="^(student|faculty|admin)$"
    )


class UserStatusUpdate(BaseModel):
    is_active: bool


class UserPremiumUpdate(BaseModel):
    is_premium: bool