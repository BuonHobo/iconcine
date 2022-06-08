import asyncio
import discord
from discord.ext import tasks
from pathlib import Path
from random import choice
import datetime
import time

immagini = [immagine for immagine in Path.cwd().joinpath("immagini").iterdir()]
with open("token.tkn", "r") as file:
    tkn = file.readline().strip()


class MyClient(discord.Client):
    async def on_ready(self):
        update_icon.start(self)
        update_counter.start(self)
        print("Ready to go\n")


@tasks.loop(seconds=10)
async def update_counter(bot: MyClient):
    seconds:datetime.timedelta=(update_icon.next_iteration-datetime.datetime.now(datetime.timezone.utc)).seconds/60
    seconds=round(seconds)
    activity= discord.Game(f"Next in {seconds}'")
    await bot.change_presence(activity=activity)


@tasks.loop(minutes=60)
async def update_icon(bot):
    global immagini
    scelta = choice(immagini)
    guild: discord.Guild = bot.get_guild(703342439028490341)

    with scelta.open("rb") as immagine:
        icon = immagine.read()

    start = time.time()
    await guild.edit(reason="Cambio periodico dell'immagine", icon=icon)
    end = time.time()

    with open("log.csv","a+",newline="\n") as file:
        file.write(f"{datetime.datetime.now()},{scelta.name},{round(end-start,2)}\n")


intents = discord.Intents.default()
client = MyClient(intents=intents)
client.run(tkn)