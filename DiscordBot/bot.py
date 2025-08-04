"""
Free Fire Discord Bot - Main Bot Class
Handles bot initialization, events, and command loading
"""

import discord
from discord.ext import commands
import aiohttp
import asyncio
import logging
import json
import os
from datetime import datetime
from config import BotConfig
from database import UserDatabase
from utils import BotUtils

logger = logging.getLogger(__name__)

class FreeFireLikeBot(commands.Bot):
    """Main Discord bot class for Free Fire like system"""
    
    def __init__(self):
        # Configure intents
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.members = True
        
        # Initialize bot with prefix and intents
        super().__init__(
            command_prefix=BotConfig.PREFIX,
            intents=intents,
            help_command=None,
            case_insensitive=True,
            strip_after_prefix=True
        )
        
        # Initialize components
        self.config = BotConfig()
        self.db = UserDatabase()
        self.utils = BotUtils()
        self.session = None
        
    async def setup_hook(self):
        """Setup hook called when bot is starting"""
        logger.info("Setting up bot...")
        
        # Create aiohttp session
        self.session = aiohttp.ClientSession()
        
        # Load cogs
        try:
            await self.load_extension('commands.freefire')
            logger.info("Loaded Free Fire commands")
        except Exception as e:
            logger.error(f"Failed to load Free Fire commands: {e}")
        
        # Sync slash commands
        try:
            synced = await self.tree.sync()
            logger.info(f"Synced {len(synced)} slash commands")
        except Exception as e:
            logger.error(f"Failed to sync slash commands: {e}")
            # Try to sync guild-specific commands as fallback
            try:
                for guild in self.guilds:
                    await self.tree.sync(guild=guild)
                logger.info("Synced guild-specific commands as fallback")
            except Exception as guild_sync_error:
                logger.error(f"Guild sync also failed: {guild_sync_error}")
    
    async def on_ready(self):
        """Called when bot is ready"""
        if self.user:
            logger.info(f"{self.user} is now online!")
            logger.info(f"Bot ID: {self.user.id}")
        logger.info(f"Guilds: {len(self.guilds)}")
        
        # Set bot activity
        activity = discord.Activity(
            type=discord.ActivityType.watching,
            name="Free Fire players | /like"
        )
        await self.change_presence(activity=activity)
    
    async def on_command_error(self, ctx, error):
        """Global error handler for commands"""
        if isinstance(error, commands.CommandNotFound):
            return
        
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title="❌ Missing Arguments",
                description=f"Missing required argument: `{error.param.name}`",
                color=0xE74C3C
            )
            await ctx.reply(embed=embed, ephemeral=True)
            return
        
        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(
                title="❌ Invalid Argument",
                description="Please check your input and try again.",
                color=0xE74C3C
            )
            await ctx.reply(embed=embed, ephemeral=True)
            return
        
        logger.error(f"Unhandled command error: {error}")
        
        embed = discord.Embed(
            title="❌ An Error Occurred",
            description="An unexpected error occurred. Please try again later.",
            color=0xE74C3C
        )
        try:
            await ctx.reply(embed=embed, ephemeral=True)
        except:
            pass
    
    async def close(self):
        """Clean up when bot is shutting down"""
        logger.info("Shutting down bot...")
        
        if self.session:
            await self.session.close()
        
        await super().close()
