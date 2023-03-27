from fastapi import FastAPI
import pydantic
from bson import ObjectId
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.middleware.cors import CORSMiddleware

# Modules
from modules.cars.cars_module import cars
from modules.users.users_module import user

# Config env
from decouple import config

# Database
DB_URL = config("DB_URL")
DB_NAME = config("DB_NAME")

# CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db = AsyncIOMotorClient(DB_URL)[DB_NAME]
    yield
    app.state.db.client.close()


app = FastAPI(
    lifespan=lifespan,
    arbitrary_types_allowed=True,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str


app.include_router(cars)
app.include_router(user)


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8010,
        reload=True,
    )
