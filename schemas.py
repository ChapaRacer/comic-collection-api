from pydantic import BaseModel, ConfigDict, EmailStr
from uuid import UUID

# ============================
# COMICS AND MANGA SCHEME
# ============================

class ComicBase(BaseModel):
    title: str
    publisher: str
    volume_number: int

class ComicCreate(ComicBase):
    pass

class ComicResponse(ComicBase):
    id: int
    user_id: UUID
    model_config = ConfigDict(from_attributes=True)

# ============
# USER SCHEME
# ============

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    role: str
    model_config = ConfigDict(from_attributes=True)