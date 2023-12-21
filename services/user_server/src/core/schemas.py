from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel
import uuid

class HealthCheck(BaseModel):
    name: str
    version: str
    description: str

class Status(BaseModel):
    message: str

# -------------- token --------------

class TokenType(Enum):
    ACCESS = "access"
    REFRESH = "refresh"

class Token(BaseModel):
    token: str
    token_type: str


class TokenData(BaseModel):
    user_id: uuid.UUID
    token_type: TokenType
    exp: datetime
    username: Optional[str] = None


class TokenBlacklistBase(BaseModel):
    token: str
    expires_at: datetime


class TokenBlacklistCreate(TokenBlacklistBase):
    pass


class TokenBlacklistUpdate(TokenBlacklistBase):
    pass
