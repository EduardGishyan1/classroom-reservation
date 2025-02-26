from motor.motor_asyncio import AsyncIOMotorClient
from app.config.settings import settings

client = AsyncIOMotorClient(settings.MONGO_URI)

db = client.get_database("classrooms")

schedule_collection = db.get_collection("schedules")
user_collection = db.get_collection("users")