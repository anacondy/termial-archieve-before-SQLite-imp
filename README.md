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

## Screenshots

### Desktop View - Terminal Interface
![Terminal Interface](https://github.com/user-attachments/assets/acf8d903-e970-4458-8b45-90db2abd7bb5)

### Desktop View - Upload Page
![Upload Page](https://github.com/user-attachments/assets/291db75d-da9d-40f2-bc71-34666f8dc153)

### Mobile View - Responsive Design
![Mobile View](https://github.com/user-attachments/assets/c31b93bb-84ff-4224-8c35-c056282dadf1)

## Testing

The application includes a comprehensive test suite to ensure all features work correctly.

### Running Tests

Run all tests with:
```bash
python test_app.py
```

### Test Coverage

The test suite includes:

- **Route Testing**: Validates all endpoints (/, /upload, /uploads/<filename>)
- **File Upload Testing**: Tests PDF, TXT, DOC, and DOCX file uploads
- **Validation Testing**: Ensures invalid file types are rejected
- **Static Files**: Verifies CSS and JavaScript files are accessible
- **Error Handling**: Tests 404 and error pages
- **File Type Validation**: Unit tests for allowed/disallowed extensions

### Test Results

All 13 tests pass successfully:
- ✓ Index route loads correctly
- ✓ Upload page loads correctly
- ✓ File uploads work (PDF, TXT, DOC, DOCX)
- ✓ Invalid file types are rejected
- ✓ Static files are accessible
- ✓ Error handlers work properly
- ✓ File validation functions correctly

### Manual Testing

For manual testing:
1. Start the application: `python app.py`
2. Open http://127.0.0.1:5000 in your browser
3. Test the terminal interface commands
4. Try uploading different file types
5. Test on mobile devices or resize browser window
6. Verify keyboard shortcuts (Ctrl+K for search)

## Technical Details

- **Backend**: Flask 3.0.0
- **File Size Limit**: 16MB
- **Allowed File Types**: PDF, DOC, DOCX, TXT
- **Styling**: Custom CSS with terminal aesthetic
- **Font**: Fira Code (monospace)
- **Mobile Optimization**: 
  - Responsive design with proper viewport scaling
  - Optimized font spacing and rendering (letter-spacing, line-height)
  - Anti-aliased font rendering for better readability
  - iOS zoom prevention (16px minimum font size)
  - Breakpoints for tablets (768px) and phones (480px)
  - Touch-friendly button sizes on mobile devices

## Code Quality & Best Practices

- **Error Handling**: Comprehensive try-catch blocks with logging
- **Security**: Secure filename handling, file type validation, size limits
- **Logging**: Application-level logging for debugging and monitoring
- **Environment Variables**: Support for SECRET_KEY via environment
- **Input Validation**: Server-side and client-side validation
- **User Feedback**: Flash messages for all user actions
- **HTTP Error Handlers**: Custom 404, 413, and 500 error pages
- **Testing**: 13 comprehensive unit and integration tests

## Note

This is the version before SQLite implementation, with new loading bar that's thinner and looks like a pipeline.
