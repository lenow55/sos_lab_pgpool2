from typing import Annotated, ClassVar, Optional
from pydantic import BaseModel, ConfigDict, Field, EmailStr
from schemas import PersistentDeletion, TimestampSchema, UUIDSchema


class UserBase(BaseModel):
    full_name: Annotated[
        str,
        Field(
            min_length=2, max_length=50,
            examples=[
                "Иванов Иван Иванович"]
        )
    ]
    username: Annotated[
        str,
        Field(
            min_length=2, max_length=20,
            pattern=r"^[a-z0-9]+$",
            examples=[
                "username"]
        )
    ]
    email: Annotated[
        EmailStr,
        Field(
            examples=["user@example.com"],
            max_length=50,
        )
    ]


class User(
        TimestampSchema, UserBase, UUIDSchema,
        PersistentDeletion):
    hashed_password: str


class UserRead(UserBase):
    model_config: ClassVar[ConfigDict] = ConfigDict(
        extra='forbid')


class UserCreate(UserBase):
    model_config: ClassVar[ConfigDict] = ConfigDict(
        extra='forbid')

    password: Annotated[
        str,
        Field(
            pattern=r"^.{8,}|[0-9]+|[A-Z]+|[a-z]+|[^a-zA-Z0-9]+$",
            examples=["Str1ngst!"]
        )
    ]


class UserCreateInternal(UserBase):
    hashed_password: str


class UserUpdate(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(
        extra='forbid')

    full_name: Annotated[
        Optional[str],
        Field(
            min_length=2,
            max_length=50,
            examples=["Иванов Иван Иванович"],
            default=None
        )
    ]
    username: Annotated[
        Optional[str],
        Field(
            min_length=2,
            max_length=20,
            pattern=r"^[a-z0-9]+$",
            examples=["username"],
            default=None
        )
    ]
    email: Annotated[
        Optional[EmailStr],
        Field(
            min_length=2,
            max_length=50,
            examples=["user@example.com"],
            default=None
        )
    ]
