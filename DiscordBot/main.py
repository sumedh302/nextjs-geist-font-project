#!/usr/bin/env python3
"""
Free Fire Discord Bot - Main Entry Point
A Discord bot that integrates with Free Fire to send likes to players
"""

import asyncio
import logging
import os
from bot import FreeFireLikeBot
from keep_alive import keep_alive

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

async def main():
    """Main function to run the Discord bot"""
    try:
        # Start keep-alive web server
        keep_alive()
        
        # Get Discord bot token from environment variables
        token = os.getenv("DISCORD_BOT_TOKEN")
        if not token:
            logger.error("DISCORD_BOT_TOKEN environment variable not set!")
            return
        
        # Initialize and run the bot
        bot = FreeFireLikeBot()
        await bot.start(token)
        
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Critical error occurred: {e}")
    finally:
        logger.info("Bot shutdown complete")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user interrupt")
