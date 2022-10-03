import configparser
from kombu import Queue
from pathlib import Path

# =========================================================================
#                           PATH PARENT CONFIG
# =========================================================================
PATH_PROJECT = Path(__file__).resolve().parent.parent


# =========================================================================
#                           ENVIRONMENT CONFIG
# =========================================================================
cfg = configparser.ConfigParser()
cfg.read(PATH_PROJECT / 'environment.ini')


# #=========================================================================
# #         ML FACE RECOGNITION INFORMATION QUEUE AND TASK NAME
# #=========================================================================
ML_FACE_RECOGNITION_cfg = cfg["ml-model_face_recognition"]
ML_FACE_RECOGNITION_task = ML_FACE_RECOGNITION_cfg["name_task"]
ML_FACE_RECOGNITION_query_name = ML_FACE_RECOGNITION_cfg["query_name"]


# =========================================================================
#                          CELERY INFORMATION
# =========================================================================
# CELERY = cfg["celery"]

# Set worker to ack only when return or failing (unhandled expection)
task_acks_late = True

# Worker only gets one task at a time
worker_prefetch_multiplier = 1

QUERY_NAME = ML_FACE_RECOGNITION_cfg["query_name"]

# Create queue for worker
# giai thich queue o day: https://docs.celeryq.dev/en/stable/userguide/routing.html
task_queues = [
    Queue(name=QUERY_NAME, routing_key='task.#')
]

result_expires = 60 * 60 * 48  # 48 hours in seconds


