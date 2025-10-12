import os
import re
from flask import Flask, request, render_template, redirect, url_for, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader, PdfWriter

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def sanitize(text):
    return "".join(c for c in text if c.isalnum() or c in (' ', '_', '-')).rstrip()


@app.route('/')
def terminal_ui():
    return render_template('index.html')


@app.route('/admin')
def upload_form():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    required_fields = ['admin_name', 'class', 'subject', 'semester', 'exam_year', 'exam_type', 'medium']
    if 'file' not in request.files or not all(field in request.form for field in required_fields):
        return "<h1>Missing form data. <a href='/admin'>Please try again.</a></h1>", 400

    file = request.files['file']

    # Get all fields, providing defaults for optional ones
    admin_name = request.form.get('admin_name', '')
    class_name = request.form.get('class', '')
    subject = request.form.get('subject', '')
    semester = request.form.get('semester', '')
    exam_year = request.form.get('exam_year', '')
    exam_type = request.form.get('exam_type', '')
    medium = request.form.get('medium', '')
    paper_code = request.form.get('paper_code', 'N-A')  # N-A for Not-Applicable
    exam_number = request.form.get('exam_number', 'N-A')
    university = request.form.get('university', 'N-A')
    time = request.form.get('time', 'N-A')
    max_marks = request.form.get('max_marks', 'N-A')

    if file.filename == '' or not all([admin_name, class_name, subject, semester, exam_year, exam_type, medium]):
        return "<h1>A required field is empty. <a href='/admin'>Please try again.</a></h1>", 400

    if file and allowed_file(file.filename):
        # MODIFIED: Filename now includes paper code and exam number, for a total of 9 tags
        tags = [
            sanitize(class_name), sanitize(subject), f"Sem-{sanitize(semester)}",
            sanitize(exam_year), sanitize(exam_type), sanitize(paper_code),
            sanitize(exam_number), sanitize(medium), sanitize(admin_name)
        ]
        filename_prefix = "_".join(f"[{tag}]" for tag in tags)

        original_secure_name = secure_filename(file.filename)
        base_filename, file_extension = os.path.splitext(original_secure_name)

        # NEW: Duplicate file handling logic
        base_filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{filename_prefix}_{base_filename}{file_extension}")
        filepath = base_filepath
        counter = 1
        while os.path.exists(filepath):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'],
                                    f"{filename_prefix}_{base_filename}({counter}){file_extension}")
            counter += 1

        new_filename = os.path.basename(filepath)
        file.save(filepath)

        try:
            reader = PdfReader(filepath)
            writer = PdfWriter()
            for page in reader.pages: writer.add_page(page)
            keywords = f"University: {university}, Class: {class_name}, Year: {exam_year}, Sem: {semester}, Type: {exam_type}, Medium: {medium}, Time: {time}, Marks: {max_marks}, Code: {paper_code}, Paper: {exam_number}"
            writer.add_metadata(
                {"/Author": admin_name, "/Title": f"{class_name} - {subject} (Sem {semester})", "/Subject": subject,
                 "/Keywords": keywords})
            with open(filepath, "wb") as f:
                writer.write(f)
        except Exception as e:
            print(f"Could not write metadata. Error: {e}")

        success_message = f"""
            <h1>File Uploaded Successfully!</h1> <p><strong>Saved as:</strong> {new_filename}</p>
        """
        if counter > 1:
            success_message += "<p><strong>Note:</strong> A file with similar tags already existed. Your upload was saved with a unique number.</p>"

        success_message += "<a href='/admin' style='display: inline-block; margin-top: 10px; padding: 10px 15px; background-color: #45a049; color: white; text-decoration: none; border-radius: 4px;'>Upload More</a>"
        success_message += "<a href='/' style='display: inline-block; margin-top: 10px; margin-left:10px; padding: 10px 15px; background-color: #555; color: white; text-decoration: none; border-radius: 4px;'>Go to Home</a>"

        # Returning a simple success string is fine for fetch, but we can make it better later
        return "Success", 200
    else:
        return "<h1>Invalid file type. Only PDFs are allowed. <a href='/admin'>Please try again</a></h1>", 400


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
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)
