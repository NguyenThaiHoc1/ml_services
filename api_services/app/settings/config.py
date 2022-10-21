import configparser
import datetime
from pathlib import Path
import os
import pytz

# =========================================================================
#                           PATH PARENT CONFIG
# =========================================================================
PATH_PROJECT = Path(__file__).resolve().parent.parent

# =========================================================================
#                           ENVIRONMENT CONFIG
# =========================================================================
cfg = configparser.ConfigParser()
cfg.read('./environment.ini')

# =========================================================================
#                           TIMING CONFIG
# =========================================================================
universal = datetime.datetime.utcnow()
universal = universal.replace(tzinfo=pytz.timezone("Asia/Ho_Chi_Minh"))

# =========================================================================
#                          PROJECT INFORMATION
# =========================================================================
PROJECT_cfg = cfg["project"]
PROJECT_NAME = PROJECT_cfg["name"]
ENVIRONMENT = PROJECT_cfg["environment"]
HOST = PROJECT_cfg["host"]
PORT = PROJECT_cfg["port"]
USER = PROJECT_cfg["user"]
PASSWORD = PROJECT_cfg["password"]

# =========================================================================
#                          FACE RECOGNITION INFORMATION
# =========================================================================
ML_FACE_RECOGNITION_cfg = cfg["ml-model_face_recognition"]
ML_FACE_RECOGNITION_image_type = ML_FACE_RECOGNITION_cfg["image_type"]
ML_FACE_RECOGNITION_task = ML_FACE_RECOGNITION_cfg["name_task"]
ML_FACE_RECOGNITION_query_name = ML_FACE_RECOGNITION_cfg["query_name"]
ML_FACE_RECOGNITION_storage_path = PATH_PROJECT / ML_FACE_RECOGNITION_cfg["storage_upload_path"]
ML_FACE_RECOGNITION_storage_path.mkdir(parents=True, exist_ok=True)  # hay

# =========================================================================
#                          FACE DETECTION INFORMATION
# =========================================================================
ML_FACE_DETECTION_cfg = cfg["ml-model_face_detection"]
ML_FACE_DETECTION_image_type = ML_FACE_DETECTION_cfg["image_type"]
ML_FACE_DETECTION_task = ML_FACE_DETECTION_cfg["name_task"]
ML_FACE_DETECTION_query_name = ML_FACE_DETECTION_cfg["query_name"]
ML_FACE_DETECTION_storage_path = PATH_PROJECT / ML_FACE_DETECTION_cfg["storage_upload_path"]
ML_FACE_DETECTION_storage_path.mkdir(parents=True, exist_ok=True)

# =========================================================================
#                          REDIS CONFIG
# =========================================================================
REDIS = cfg["redis"]
REDIS_queue = "redis://:{password}@{hostname}:{port}/{db_name}".format(
    password=REDIS["pass"],
    hostname=REDIS["host"],
    port=REDIS["port"],
    db_name=REDIS["broker_name"]
)
REDIS_backend = "redis://:{password}@{hostname}:{port}/{db_name}".format(
    password=REDIS["pass"],
    hostname=REDIS["host"],
    port=REDIS["port"],
    db_name=REDIS["backend_db_name"]
)
