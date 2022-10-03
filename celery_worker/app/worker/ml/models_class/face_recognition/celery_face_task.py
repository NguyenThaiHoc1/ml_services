import logging
from celery import Task
from worker.ml.models_class.face_recognition.model import FaceRecModel


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
            self.model = FaceRecModel()
            logging.info('Model loaded')
        return self.run(*args, **kwargs)
