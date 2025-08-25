import os
import uuid
import tempfile
import logging
from flask import Flask, render_template, request, jsonify, send_file, abort
from werkzeug.utils import secure_filename
from video_processor import VideoProcessor
from utils import format_file_size, cleanup_temp_files
import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor
import json

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Store for processed files (in production, use Redis or database)
processed_files = {}

# Thread pool for video processing
executor = ThreadPoolExecutor(max_workers=2)

# Initialize video processor
video_processor = VideoProcessor()

@app.route('/')
def index():
    """Serve the main HTML page."""
    return send_file('index.html')

@app.route('/style.css')
def style():
    """Serve CSS file."""
    return send_file('style.css', mimetype='text/css')

@app.route('/script.js')
def script():
    """Serve JavaScript file."""
    return send_file('script.js', mimetype='application/javascript')

@app.route('/api/process-video', methods=['POST'])
def process_video():
    """Handle video processing requests."""
    try:
        # Check if file is present
        if 'video' not in request.files:
            return jsonify({'success': False, 'error': 'No video file provided'}), 400
        
        file = request.files['video']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        # Validate file type
        allowed_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm'}
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in allowed_extensions:
            return jsonify({'success': False, 'error': 'Invalid file type'}), 400
        
        # Generate unique ID for this processing task
        task_id = str(uuid.uuid4())
        
        # Create temporary directory
        temp_dir = tempfile.mkdtemp(prefix=f'video_processing_{task_id}_')
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        input_path = os.path.join(temp_dir, filename)
        file.save(input_path)
        
        # Get original file size
        original_size = os.path.getsize(input_path)
        
        logger.info(f"Processing video: {filename} ({format_file_size(original_size)})")
        
        # Process video asynchronously
        def process_video_sync():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                return loop.run_until_complete(
                    video_processor.process_video(input_path, temp_dir)
                )
            finally:
                loop.close()
        
        # Submit processing task
        future = executor.submit(process_video_sync)
        processed_path = future.result(timeout=120)  # 2 minute timeout
        
        if not processed_path or not os.path.exists(processed_path):
            cleanup_temp_files([temp_dir])
            return jsonify({'success': False, 'error': 'Video processing failed'}), 500
        
        # Get processed file size
        processed_size = os.path.getsize(processed_path)
        
        # Store file info for download
        download_id = str(uuid.uuid4())
        processed_files[download_id] = {
            'path': processed_path,
            'temp_dir': temp_dir,
            'original_name': filename,
            'method': video_processor.last_method_used,
            'original_size': original_size,
            'processed_size': processed_size
        }
        
        logger.info(f"Processing complete: {filename} -> {format_file_size(processed_size)}")
        
        return jsonify({
            'success': True,
            'download_id': download_id,
            'method': video_processor.last_method_used,
            'original_size': original_size,
            'processed_size': processed_size,
            'original_size_formatted': format_file_size(original_size),
            'processed_size_formatted': format_file_size(processed_size)
        })
        
    except Exception as e:
        logger.error(f"Error processing video: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/download/<download_id>')
def download_video(download_id):
    """Handle video download requests."""
    try:
        if download_id not in processed_files:
            abort(404)
        
        file_info = processed_files[download_id]
        processed_path = file_info['path']
        
        if not os.path.exists(processed_path):
            abort(404)
        
        # Generate download filename
        base_name = os.path.splitext(file_info['original_name'])[0]
        download_name = f"{base_name}_processed.mp4"
        
        # Schedule cleanup after successful download (longer delay)
        def schedule_cleanup():
            def cleanup_delayed():
                import time
                time.sleep(300)  # Wait 5 minutes before cleanup
                if download_id in processed_files:
                    temp_dir = processed_files[download_id]['temp_dir']
                    cleanup_temp_files([temp_dir])
                    del processed_files[download_id]
                    logger.info(f"Cleaned up processed file: {download_id}")
            
            # Start cleanup timer in background
            cleanup_thread = threading.Thread(target=cleanup_delayed)
            cleanup_thread.daemon = True
            cleanup_thread.start()
        
        # Only schedule cleanup after first download attempt
        if 'cleanup_scheduled' not in file_info:
            file_info['cleanup_scheduled'] = True
            schedule_cleanup()
        
        return send_file(
            processed_path,
            as_attachment=True,
            download_name=download_name,
            mimetype='video/mp4'
        )
        
    except Exception as e:
        logger.error(f"Error downloading video: {str(e)}")
        abort(500)

@app.route('/api/health')
def health_check():
    """Health check endpoint."""
    ffmpeg_available = video_processor.check_ffmpeg_installation()
    return jsonify({
        'status': 'healthy',
        'ffmpeg_available': ffmpeg_available
    })

@app.errorhandler(413)
def too_large(e):
    return jsonify({'success': False, 'error': 'File too large (max 50MB)'}), 413

@app.errorhandler(404)
def not_found(e):
    return jsonify({'success': False, 'error': 'File not found'}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'success': False, 'error': 'Internal server error'}), 500

# Cleanup old files on startup
def cleanup_old_files():
    """Clean up any old temporary files."""
    cleanup_temp_files()
    logger.info("Cleaned up old temporary files")

if __name__ == '__main__':
    cleanup_old_files()
    
    # Check FFmpeg installation
    if not video_processor.check_ffmpeg_installation():
        logger.warning("FFmpeg not found! Video processing will not work.")
    else:
        logger.info("FFmpeg is available - video processing ready")
    
    logger.info("Starting Video Fingerprint Modifier Web App...")
    app.run(host='0.0.0.0', port=5000, debug=False)