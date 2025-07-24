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
            self._method_framerate_modify,
            self._method_resolution_scale,
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
            
            # Get video info using ffprobe
            probe_cmd = [
                'ffprobe', '-v', 'quiet', '-print_format', 'json',
                '-show_streams', input_path
            ]
            result = subprocess.run(probe_cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                return False
                
            probe_data = json.loads(result.stdout)
            video_stream = next((stream for stream in probe_data['streams'] if stream['codec_type'] == 'video'), None)
            
            if not video_stream:
                return False
                
            # Calculate new bitrate (80-95% of original)
            original_bitrate = int(video_stream.get('bit_rate', 1000000))
            new_bitrate = int(original_bitrate * random.uniform(0.8, 0.95))
            
            # Process with ffmpeg
            cmd = [
                'ffmpeg', '-i', input_path, '-c:v', 'libx264', 
                '-b:v', str(new_bitrate), '-c:a', 'aac', '-y', output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0
            
        except Exception as e:
            logger.error(f"Bitrate adjustment failed: {str(e)}")
            return False
            
    async def _method_framerate_modify(self, input_path: str, output_path: str) -> bool:
        """Method 2: Modify framerate slightly."""
        try:
            self.last_method_used = "Framerate Modification"
            
            # Get original framerate using ffprobe
            probe_cmd = [
                'ffprobe', '-v', 'quiet', '-print_format', 'json',
                '-show_streams', input_path
            ]
            result = subprocess.run(probe_cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                return False
                
            probe_data = json.loads(result.stdout)
            video_stream = next((stream for stream in probe_data['streams'] if stream['codec_type'] == 'video'), None)
            
            if not video_stream:
                return False
                
            # Get framerate
            fps_str = video_stream.get('r_frame_rate', '30/1')
            fps_parts = fps_str.split('/')
            original_fps = float(fps_parts[0]) / float(fps_parts[1])
            
            # Slightly modify framerate (±5%)
            fps_multiplier = random.uniform(0.95, 1.05)
            new_fps = original_fps * fps_multiplier
            
            # Process with ffmpeg
            cmd = [
                'ffmpeg', '-i', input_path, '-c:v', 'libx264', 
                '-r', str(new_fps), '-c:a', 'aac', '-y', output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0
            
        except Exception as e:
            logger.error(f"Framerate modification failed: {str(e)}")
            return False
            
    async def _method_resolution_scale(self, input_path: str, output_path: str) -> bool:
        """Method 3: Scale resolution slightly."""
        try:
            self.last_method_used = "Resolution Scaling"
            
            # Get original resolution using ffprobe
            probe_cmd = [
                'ffprobe', '-v', 'quiet', '-print_format', 'json',
                '-show_streams', input_path
            ]
            result = subprocess.run(probe_cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                return False
                
            probe_data = json.loads(result.stdout)
            video_stream = next((stream for stream in probe_data['streams'] if stream['codec_type'] == 'video'), None)
            
            if not video_stream:
                return False
                
            width = int(video_stream['width'])
            height = int(video_stream['height'])
            
            # Scale by 98-102% (barely noticeable)
            scale_factor = random.uniform(0.98, 1.02)
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            
            # Ensure even dimensions for H.264
            new_width = new_width - (new_width % 2)
            new_height = new_height - (new_height % 2)
            
            # Process with ffmpeg
            cmd = [
                'ffmpeg', '-i', input_path, '-c:v', 'libx264', 
                '-s', f'{new_width}x{new_height}', '-c:a', 'aac', '-y', output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0
            
        except Exception as e:
            logger.error(f"Resolution scaling failed: {str(e)}")
            return False
            
    async def _method_codec_params(self, input_path: str, output_path: str) -> bool:
        """Method 4: Modify codec parameters."""
        try:
            self.last_method_used = "Codec Parameter Modification"
            
            # Random codec parameters
            crf_value = random.randint(18, 28)  # Quality factor
            preset = random.choice(['fast', 'medium', 'slow'])
            
            # Process with ffmpeg
            cmd = [
                'ffmpeg', '-i', input_path, '-c:v', 'libx264',
                '-crf', str(crf_value), '-preset', preset,
                '-c:a', 'aac', '-y', output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0
            
        except Exception as e:
            logger.error(f"Codec parameter modification failed: {str(e)}")
            return False
            
    async def _method_compression_optimize(self, input_path: str, output_path: str) -> bool:
        """Method 5: Apply compression optimization."""
        try:
            self.last_method_used = "Compression Optimization"
            
            # Random compression settings
            profile = random.choice(['baseline', 'main', 'high'])
            level = random.choice(['3.0', '3.1', '4.0'])
            
            # Process with ffmpeg
            cmd = [
                'ffmpeg', '-i', input_path, '-c:v', 'libx264',
                '-profile:v', profile, '-level', level,
                '-c:a', 'aac', '-movflags', 'faststart',
                '-y', output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0
            
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
