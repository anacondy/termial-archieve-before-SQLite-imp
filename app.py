import os
import re
import secrets
from flask import Flask, request, render_template, redirect, url_for, jsonify, send_from_directory, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader, PdfWriter

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB limit

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(32))
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Rate limiting setup
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def sanitize(text):
    """Sanitize text to prevent path traversal and XSS attacks"""
    if not text or not isinstance(text, str):
        return ""
    # Remove any potential path traversal attempts
    text = text.replace('..', '').replace('/', '').replace('\\', '')
    # Only allow alphanumeric characters, spaces, underscores, and hyphens
    sanitized = "".join(c for c in text if c.isalnum() or c in (' ', '_', '-')).rstrip()
    # Limit length to prevent abuse
    return sanitized[:100]


@app.route('/')
def terminal_ui():
    return render_template('index.html')


@app.route('/admin')
def upload_form():
    return render_template('upload.html')


# Add security headers to all responses
@app.after_request
def add_security_headers(response):
    # Prevent clickjacking
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    # Prevent XSS attacks
    response.headers['X-Content-Type-Options'] = 'nosniff'
    # Enable XSS protection
    response.headers['X-XSS-Protection'] = '1; mode=block'
    # Content Security Policy
    response.headers['Content-Security-Policy'] = "default-src 'self' https://fonts.googleapis.com https://fonts.gstatic.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; script-src 'self' 'unsafe-inline';"
    # Referrer policy
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    return response


@app.route('/upload', methods=['POST'])
@limiter.limit("10 per hour")  # Limit uploads to prevent abuse
def upload_file():
    required_fields = ['admin_name', 'class', 'subject', 'semester', 'exam_year', 'exam_type', 'medium']
    
    # Validate that all required fields are present
    if 'file' not in request.files or not all(field in request.form for field in required_fields):
        return jsonify({"error": "Missing form data"}), 400

    file = request.files['file']

    # Validate file was selected
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # Get all fields with proper validation
    admin_name = sanitize(request.form.get('admin_name', ''))
    class_name = sanitize(request.form.get('class', ''))
    subject = sanitize(request.form.get('subject', ''))
    semester = sanitize(request.form.get('semester', ''))
    exam_year = sanitize(request.form.get('exam_year', ''))
    exam_type = sanitize(request.form.get('exam_type', ''))
    medium = sanitize(request.form.get('medium', ''))
    paper_code = sanitize(request.form.get('paper_code', 'N-A'))
    exam_number = sanitize(request.form.get('exam_number', 'N-A'))
    university = sanitize(request.form.get('university', 'N-A'))
    time = sanitize(request.form.get('time', 'N-A'))
    max_marks = sanitize(request.form.get('max_marks', 'N-A'))

    # Validate all required fields have values after sanitization
    if not all([admin_name, class_name, subject, semester, exam_year, exam_type, medium]):
        return jsonify({"error": "A required field is empty or invalid"}), 400

    # Validate file type
    if not file or not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type. Only PDFs are allowed"}), 400

    try:
        # Create filename with sanitized tags
        tags = [
            class_name, subject, f"Sem-{semester}",
            exam_year, exam_type, paper_code,
            exam_number, medium, admin_name
        ]
        filename_prefix = "_".join(f"[{tag}]" for tag in tags)

        original_secure_name = secure_filename(file.filename)
        base_filename, file_extension = os.path.splitext(original_secure_name)

        # Handle duplicate files
        base_filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{filename_prefix}_{base_filename}{file_extension}")
        filepath = base_filepath
        counter = 1
        while os.path.exists(filepath):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'],
                                    f"{filename_prefix}_{base_filename}({counter}){file_extension}")
            counter += 1

        new_filename = os.path.basename(filepath)
        
        # Save the file
        file.save(filepath)

        # Add metadata to PDF
        try:
            reader = PdfReader(filepath)
            writer = PdfWriter()
            for page in reader.pages:
                writer.add_page(page)
            
            keywords = f"University: {university}, Class: {class_name}, Year: {exam_year}, Sem: {semester}, Type: {exam_type}, Medium: {medium}, Time: {time}, Marks: {max_marks}, Code: {paper_code}, Paper: {exam_number}"
            writer.add_metadata({
                "/Author": admin_name,
                "/Title": f"{class_name} - {subject} (Sem {semester})",
                "/Subject": subject,
                "/Keywords": keywords
            })
            
            with open(filepath, "wb") as f:
                writer.write(f)
        except Exception as e:
            print(f"Could not write metadata. Error: {e}")
            # Continue even if metadata writing fails

        return jsonify({
            "success": True,
            "filename": new_filename,
            "duplicate": counter > 1
        }), 200
        
    except Exception as e:
        print(f"Upload error: {e}")
        return jsonify({"error": "Upload failed. Please try again"}), 500


@app.route('/api/papers')
def get_papers():
    papers = []
    # MODIFIED: The Regex pattern now looks for 9 tags to match the new filename structure
    pattern = re.compile(
        r"\[(.*?)\]_\[(.*?)\]_\[(.*?)\]_\[(.*?)\]_\[(.*?)\]_\[(.*?)\]_\[(.*?)\]_\[(.*?)\]_\[(.*?)\]_(.*)",
        re.IGNORECASE)
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        match = pattern.match(filename)
        if match:
            try:
                groups = match.groups()
                paper_details = {
                    'class': groups[0], 'subject': groups[1], 'semester': groups[2].replace('Sem-', ''),
                    'year': groups[3], 'exam_type': groups[4], 'paper_code': groups[5],
                    'exam_number': groups[6], 'medium': groups[7], 'uploader': groups[8],
                    'original_name': groups[9], 'url': url_for('get_uploaded_file', filename=filename)
                }
                papers.append(paper_details)
            except Exception as e:
                print(f"Error processing matched file {filename}: {e}")
    return jsonify(papers)


@app.route('/uploads/<path:filename>')
def get_uploaded_file(filename):
    # Prevent path traversal attacks
    filename = secure_filename(filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    # Ensure the file exists and is within the upload folder
    if not os.path.exists(filepath) or not os.path.abspath(filepath).startswith(os.path.abspath(app.config['UPLOAD_FOLDER'])):
        abort(404)
    
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    # Never run with debug=True in production
    # Set environment variable FLASK_ENV=production for production deployment
    is_production = os.environ.get('FLASK_ENV') == 'production'
    app.run(debug=not is_production, host='127.0.0.1', port=5000)
