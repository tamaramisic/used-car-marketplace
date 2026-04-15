from fastapi import APIRouter
from app.routers import comment, listing, chat

master_router = APIRouter()

master_router.include_router(comment.router)
master_router.include_router(listing.router)
master_router.include_router(chat.router)
