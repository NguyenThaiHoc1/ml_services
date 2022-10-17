import grpc
import json
import requests
import numpy as np
import tensorflow as tf
from protocols.protocols_class import ProtocolClass
from tensorflow_serving.apis import predict_pb2, prediction_service_pb2_grpc


class ProtoFaceRec(ProtocolClass):

    def __init__(self, dict_http, dict_grpc):
        super(ProtoFaceRec, self).__init__()
        # setup http
        self.dict_http = dict_http
        self.url_http = self.dict_http["url_main"]

        # setup grpc
        self.dict_grpc = dict_grpc
        self.url_grpc = self.dict_grpc["url_main"]
        self.model_name = self.dict_grpc["model_name"]
        self.grpc_config_options = self.dict_grpc["grpc_config_options"]
        self.signature_name = self.dict_grpc["signature_name"]

    def http_send_request(self, img_np_array):
        if self.dict_http is None:
            return "HTTP's protocol is not setting."
        data = json.dumps({
            "instances": img_np_array.tolist()
        })
        headers = {"content-type": "application/json"}
        json_response = requests.post(
            self.url_http,
            data=data,
            headers=headers
        )
        if json_response.status_code == 200:
            y_pred = json.loads(json_response.text)['predictions']
            return y_pred
        else:
            return None

    def grpc_send_request(self, img_np_array):
        if self.dict_grpc is None:
            return "gRPC's protocol is not setting."

        request = predict_pb2.PredictRequest()
        request.model_spec.name = self.model_name
        request.model_spec.signature_name = self.signature_name
        request.inputs["input_face_masked"].CopyFrom(
            tf.make_tensor_proto(
                img_np_array,
                dtype=np.float32,
                shape=img_np_array.shape
            )
        )

        with grpc.insecure_channel(self.url_grpc, options=self.grpc_config_options) as channel:
            stub = prediction_service_pb2_grpc.PredictionServiceStub(channel=channel)
            result = stub.Predict(request, 500)

        # convert result from tf-serving: nhớ dùng saved_model_cli để biết input + output name của mô hình.
        result = result.outputs["InceptionResNetV1"].float_val
        result = np.array(result).reshape((-1, 512))
        return result
