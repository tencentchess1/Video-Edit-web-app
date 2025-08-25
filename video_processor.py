
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
            self._method_compression_optimize,
            self._method_quality_enhance,
            self._method_metadata_inject,
            self._method_frame_duplicate,
            self._method_audio_enhance
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
            
            # Small bitrate adjustment for minimal size increase
            bitrate_values = ['1800k', '2000k', '2200k', '2400k']
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
            
            # Minimal quality codec parameters for small size increase
            crf_value = random.randint(20, 25)  # Small quality increase
            preset = random.choice(['medium', 'fast'])  # Balanced compression
            
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
            
            # High quality compression settings to increase file size
            profile = 'high'
            level = random.choice(['4.1', '4.2', '5.0'])
            
            # Process with ffmpeg with timeout
            cmd = [
                'ffmpeg', '-i', input_path, '-c:v', 'libx264',
                '-profile:v', profile, '-level', level, '-c:a', 'aac', 
                '-b:a', '192k', '-movflags', 'faststart', '-y', output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            return result.returncode == 0
            
        except subprocess.TimeoutExpired:
            logger.error("Compression optimization timed out")
            return False
        except Exception as e:
            logger.error(f"Compression optimization failed: {str(e)}")
            return False

    async def _method_quality_enhance(self, input_path: str, output_path: str) -> bool:
        """Method 4: Quality enhancement to increase file size."""
        try:
            self.last_method_used = "Quality Enhancement"
            
            # Small quality settings
            crf_value = random.randint(18, 22)  # Small quality increase
            
            # Process with ffmpeg with timeout
            cmd = [
                'ffmpeg', '-i', input_path, '-c:v', 'libx264',
                '-crf', str(crf_value), '-preset', 'slow', 
                '-c:a', 'aac', '-b:a', '192k', '-y', output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            return result.returncode == 0
            
        except subprocess.TimeoutExpired:
            logger.error("Quality enhancement timed out")
            return False
        except Exception as e:
            logger.error(f"Quality enhancement failed: {str(e)}")
            return False

    async def _method_metadata_inject(self, input_path: str, output_path: str) -> bool:
        """Method 5: Inject metadata to increase file size."""
        try:
            self.last_method_used = "Metadata Injection"
            
            # Add metadata to increase file size slightly
            metadata = [
                '-metadata', 'title=Processed Video',
                '-metadata', 'artist=Video Processor',
                '-metadata', 'album=Fingerprint Modified',
                '-metadata', 'year=2025',
                '-metadata', 'comment=Digital fingerprint modified for enhanced privacy'
            ]
            
            # Process with ffmpeg with timeout
            cmd = [
                'ffmpeg', '-i', input_path, '-c:v', 'libx264',
                '-b:v', '2200k', '-c:a', 'aac', '-b:a', '192k'
            ] + metadata + ['-y', output_path]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            return result.returncode == 0
            
        except subprocess.TimeoutExpired:
            logger.error("Metadata injection timed out")
            return False
        except Exception as e:
            logger.error(f"Metadata injection failed: {str(e)}")
            return False

    async def _method_frame_duplicate(self, input_path: str, output_path: str) -> bool:
        """Method 6: Frame duplication technique to increase file size."""
        try:
            self.last_method_used = "Frame Processing"
            
            # Subtle frame processing to increase size
            framerate_boost = random.choice(['1.05', '1.1', '1.15'])
            
            # Process with ffmpeg with timeout
            cmd = [
                'ffmpeg', '-i', input_path, '-c:v', 'libx264',
                '-vf', f'setpts={1/float(framerate_boost)}*PTS',
                '-r', '30', '-b:v', '2400k', '-c:a', 'aac', 
                '-b:a', '192k', '-y', output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            return result.returncode == 0
            
        except subprocess.TimeoutExpired:
            logger.error("Frame processing timed out")
            return False
        except Exception as e:
            logger.error(f"Frame processing failed: {str(e)}")
            return False

    async def _method_audio_enhance(self, input_path: str, output_path: str) -> bool:
        """Method 7: Audio enhancement to increase file size."""
        try:
            self.last_method_used = "Audio Enhancement"
            
            # Low audio settings
            audio_bitrate = random.choice(['160k', '192k', '224k'])
            
            # Process with ffmpeg with timeout
            cmd = [
                'ffmpeg', '-i', input_path, '-c:v', 'libx264',
                '-b:v', '2000k', '-c:a', 'aac', '-b:a', audio_bitrate,
                '-ar', '48000', '-ac', '2', '-y', output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            return result.returncode == 0
            
        except subprocess.TimeoutExpired:
            logger.error("Audio enhancement timed out")
            return False
        except Exception as e:
            logger.error(f"Audio enhancement failed: {str(e)}")
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
