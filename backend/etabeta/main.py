import logging
import os
from pathlib import Path
from etabeta.common.logging import configure_logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from etabeta.sessions.sessions_route import router as sessions_route
from etabeta.session.session_route import router as session_route

app = FastAPI()

# configure logging
configure_logging()

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

log = logging.getLogger(__name__)
log.info("Starting EtaBeta server.")
