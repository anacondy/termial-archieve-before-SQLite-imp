# Terminal Archive - Previous Year Papers

A Flask-based web application for managing and accessing previous year academic papers with a terminal-style interface.

## Features

- 📁 Terminal-style interface for browsing papers
- 🔍 Search functionality with keyboard shortcuts (Ctrl+K)
- 📤 File upload with progress bar
- 🎨 Retro terminal aesthetic with green theme
- 📱 Responsive design for mobile devices

## Project Structure

```
paper-achieve-terminal/
├── static/
│   ├── script.js      # Terminal interface logic
│   ├── style.css      # Styling with terminal theme
│   └── upload.js      # Upload functionality with progress bar
├── templates/
│   ├── index.html     # Main terminal interface
│   └── upload.html    # Upload page
├── uploads/           # Directory for uploaded files
├── app.py            # Flask application
└── requirements.txt  # Python dependencies
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/anacondy/termial-archieve-before-SQLite-imp.git
cd termial-archieve-before-SQLite-imp
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to `http://127.0.0.1:5000`

## Usage

### Terminal Interface
- Type `help` to see available commands
- Type `list` to view all papers
- Type `search` to search for papers
- Type `upload` to go to upload page
- Type `clear` to clear the screen
- Press `Ctrl+K` to open quick search modal

### Uploading Papers
1. Click "Upload" or type `upload` in terminal
2. Select a file (PDF, DOC, DOCX, or TXT)
3. Watch the progress bar as your file uploads
4. Files are stored in the `uploads/` directory

## Technical Details

- **Backend**: Flask 3.0.0
- **File Size Limit**: 16MB
- **Allowed File Types**: PDF, DOC, DOCX, TXT
- **Styling**: Custom CSS with terminal aesthetic
- **Font**: Fira Code (monospace)

## Note

This is the version before SQLite implementation, with new loading bar that's thinner and looks like a pipeline.
