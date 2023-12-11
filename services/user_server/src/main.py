from fastapi import FastAPI

from tortoise import Tortoise
from src.settings import serverSettings

from src.database.register import register_tortoise
from src.database.config import TORTOISE_ORM

#from src.routes import base_config

Tortoise.init_models(["src.database.models"], "models")

app = FastAPI(
        description="Effective PP2",
        version="0.0.2",
        root_path=serverSettings.root_path)

#app.include_router(base_config.router)

@app.get("/")
def test():
    return "TEST"

register_tortoise(app, config=TORTOISE_ORM, generate_schemas=False)


