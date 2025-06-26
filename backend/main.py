import asyncio
import sys

# Dieser Block behebt ein Kompatibilitätsproblem von Playwright/Asyncio unter Windows
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from fastapi import FastAPI
#from backend.backend.routers import OpenAIAgentsRouter, PerplexityAgentsRouter
from .routers import AnalyzeAllRouter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Einbinden der verschiedenen API-Routen
app.include_router(AnalyzeAllRouter.router)
#app.include_router(OpenAIAgentsRouter.router)
#app.include_router(PerplexityAgentsRouter.router)

# Standard-Endpunkt zur Überprüfung, ob der Server läuft
@app.get("/")
async def root():
    return {"message": "Hello World"}

# Einfacher Test-Endpunkt
@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}