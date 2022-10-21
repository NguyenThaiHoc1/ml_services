from fastapi import APIRouter
from api_endpoint.resources.v1 import hello
from api_endpoint.resources.v1.face_recognition import router as face_recognition
from api_endpoint.resources.v1.face_detection import router as face_detection

api_routers = APIRouter()

# TEST - FIELD: Test-API
api_routers.include_router(hello.router, prefix="/helloworld", tags=["Greetings"])

# MODEL - FIELD: FACE
api_routers.include_router(face_recognition.router, prefix="/face-reco", tags=["ML-Model"])
api_routers.include_router(face_detection.router, prefix="/face-det", tags=["ML-Model"])
