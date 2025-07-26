from fastapi import APIRouter
from app.schemas.user_schema import UserCreateSchema, UserSchema
from app.services.user_service import create_user

router = APIRouter()

@router.post("/register", response_model=UserSchema)
async def register(user: UserCreateSchema):
    user_id = await create_user(user.email, user.password, user.interests)
    return {"id": user_id, "email": user.email, "interests": user.interests}
