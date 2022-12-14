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
cfg.read(PATH_PROJECT / 'environment.ini')

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


# =========================================================================
#                          ML - FACE RECOGNITION MODEL PATH
# =========================================================================
FACE_REC_cfg = cfg["ml-model_face_recognition"]
FACE_REC_model_path = PATH_PROJECT / FACE_REC_cfg["model_path"]
