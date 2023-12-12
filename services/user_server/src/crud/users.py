from fastapi import HTTPException
from passlib.context import CryptContext
from tortoise.exceptions import DoesNotExist, IntegrityError

from src.database.models import User
from src.schemas.user import UserInSchema, UserOutSchema


pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_user(user: UserIn):
    user.password = pwd_context.encrypt(user.password)

    try:
        user_obj: User = await User.create(**user.dict(exclude_unset=True))
    except IntegrityError:
        raise HTTPException(status_code=401, detail=f"Sorry, that username already exists.")

    return await UserOutSchema.from_tortoise_orm(user_obj)


async def delete_user(user_id, current_user):
    try:
        db_user = await UserOutSchema.from_queryset_single(User.get(id=user_id))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")

    if db_user.id == current_user.id:
        deleted_count = await User.filter(id=user_id).delete()
        if not deleted_count:
            raise HTTPException(status_code=404, detail=f"User {user_id} not found")
        return f"Deleted user {user_id}"

    raise HTTPException(status_code=403, detail=f"Not authorized to delete")
