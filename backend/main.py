from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException

import sessions_route
import session_route

app = FastAPI()

origins = [
    "http://localhost:4000", # for development
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(sessions_route.router)
app.include_router(session_route.router)