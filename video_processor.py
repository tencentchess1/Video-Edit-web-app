
import os
import random
import logging
import subprocess
import tempfile
from typing import Optional
import json

logger = logging.getLogger(__name__)

class VideoProcessor:
    def __init__(self):
        self.last_method_used = None
        self.processing_methods = [
            self._method_bitrate_adjust,
            self._method_codec_params,
            self._method_compression_optimize
        ]
        
    async def process_video(self, input_path: str, temp_dir: str) -> Optional[str]:
        """Process video using a random method to change digital fingerprint."""
        try:
            # Choose random processing method
            method = random.choice(self.processing_methods)
            
            # Generate output filename
            base_name = os.path.splitext(os.path.basename(input_path))[0]
            output_path = os.path.join(temp_dir, f"{base_name}_processed.mp4")
            
            # Apply the chosen method
            success = await method(input_path, output_path)
            
            if success and os.path.exists(output_path):
                return output_path
            else:
                logger.error(f"Processing failed with method: {method.__name__}")
                return None
                
        except Exception as e:
            logger.error(f"Error in video processing: {str(e)}")
            return None
            
    async def _method_bitrate_adjust(self, input_path: str, output_path: str) -> bool:
        """Method 1: Adjust bitrate to change fingerprint."""
        try:
            self.last_method_used = "Bitrate Adjustment"
            
            # Simple bitrate adjustment without complex probing
            bitrate_values = ['1000k', '1500k', '2000k', '2500k']
            selected_bitrate = random.choice(bitrate_values)
            
            # Process with ffmpeg with timeout
            cmd = [
                'ffmpeg', '-i', input_path, '-c:v', 'libx264', 
                '-b:v', selected_bitrate, '-c:a', 'aac', '-y', output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            return result.returncode == 0
            
        except subprocess.TimeoutExpired:
            logger.error("Bitrate adjustment timed out")
            return False
        except Exception as e:
            logger.error(f"Bitrate adjustment failed: {str(e)}")
            return False
            
    async def _method_codec_params(self, input_path: str, output_path: str) -> bool:
        """Method 2: Modify codec parameters."""
        try:
            self.last_method_used = "Codec Parameter Modification"
            
            # Random codec parameters
            crf_value = random.randint(18, 28)  # Quality factor
            preset = random.choice(['fast', 'medium'])
            
            # Process with ffmpeg with timeout
            cmd = [
                'ffmpeg', '-i', input_path, '-c:v', 'libx264',
                '-crf', str(crf_value), '-preset', preset,
                '-c:a', 'aac', '-y', output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            return result.returncode == 0
            
        except subprocess.TimeoutExpired:
            logger.error("Codec parameter modification timed out")
            return False
        except Exception as e:
            logger.error(f"Codec parameter modification failed: {str(e)}")
            return False
            
    async def _method_compression_optimize(self, input_path: str, output_path: str) -> bool:
        """Method 3: Apply compression optimization."""
        try:
            self.last_method_used = "Compression Optimization"
            
            # Simple compression settings
            profile = random.choice(['main', 'high'])
            
            # Process with ffmpeg with timeout
            cmd = [
                'ffmpeg', '-i', input_path, '-c:v', 'libx264',
                '-profile:v', profile, '-c:a', 'aac', 
                '-movflags', 'faststart', '-y', output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            return result.returncode == 0
            
        except subprocess.TimeoutExpired:
            logger.error("Compression optimization timed out")
            return False
        except Exception as e:
            logger.error(f"Compression optimization failed: {str(e)}")
            return False

    def check_ffmpeg_installation(self) -> bool:
        """Check if FFmpeg is installed and accessible."""
        try:
            result = subprocess.run(['ffmpeg', '-version'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=10)
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
