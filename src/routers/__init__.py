from fastapi import APIRouter

router = APIRouter(
    prefix='/api/v1'
)

from .auth import router as auth_router
router.include_router(
    auth_router, 
    tags=['Auth'],
    prefix='/auth'
)

from .profile import router as profile_router
router.include_router(
    profile_router,
    tags=['Profile'],
    prefix='/profile'
)

from .chats import router as chats_router
router.include_router(
    chats_router,
    tags=['Chats'],
    prefix='/chats'
)

from .me import router as me_router
from .messages import router as messages_router

me_router_prefix = '/me/chats'

router.include_router(
    messages_router,
    tags=['Messages'],
    prefix=me_router_prefix + '/{chat_id}/msg'
)

router.include_router(
    me_router,
    tags=['Me'],
    prefix=me_router_prefix
)