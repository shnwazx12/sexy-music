import asyncio
import importlib

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from AviaxMusic import LOGGER, app, userbot
from AviaxMusic.core.call import Aviax
from AviaxMusic.misc import sudo
from AviaxMusic.plugins import ALL_MODULES
from AviaxMusic.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS

# Start Render health-check server (binds PORT so Render keeps service alive)
from render_health import start_health_server
start_health_server()


async def init():
    if not any([config.STRING1, config.STRING2, config.STRING3,
                config.STRING4, config.STRING5]):
        LOGGER(__name__).error("No STRING_SESSION defined. Please set at least STRING_SESSION.")
        exit()

    await sudo()

    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except Exception:
        pass

    await app.start()

    for all_module in ALL_MODULES:
        importlib.import_module("AviaxMusic.plugins" + all_module)
    LOGGER("AviaxMusic.plugins").info("Successfully Imported All Modules.")

    await userbot.start()
    await Aviax.start()

    try:
        await Aviax.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("AviaxMusic").error(
            "Please enable video chat in your LOG_GROUP_ID channel/group and restart."
        )
        exit()
    except Exception:
        pass

    await Aviax.decorators()
    LOGGER("AviaxMusic").info("MusicBot Started Successfully on Render!")

    await idle()
    await app.stop()
    await userbot.stop()
    LOGGER("AviaxMusic").info("MusicBot Stopped.")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
