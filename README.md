
# 🎬 Video Fingerprint Modifier

A powerful video processing application that modifies digital fingerprints while preserving visual quality. Available as both a web application and Telegram bot.

## ✨ Features

- **🎯 7 Processing Methods**: Multiple techniques applied for unpredictable fingerprint modification
- **🎨 Quality Preservation**: Maintains visual quality while modifying technical parameters
- **🌐 Web Interface**: User-friendly web app with drag-and-drop file upload
- **🤖 Telegram Bot**: Process videos directly through Telegram
- **📤 Automatic Forwarding**: Bot can forward processed videos to configured target group
- **📊 File Size Management**: Handles files up to 50MB with optimization
- **⚡ Instant Processing**: Fast video processing with real-time status updates

## 🚀 Quick Setup on Replit

### 1. Fork this Repl
Simply fork this Repl to get started immediately with all dependencies pre-installed.

### 2. Run the Web Application
Click the **Run** button to start the web interface at `https://your-repl-name.your-username.repl.co`

### 3. Configure Telegram Bot (Optional)
For Telegram bot functionality:
1. Get a bot token from [@BotFather](https://t.me/BotFather)
2. Add your token to the Secrets tab:
   - Key: `TELEGRAM_TOKEN`
   - Value: Your bot token
3. Optionally add `TARGET_GROUP_ID` for auto-forwarding
4. Run the "Start Bot" workflow

## 💻 Usage

### Web Interface
1. Open the web application
2. Drag and drop or browse for a video file (up to 50MB)
3. Click "Process Video"
4. Download the processed video

### Telegram Bot
1. Start a chat with your bot
2. Send a video file
3. Receive the processed video automatically

## 🔧 Processing Methods

The application randomly selects from 7 different processing techniques:

1. **📊 Bitrate Adjustment** - High bitrate modification to increase file size
2. **🎯 Codec Parameters** - Enhanced encoding parameters for larger output
3. **🗜️ Compression Optimization** - Quality-focused compression settings
4. **✨ Quality Enhancement** - Maximum quality settings for significant size increase
5. **📝 Metadata Injection** - Adds metadata and properties to expand file size
6. **🎬 Frame Processing** - Advanced frame techniques to boost file size
7. **🔊 Audio Enhancement** - High-quality audio processing for larger files

## 🛠️ Development

### Local Development
1. Install dependencies: `pip install python-telegram-bot ffmpeg-python`
2. Set environment variables (if using Telegram bot):
   ```bash
   export TELEGRAM_TOKEN="your_bot_token"
   export TARGET_GROUP_ID="your_group_id"  # optional
   ```
3. Run the web app: `python app.py`
4. Run the bot: `python start_bot.py`

### File Structure
```
├── app.py              # Flask web application
├── bot.py              # Telegram bot implementation
├── video_processor.py  # Core video processing logic
├── config.py           # Configuration management
├── index.html          # Web interface
├── style.css           # Web styling
├── script.js           # Web functionality
└── requirements.txt    # Python dependencies
```

## 📋 Supported Formats

**Input:** MP4, AVI, MOV, MKV, WMV, FLV
**Output:** MP4 (optimized)
**File Size:** Up to 50MB

## 🔒 Privacy & Security

- Files are processed locally and securely
- No data is stored permanently
- Automatic cleanup of temporary files
- All processing happens on your Repl

## 📚 Dependencies

- **FFmpeg**: Video processing engine
- **python-telegram-bot**: Telegram Bot API
- **Flask**: Web framework
- **ffmpeg-python**: Python FFmpeg bindings

## 🚀 Deployment

This application is optimized for Replit deployment:
- Pre-configured with all necessary dependencies
- FFmpeg installed and ready
- Automatic port forwarding
- Easy environment variable management through Secrets

## 📄 License

This project is open source and available under the MIT License.

---

**Ready to get started?** Click the Run button and start processing your videos! 🎬
