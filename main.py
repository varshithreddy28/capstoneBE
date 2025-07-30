from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.user_routes import router as user_router
from app.routes.auth_routes import router as auth_router
from app.routes.chatroutes import router as chat_router
from app.database.mongo import db
from app.database.ttl import create_ttl_index

app = FastAPI()

# Allow all origins (open CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# Register your routers
app.include_router(user_router, prefix="/api/users", tags=["Users"])
app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
app.include_router(chat_router, prefix="/api", tags=["Chat"])

@app.on_event("startup")
async def startup_event():
    # Ensure TTL index exists
    await create_ttl_index()
