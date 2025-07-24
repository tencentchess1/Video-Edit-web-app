#!/usr/bin/env python3
"""
Test script for Telegram Video Processing Bot
This script runs a quick test to ensure all components work properly
"""

import os
import sys
import asyncio
import logging
from config import Config
from video_processor import VideoProcessor

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def test_config():
    """Test configuration loading"""
    try:
        logger.info("Testing configuration...")
        
        # Set test token if not provided
        if not os.getenv('TELEGRAM_TOKEN'):
            os.environ['TELEGRAM_TOKEN'] = '7703883287:AAEP7SwRri5Hsm_HspAMznK561e_A8PD_qw'
            
        config = Config()
        logger.info(f"✓ Config loaded successfully")
        logger.info(f"✓ Bot token configured: {config.telegram_token[:10]}...")
        logger.info(f"✓ Target group configured: {config.is_target_group_configured}")
        return True
        
    except Exception as e:
        logger.error(f"✗ Config test failed: {e}")
        return False

def test_video_processor():
    """Test video processor initialization"""
    try:
        logger.info("Testing video processor...")
        processor = VideoProcessor()
        
        # Test FFmpeg installation
        if processor.check_ffmpeg_installation():
            logger.info("✓ FFmpeg is installed and accessible")
        else:
            logger.warning("✗ FFmpeg not found - video processing will fail")
            return False
            
        logger.info("✓ Video processor initialized successfully")
        return True
        
    except Exception as e:
        logger.error(f"✗ Video processor test failed: {e}")
        return False

def main():
    """Run all tests"""
    logger.info("Starting bot component tests...")
    
    tests = [
        ("Configuration", test_config),
        ("Video Processor", test_video_processor)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        logger.info(f"\n--- Testing {test_name} ---")
        if test_func():
            passed += 1
            logger.info(f"✓ {test_name} test PASSED")
        else:
            failed += 1
            logger.error(f"✗ {test_name} test FAILED")
    
    logger.info(f"\n--- Test Results ---")
    logger.info(f"Passed: {passed}")
    logger.info(f"Failed: {failed}")
    
    if failed == 0:
        logger.info("🎉 All tests passed! Bot is ready to run.")
        return 0
    else:
        logger.error("❌ Some tests failed. Please fix the issues before running the bot.")
        return 1

if __name__ == '__main__':
    sys.exit(main())