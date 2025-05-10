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

DEV_ID = int(os.environ['DEV_ID'])
bot = commands.Bot(command_prefix='?',
                   owner_ids=[DEV_ID],
                   intents=intents,
                   )

AVRAE_USER_ID = 261302296103747584
TEST_GUILD = discord.Object(id=os.environ['TEST_GUILD_ID'])

# sync the slash command to your server
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.tree.command(name="rule", description="Lookup D&D 5e rules")
async def slash_one(interaction: discord.Interaction, query: str):
    await interaction.response.send_message(f'Your query is: {query}')

global_synced = []
@bot.command()
async def sync(ctx, *args):
    if ctx.author.id == DEV_ID:
        print(f'Received request to sync to {ctx.guild.name} ({ctx.guild.id})')
        if not global_synced and args and args[0].lower() == 'all':
            global_synced.append(1)
            await bot.tree.sync()
            await ctx.send('Command tree synced globally.')
        else:
            await bot.tree.sync(guild=discord.Object(id=ctx.guild.id))
            await ctx.send('Command tree synced on this server.')
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
