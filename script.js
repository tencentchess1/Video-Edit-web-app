class VideoProcessor {
    constructor() {
        this.currentFile = null;
        this.processedData = null;
        this.initializeElements();
        this.attachEventListeners();
    }

    initializeElements() {
        this.uploadArea = document.getElementById('uploadArea');
        this.fileInput = document.getElementById('fileInput');
        this.browseBtn = document.getElementById('browseBtn');
        this.fileInfo = document.getElementById('fileInfo');
        this.processing = document.getElementById('processing');
        this.result = document.getElementById('result');
        this.error = document.getElementById('error');
        
        // File info elements
        this.fileName = document.getElementById('fileName');
        this.fileSize = document.getElementById('fileSize');
        this.fileType = document.getElementById('fileType');
        
        // Button elements
        this.processBtn = document.getElementById('processBtn');
        this.clearBtn = document.getElementById('clearBtn');
        this.downloadBtn = document.getElementById('downloadBtn');
        this.newVideoBtn = document.getElementById('newVideoBtn');
        this.retryBtn = document.getElementById('retryBtn');
        
        // Processing elements
        this.processingStatus = document.getElementById('processingStatus');
        this.progressFill = document.getElementById('progressFill');
        
        // Result elements
        this.originalSize = document.getElementById('originalSize');
        this.processedSize = document.getElementById('processedSize');
        this.methodUsed = document.getElementById('methodUsed');
        this.errorMessage = document.getElementById('errorMessage');
    }

    attachEventListeners() {
        // Upload area events
        this.uploadArea.addEventListener('click', () => this.fileInput.click());
        this.browseBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            this.fileInput.click();
        });
        
        // File input change
        this.fileInput.addEventListener('change', (e) => this.handleFileSelect(e.target.files[0]));
        
        // Drag and drop
        this.uploadArea.addEventListener('dragover', (e) => this.handleDragOver(e));
        this.uploadArea.addEventListener('dragleave', (e) => this.handleDragLeave(e));
        this.uploadArea.addEventListener('drop', (e) => this.handleDrop(e));
        
        // Button events
        this.processBtn.addEventListener('click', () => this.processVideo());
        this.clearBtn.addEventListener('click', () => this.clearFile());
        this.downloadBtn.addEventListener('click', () => this.downloadProcessedVideo());
        this.newVideoBtn.addEventListener('click', () => this.clearFile());
        this.retryBtn.addEventListener('click', () => this.hideError());
    }

    handleDragOver(e) {
        e.preventDefault();
        this.uploadArea.classList.add('drag-over');
    }

    handleDragLeave(e) {
        e.preventDefault();
        this.uploadArea.classList.remove('drag-over');
    }

    handleDrop(e) {
        e.preventDefault();
        this.uploadArea.classList.remove('drag-over');
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            this.handleFileSelect(files[0]);
        }
    }

    handleFileSelect(file) {
        if (!file) return;

        // Validate file type
        const validTypes = ['video/mp4', 'video/avi', 'video/mov', 'video/quicktime', 'video/x-msvideo', 'video/x-ms-wmv', 'video/x-flv', 'video/webm'];
        if (!validTypes.includes(file.type)) {
            this.showError('Please select a valid video file (MP4, AVI, MOV, MKV, WMV, FLV)');
            return;
        }

        // Validate file size (50MB limit)
        const maxSize = 50 * 1024 * 1024; // 50MB
        if (file.size > maxSize) {
            this.showError(`File too large! Maximum size is 50MB. Your file: ${this.formatFileSize(file.size)}`);
            return;
        }

        this.currentFile = file;
        this.showFileInfo(file);
    }

    showFileInfo(file) {
        this.fileName.textContent = file.name;
        this.fileSize.textContent = this.formatFileSize(file.size);
        this.fileType.textContent = file.type;
        
        this.hideAllSections();
        this.fileInfo.style.display = 'block';
        this.fileInfo.classList.add('fade-in');
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 B';
        const k = 1024;
        const sizes = ['B', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
    }

    async processVideo() {
        if (!this.currentFile) return;

        this.showProcessing();

        try {
            // Create form data
            const formData = new FormData();
            formData.append('video', this.currentFile);

            // Update progress
            this.updateProcessingStatus('Uploading video...', 20);

            // Send to backend
            const response = await fetch('/api/process-video', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error(`Server error: ${response.status}`);
            }

            this.updateProcessingStatus('Processing video...', 60);

            const result = await response.json();

            if (!result.success) {
                throw new Error(result.error || 'Processing failed');
            }

            this.updateProcessingStatus('Finalizing...', 90);

            // Simulate final processing
            await this.delay(1000);

            this.updateProcessingStatus('Complete!', 100);
            
            // Store processed data
            this.processedData = result;
            
            // Show result after a short delay
            setTimeout(() => this.showResult(result), 500);

        } catch (error) {
            console.error('Processing error:', error);
            this.showError(`Processing failed: ${error.message}`);
        }
    }

    updateProcessingStatus(status, progress) {
        this.processingStatus.textContent = status;
        this.progressFill.style.width = progress + '%';
    }

    async delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    showProcessing() {
        this.hideAllSections();
        this.processing.style.display = 'block';
        this.processing.classList.add('fade-in');
        this.updateProcessingStatus('Initializing...', 0);
    }

    showResult(data) {
        this.originalSize.textContent = this.formatFileSize(this.currentFile.size);
        this.processedSize.textContent = this.formatFileSize(data.processed_size);
        this.methodUsed.textContent = data.method;
        
        this.hideAllSections();
        this.result.style.display = 'block';
        this.result.classList.add('fade-in');
    }

    showError(message) {
        this.errorMessage.textContent = message;
        this.hideAllSections();
        this.error.style.display = 'block';
        this.error.classList.add('fade-in');
    }

    hideError() {
        this.error.style.display = 'none';
        if (this.currentFile) {
            this.showFileInfo(this.currentFile);
        }
    }

    async downloadProcessedVideo() {
        if (!this.processedData) return;

        try {
            const response = await fetch(`/api/download/${this.processedData.download_id}`);
            if (!response.ok) throw new Error('Download failed');

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `processed_${this.currentFile.name}`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        } catch (error) {
            this.showError(`Download failed: ${error.message}`);
        }
    }

    clearFile() {
        this.currentFile = null;
        this.processedData = null;
        this.fileInput.value = '';
        this.hideAllSections();
    }

    hideAllSections() {
        this.fileInfo.style.display = 'none';
        this.processing.style.display = 'none';
        this.result.style.display = 'none';
        this.error.style.display = 'none';
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new VideoProcessor();
});

// Prevent default drag behaviors on the window
window.addEventListener('dragover', e => e.preventDefault());
window.addEventListener('drop', e => e.preventDefault());