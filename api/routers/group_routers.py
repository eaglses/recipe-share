from fastapi import (
    Depends,
    APIRouter,
)
from authenticator import authenticator


router = APIRouter(tags=["group"])
