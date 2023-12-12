import logging
from tortoise.contrib.pydantic.base import PydanticModel
from src.api.paginated import ListResponse
from src.exceptions.http_exceptions import DuplicateValueException, CustomException, NotFoundException
from tortoise.exceptions import DoesNotExist, IntegrityError
from src.database.models import User
import src.schemas.user as schemas
from src.core.security import get_password_hash
from src.core.logger import configureLogger
import uuid as uuid_pkg

logger = logging.getLogger(__name__)
logger = configureLogger(logger)
print(logger)
print(logger.handlers)

class UserService():
    async def create_user(self, user_in_obj: schemas.UserCreate) -> schemas.User:
        user_internal_dict: dict = user_in_obj.model_dump()
        user_internal_dict["hashed_password"] = get_password_hash(
            password=user_internal_dict["password"])
        del user_internal_dict["password"]
        user_obj = None
        try:
            user_obj = await User.create(**user_internal_dict)
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
                User.get(uuid=user_id).only(*schemas.UserRead.model_fields.keys())
            )
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

    async def get_multi_users(
            self,
            offset: int = 0,
            limit: int = 100
    ) -> ListResponse[schemas.User]:
        users = await schemas.User.from_queryset(
            User.all().offset(offset).limit(limit).only(
                *schemas.User.model_fields.keys()
            )
        )
        total_count: int = await User.all().count()
        return ListResponse(
            data=users, total_count=total_count)

    async def delete_user(self, user_id: uuid_pkg.UUID) -> schemas.User:
        try:
            db_user = await schemas.User.from_queryset_single(User.get(uuid=user_id))
            #db_user = await User.get(uuid=user_id)
        except DoesNotExist:
            raise NotFoundException(
                detail=f"User {user_id} not found")


        logger.debug(db_user)

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
        return db_user


userService: UserService = UserService()
