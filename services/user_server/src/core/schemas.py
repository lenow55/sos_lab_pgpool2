from datetime import datetime
from enum import Enum
from typing import Optional
import orjson
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
    token_type: Optional[TokenType]
    exp: Optional[datetime]

    @field_serializer('exp')
    def serialize_dt(self, exp: datetime, _info) -> int:
        return int(exp.timestamp())

class RefreshData(TokenData):
    refresh_id: uuid.UUID

class AccessData(TokenData):
    user_id: uuid.UUID
    username: Optional[str] = None


class TokenBlacklistBase(BaseModel):
    token: str
    expires_at: datetime

def orjson_dumps(v, *, default):
    # orjson.dumps returns bytes, to match standard json.dumps we need to decode
    return orjson.dumps(v, default=default).decode()

class RefreshSessionData(BaseModel):
    user_id: uuid.UUID
    username: Optional[str] = None
    refresh_id: uuid.UUID
    fingerpring: Optional[str] = None
    ip: Optional[str] = None
    expires_at: int
    created_at: datetime

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
