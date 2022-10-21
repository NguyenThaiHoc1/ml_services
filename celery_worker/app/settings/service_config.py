import configparser
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


# =========================================================================
#                           FACE REC - PROTOCOLS CONFIG
# =========================================================================
GRPC_cfg_face_rec = cfg["face_rec-grpc"]
GRPC_DOMAIN_face_rec = GRPC_cfg_face_rec["domain"]
GRPC_PORT_face_rec = GRPC_cfg_face_rec["port"]
GRPC_MODEL_NAME_face_rec = GRPC_cfg_face_rec["model_name"]
GRPC_SIGNATURE_NAME_face_rec = GRPC_cfg_face_rec["signature_name"]
GRPC_MAX_MESSAGE_LENGTH_face_rec = GRPC_cfg_face_rec["max_message_length"]

HTTP_cfg_face_rec = cfg["face_rec-http"]
HTTP_DOMAIN_face_rec = HTTP_cfg_face_rec["domain"]
HTTP_PORT_face_rec = HTTP_cfg_face_rec["port"]
HTTP_MODEL_NAME_face_rec = HTTP_cfg_face_rec["model_name"]

# =========================================================================
#                           FACE DETECTION - PROTOCOLS CONFIG
# =========================================================================
GRPC_cfg_face_det = cfg["face_det-grpc"]
GRPC_DOMAIN_face_det = GRPC_cfg_face_det["domain"]
GRPC_PORT_face_det = GRPC_cfg_face_det["port"]
GRPC_MODEL_NAME_face_det = GRPC_cfg_face_det["model_name"]
GRPC_SIGNATURE_NAME_face_det = GRPC_cfg_face_det["signature_name"]
GRPC_MAX_MESSAGE_LENGTH_face_det = GRPC_cfg_face_det["max_message_length"]

HTTP_cfg_face_det = cfg["face_det-http"]
HTTP_DOMAIN_face_det = GRPC_cfg_face_det["domain"]
HTTP_PORT_face_det = GRPC_cfg_face_det["port"]
HTTP_MODEL_NAME_face_det = GRPC_cfg_face_det["model_name"]


