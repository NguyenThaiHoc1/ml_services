from abc import abstractmethod


class BaseModel(object):

    def __init__(self):
        pass

    @abstractmethod
    def _load_model(self):
        pass

    @abstractmethod
    def predict(self, np_array):
        pass
