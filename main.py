from fastapi import FastAPI
from app.routes.user_routes import router as user_router
from app.routes.auth_routes import router as auth_router
from app.database.mongo import db
from app.routes.chatroutes import router as chat_router
from app.database.ttl import create_ttl_index

app = FastAPI()    

app.include_router(user_router, prefix="/api/users", tags=["Users"])
app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
app.include_router(chat_router, prefix="/api", tags=["Chat"])

@app.on_event("startup")
async def startup_event():
    # Ensure TTL index exists
    await create_ttl_index()