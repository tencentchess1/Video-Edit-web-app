import os
import logging
import tempfile
import shutil
from typing import List, Optional

logger = logging.getLogger(__name__)

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format."""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes = size_bytes / 1024.0
        i += 1
        
    return f"{size_bytes:.1f} {size_names[i]}"

def cleanup_temp_files(temp_dirs: Optional[List[str]] = None):
    """Clean up temporary files and directories."""
    try:
        if temp_dirs:
            for temp_dir in temp_dirs:
                if os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir)
                    logger.info(f"Cleaned up temp directory: {temp_dir}")
        
        # Clean up any remaining temp files
        temp_base = tempfile.gettempdir()
        for item in os.listdir(temp_base):
            if item.startswith('tmp') and 'video' in item.lower():
                item_path = os.path.join(temp_base, item)
                try:
                    if os.path.isfile(item_path):
                        os.remove(item_path)
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                except Exception as e:
                    logger.warning(f"Could not clean up {item_path}: {e}")
                    
    except Exception as e:
        logger.warning(f"Error during cleanup: {e}")

def validate_video_file(file_path: str) -> bool:
    """Validate if file is a supported video format."""
    if not os.path.exists(file_path):
        return False
        
    # Check file extension
    supported_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm']
    file_extension = os.path.splitext(file_path)[1].lower()
    
    return file_extension in supported_extensions

def get_file_info(file_path: str) -> dict:
    """Get basic file information."""
    try:
        stat_info = os.stat(file_path)
        return {
            'size': stat_info.st_size,
            'size_formatted': format_file_size(stat_info.st_size),
            'name': os.path.basename(file_path),
            'extension': os.path.splitext(file_path)[1].lower(),
            'exists': True
        }
    except Exception as e:
        logger.error(f"Error getting file info for {file_path}: {e}")
        return {
            'size': 0,
            'size_formatted': '0 B',
            'name': 'unknown',
            'extension': '',
            'exists': False
        }

def ensure_directory_exists(directory: str):
    """Ensure directory exists, create if it doesn't."""
    try:
        os.makedirs(directory, exist_ok=True)
    except Exception as e:
        logger.error(f"Error creating directory {directory}: {e}")
        raise

def safe_filename(filename: str) -> str:
    """Generate a safe filename by removing/replacing invalid characters."""
    import re
    
    # Remove or replace invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Remove leading/trailing spaces and dots
    filename = filename.strip(' .')
    
    # Ensure filename is not empty
    if not filename:
        filename = "processed_video"
        
    return filename
