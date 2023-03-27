from fastapi import APIRouter, Request, Body, status, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from models.user_model import UserBase, LoginUser, CurrentUser, UserCreate
from models.authentication import Authorization
from typing import Optional, List

user = APIRouter(prefix="/users", tags=["users"])
auth_handler = Authorization()


@user.get("/", response_description="List all users")
async def welcome():
    return {"message": "Welcome to the user module"}


@user.post("/register", response_description="Register a new user")
async def register_user(request: Request, user: UserCreate = Body(...)) -> UserBase:
    user.password = auth_handler.get_password_hash(user.password)
    user = jsonable_encoder(user)

    if (existing_email := await request.app.state.db["users"].find_one({"email": user["email"]})) is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Email {user['email']} already registered")

    if (existing_username := await request.app.state.db["users"].find_one({"username": user["username"]})) is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Username {user['username']} already registered")

    user = await request.app.state.db["users"].insert_one(user)
    new_user = await request.app.state.db["users"].find_one({"_id": ObjectId(user.inserted_id)})
    new_user["_id"] = str(new_user["_id"])
    new_user.pop("password")
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=new_user)


@user.post("/login", response_description="Login a user")
async def login(request: Request, login_user: LoginUser = Body(...)) -> str:
    user = await request.app.state.db["users"].find_one({"email": login_user.email})
    if (user is None) or (not auth_handler.verify_password(login_user.password, user["password"])):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect email or password")

    token = auth_handler.encode_token(str(user["_id"]))
    return JSONResponse(content={"token": token})


@user.post("/me", response_description="Get current user")
async def get_current_user(request: Request, user_id=Depends(auth_handler.auth_wrapper)) -> CurrentUser:
    user = await request.app.state.db["users"].find_one({"_id": ObjectId(user_id)})
    user["_id"] = str(user["_id"])
    user.pop("password")
    return JSONResponse(status_code=status.HTTP_200_OK, content=user)
