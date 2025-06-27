import discord
import asyncio
from config import TOKENS, GUILD, OWNER


class Bot(discord.Client):
    async def on_ready(self):
        print(f"{self.user} awake")
        c = self.get_guild(GUILD).get_member(OWNER).voice.channel
        await c.connect()


async def main():
    bots = []
    try:
        async with asyncio.TaskGroup() as tg:
            for token in TOKENS:
                bot = Bot(intents=discord.Intents.default())
                bots.append(bot)
                tg.create_task(bot.start(token))
    except asyncio.exceptions.CancelledError:
        print("Exiting cleanly")
        async with asyncio.TaskGroup() as tg:
            for bot in bots:
                tg.create_task(bot.close())
            await asyncio.sleep(2)
            raise


asyncio.run(main())
