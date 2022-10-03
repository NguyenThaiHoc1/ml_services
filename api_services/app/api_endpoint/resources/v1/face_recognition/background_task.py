import datetime
import json

from fastapi import (
    BackgroundTasks, UploadFile
)
from api_endpoint.serializers.serials_face_recognition import MlResult
from settings import config
from helpers import time as time_helpers
from helpers import storages as storages_helpers
from redis_main import redis
from celery_worker import celery_execute

"""
    Giải thích một số điều cơ bản 
    Tại sao ở đây lại dùng hàm thường chứ không dùng hàm Async I/O 
    - vì đây là một tác vụ không kết nối
        nó không cần các tác vụ gọi tới một nơi nào để xử lý 
    - các operation (phép tính là phụ thuộc lẫn nhau) => nếu giả sử để async 
    function thì nó sẽ là 1 hàm bất đồng bộ (Async)
    - Nếu dùng Async function thì phải dùng rất nhiều await (==> Code rối và không tối ưu)
    
    từ các vấn đề trên ta chỉ nên dùng Normal function ko phải là Async Function 
    (trong JavaScript thì luôn chạy cơ chế "Async" vì thể họ phải dùng nhiều await hay then, Promise để tránh)
    còn Python default là đồng bộ 
"""


def background_image_upload(file: UploadFile, task_id: str, time: datetime, data: MlResult):
    file_name = task_id + config.ML_FACE_RECOGNITION_image_type
    dir_path = config.ML_FACE_RECOGNITION_storage_path / str(time_helpers.str_dd_mm_yyyy())
    storages_helpers.create_path(dir_path)
    abs_path_file_name = dir_path / file_name
    file_bytes = file.file.read()
    try:
        storages_helpers.upload_file_bytes(file_bytes, abs_path_file_name)
        data.time['end_upload'] = str(time_helpers.now_utc())
        data.status['upload_status'] = "SUCCESS"
        data.upload_result = {
            "path": str(abs_path_file_name),
            "file_type": config.ML_FACE_RECOGNITION_image_type
        }
        data_dump = json.dumps(data.__dict__)
        redis.set(task_id, data_dump)
        celery_execute.send_task(
            name="{}.{}".format(config.ML_FACE_RECOGNITION_query_name, config.ML_FACE_RECOGNITION_task),
            kwargs={
                'task_id': task_id,
                'data': data_dump,
            },
            queue=config.ML_FACE_RECOGNITION_query_name
        )
    except Exception as e:
        data.status['upload_status'] = "FAILED"
        data.status['general_status'] = "FAILED"
        data.error = str(e)
        redis.set(task_id, json.dumps(data.__dict__))
