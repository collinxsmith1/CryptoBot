#!/usr/bin/env python3

# Discord bot for getting crypto information

#%% LIBRARIES #######################################################################
import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands, tasks

# https://discordpy.readthedocs.io/en/stable/ext/tasks/index.html

import json
import asyncio
import time
import os
import sys

from datetime import timedelta, datetime
import aiohttp
import aiofiles
import random
import glob

import matplotlib.pyplot as plt

from botPaths import *

#%% CONSTANTS #######################################################################

CVERSION = "v0.1"
DSTHourSub = -6 # DSTHourSub= -6 for CDT (Fall), -5 for CST (Spring)

with open(os.path.join(authPath, "cryptobot.json")) as auth:
    secret = json.loads(auth.read())

#%% FUNCTIONS #######################################################################

#%% BOT #############################################################################

botintents = discord.Intents.default()
bot = discord.Bot(intents=botintents)
# loop = asyncio.get_event_loop()

#%% BOT EVENTS ######################################################################

class CryptoBotStats(commands.Cog):
    def __init__(self, bot_: discord.Bot):
        self.bot = bot_
        self.task_stat_loop.start()

    def cog_unload(self):
        self.self.task_stat_loop.cancel()

    @tasks.loop(hours=1)
    async def task_stat_loop(self):
        await asyncio.sleep(5)
        print("Running CryptoBot 1 hour loop")
        numGuilds = len(bot.guilds)
        print(f"CryptoBot in {numGuilds} guilds")
    
    @task_stat_loop.before_loop
    async def before_task_stat_loop(self):
        await self.bot.wait_until_ready()


class CryptoBotBackground(commands.Cog):
    def __init__(self, bot_: discord.Bot):
        self.bot = bot_
        self.change_status.start()
    
    def cog_unload(self):
        self.change_status.cancel()

    @tasks.loop(hours=6.0)
    async def change_status(self):
        print("Renewed bot status")
        action = discord.Game(f"/intro | {CVERSION}")
        await self.bot.change_presence(status=discord.Status.online, activity=action)
    
    @change_status.before_loop
    async def before_change_status(self):
        print("Logging in...")
        await self.bot.wait_until_ready()

    @commands.slash_command(
        name="crypto_dev",
        description="development command",
        checks=[commands.is_owner().predicate]
    )
    async def crypto_dev(self, ctx: discord.ApplicationContext):
        """development command"""
        # await ctx.defer()
        await ctx.respond(f"CryptoBot development command response")


class CryptoBot(discord.Cog):
    def __init__(self, bot_: discord.Bot):
        self.bot = bot_
        
    @bot.event
    async def on_ready():
        print(f"Logged in as {bot.user} (ID: {bot.user.id})")
        print(f"running code version {CVERSION}")
        print(f"API version: {discord.__version__}")
        print("-------------------")

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.respond(error)
        elif isinstance(error, commands.NotOwner):
            await ctx.respond("You can't use that command!")
        else:
            raise error

    @bot.event
    async def on_guild_join(guild: discord.Guild):
        pTime = (datetime.utcnow() + timedelta(hours=DSTHourSub)).strftime("%H%M%S") # DSTHourSub= -6 for CDT (Fall), -5 for CST (Spring)
        print(f"{pTime}: Client has joined a Guild: {guild} -- {str(guild.id)}")

    @bot.event
    async def on_guild_remove(guild: discord.Guild):
        pTime = (datetime.utcnow() + timedelta(hours=DSTHourSub)).strftime("%H%M%S") # DSTHourSub= -6 for CDT (Fall), -5 for CST (Spring)
        print(f"{pTime}: banned/kicked/left the Guild or Guild was deleted: {guild} -- {str(guild.id)}")


    crypto_cmd = SlashCommandGroup("crypto", "Base command to interact with CryptoBot")

    @crypto_cmd.command()
    async def help(self, ctx: discord.ApplicationContext):
        """
        Get general CryptoBot info to help get started
        """
        MEM = ctx.author
        MEMID = str(MEM.id)
        TXCHAN = ctx.channel
        GUILD = None
        dm_flag = False
        print(f"/crypto help - by {MEM}")
        
        if TXCHAN.type == discord.ChannelType.private:
            botName = f"{bot.user.name}"
            dm_flag = True
        elif TXCHAN.type == discord.ChannelType.text:
            GUILD = TXCHAN.guild
            botName = f"{GUILD.me.display_name}"
        
        dm_channel = MEM.dm_channel

        if dm_channel == None:
            print(f"dm channel does not exist, creating one with {MEM}")
            dm_channel = await MEM.create_dm()
        else:
            print(f"existing dm found with {MEM}, sent a message")

        embed1 = discord.Embed(title = f"Greetings, I am {botName}!",
            color=discord.Color.gold())
        
        gMsg = "I listen for commands and respond with information about cryptocurrencies.\nMy prefix is `/crypto`"
        embed1.add_field(name="What can I do?", value=gMsg, inline=False)

        sCommands = "say `/crypto add` to see how you can add a crypto token to your watchlist"
        embed1.add_field(name="To Get Started", value=sCommands, inline=False)

        gCommands = "`/crypto help` - See this help message \n \
            `/crypto list` - Return your list of indexed watchlist tokens \n \
            `/crypto remove` - Remove an crypto token from your watchlist"
        embed1.add_field(name="General Commands", value=gCommands, inline=False)

        if dm_flag:
            await dm_channel.send(embed = embed1)
        else:
            await ctx.respond(embed = embed1)


    @crypto_cmd.command()
    async def list(self, ctx: discord.ApplicationContext):
        """
        Get your watchlist of crypto tokens
        """
        MEM = ctx.author
        MEMID = str(MEM.id)
        TXCHAN = ctx.channel
        GUILD = TXCHAN.guild
        GUILDID = str(GUILD.id)

        print('/intro list by {} in {} of {}'.format(MEM, TXCHAN, GUILD))

        await ctx.defer()
        await asyncio.sleep(3)
        await ctx.respond(f"here is your list, {MEM}")


#%% RUN #############################################################################

bot.add_cog(CryptoBotStats(bot))
bot.add_cog(CryptoBotBackground(bot))
bot.add_cog(CryptoBot(bot))
bot.run(secret["token"])