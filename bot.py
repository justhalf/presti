# -*- coding: utf-8 -*-
"""
Here goes the program description
"""
import sys
import os
import discord
from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user: return
    if message.author.id != 261302296103747584: return
    if len(message.embeds) == 0: return

    for embed in message.embeds:
        if embed.type != 'rich': continue
        title = embed.title
        desc = embed.description
        fields = embed.fields
        footer = embed.footer
        msg = (f'Title: {title}\n'
               f'Desc: {desc}\n'
               f'Fields: [{len(fields)} fields]\n'
               f'Footer: {footer}')
        await message.channel.send(msg)

discord_token = os.environ['DISCORD_BOT_TOKEN']
client.run(discord_token)
