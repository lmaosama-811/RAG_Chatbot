from fastapi import FastAPI

from .api import upload,chat

app = FastAPI()

app.include_router(upload.router)
app.include_router(chat.router)
