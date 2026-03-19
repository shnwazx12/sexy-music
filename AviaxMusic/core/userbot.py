from pyrogram import Client

import config
from ..logging import LOGGER

assistants = []
assistantids = []


def _make_client(name, session_string):
    """Only create client if session_string is set."""
    if not session_string:
        return None
    return Client(
        name=name,
        api_id=config.API_ID,
        api_hash=config.API_HASH,
        session_string=session_string,
        no_updates=True,
        in_memory=True,
    )


class Userbot:
    def __init__(self):
        self.one   = _make_client("AviaxAss1", config.STRING1)
        self.two   = _make_client("AviaxAss2", config.STRING2)
        self.three = _make_client("AviaxAss3", config.STRING3)
        self.four  = _make_client("AviaxAss4", config.STRING4)
        self.five  = _make_client("AviaxAss5", config.STRING5)

    async def _start_one(self, client, num):
        await client.start()
        try:
            await client.join_chat("NexGenBots")
            await client.join_chat("NexGenBotsIndia")
        except Exception:
            pass
        assistants.append(num)
        try:
            await client.send_message(config.LOG_GROUP_ID, f"Assistant {num} Started ✅")
        except Exception:
            LOGGER(__name__).error(
                f"Assistant {num} could not access LOG_GROUP_ID. "
                "Add it to the group and promote as admin!"
            )
            exit()
        client.id = client.me.id
        client.name = client.me.mention
        client.username = client.me.username
        assistantids.append(client.id)
        LOGGER(__name__).info(f"Assistant {num} started as {client.name}")

    async def start(self):
        LOGGER(__name__).info("Starting Assistants...")
        for num, client in enumerate(
            [self.one, self.two, self.three, self.four, self.five], 1
        ):
            if client:
                await self._start_one(client, num)

    async def stop(self):
        LOGGER(__name__).info("Stopping Assistants...")
        for client in [self.one, self.two, self.three, self.four, self.five]:
            try:
                if client:
                    await client.stop()
            except Exception:
                pass
