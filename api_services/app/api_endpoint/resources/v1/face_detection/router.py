from fastapi import (
    APIRouter, UploadFile, File,
    BackgroundTasks,
    HTTPException
)
from starlette.status import (
    HTTP_400_BAD_REQUEST, HTTP_200_OK
)

import uuid
import json
from settings import config
from redis_main import redis

from helpers import time as time_helper
from api_endpoint.serializers.serials_face_detection import (
    MlTimeHandler, MlStatusHandler, MlResult, MlResponse
)
from api_endpoint.resources.v1.face_detection.background_task import background_image_upload

router = APIRouter()


@router.post("/process")
async def ml_process(
        *,
        file: UploadFile = File(...),
        backgroundtasks: BackgroundTasks
):
    list_file_content_type = ["image/jpeg", "image/png"]
    if file.content_type not in list_file_content_type:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="this file_type is not support.")

    time_now = time_helper.now_utc()
    task_id = str(
        uuid.uuid5(namespace=uuid.NAMESPACE_OID, name=config.ML_FACE_DETECTION_query_name + "_" + str(time_now))
    )
    time_handler = MlTimeHandler(start_upload=str(time_now)).__dict__
    status_handler = MlStatusHandler().__dict__
    data = MlResult(
        task_id=task_id,
        status=status_handler,
        time=time_handler,
    )
    redis.set(task_id, json.dumps(data.__dict__))
    backgroundtasks.add_task(background_image_upload, file, task_id, time_now, data)
    return MlResponse(
        status_code=HTTP_200_OK,
        time=time_now,
        task_id=task_id
    )


@router.get("/status/{task_id}", response_model=MlResult)
def ml_get_status(
        *,
        task_id: str
):
    data = redis.get(task_id)
    if data is None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="task id not found!")

    message = json.loads(data)
    return message
