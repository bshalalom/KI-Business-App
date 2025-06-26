from fastapi import FastAPI
from backend.routers import AnalyzeAllRouter
from backend.routers import OpenAIAgentsRouter
from backend.routers import PerplexityAgentsRouter

app = FastAPI()

# Binde alle Router ein
app.include_router(AnalyzeAllRouter.router)
app.include_router(OpenAIAgentsRouter.router)
app.include_router(PerplexityAgentsRouter.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
