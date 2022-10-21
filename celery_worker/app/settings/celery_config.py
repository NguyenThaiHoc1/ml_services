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
ML_FACE_RECOGNITION_img_type = ML_FACE_RECOGNITION_cfg["image_type"]
ML_FACE_RECOGNITION_task = ML_FACE_RECOGNITION_cfg["name_task"]
ML_FACE_RECOGNITION_query_name = ML_FACE_RECOGNITION_cfg["query_name"]
ML_FACE_RECOGNITION_storage_path = PATH_PROJECT / ML_FACE_RECOGNITION_cfg["storages_path"]
ML_FACE_RECOGNITION_storage_path.mkdir(parents=True, exist_ok=True)

# #=========================================================================
# #         ML FACE DETECTION INFORMATION QUEUE AND TASK NAME
# #=========================================================================
ML_FACE_DETECTION_cfg = cfg["ml-model_face_detection"]
ML_FACE_DETECTION_img_type = ML_FACE_DETECTION_cfg["image_type"]
ML_FACE_DETECTION_task = ML_FACE_DETECTION_cfg["name_task"]
ML_FACE_DETECTION_query_name = ML_FACE_DETECTION_cfg["query_name"]
ML_FACE_DETECTION_storage_path = PATH_PROJECT / ML_FACE_DETECTION_cfg["storages_path"]
ML_FACE_DETECTION_storage_path.mkdir(parents=True, exist_ok=True)

# #=========================================================================
# Set worker to ack only when return or failing (unhandled expection)
task_acks_late = True

# Worker only gets one task at a time
worker_prefetch_multiplier = 2

# Create queue for worker
# giai thich queue o day: https://docs.celeryq.dev/en/stable/userguide/routing.html
task_queues = [
    Queue(name=ML_FACE_RECOGNITION_query_name, routing_key='task_facerec.#'),
    Queue(name=ML_FACE_DETECTION_query_name, routing_key='task_facedet.#')
]

result_expires = 60 * 60 * 48  # 48 hours in seconds
