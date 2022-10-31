from fastapi import APIRouter

from endpoints import endpoints

api_router = APIRouter()
api_router.include_router(endpoints.app, tags=["books"])

