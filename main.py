from fastapi import FastAPI

from routes import trains_routes

app = FastAPI()

app.include_router(trains_routes.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
