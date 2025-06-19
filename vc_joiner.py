import discord
import asyncio
from config import TOKENS, GUILD, OWNER


def make_bot():
    bot = discord.Client(intents=discord.Intents.default())

    @bot.event
    async def on_ready():
        print(f"{bot.user} awake")
        c = bot.get_guild(GUILD).get_member(OWNER).voice.channel
        await c.connect()

        def check(m):
            return m.channel == c and m.content == "!exit" and m.author.id == OWNER

        await bot.wait_for("message", check=check)
        print(f"{bot.user} going gentle into that good night")
        await bot.close()

    return bot


async def main():
    bots = []
    async with asyncio.TaskGroup() as tg:
        for token in TOKENS:
            bot = make_bot()
            bots.append(bot)
            tg.create_task(bot.start(token))


asyncio.run(main())
