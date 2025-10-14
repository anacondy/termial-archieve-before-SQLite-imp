# Terminal Archives - Previous Year Papers Management System

A terminal-style web application for managing and searching previous year examination papers. Features a retro terminal interface with secure file upload and search capabilities.

## 🎯 Project Overview

**Terminal Archives** is a Flask-based web application that provides an intuitive terminal-style interface for managing educational resources, specifically previous year examination papers. The application allows administrators to upload PDF files with detailed metadata and users to search through the archives efficiently.

### Main Features
- 🖥️ **Retro Terminal UI**: Clean, minimalist terminal-style interface
- 📱 **Responsive Design**: Works seamlessly on desktop and mobile devices
- 🔍 **Advanced Search**: Fast search across all paper metadata
- 📄 **PDF Management**: Upload, tag, and serve PDF files securely
- 🔒 **Security First**: Multiple security layers to protect against common vulnerabilities
- 📊 **Metadata Support**: Automatic PDF metadata embedding

## 🔒 Security Features

This application implements multiple security best practices:

### Implemented Security Measures
1. **Secret Key Management**: Uses cryptographically secure secret keys
2. **File Upload Security**:
   - File type validation (PDF only)
   - File size limits (50 MB max)
   - Secure filename sanitization
   - Path traversal prevention
3. **Input Sanitization**: All user inputs are sanitized to prevent XSS and injection attacks
4. **Security Headers**:
   - X-Frame-Options (prevents clickjacking)
   - X-Content-Type-Options (prevents MIME sniffing)
   - Content-Security-Policy (prevents XSS)
   - X-XSS-Protection
   - Referrer-Policy
5. **Debug Mode**: Disabled in production environments
6. **Error Handling**: Proper error messages without leaking sensitive information

### Security Rating: 8/10
- ✅ Input validation and sanitization
- ✅ Secure file handling
- ✅ Security headers implemented
- ✅ No hardcoded secrets
- ⚠️ Consider adding: Rate limiting, authentication system, HTTPS enforcement

## 🚀 Setup Instructions

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/anacondy/termial-archieve-before-SQLite-imp.git
   cd termial-archieve-before-SQLite-imp
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables** (optional but recommended)
   ```bash
   # On Windows
   set SECRET_KEY=your-secret-key-here
   set FLASK_ENV=production
   
   # On macOS/Linux
   export SECRET_KEY=your-secret-key-here
   export FLASK_ENV=production
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   - Open your browser and navigate to: `http://127.0.0.1:5000`
   - Admin upload page: `http://127.0.0.1:5000/admin`

## 📖 Usage Guide

### For Users (Searching Papers)
1. Visit the homepage
2. On desktop: Press `Ctrl + K` to open search
3. On mobile: Use the search bar at the bottom
4. Type your query (e.g., "Physics 2024")
5. Press Enter to search
6. Click on results to download papers

### For Administrators (Uploading Papers)
1. Visit `/admin` or type "upload" in the search
2. Drag and drop PDF files or click to browse
3. Fill in required metadata:
   - Your name
   - Class (BA, BSc, BBA, etc.)
   - Subject name
   - Semester
   - Exam year
   - Exam type (Main Semester, CIA, etc.)
   - Medium (English, Hindi, Hinglish)
4. Optional fields: Paper code, university, time, marks
5. Click "Upload All Pending Files"

## 🔧 Configuration

### Environment Variables
- `SECRET_KEY`: Secret key for Flask sessions (auto-generated if not set)
- `FLASK_ENV`: Set to "production" for production deployment

### File Limits
- Maximum file size: 50 MB
- Allowed file types: PDF only
- Files are stored in the `uploads/` directory

## 🌐 Deployment

### Important Note for GitHub Pages
⚠️ **This application CANNOT be deployed to GitHub Pages** because:
- GitHub Pages only supports static HTML/CSS/JS files
- This is a Flask (Python) application requiring a backend server
- File uploads require server-side processing

### Recommended Deployment Options
1. **Heroku** (Free tier available)
2. **PythonAnywhere** (Free tier available)
3. **AWS EC2** or **DigitalOcean**
4. **Google Cloud Platform**
5. **Railway** or **Render**

### Production Deployment Checklist
- [ ] Set `FLASK_ENV=production`
- [ ] Set a strong `SECRET_KEY` environment variable
- [ ] Use a production WSGI server (Gunicorn, uWSGI)
- [ ] Enable HTTPS/SSL
- [ ] Set up proper database (if extending functionality)
- [ ] Configure proper logging
- [ ] Set up backup system for uploaded files
- [ ] Add rate limiting (e.g., Flask-Limiter)
- [ ] Consider adding authentication

## 🏗️ Architecture

### Technology Stack
- **Backend**: Flask (Python 3)
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **PDF Processing**: PyPDF2
- **Font**: Fira Code (monospace)

### File Structure
```
termial-archieve-before-SQLite-imp/
├── app.py                 # Flask backend application
├── index.html            # Main terminal interface (Jinja2 template)
├── upload.html           # Admin upload interface (Jinja2 template)
├── script.js             # Frontend JavaScript for terminal
├── upload.js             # Frontend JavaScript for uploads
├── style.css             # Styling for terminal interface
├── requirements.txt      # Python dependencies
├── uploads/              # Directory for uploaded PDFs (not committed)
└── README.md            # This file
```

## 🐛 Known Limitations

1. **Not GitHub Pages Compatible**: Requires backend server
2. **No Authentication**: Admin upload is not password-protected
3. **No Database**: Uses file system for storage (consider SQLite for production)
4. **No Rate Limiting**: Should be added for production
5. **Single Server**: No load balancing or scaling built-in

## 🎨 UI Design

**Rating: 7/10**
- ✅ Clean, minimalist terminal aesthetic
- ✅ Responsive mobile design
- ✅ Good user experience
- ⚠️ Could add: Dark/light theme toggle, accessibility improvements

## 💡 Innovation

**New Technology Used: 6/10**
- Modern Flask practices
- Responsive design techniques
- PDF metadata manipulation
- Progressive enhancement for mobile

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

## 🔮 Future Enhancements

- [ ] Add user authentication system
- [ ] Implement rate limiting
- [ ] Add SQLite database support
- [ ] Add paper preview functionality
- [ ] Implement full-text search in PDFs
- [ ] Add download statistics
- [ ] Create admin dashboard
- [ ] Add email notifications
- [ ] Implement batch upload
- [ ] Add API for external access

## 👨‍💻 Author

**Anuj Meena** (anacondy)

## 🙏 Acknowledgments

- Terminal UI inspiration from classic Unix terminals
- Font: Fira Code by Nikita Prokopov
- Flask framework and Python community

---

**Note**: This application is designed for educational purposes and managing examination papers. Ensure you have proper permissions before uploading or distributing copyrighted material.

