from fastapi import APIRouter
from app.routers import comment, listing, chat, user, role

master_router = APIRouter()

master_router.include_router(comment.router)
master_router.include_router(listing.router)
master_router.include_router(user.router)
master_router.include_router(role.router)


master_router.include_router(chat.router)
