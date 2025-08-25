# Overview

This is a Telegram Video Processing Bot that modifies video digital fingerprints while preserving visual quality. The bot accepts video files up to 50MB, processes them using one of several randomized methods (bitrate adjustment, codec parameter changes, compression optimization), and can automatically forward processed videos to a configured target group. The application can run both as a standalone Telegram bot and as a web application with a Flask interface, designed to operate continuously via GitHub Actions for free hosting.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Bot Architecture
- **Telegram Bot Integration**: Built using python-telegram-bot library for handling Telegram API interactions
- **Dual Interface Design**: Supports both Telegram bot interface and web interface via Flask
- **Asynchronous Processing**: Uses asyncio for handling concurrent video processing tasks
- **Configuration Management**: Environment-based configuration using python-dotenv for token and group ID management

## Video Processing Engine
- **FFmpeg Integration**: Core video processing powered by FFmpeg with Python bindings (ffmpeg-python)
- **Randomized Processing Methods**: Implements multiple processing techniques (bitrate adjustment, codec parameters, compression optimization) selected randomly to ensure unpredictable fingerprint modification
- **Quality Preservation Strategy**: Focuses on technical parameter modification rather than visual quality degradation
- **File Size Management**: Handles file size constraints and optimization for Telegram's 50MB limit

## Web Interface
- **Flask Web Server**: Provides HTTP endpoints for video upload and processing via web browser
- **RESTful API Design**: Implements `/api/process-video` endpoint for programmatic access
- **Concurrent Processing**: Uses ThreadPoolExecutor for handling multiple video processing requests
- **Static File Serving**: Serves HTML, CSS, and JavaScript files directly from Flask

## File Management
- **Temporary File Handling**: Creates isolated temporary directories for each processing session
- **Automatic Cleanup**: Implements comprehensive cleanup routines to prevent disk space issues
- **File Validation**: Validates video file formats and sizes before processing
- **State Management**: Maintains processing state in memory (suitable for single-instance deployment)

## Deployment Strategy
- **GitHub Actions Integration**: Designed for 24/7 operation using GitHub Actions as hosting platform
- **Environment Variable Configuration**: All sensitive data (bot tokens, group IDs) managed through environment variables
- **Container-Ready**: Architecture supports containerized deployment with minimal dependencies

# External Dependencies

## Core Processing
- **FFmpeg**: Video processing engine for codec manipulation, bitrate adjustment, and format conversion
- **ffmpeg-python**: Python bindings for FFmpeg operations

## Telegram Integration
- **python-telegram-bot**: Official Telegram Bot API library for handling bot interactions, file downloads, and message processing
- **Telegram Bot API**: External service for bot communication and file transfer

## Web Framework
- **Flask**: Lightweight web framework for HTTP server and API endpoints
- **Werkzeug**: WSGI utilities for secure filename handling and file uploads

## Configuration and Utilities
- **python-dotenv**: Environment variable management from .env files
- **requests**: HTTP client library for external API calls

## Runtime Environment
- **GitHub Actions**: Primary hosting and execution environment for continuous bot operation
- **Python 3.x**: Runtime environment with asyncio support for concurrent processing

## Optional Integrations
- **Target Group Forwarding**: Configured Telegram group for automatic processed video forwarding (optional feature controlled by TARGET_GROUP_ID environment variable)