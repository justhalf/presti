# -*- coding: utf-8 -*-
"""
Here goes the program description
"""
import sys
import os
import discord
import sqlite3 as sql
import dbman
import re
from pathlib import Path
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
    # dbman.init_db()
    print(f'Logged in as {bot.user}')

@bot.tree.command(name="rule", description="Lookup D&D 5e rules")
async def rule(interaction: discord.Interaction, query: str):
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
    got_critted, rolled_1dex = parse_message(message)
    if got_critted or rolled_1dex:
        crit_s = '\n* '.join(['']+[f'**{name}**' for name in got_critted])
        dex1_s = '\n* '.join(['']+[f'**{name}**' for name in rolled_1dex])
        crit_s = f'These characters got hit by a critical hit:{crit_s}' if crit_s else ''
        dex1_s = f'These characters rolled 1 on a Dex save:{dex1_s}' if dex1_s else ''
        msg = '\n'.join(f for f in [crit_s, dex1_s] if f)
        msg = f'{msg}\n:information_source: Check for on-crit or Alchemist\'s Potion Belt effect'
        await message.reply(msg)

def parse_message(message):
    for embed in message.embeds:
        if embed.type != 'rich': continue
        break
    
    title = embed.title
    footer = embed.footer
    desc = embed.description
    fields = embed.fields
    fields_s = ', '.join(f.name for f in fields if f and f.name)
    fields_s = f'[{fields_s}]'

    got_critted = []
    rolled_1dex = []
    try:
        field_name = None
        for field in fields:
            if not field.name: continue
            if field.name != '** **': field_name = field.name
            hits = field.value.split('**To Hit**')[1:]
            hits = [h.split('\n', 1) for h in hits]
            for hit in hits:
                if 'CRIT!' in hit[1]:
                    if field_name not in got_critted:
                        got_critted.append(field_name)
                    break
            saves = field.value.split('**DEX Save**')[1:]
            saves = [s.split('\n', 1) for s in saves]
            for save in saves:
                save = re.sub('~~[0123456789*]+~~(, ?)?', '', save[0]).replace(', )', ')')
                if '**1**' in save:
                    if field_name not in rolled_1dex:
                        rolled_1dex.append(field_name)
                    break

        msg = (f'Title: {title}\n'
               f'Desc: {desc}\n'
               f'Fields: [{len(fields)} fields: {fields_s}]\n'
               f'Footer: {footer}\n'
               f'Time: {message.created_at}')
    except:
        print(msg)
    return got_critted, rolled_1dex

discord_token = os.environ['DISCORD_BOT_TOKEN']
bot.run(discord_token)
