from fastapi import APIRouter
from api_endpoint.resources.v1 import hello
from api_endpoint.resources.v1.face_recognition import router as face_recognition

api_routers = APIRouter()

api_routers.include_router(hello.router, prefix="/helloworld", tags=["Greetings"])
api_routers.include_router(face_recognition.router, prefix="/face-reco", tags=["ML-Model"])
