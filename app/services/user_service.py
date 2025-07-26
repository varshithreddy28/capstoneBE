from app.database.mongo import db
from app.utils.hash import hash_password
from fastapi import HTTPException

async def create_user(email: str, password: str, interests: list):
    user_collection = db["users"]
    if await user_collection.find_one({"email": email}):
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = hash_password(password)
    user = {"email": email, "hashed_password": hashed, "interests": interests}
    result = await user_collection.insert_one(user)
    return str(result.inserted_id)
