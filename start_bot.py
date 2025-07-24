#!/usr/bin/env python3
"""
Start script for Telegram Video Processing Bot
This script can be used to run the bot directly or via GitHub Actions
"""

import os
import sys
import asyncio
import logging
from bot import TelegramVideoBot

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    """Main function to start the bot"""
    try:
        # Check if token is provided
        if not os.getenv('TELEGRAM_TOKEN'):
            logger.error("TELEGRAM_TOKEN environment variable is required")
            sys.exit(1)
        
        # Initialize and run the bot
        logger.info("Initializing Telegram Video Processing Bot...")
        bot = TelegramVideoBot()
        
        # Run the bot
        asyncio.run(bot.run())
        
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot failed to start: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()