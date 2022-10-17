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
#                           FACE - PROTOCOLS CONFIG
# =========================================================================
GRPC_cfg = cfg["grpc"]
GRPC_DOMAIN = GRPC_cfg["domain"]
GRPC_PORT = GRPC_cfg["port"]
GRPC_MODEL_NAME = GRPC_cfg["model_name"]
GRPC_SIGNATURE_NAME = GRPC_cfg["signature_name"]
GRPC_MAX_MESSAGE_LENGTH = GRPC_cfg["max_message_length"]

HTTP_cfg = cfg["http"]
HTTP_DOMAIN = HTTP_cfg["domain"]
HTTP_PORT = HTTP_cfg["port"]
HTTP_MODEL_NAME = HTTP_cfg["model_name"]


