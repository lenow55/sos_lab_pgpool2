from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, field_serializer
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
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: uuid.UUID
    token_type: Optional[TokenType]
    exp: Optional[datetime]
    username: Optional[str] = None

    @field_serializer('exp')
    def serialize_dt(self, exp: datetime, _info):
        return int(exp.timestamp())


class TokenBlacklistBase(BaseModel):
    token: str
    expires_at: datetime


class TokenBlacklistCreate(TokenBlacklistBase):
    pass


class TokenBlacklistUpdate(TokenBlacklistBase):
    pass
