# 🎬 Telegram Video Processing Bot

.

## ✨ Features


- **🎯 5 Processing Methods**: Different techniques applied randomly for unpredictable results
- **🎨 Quality Preservation**: Maintains visual quality while modifying technical parameters
- **📤 Automatic Forwarding**: Sends processed videos to configured target group
- **📊 File Size Management**: Handles file size limits and optimization
- **🚀 GitHub Actions Integration**: Runs 24/7 for free on GitHub Actions
- **⚡ Instant Processing**: Fast video processing with real-time status updates

## 🚀 Quick Setup

### 1. Deploy to GitHub
```bash
# Clone or download this repository
git clone https://github.com/YOUR_USERNAME/telegram-video-bot.git
cd telegram-video-bot

# Quick deploy (use provided script)
./quick_deploy.sh
```

### 2. Configure GitHub Secrets
Go to your repository → Settings → Secrets and variables → Actions

**Required:**
- `TELEGRAM_TOKEN`: Your bot token from @BotFather

**Optional:**
- `TARGET_GROUP_ID`: Group ID for forwarding processed videos

### 3. Enable GitHub Actions
- Go to Actions tab → Enable workflows
- Bot starts automatically and runs every 6 hours
- Manual trigger available anytime

## Usage

1. Start a chat with your bot
2. Send a video file (up to 50MB)
3. Bot processes the video using one of 5 methods:
   - Bitrate adjustment
   - Framerate modification
   - Resolution scaling
   - Codec parameter changes
   - Compression optimization
4. Processed video is sent to your configured group (or back to you)

## Processing Methods

### Method 1: Bitrate Adjustment
Modifies video bitrate to 80-95% of original while maintaining quality.

### Method 2: Framerate Modification
Slightly adjusts framerate by ±5% (barely noticeable).

### Method 3: Resolution Scaling
Scales resolution by 98-102% (imperceptible to human eye).

### Method 4: Codec Parameter Modification
Changes H.264 encoding parameters (CRF, preset, profile).

### Method 5: Compression Optimization
Applies different compression settings and optimization flags.

## GitHub Actions Workflows

### Deploy Workflow (`deploy.yml`)
- Runs on push to main branch
- Installs dependencies and validates configuration
- Tests FFmpeg installation

### Run Bot Workflow (`run-bot.yml`)
- Runs the bot continuously
- Executes every 6 hours via cron schedule
- Can be manually triggered
- Includes automatic cleanup

## Development

### Local Development with Codespaces

1. Open in GitHub Codespaces
2. Environment automatically set up with FFmpeg and Python dependencies
3. Set environment variables in terminal:
   ```bash
   export TELEGRAM_TOKEN="your_bot_token"
   export TARGET_GROUP_ID="your_group_id"  # optional
   ```
4. Run the bot:
   ```bash
   python bot.py
   ```

### Manual Installation

```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install -y ffmpeg

# Install Python dependencies
pip install -r requirements.txt

# Set environment variables
export TELEGRAM_TOKEN="your_bot_token"
export TARGET_GROUP_ID="your_group_id"  # optional

# Run the bot
python bot.py
