from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    full_name: str
    password: str = Field(min_length=8)
    exams: list[str]


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: str
    exams: str
    is_active: bool
    is_verified: bool
    is_premium: bool

    class Config:
        from_attributes = True