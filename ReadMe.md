# 🔍 Real-Time OCR Web Application

A full-stack OCR web application built with Flask that supports batch image and PDF text extraction, multi-language OCR, real-time progress tracking, authentication, and multi-format downloads.

## 🚀 Features
- User authentication & session management
- Batch OCR for images and PDFs
- Multi-language support (English, Hindi, Malayalam)
- Real-time progress updates using WebSockets
- Drag & drop file upload
- OCR result export (TXT, ZIP, JSON)
- Clean, responsive UI

## 🏗️ Architecture
- Frontend: HTML, CSS, JavaScript
- Backend: Flask + Flask-SocketIO
- OCR Engine: Tesseract OCR
- Database: SQLite
- Real-time Communication: WebSockets

## 🛠️ Setup Instructions

# Clone the repository
git clone <your-repo-url>
cd real-time-ocr-web-app

# Install dependencies
pip install -r requirements.txt

# Initialize the database
python init_db.py

# Run the application
python app.py
