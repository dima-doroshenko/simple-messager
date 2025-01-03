from fastapi import APIRouter

router = APIRouter(
    prefix='/api'
)

from .auth import router as auth_router
router.include_router(
    auth_router, 
    tags=['Auth'],
    prefix='/auth'
)