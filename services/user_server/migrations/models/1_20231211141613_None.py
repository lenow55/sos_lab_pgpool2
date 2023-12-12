from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "modelconfig" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "model_id" UUID NOT NULL,
    "model_name" VARCHAR(50),
    "version" INT NOT NULL,
    "params_json" JSONB NOT NULL,
    "create_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "modify_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS "idx_modelconfig_model_i_3eae59" ON "modelconfig" ("model_id");
CREATE TABLE IF NOT EXISTS "user" (
    "uuid" UUID NOT NULL  PRIMARY KEY,
    "full_name" VARCHAR(50) NOT NULL,
    "username" VARCHAR(20) NOT NULL UNIQUE,
    "email" VARCHAR(50) NOT NULL UNIQUE,
    "hashed_password" BYTEA NOT NULL,
    "create_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "update_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "is_deleted" BOOL NOT NULL  DEFAULT False,
    "deleted_at" TIMESTAMPTZ NOT NULL
);
CREATE INDEX IF NOT EXISTS "idx_user_usernam_018265" ON "user" ("username", "is_deleted", "email");
CREATE TABLE IF NOT EXISTS "baseconfig" (
    "uuid" UUID NOT NULL  PRIMARY KEY,
    "count_connections" INT NOT NULL,
    "read_write_percent" INT NOT NULL,
    "query_complex" INT NOT NULL,
    "base_in_cache" BOOL NOT NULL,
    "query_cache" BOOL NOT NULL,
    "pgpool_enabled" BOOL NOT NULL,
    "create_date" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "update_date" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "author_id" UUID REFERENCES "user" ("uuid") ON DELETE SET NULL
);
CREATE TABLE IF NOT EXISTS "superuser" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "uuid_super_user_id" UUID NOT NULL REFERENCES "user" ("uuid") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
