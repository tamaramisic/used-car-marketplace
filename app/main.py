from fastapi import FastAPI
from .master_router import master_router


app = FastAPI()

app.include_router(master_router)