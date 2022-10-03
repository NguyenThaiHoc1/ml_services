"""
[Summary] Workers
[Information]
    @author: Nguyen Thai Hoc
    @email: nguyenthaihoc1996@outlook.com
    @create: 28-09-2022
"""
import json
import logging
from celery import Celery
from helpers import init_redis, init_broker
from settings import celery_config, config
from helpers import time as time_helpers
from redis_main import redis

# logging tests
from celery.signals import after_setup_logger

# import helpers
from worker.ml.helpers import facerec_utilis as face_helpers

# import Task Model
from worker.ml.models_class.face_recognition.celery_face_task import FacePredictTask

# check connect redis
if not init_redis.is_backend_running(): exit()
if not init_broker.is_broker_running(): exit()

app = Celery(celery_config.QUERY_NAME, broker=config.REDIS_queue, backend=config.REDIS_backend)
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
        image = face_helpers.read_image_from_path_to_numpy(path=path_image)
        image = face_helpers.preprocess_image(np_array=image)
        embeddings = self.model.predict(image)
        data["time"]["end_face_rec"] = str(time_helpers.now_utc())
        data["status"]["face_rec_status"] = "SUCCESS"
        data["status"]["general_status"] = "SUCCESS"
        data["face_rec_result"] = embeddings.numpy().tolist()
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
