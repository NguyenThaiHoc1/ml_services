import logging
from celery import Task
from settings import service_config
from protocols.face_detection.proto_face_detection import ProtoFaceDet


class FaceDetectionPredictTask(Task):
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
                    domain=service_config.HTTP_DOMAIN_face_det,
                    port=service_config.HTTP_PORT_face_det,
                    model_name=service_config.HTTP_MODEL_NAME_face_det
                )
            }

            proto_grpc = {
                'url_main': "{domain}:{port}".format(
                    domain=service_config.GRPC_DOMAIN_face_det,
                    port=service_config.GRPC_PORT_face_det
                ),
                'signature_name': service_config.GRPC_SIGNATURE_NAME_face_det,
                'model_name': service_config.GRPC_MODEL_NAME_face_det,
                'grpc_config_options': [
                    ('grpc.max_send_message_length', service_config.GRPC_MAX_MESSAGE_LENGTH_face_det),
                    ('grpc.max_receive_message_length', service_config.GRPC_MAX_MESSAGE_LENGTH_face_det)
                ]
            }

            self.model = ProtoFaceDet(
                dict_http=proto_http,
                dict_grpc=proto_grpc
            )
            logging.info('Model loaded')
        return self.run(*args, **kwargs)
