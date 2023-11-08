import os


TORTOISE_ORM = {
        "connections": {
            "default": {
                "engine": "tortoise.backends.asyncpg",
                "credentials": {
                    "host": os.environ.get("DB_HOST"),
                    "port": os.environ.get("DB_PORT"),
                    "user": os.environ.get("DB_USER"),
                    "password": os.environ.get("DB_PASSWORD"),
                    "database": os.environ.get("DB_NAME"),
                    }
                }
            },
        "apps": {
            "models": {
                "models": [
                    "src.database.models", "aerich.models"
                    ],
                "default_connection": "default"
                }
            }
        }
