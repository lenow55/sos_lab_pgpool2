from fastapi import FastAPI

from tortoise import Tortoise
from src.core.settings import serverSettings

from src.database.register import register_tortoise
from src.database.config import TORTOISE_ORM

from src.core.schemas import HealthCheck
from src.core.setup import register_redis


import logging
from src.core import logger as logger_mod
logger = logging.getLogger(__name__)


Tortoise.init_models(["src.database.models"], "models")

#from src.routes import base_config
from src.api.v1 import router

app = FastAPI(
        title="Effective PP2",
        description="Сервис для работы с конфигурациями базы данных",
        version="0.0.2",
        root_path=serverSettings.root_path)

app.include_router(router)

@app.get("/", tags=["HealthCheck"], response_model=HealthCheck)
def test() -> HealthCheck:
    return HealthCheck(
            name=app.title,
            version=app.version,
            description=app.description)


register_tortoise(app, config=TORTOISE_ORM, generate_schemas=False)
register_redis(app)

