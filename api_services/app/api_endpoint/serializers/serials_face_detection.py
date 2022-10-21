from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class MlTimeHandler(BaseModel):
    start_upload: str = None
    end_upload: str = None
    start_face_det: str = None
    end_face_det: str = None


class MlStatusHandler(BaseModel):
    general_status: str = "PENDING"
    upload_status: str = "PENDING"
    face_det_status: str = None


class MlResult(BaseModel):
    task_id: str
    status: dict = None
    time: dict = None
    upload_result: dict = None
    face_det_result: list = None
    error: Optional[str] = None


class MlResponse(BaseModel):
    status: str = "PENDING"
    status_code: int
    time: datetime
    task_id: str
