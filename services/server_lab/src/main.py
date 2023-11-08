from fastapi import FastAPI

from tortoise import Tortoise

from src.env import get_debug, get_root

from src.database.register import register_tortoise
from src.database.config import TORTOISE_ORM

#from src.routes import base_config

Tortoise.init_models(["src.database.models"], "models")

app = FastAPI(
        description="Effective PP2",
        version="0.0.2",
        root_path=get_root())

#app.include_router(base_config.router)

@app.get("/")
def test():
    return "TEST"

register_tortoise(app, config=TORTOISE_ORM, generate_schemas=False)


debug = get_debug()
print(debug)
if debug == True:
    from tortoise.log import logger, db_client_logger
    import logging
    import sys
    print("DEBUG MODE")
    fmt = logging.Formatter(
        fmt="%(asctime)s - %(name)s:%(lineno)d - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(logging.DEBUG)
    sh.setFormatter(fmt)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(sh)
    db_client_logger.setLevel(logging.DEBUG)
    db_client_logger.addHandler(sh)
