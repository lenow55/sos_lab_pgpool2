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


class RefreshSessionData(BaseModel):
    user_id: uuid.UUID
    username: Optional[str] = None
    refresh_id: uuid.UUID
    fingerpring: Optional[str] = None
    ip: Optional[str] = None
    expires_at: int
    created_at: datetime

class TaskOut(BaseModel):
    id: uuid.UUID

class TaskIn(BaseModel):
    cost: int
    percent_write: int
    count_connections: int
    cache_enabled: bool
    base_in_cache: bool

    @field_serializer('cache_enabled')
    def serialize_qcache(self, cache_enabled: bool, _info) -> int:
        return int(cache_enabled)

    @field_serializer('base_in_cache')
    def serialize_cache(self, base_in_cache: bool, _info) -> int:
        return int(base_in_cache)
