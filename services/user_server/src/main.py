from fastapi import FastAPI

from tortoise import Tortoise
from src.core.settings import serverSettings

from src.database.register import register_tortoise
from src.database.config import TORTOISE_ORM

from src.core.schemas import HealthCheck

#from src.routes import base_config
from src.api.v1 import router

import logging
from src.core import logger as logger_mod
logger = logging.getLogger(__name__)


Tortoise.init_models(["src.database.models"], "models")

app = FastAPI(
        description="Effective PP2",
        version="0.0.2",
        root_path=serverSettings.root_path)

#app.include_router(base_config.router)
app.include_router(router)

@app.get("/", response_model=HealthCheck)
def test() -> HealthCheck:
    return HealthCheck(
            name=app.title,
            version=app.version,
            description=app.description)


register_tortoise(app, config=TORTOISE_ORM, generate_schemas=False)

