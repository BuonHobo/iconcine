from lib2to3.pgen2 import token
import discord
from discord.ext import tasks
from pathlib import Path
from random import choice

immagini=[immagine for immagine in Path.cwd().joinpath("immagini").iterdir()]
with open("token.txt","r") as file:
    tkn=file.readline().strip()

class MyClient(discord.Client):
    async def on_ready(self):
        slow_count.start(self)
        print("Ready to go")
        

@tasks.loop(minutes=60)
async def slow_count(bot):
    global immagini
    scelta = choice(immagini)
    print(f'I\'m about to change server icon to {scelta}')
    guild:discord.Guild=bot.get_guild(703342439028490341)
    with scelta.open("rb") as immagine:
        icon=immagine.read()
    await guild.edit(reason="Cambio periodico dell'immagine",icon=icon)
    print("done")


intents = discord.Intents.default()
client = MyClient(intents=intents)
client.run(tkn)