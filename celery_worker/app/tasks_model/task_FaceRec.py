import logging
from celery import Task
from settings import service_config
from protocols.face_recognition.proto_face_reco import ProtoFaceRec


class FacePredictTask(Task):
    abstract = True

    def __init__(self):
        super().__init__()
        self.model = None

    def __call__(self, *args, **kwargs):
        """
            Load model on first call (i.e. first task processed)
            Avoids the need to load model on each task request
        """
        if not self.model:
            logging.info('Loading Model...')

            proto_http = {
                'url_main': "http://{domain}:{port}/v1/models/{model_name}:predict".format(
                    domain=service_config.HTTP_DOMAIN,
                    port=service_config.HTTP_PORT,
                    model_name=service_config.HTTP_MODEL_NAME
                )
            }

            proto_grpc = {
                'url_main': "{domain}:{port}".format(
                    domain=service_config.GRPC_DOMAIN,
                    port=service_config.GRPC_PORT
                ),
                'signature_name': service_config.GRPC_SIGNATURE_NAME,
                'model_name': service_config.GRPC_MODEL_NAME,
                'grpc_config_options': [
                    ('grpc.max_send_message_length', service_config.GRPC_MAX_MESSAGE_LENGTH),
                    ('grpc.max_receive_message_length', service_config.GRPC_MAX_MESSAGE_LENGTH)
                ]
            }

            self.model = ProtoFaceRec(
                dict_http=proto_http,
                dict_grpc=proto_grpc
            )
            logging.info('Model loaded')
        return self.run(*args, **kwargs)
