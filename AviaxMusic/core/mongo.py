import sys
from motor.motor_asyncio import AsyncIOMotorClient

from config import MONGO_DB_URI
from ..logging import LOGGER

if not MONGO_DB_URI:
    LOGGER(__name__).error("MONGO_DB_URI not set! Please set it in environment variables.")
    sys.exit(1)

LOGGER(__name__).info("Connecting to MongoDB...")
try:
    _mongo_async_ = AsyncIOMotorClient(MONGO_DB_URI)
    mongodb = _mongo_async_.MusicBot
    LOGGER(__name__).info("Connected to MongoDB successfully.")
except Exception as e:
    LOGGER(__name__).error(f"Failed to connect to MongoDB: {e}")
    sys.exit(1)
