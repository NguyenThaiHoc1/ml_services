import json
import datetime
from fastapi import (
    UploadFile
)
from settings import config
from redis_main import redis
from celery_worker import celery_execute
from helpers import time as time_helpers
from helpers import storages as storages_helpers
from api_endpoint.serializers.serials_face_detection import MlResult


def background_image_upload(file: UploadFile, task_id: str, time: datetime, data: MlResult):
    filename = task_id + config.ML_FACE_DETECTION_image_type
    dir_path = config.ML_FACE_DETECTION_storage_path / str(time_helpers.str_dd_mm_yyyy())
    storages_helpers.create_path(dir_path)
    abs_path_file_name = dir_path / filename
    file_bytes = file.file.read()
    try:
        storages_helpers.upload_file_bytes(file_bytes, abs_path_file_name)
        data.time['end_upload'] = str(time_helpers.now_utc())
        data.status['upload_status'] = "SUCCESS"
        data.upload_result = {
            "path": str(abs_path_file_name),
            "file_type": config.ML_FACE_DETECTION_image_type
        }
        data_dump = json.dumps(data.__dict__)
        redis.set(task_id, data_dump)
        celery_execute.send_task(
            name="{}.{}".format(config.ML_FACE_DETECTION_query_name, config.ML_FACE_DETECTION_task),
            kwargs={
                'task_id': task_id,
                'data': data_dump
            },
            queue=config.ML_FACE_DETECTION_query_name
        )
    except Exception as e:
        data.status['upload_status'] = "FAILED"
        data.status['general_status'] = "FAILED"
        data.error = str(e)
        redis.set(task_id, json.dumps(data.__dict__))
