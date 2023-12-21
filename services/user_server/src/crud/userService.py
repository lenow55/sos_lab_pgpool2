from tortoise.contrib.pydantic.base import PydanticModel
from tortoise.query_utils import Prefetch
from src.api.paginated import ListResponse
from src.exceptions.http_exceptions import DuplicateValueException, CustomException, NotFoundException
from tortoise.exceptions import DoesNotExist, IntegrityError
from src.database.models import BaseConfig, User
import src.schemas.user as schemas
import uuid as uuid_pkg

import logging
from src.core import logger as logger_mod
from src.core.schemas import Status
logger = logging.getLogger(__name__)

logger.debug("Debug Message")


class UserService():
    async def create_user(self, user_in_obj: schemas.UserCreateInternal) -> schemas.User:
        try:
            user_obj = await User.create(**user_in_obj.model_dump())
        except IntegrityError:
            raise DuplicateValueException()

        out_user: PydanticModel | schemas.User = await schemas.User.from_tortoise_orm(user_obj)
        if isinstance(out_user, schemas.User):
            return out_user
        else:
            logger.error(
                f"Bad user type {type(out_user)}")
            raise CustomException(
                detail="Bad user instance")

    async def get_user(self, user_id: uuid_pkg.UUID) -> schemas.UserRead:
        try:
            db_user: PydanticModel | schemas.UserRead = await schemas.UserRead.from_queryset_single(
                User.get(uuid=user_id).prefetch_related(
                    Prefetch(
                        "base_config",
                        BaseConfig.filter(author_id=user_id)
                    )
                )
            )  # .only(*schemas.UserRead.model_fields.keys())
        except DoesNotExist:
            raise NotFoundException(
                detail=f"User {user_id} not found")

        if isinstance(db_user, schemas.UserRead):
            return db_user
        else:
            logger.error(
                f"Bad user type {type(db_user)}"
            )
            raise CustomException(
                detail="Bad user instance")

    async def find_user(self, **kwargs) -> schemas.UserRead:
        try:
            db_user: PydanticModel | schemas.UserRead\
                = await schemas.UserRead.from_queryset_single(
                    User.get(kwargs=kwargs)
                )
        except DoesNotExist:
            raise NotFoundException(
                detail=f"User {kwargs} not found")

        if isinstance(db_user, schemas.UserRead):
            return db_user
        else:
            logger.error(
                f"Bad user type {type(db_user)}"
            )
            raise CustomException(
                detail="Bad user instance")

    async def get_multi_users(
            self,
            offset: int = 0,
            limit: int = 100
    ) -> ListResponse[schemas.User]:
        users = await schemas.User.from_queryset(
            User.all().offset(offset).limit(limit)
        )
        total_count: int = await User.all().count()
        return ListResponse(
            data=users, total_count=total_count)

    async def delete_user(self, user_id: uuid_pkg.UUID) -> Status:
        try:
            db_user = await schemas.User.from_queryset_single(User.get(uuid=user_id))
        except DoesNotExist:
            raise NotFoundException(
                detail=f"User {user_id} not found")

        if not isinstance(db_user, schemas.User):
            logger.error(
                f"Bad user type {type(db_user)}"
            )
            raise CustomException(
                detail="Bad user instance")

        deleted_count = await User.filter(uuid=user_id).delete()
        if not deleted_count:
            raise NotFoundException(detail={
                "error": f"User[{user_id}] not found"})
        return Status(message=f"Deleted user {user_id}")

    async def update_user(
            self,
            user_id: uuid_pkg.UUID,
            user_update_info: schemas.UserUpdate) -> schemas.User:
        try:
            user: User = await User.get(uuid=user_id)
            logger.debug(
                f"Object to update {user_update_info.model_dump()}")
            if len(user_update_info.model_fields_set) != 0:
                user.update_from_dict(
                    user_update_info.model_dump(
                        exclude_unset=True))
                await user.save(update_fields=user_update_info.model_fields_set)
            logger.debug(f"Object Updated {user}")
            return await schemas.User.from_tortoise_orm(user)
        except DoesNotExist:
            raise NotFoundException(
                detail=f"User {user_id} not found")
        except IntegrityError as e:
            raise DuplicateValueException(
                detail=f"Inconsistent state {e}")


userService: UserService = UserService()
