from src.core.settings import dbSettings


TORTOISE_ORM = {
        "connections": {
            "default": {
                "engine": "tortoise.backends.asyncpg",
                "credentials": {
                    "host": dbSettings.db_host,
                    "port": dbSettings.db_port,
                    "user": dbSettings.db_user,
                    "password": dbSettings.db_password.get_secret_value(),
                    "database": dbSettings.db_name,
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
