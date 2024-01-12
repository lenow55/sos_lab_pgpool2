from celery import Celery, Task
from src.settings import backend_settings, broker_settings
from src.model import DetectModel
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

import os
import sys

class CeleryConfig:
    broker_url = broker_settings.broker_url
    result_backend = backend_settings.backend_url


app = Celery()
app.config_from_object(CeleryConfig)
# Celery routing
app.conf.task_routes = {
    "src.main.*": {
        "queue": "ml_service",
    },
}
app.conf.broker_transport_options = {"visibility_timeout": 36000}  # 1h

class PredictTask(Task):
    """
    Abstraction of Celery's Task class to support loading ML model.
    """

    abstract = True

    def __init__(self):
        super().__init__()
        self.model = None
        print("PredictTask initialized")

    def __call__(self, *args, **kwargs):
        """
        Load model on first call (i.e. first task processed)
        Avoids the need to load model on each task request
        """
        if not self.model:
            print("Loading Model...")

            # NOTE: Use `parent_package.package`, so for getting `model.py`, it should be `mock_model.model`
            self.model = DetectModel()

            print("Model loaded")
        return self.run(*args, **kwargs)


@app.task(
    ignore_result=False,
    bind=True,
    base=PredictTask,
)
def detect_spam(self, msg: str):
    """
    Essentially the run method of PredictTask
    """
    logger.info(f"Get message {msg}")

    result = self.model.predict(msg)
    return result
