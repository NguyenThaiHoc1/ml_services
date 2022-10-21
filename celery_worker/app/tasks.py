"""
[Summary] Workers
[Information]
    @author: Nguyen Thai Hoc
    @email: nguyenthaihoc1996@outlook.com
    @create: 28-09-2022
"""
import json
import logging
import numpy as np
from celery import Celery
from helpers import init_redis, init_broker
from settings import celery_config, config
from helpers import time as time_helpers
from helpers import storages as storages_helpers
from redis_main import redis

# logging tests
from celery.signals import after_setup_logger

# import helpers - facerec
from helpers.ml import facerec_utilis as facerec_helpers

# import helpers - facedet
from helpers.ml.facedet_utils import facedet_reprocess as facedet_helpers
from helpers.ml.facedet_utils import convert_output as facedet_convert_helpers

# import Task Model
from tasks_model.task_FaceRec import FacePredictTask
from tasks_model.task_FaceDetection import FaceDetectionPredictTask

# check connect redis
if not init_redis.is_backend_running(): exit()
if not init_broker.is_broker_running(): exit()

app = Celery("Task-Manager", broker=config.REDIS_queue, backend=config.REDIS_backend)
app.config_from_object('settings.celery_config')


@after_setup_logger.connect
def setup_loggers(logger, *args, **kwargs):
    formatter = logging.Formatter('[%(asctime)s - %(name)s - %(levelname)s]: %(message)s')

    # add filehandler
    fh = logging.FileHandler(config.PATH_PROJECT / "logs" / "workers.log")
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    logger.addHandler(fh)


# Face-Recognition consumer
@app.task(bind=True, base=FacePredictTask,
          name="{query}.{task_name}".format(query=celery_config.ML_FACE_RECOGNITION_query_name,
                                            task_name=celery_config.ML_FACE_RECOGNITION_task))
def face_recognition_task(self, task_id: str, data: bytes):
    """
        _summary_: face recognition by tensorflow model
           Args:
               task_id (str): _description_
               data (bytes): _description_
           Returns:
               _type_: _description_
    """
    try:
        logging.info(f"== API_TASK: {task_id} RUNNING...")
        data = json.loads(data)
        data["time"]["start_face_rec"] = str(time_helpers.now_utc())
        path_image = data["upload_result"]["path"]
        image = facerec_helpers.read_image_from_path_to_numpy(path=path_image)
        image = facerec_helpers.preprocess_image(np_array=image)
        embeddings = self.model.http_send_request(image)
        if embeddings is None:
            raise TypeError("Embeddings of face-rec is none please check.")
        data["time"]["end_face_rec"] = str(time_helpers.now_utc())
        data["status"]["face_rec_status"] = "SUCCESS"
        data["status"]["general_status"] = "SUCCESS"
        data["face_rec_result"] = embeddings
        data_dump = json.dumps(data)
        redis.set(task_id, data_dump)
        logging.info(f"== API_TASK: {task_id} DONE...")
    except Exception as e:
        data["time"]["end_face_rec"] = str(time_helpers.now_utc())
        data["status"]["face_rec_status"] = "FAILED"
        data["status"]["general_status"] = "FAILED"
        data["error"] = str(e)
        data_dump = json.dumps(data)
        redis.set(task_id, data_dump)


# Face-Detection consumer
@app.task(bind=True, base=FaceDetectionPredictTask,
          name="{query}.{task_name}".format(query=celery_config.ML_FACE_DETECTION_query_name,
                                            task_name=celery_config.ML_FACE_DETECTION_task))
def face_detection_task(self, task_id: str, data: bytes):
    file_name = str(task_id) + celery_config.ML_FACE_DETECTION_img_type
    dir_path = celery_config.ML_FACE_DETECTION_storage_path / str(time_helpers.str_dd_mm_yyyy())
    storages_helpers.create_path(dir_path)
    abs_path_file_name = dir_path / file_name
    try:
        logging.info(f"== API_TASK: {task_id} RUNNING...")
        data = json.loads(data)
        data["time"]["start_face_det"] = str(time_helpers.now_utc())
        path_image = data["upload_result"]["path"]
        image, width, height = facedet_helpers.read_image_from_path_to_numpy(path=path_image)
        image_preprocessed = facedet_helpers.preprocess_image(image.copy())
        y_bboxes_output, y_cls_output = self.model.http_send_request(image_preprocessed)
        if y_bboxes_output is None or y_cls_output is None:
            raise TypeError("Predict at face detection have a problem, please check.")
        output_info, img_output = facedet_helpers.decode_all_boxes(image,
                                                                   y_bboxes_output, y_cls_output,
                                                                   width=width, height=height)
        # saving image to storages
        img_output.save(abs_path_file_name)
        data["time"]["end_face_det"] = str(time_helpers.now_utc())
        data["status"]["face_det_status"] = "SUCCESS"
        data["status"]["general_status"] = "SUCCESS"
        data["face_det_result"] = facedet_convert_helpers.convert_output_2jsondumps(output_info)
        data_dump = json.dumps(data)
        redis.set(task_id, data_dump)
        logging.info(f"== API_TASK: {task_id} DONE...")
    except Exception as e:
        data["time"]["end_face_det"] = str(time_helpers.now_utc())
        data["status"]["face_det_status"] = "FAILED"
        data["status"]["general_status"] = "FAILED"
        data["error"] = str(e)
        logging.error(str(e))
        data_dump = json.dumps(data)
        redis.set(task_id, data_dump)
