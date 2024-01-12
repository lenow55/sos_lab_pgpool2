from src.api.v1 import router
from celery.canvas import Signature
from fastapi import FastAPI
from starlette.responses import PlainTextResponse

from tortoise import Tortoise
from src.core.settings import serverSettings
from src.core.settings import backend_settings, broker_settings

from src.database.register import register_tortoise
from src.database.config import TORTOISE_ORM

from src.core.schemas import HealthCheck, TaskIn, TaskOut
from src.core.setup import register_redis
from celery import Celery, signature
from celery.result import AsyncResult

import logging
from src.core import logger as logger_mod
logger = logging.getLogger(__name__)


class CeleryConfig:
    broker_url = broker_settings.broker_url
    result_backend = backend_settings.backend_url


celery_app = Celery()
celery_app.config_from_object(CeleryConfig)
# Celery routing
celery_app.conf.task_routes = {
    "src.main.*": {
        "queue": "ml_service",
    },
}
celery_app.conf.broker_transport_options = {
    "visibility_timeout": 36000}  # 1h


Tortoise.init_models(["src.database.models"], "models")

# from src.routes import base_config

app = FastAPI(
    title="Effective PP2",
    description="Сервис для работы с конфигурациями базы данных",
    version="0.0.2",
    root_path=serverSettings.root_path)

app.include_router(router)


@app.get("/", tags=["HealthCheck"],
         response_model=HealthCheck)
def test() -> HealthCheck:
    return HealthCheck(
        name=app.title,
        version=app.version,
        description=app.description)


@app.post("/task", tags=["Task"], response_model=TaskOut)
def task(config: TaskIn) -> TaskOut:
    add_task_signature: Signature = celery_app.signature(
        'src.main.detect_spam',
        kwargs={"msg": config.model_dump_json()})
    result: AsyncResult = add_task_signature.apply_async()
    return TaskOut(id=result.id)


@app.get("/task/{id}", tags=["Task"])
def get_task(id: str) -> PlainTextResponse:
    result: AsyncResult = AsyncResult(id=id, app=celery_app)
    return PlainTextResponse(f"task id = {result.id} \n\
status: {result.status}\nresult {result.result}")


register_tortoise(app, config=TORTOISE_ORM,
                  generate_schemas=False)
register_redis(app)
