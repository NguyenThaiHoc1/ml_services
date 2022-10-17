import logging
import numpy as np
from PIL import Image


def l2_norm(embeddings, axis=1):
    norm = np.linalg.norm(embeddings, axis=axis, keepdims=True)
    output = embeddings / norm
    return output


def preprocess_image(np_array):
    logging.info("\tPreprocess image ...")
    np_image_preprocess = np_array.astype(np.float32) / 255.
    np_image_preprocess = np.expand_dims(np_image_preprocess, axis=0)
    logging.info("\tPreprocess image done.")
    return np_image_preprocess


def read_image_from_path_to_numpy(path):
    logging.info("\tReading image ...")
    image = Image.open(path)
    image = image.convert('RGB')
    image = image.resize((160, 160))
    logging.info("\tReading image done.")
    return np.asarray(image)
