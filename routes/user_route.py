from fastapi import APIRouter
from database import users_collection
from models.user import User

router = APIRouter()


@router.post("/Addusers")
def add_user(user: User):
    users_collection.insert_one(user.model_dump())
    return {"message": "User Added Successfully"}


@router.get("/users")
def get_all_users():
    users = []
    for user in users_collection.find():
        user["_id"] = str(user["_id"])
        users.append(user)

    return users


@router.get("/users/{name}")
def get_user(name: str):
    user = users_collection.find_one({"name": name})
    if not user:
        return {"message": "User not found"}
    user["_id"] = str(user["_id"])

    return user


@router.put("/users/{name}")
def increment_age(name: str):
    user = users_collection.find_one({"name": name})
    if not user:
        return {"message": "User not found"}
    users_collection.update_one(
        {"name": name},
        {"$inc": {"age": 1}}
    )
    updated = users_collection.find_one({"name": name})
    updated["_id"] = str(updated["_id"])

    return updated


@router.delete("/users/{name}")
def delete_user(name: str):
    user = users_collection.find_one({"name": name})
    if not user:
        return {"message": "User not found"}
    users_collection.delete_one({"name": name})

    return {"message": "User deleted successfully"}