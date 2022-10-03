from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class MlTimeHandler(BaseModel):
    start_upload: str = None
    end_upload: str = None
    start_face_rec: str = None
    end_face_rec: str = None


class MlStatusHandler(BaseModel):
    general_status: str = "PENDING"
    upload_status: str = "PENDING"
    face_rec_status: str = None


class MlResult(BaseModel):
    task_id: str
    status: dict = None
    time: dict = None
    upload_result: dict = None
    face_rec_result: list = None
    error: Optional[str] = None


class MlResponse(BaseModel):
    status: str = "PENDING"
    status_code: int
    time: datetime
    task_id: str
