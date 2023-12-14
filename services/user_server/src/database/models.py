from tortoise import fields, models
from tortoise.fields import CASCADE, SET_NULL, ForeignKeyNullableRelation


class User(models.Model):
    uuid = fields.UUIDField(pk=True)

    full_name = fields.CharField(
        max_length=50, null=False)
    username = fields.CharField(
        max_length=20, unique=True)
    email = fields.CharField(
        max_length=50, unique=True
    )
    hashed_password = fields.BinaryField(
        null=False)
    base_config = fields.ReverseRelation["BaseConfig"]

    create_at = fields.DatetimeField(
        auto_now_add=True)
    update_at = fields.DatetimeField(
        auto_now=True)

    is_deleted = fields.BooleanField(
        default=False)
    deleted_at = fields.DatetimeField(
        auto_now=True)

    class Meta(models.Model.Meta):
        indexes: tuple = ("username", "is_deleted", "email")

class SuperUser(models.Model):
    id = fields.IntField(pk=True)
    uuid_super_user = fields.ForeignKeyField(
        "models.User",
        related_name=False,
        null=False,
        on_delete=CASCADE
    )


class BaseConfig(models.Model):
    uuid = fields.UUIDField(pk=True)
    count_connections = fields.IntField()
    read_write_percent = fields.IntField()
    query_complex = fields.IntField()
    base_in_cache = fields.BooleanField()
    query_cache = fields.BooleanField()
    pgpool_enabled = fields.BooleanField()
    author: ForeignKeyNullableRelation = fields.ForeignKeyField(
        "models.User",
        related_name="base_config",
        null=True,
        on_delete=SET_NULL)
    create_date = fields.DatetimeField(
        auto_now_add=True)
    update_date = fields.DatetimeField(
        auto_now=True)

    class Meta(models.Model.Meta):
        # Define the default ordering
        #  the pydantic serialiser will use this to order the results
        ordering = ["uuid"]


class ModelConfig(models.Model):
    id = fields.UUIDField(pk=True)
    model_id = fields.UUIDField(index=True)
    model_name = fields.CharField(
        max_length=50, null=True)
    version = fields.IntField()
    # прописать энкодер и декодер
    # надо это потому что параметры для модели нельзя будет в одну схему упаковать
    params_json = fields.JSONField()
    create_at = fields.DatetimeField(
        auto_now_add=True)
    modify_at = fields.DatetimeField(
        auto_now=True)
