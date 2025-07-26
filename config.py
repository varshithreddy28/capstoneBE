import os
from dotenv import load_dotenv

load_dotenv()
print("Mongo URL")
print(os.environ.get("MONGO_URI"))
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.environ.get("DB_NAME", "fastapi_app")
SECRET_KEY = os.environ.get("SECRET_KEY", "fastapi_app")

