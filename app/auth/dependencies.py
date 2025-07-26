from fastapi import HTTPException, Depends
from app.auth.jwt_handler import decode_access_token
from app.database.mongo import db
from app.auth.jwt_auth import JWTBearer

async def get_user_from_token(token: str):
    try:
        payload = decode_access_token(token)
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token payload")

        user = await db["users"].find_one({"email": email})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user["_id"] = str(user["_id"])
        return user

    except Exception as e:
        raise HTTPException(status_code=401, detail="Token is invalid or expired")


from app.schemas.user_schema import UserSchema

async def get_current_user_from_token(token: str = Depends(JWTBearer())) -> UserSchema:
    user_dict = await get_user_from_token(token)

    return UserSchema(
        id=user_dict["_id"],
        email=user_dict["email"],
        interests=user_dict.get("interests", [])
    )

