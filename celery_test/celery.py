import os
import logging

from celery import Celery, signals, current_task
from celery.utils.log import get_task_logger

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

app = Celery("proj")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

logger = logging.getLogger(__name__)


class TaskLogRecord(logging.LogRecord):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if current_task:
            self.task_name = current_task.name
            self.task_id = current_task.request.id


@signals.setup_logging.connect
def change_log_record_factory(**kwargs):
    logging.setLogRecordFactory(TaskLogRecord)


@app.task
def debug_task():
    logger.info("oi")
