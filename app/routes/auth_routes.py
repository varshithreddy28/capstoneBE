from fastapi import APIRouter, Depends, HTTPException
from app.schemas.auth_schema import LoginSchema, TokenResponse
from app.auth.jwt_handler import create_access_token
from app.utils.hash import verify_password
from app.database.mongo import db
from app.schemas.user_schema import UserSchema
from app.auth.jwt_auth import JWTBearer
from app.auth.dependencies import get_user_from_token

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
async def login(data: LoginSchema):
    user = await db["users"].find_one({"email": data.email})
    if not user or not verify_password(data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user["email"]})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserSchema, dependencies=[Depends(JWTBearer())])
async def get_me(token: str = Depends(JWTBearer())):
    user = await get_user_from_token(token)
    return {
        "id": user["_id"],
        "email": user["email"],
        "interests": user.get("interests", [])
    }