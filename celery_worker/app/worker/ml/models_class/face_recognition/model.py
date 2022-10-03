import logging
import tensorflow as tf
from settings import config
from worker.ml.helpers import facerec_utilis as face_helpers
from worker.ml.models_class.base_class import BaseModel


class FaceRecModel(BaseModel):

    def __init__(self):
        super(FaceRecModel, self).__init__()
        self.model = self._load_model()

    def _load_model(self):
        return tf.keras.models.load_model(config.FACE_REC_model_path)

    def predict(self, np_array):
        logging.info("\tModel face recognition is predicting ...")
        output = face_helpers.l2_norm(self.model(np_array, training=False))
        logging.info("\tModel face recognition done .")
        return output
