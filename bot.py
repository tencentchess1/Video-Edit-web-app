import os
import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from telegram.constants import ParseMode
from video_processor import VideoProcessor
from config import Config
from utils import format_file_size, cleanup_temp_files
import tempfile
import time

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TelegramVideoBot:
    def __init__(self):
        self.config = Config()
        self.video_processor = VideoProcessor()
        self.application = Application.builder().token(self.config.telegram_token).build()
        
        # Add handlers
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("help", self.help))
        self.application.add_handler(MessageHandler(filters.VIDEO, self.handle_video))
        self.application.add_handler(MessageHandler(filters.ATTACHMENT, self.handle_attachment))
        
    async def start(self, update: Update, context: CallbackContext):
        """Send a message when the command /start is issued."""
        welcome_message = """
🎬 **Video Fingerprint Modifier Bot** 🎬

Send me a video file (up to 50MB) and I'll process it to change its digital fingerprint while maintaining quality!

**Features:**
• 5 different processing methods
• Quality preservation
• Automatic forwarding to target group
• File size optimization

Just send a video and I'll handle the rest! 🚀
        """
        await update.message.reply_text(welcome_message, parse_mode=ParseMode.MARKDOWN)
        
    async def help(self, update: Update, context: CallbackContext):
        """Send help message."""
        help_message = """
📋 **How to use this bot:**

1. Send a video file (up to 50MB)
2. I'll process it using one of 5 different methods
3. The processed video will be sent to the configured group
4. Original digital fingerprint will be modified

**Supported formats:** MP4, AVI, MOV, MKV, WMV, FLV

**Processing methods:**
• Bitrate adjustment
• Frame rate modification
• Resolution scaling
• Codec parameter changes
• Compression optimization

Need help? Just send /help again! 🤖
        """
        await update.message.reply_text(help_message, parse_mode=ParseMode.MARKDOWN)
        
    async def handle_video(self, update: Update, context: CallbackContext):
        """Handle video file uploads."""
        await self.process_video_file(update, context, update.message.video)
        
    async def handle_attachment(self, update: Update, context: CallbackContext):
        """Handle document attachments that might be videos."""
        document = update.message.document
        if document and document.mime_type and document.mime_type.startswith('video/'):
            await self.process_video_file(update, context, document)
        else:
            await update.message.reply_text(
                "⚠️ Please send a video file. Supported formats: MP4, AVI, MOV, MKV, WMV, FLV"
            )
            
    async def process_video_file(self, update: Update, context: CallbackContext, file_obj):
        """Process the video file."""
        try:
            # Check file size (50MB limit)
            max_size = 50 * 1024 * 1024  # 50MB in bytes
            if file_obj.file_size > max_size:
                await update.message.reply_text(
                    f"❌ File too large! Maximum size is 50MB.\n"
                    f"Your file: {format_file_size(file_obj.file_size)}"
                )
                return
                
            # Send processing message
            processing_msg = await update.message.reply_text(
                f"🎬 Processing video...\n"
                f"📁 File: {file_obj.file_name or 'video'}\n"
                f"📊 Size: {format_file_size(file_obj.file_size)}\n"
                f"⏳ This may take a few moments..."
            )
            
            # Create temporary directory for processing
            with tempfile.TemporaryDirectory() as temp_dir:
                # Download the file
                file_path = os.path.join(temp_dir, file_obj.file_name or 'input_video.mp4')
                await processing_msg.edit_text(
                    f"🎬 Processing video...\n"
                    f"📁 File: {file_obj.file_name or 'video'}\n"
                    f"📊 Size: {format_file_size(file_obj.file_size)}\n"
                    f"⬇️ Downloading..."
                )
                
                file = await context.bot.get_file(file_obj.file_id)
                await file.download_to_drive(file_path)
                
                # Process the video
                await processing_msg.edit_text(
                    f"🎬 Processing video...\n"
                    f"📁 File: {file_obj.file_name or 'video'}\n"
                    f"📊 Size: {format_file_size(file_obj.file_size)}\n"
                    f"⚙️ Applying fingerprint modification..."
                )
                
                processed_path = await self.video_processor.process_video(file_path, temp_dir)
                
                if not processed_path or not os.path.exists(processed_path):
                    await processing_msg.edit_text("❌ Video processing failed. Please try again.")
                    return
                
                # Get processed file info
                processed_size = os.path.getsize(processed_path)
                
                # Send to target group if configured
                if self.config.target_group_id:
                    await processing_msg.edit_text(
                        f"🎬 Processing complete!\n"
                        f"📁 Original: {format_file_size(file_obj.file_size)}\n"
                        f"📁 Processed: {format_file_size(processed_size)}\n"
                        f"📤 Sending to target group..."
                    )
                    
                    with open(processed_path, 'rb') as video_file:
                        await context.bot.send_video(
                            chat_id=self.config.target_group_id,
                            video=video_file,
                            caption=f"🎬 Processed video\n"
                                   f"📊 Original size: {format_file_size(file_obj.file_size)}\n"
                                   f"📊 Processed size: {format_file_size(processed_size)}\n"
                                   f"🔧 Method: {self.video_processor.last_method_used}\n"
                                   f"⏰ Processed at: {time.strftime('%Y-%m-%d %H:%M:%S')}"
                        )
                    
                    await processing_msg.edit_text(
                        f"✅ Video processed successfully!\n"
                        f"📁 Original: {format_file_size(file_obj.file_size)}\n"
                        f"📁 Processed: {format_file_size(processed_size)}\n"
                        f"🔧 Method: {self.video_processor.last_method_used}\n"
                        f"📤 Sent to target group!"
                    )
                else:
                    # Send back to user if no target group configured
                    await processing_msg.edit_text(
                        f"🎬 Processing complete!\n"
                        f"📁 Original: {format_file_size(file_obj.file_size)}\n"
                        f"📁 Processed: {format_file_size(processed_size)}\n"
                        f"📤 Sending processed video..."
                    )
                    
                    with open(processed_path, 'rb') as video_file:
                        await context.bot.send_video(
                            chat_id=update.message.chat_id,
                            video=video_file,
                            caption=f"🎬 Processed video\n"
                                   f"📊 Original size: {format_file_size(file_obj.file_size)}\n"
                                   f"📊 Processed size: {format_file_size(processed_size)}\n"
                                   f"🔧 Method: {self.video_processor.last_method_used}"
                        )
                    
                    await processing_msg.edit_text(
                        f"✅ Video processed successfully!\n"
                        f"📁 Original: {format_file_size(file_obj.file_size)}\n"
                        f"📁 Processed: {format_file_size(processed_size)}\n"
                        f"🔧 Method: {self.video_processor.last_method_used}\n"
                        f"📤 Done!"
                    )
                    
        except Exception as e:
            logger.error(f"Error processing video: {str(e)}")
            await update.message.reply_text(
                f"❌ Error processing video: {str(e)}\n"
                f"Please try again with a different video file."
            )
            
    async def run(self):
        """Run the bot."""
        logger.info("Starting Telegram Video Processing Bot...")
        await self.application.initialize()
        await self.application.start()
        
        # Start polling
        await self.application.updater.start_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True
        )
        
        logger.info("Bot is running and polling for updates...")
        
        # Keep the bot running
        try:
            await asyncio.Event().wait()
        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
        finally:
            await self.application.stop()
            cleanup_temp_files()

if __name__ == '__main__':
    bot = TelegramVideoBot()
    asyncio.run(bot.run())
