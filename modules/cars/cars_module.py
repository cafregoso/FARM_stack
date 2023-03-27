from fastapi import APIRouter, Request, Body, status, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from typing import Optional, List
from models.car_model import CarDB, CarUpdate, CarBase
from models.authentication import Authorization

cars = APIRouter(prefix="/cars", tags=["cars"])
auth_handler = Authorization()


@cars.get("/", response_description="List all cars")
async def list_cars(
    request: Request,
    min_price: int = 0,
    max_price: int = 1000000,
    page: int = 1,
    brand: Optional[str] = None,
    user_id: str = Depends(auth_handler.auth_wrapper)
) -> List[CarDB]:
    result_per_page = 25
    skip = (page - 1) * result_per_page
    query = {"price": {"$gte": min_price, "$lte": max_price}}
    if brand:
        query["brand"] = brand

    full_query = request.app.state.db["cars"].find(
        query).sort("_id", 1).skip(skip).limit(result_per_page)
    results = [car async for car in full_query]
    return results


@cars.post("/create", response_description="Create a new car")
async def create_car(
    request: Request,
    car: CarBase = Body(...),
    user_id: str = Depends(auth_handler.auth_wrapper)
):
    car = jsonable_encoder(car)
    car["owner"] = user_id
    new_car = await request.app.state.db["cars"].insert_one(car)
    created_car = await request.app.state.db["cars"].find_one({"_id": ObjectId(new_car.inserted_id)})
    created_car["_id"] = str(created_car["_id"])
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_car)


@cars.get("/{id}", response_description="Get a single car")
async def get_car(request: Request, id: str):
    if (car := await request.app.state.db["cars"].find_one({"_id": ObjectId(id)})) is not None:
        car["_id"] = str(car["_id"])
        return JSONResponse(status_code=status.HTTP_200_OK, content=car)
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": f"Car with {id} not found"})


@cars.patch("/{id}", response_description="Update a car")
async def update_car(
    request: Request,
    id: str,
    car: CarUpdate = Body(...),
    user_id: str = Depends(auth_handler.auth_wrapper)
):
    user = await request.app.state.db["users"].find_one({"_id": ObjectId(user_id)})
    find_car = await request.app.state.db["cars"].find_one({"_id": ObjectId(id)})

    if find_car["owner"] != user_id and not user["role"] != "Admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Only the owner or admin can update a car")

    await request.app.state.db["cars"].update_one({"_id": ObjectId(id)}, {"$set": car.dict(exclude_unset=True)})
    if (car := await request.app.state.db["cars"].find_one({"_id": ObjectId(id)})) is not None:
        car["_id"] = str(car["_id"])
        return JSONResponse(status_code=status.HTTP_200_OK, content=car)
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": f"Car with {id} not found"})


@cars.delete("/{id}", response_description="Delete a car")
async def delete_car(request: Request, id: str):
    delete_result = await request.app.state.db["cars"].delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={"message": f"Car with {id} deleted"})
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": f"Car with {id} not found"})
