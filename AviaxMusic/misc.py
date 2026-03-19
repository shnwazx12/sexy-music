import socket
import time

from pyrogram import filters

import config
from AviaxMusic.core.mongo import mongodb
from .logging import LOGGER

SUDOERS = filters.user()
HAPP = None
_boot_ = time.time()


def is_heroku():
    return "heroku" in socket.getfqdn()


XCB = [
    "/", "@", ".", "com", ":", "git", "heroku", "push",
    str(config.HEROKU_API_KEY),
    "https",
    str(config.HEROKU_APP_NAME),
    "HEAD", "master",
]


def dbb():
    global db
    db = {}
    LOGGER(__name__).info("Local Database Initialized.")


async def sudo():
    global SUDOERS
    if config.OWNER_ID:
        SUDOERS.add(config.OWNER_ID)
    sudoersdb = mongodb.sudoers
    sudoers = await sudoersdb.find_one({"sudo": "sudo"})
    sudoers = [] if not sudoers else sudoers.get("sudoers", [])
    if config.OWNER_ID and config.OWNER_ID not in sudoers:
        sudoers.append(config.OWNER_ID)
        await sudoersdb.update_one(
            {"sudo": "sudo"},
            {"$set": {"sudoers": sudoers}},
            upsert=True,
        )
    for user_id in sudoers:
        SUDOERS.add(user_id)
    LOGGER(__name__).info("Sudoers Loaded.")


def heroku():
    global HAPP
    if is_heroku() and config.HEROKU_API_KEY and config.HEROKU_APP_NAME:
        try:
            import heroku3
            Heroku = heroku3.from_key(config.HEROKU_API_KEY)
            HAPP = Heroku.app(config.HEROKU_APP_NAME)
            LOGGER(__name__).info("Heroku App Configured")
        except Exception as e:
            LOGGER(__name__).warning(f"Heroku config error: {e}")
