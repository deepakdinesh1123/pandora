import motor.motor_asyncio

MONGO_DETAILS = "mongodb://localhost:27017"

db_client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
