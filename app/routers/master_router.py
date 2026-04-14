from fastapi import APIRouter
from app.routers import comment, listing, message

master_router = APIRouter()

master_router.include_router(comment.router)
master_router.include_router(listing.router)
master_router.include_router(message.router)
