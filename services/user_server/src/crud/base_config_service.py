import json
from tortoise.contrib.pydantic.base import PydanticModel
from src.api.paginated import ListResponse
from src.exceptions.http_exceptions import DuplicateValueException, CustomException, NotFoundException, UnauthorizedException
from tortoise.exceptions import DoesNotExist, IntegrityError
from src.database.models import BaseConfig
import src.schemas.base_config as schemas
import uuid as uuid_pkg

from src.core.schemas import Status

import logging
from src.core import logger as logger_mod
logger = logging.getLogger(__name__)


class BaseConfigService():
    async def create_base_config(
            self,
            obj: schemas.BaseConfigCreate,
            current_user_id: uuid_pkg.UUID) -> schemas.BaseConfig:
        try:
            out_model_obj = await BaseConfig.create(
                **obj.model_dump(),
                author_id=current_user_id)
        except IntegrityError:
            raise DuplicateValueException()

        out_obj: PydanticModel | schemas.BaseConfig\
            = await schemas.BaseConfig.from_tortoise_orm(out_model_obj)
        if isinstance(out_obj, schemas.BaseConfig):
            return out_obj
        else:
            logger.error(
                f"Bad user type {type(out_obj)}")
            raise CustomException(
                detail="Bad user instance")

    async def get_base_config(self,
                              id: uuid_pkg.UUID) -> schemas.BaseConfigRead:
        try:
            db_user: PydanticModel | schemas.BaseConfigRead\
                = await schemas.BaseConfigRead.from_queryset_single(
                    BaseConfig.get(
                        uuid=id
                    )  # .only(*schemas.BaseConfigRead.model_fields.keys())
                )
        except DoesNotExist:
            raise NotFoundException(
                detail=f"BaseConfig {id} not found")

        if isinstance(db_user, schemas.BaseConfigRead):
            return db_user
        else:
            logger.error(
                f"Bad user type {type(db_user)}"
            )
            raise CustomException(
                detail="Bad user instance")

    async def get_multi_base_configs(
            self,
            offset: int = 0,
            limit: int = 100
    ) -> ListResponse[schemas.BaseConfigRead]:
        objects = await schemas.BaseConfigRead.from_queryset(
            BaseConfig.all().offset(offset).limit(limit)
        )
        total_count: int = await BaseConfig.all().count()
        return ListResponse(
            data=objects, total_count=total_count)

    async def delete_base_config(self,
                                 id: uuid_pkg.UUID,
                                 user_id: uuid_pkg.UUID) -> Status:
        try:
            obj = await schemas.BaseConfigOnly.from_queryset_single(
                BaseConfig.get(uuid=id)
            )
        except DoesNotExist:
            raise NotFoundException(
                detail=f"BaseConfig {id} not found")

        if not isinstance(obj, schemas.BaseConfig):
            logger.error(
                f"Bad user type {type(obj)}"
            )
            if obj.author_id != None:
                if obj.author_id != user_id:
                    raise UnauthorizedException(
                        detail=f"User with {user_id} can't delete base_config with {obj.uuid}"
                    )
            raise CustomException(
                detail="Bad user instance")

        deleted_count = await BaseConfig.filter(uuid=id).delete()
        if not deleted_count:
            raise NotFoundException(detail={
                "error": f"BaseConfig[{id}] not found"})
        return Status(message=f"Deleted BaseConfig {id} for User {user_id}")

    async def update_base_config(
            self,
            id: uuid_pkg.UUID,
            user_id: uuid_pkg.UUID,
            obj_update_info: schemas.BaseConfigUpdate) -> schemas.BaseConfigOnly:
        try:
            model_obj: BaseConfig = await BaseConfig.get(uuid=id)
            obj = await schemas.BaseConfigOnly.from_tortoise_orm(model_obj)
            if obj.author_id != user_id:
                raise UnauthorizedException(
                    detail=f"User with {user_id} can't delete base_config with {obj.uuid}"
                )
            if len(obj_update_info.model_fields_set) != 0:
                model_obj.update_from_dict(
                    obj_update_info.model_dump(
                        exclude_unset=True))
                await model_obj.save(update_fields=obj_update_info.model_fields_set)
            return await schemas.BaseConfigOnly.from_tortoise_orm(model_obj)
        except DoesNotExist:
            raise NotFoundException(
                detail=f"BaseConfig {id} not found")
        except IntegrityError as e:
            raise DuplicateValueException(
                detail=f"Inconsistent state {e}")


baseConfigService: BaseConfigService = BaseConfigService()
