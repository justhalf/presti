# -*- coding: utf-8 -*-
"""
Here goes the program description
"""
import sys
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='?', intents=intents)

AVRAE_USER_ID = 261302296103747584
MY_GUILD = discord.Object(id=799318267750514728)

# sync the slash command to your server
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.tree.command(name="rule", description="Lookup D&D 5e rules", guild=MY_GUILD)
async def slash_one(interaction: discord.Interaction, text: str = ''):
    await interaction.response.send_message(f'You got me: {text}')

@bot.command()
async def sync(ctx):
    if ctx.author.id == 471751375248687125:
        print(f'Received request to sync to {ctx.guild.name} ({ctx.guild.id})')
        await bot.tree.sync(guild=discord.Object(id=ctx.guild.id))
        await ctx.send('Command tree synced.')
    else:
        await ctx.send('You must be the bot owner to run this command!')

@bot.event
async def on_message(message):
    if message.author == bot.user: return
    if message.author.id != AVRAE_USER_ID:
        await bot.process_commands(message)
        return
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
bot.run(discord_token)
