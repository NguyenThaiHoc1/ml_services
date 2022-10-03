import numpy as np
from PIL import Image


def read_image_from_path_to_numpy(path):
    image = Image.open(path)
    image = image.convert('RGB')
    return np.asarray(image)
