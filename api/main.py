from fastapi import FastAPI

from db import init_db
from routes import trains_routes

init_db()

app = FastAPI()

app.include_router(trains_routes.router)


@app.get("/")
async def root():
    return {"message": "Hello World", "docs": "http://localhost:8000/docs"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
