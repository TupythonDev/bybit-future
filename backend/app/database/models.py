from typing import Optional
from enum import Enum
from datetime import timezone, datetime
from uuid import UUID, uuid4
from pydantic import EmailStr, model_validator
from sqlmodel import SQLModel, Field

class UserBase(SQLModel):
    email:EmailStr = Field(unique=True)

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    MODERATOR = "moderator"

class UserAudit(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID
    field_changed: str
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    changed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    changed_by: Optional[UUID] = None

class UserCreate(UserBase):
    password:str

class UserUpdate(SQLModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    bybit_api_key: Optional[str] = None
    bybit_api_secret: Optional[str] = None

    @model_validator(mode="after")
    def check_bybit_fields(self):
        if (self.bybit_api_key and not self.bybit_api_secret) or (self.bybit_api_secret and not self.bybit_api_key):
            raise ValueError("bybit_api_key e bybit_api_secret devem ser enviados juntos.")
        return self

class UserRead(UserBase):
    id:UUID
    created_at:datetime
    updated_at:Optional[datetime] = None

class User(UserBase, table=True):
    id:UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = Field(default=None)
    role: UserRole = Field(default=UserRole.USER)
    password:str

    bybit_api_key: Optional[str] = Field(default=None, unique=True)
    bybit_api_secret: Optional[str] = Field(default=None)
