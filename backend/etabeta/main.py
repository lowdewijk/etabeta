import os
from pathlib import Path
import logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from etabeta.sessions.sessions_route import router as sessions_route
from etabeta.session.session_route import router as session_route

app = FastAPI()

# Get the uvicorn logger
uvicorn_logger = logging.getLogger("fastapi")
uvicorn_logger.setLevel(logging.WARNING)

origins = [
    "*",  # for development
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


cwd = Path(os.path.dirname(os.path.abspath(__file__)))
static_data = cwd.joinpath("static_data")
app.mount("/static", StaticFiles(directory=static_data, html=True), name="static")
app.include_router(sessions_route)
app.include_router(session_route)
