from app.database.mongo import db

async def create_ttl_index():
    await db["chat_sessions"].create_index(
        "createdAt",
        expireAfterSeconds=86400,  # 24 hours
        name="chatSessionTTL"
    )
