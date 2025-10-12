// Upload page functionality with progress bar
document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('upload-form');
    const progressContainer = document.querySelector('.progress-container');
    const progressFill = document.querySelector('.progress-fill');
    const progressText = document.querySelector('.progress-text');
    const fileInput = document.getElementById('file');

    if (uploadForm) {
        uploadForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(uploadForm);
            const file = fileInput.files[0];
            
            if (!file) {
                alert('Please select a file to upload');
                return;
            }
            
            // Show progress bar
            progressContainer.style.display = 'block';
            
            // Create XMLHttpRequest for upload with progress tracking
            const xhr = new XMLHttpRequest();
            
            // Track upload progress
            xhr.upload.addEventListener('progress', function(e) {
                if (e.lengthComputable) {
                    const percentComplete = (e.loaded / e.total) * 100;
                    updateProgress(percentComplete);
                }
            });
            
            // Handle completion
            xhr.addEventListener('load', function() {
                if (xhr.status === 200) {
                    updateProgress(100);
                    setTimeout(() => {
                        window.location.href = '/';
                    }, 1000);
                } else {
                    alert('Upload failed. Please try again.');
                    resetProgress();
                }
            });
            
            // Handle errors
            xhr.addEventListener('error', function() {
                alert('Upload failed due to network error.');
                resetProgress();
            });
            
            // Handle abort
            xhr.addEventListener('abort', function() {
                alert('Upload cancelled.');
                resetProgress();
            });
            
            // Send the request
            xhr.open('POST', '/upload', true);
            xhr.send(formData);
        });
    }
    
    // File input change handler
    if (fileInput) {
        fileInput.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                // Validate file size (16MB max)
                const maxSize = 16 * 1024 * 1024;
                if (file.size > maxSize) {
                    alert('File size exceeds 16MB limit');
                    this.value = '';
                    return;
                }
                
                // Validate file type
                const allowedTypes = ['application/pdf', 'application/msword', 
                                     'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                                     'text/plain'];
                if (!allowedTypes.includes(file.type)) {
                    alert('Invalid file type. Please upload PDF, DOC, DOCX, or TXT files only.');
                    this.value = '';
                    return;
                }
            }
        });
    }
    
    function updateProgress(percent) {
        progressFill.style.width = percent + '%';
        progressText.textContent = Math.round(percent) + '%';
    }
    
    function resetProgress() {
        progressContainer.style.display = 'none';
        progressFill.style.width = '0%';
        progressText.textContent = '0%';
    }
});
