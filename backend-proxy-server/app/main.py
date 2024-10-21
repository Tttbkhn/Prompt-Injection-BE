from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.messages import NewMessage
from contextlib import asynccontextmanager
from beanie import init_beanie

from db import db

from routers import detection

origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://chatbox.guru"
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_beanie(
        database=db,
        document_models=[
            NewMessage
        ],
    )
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(detection.router)