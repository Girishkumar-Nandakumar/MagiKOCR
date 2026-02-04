# 🔮 MagiKOCR — Real-Time OCR Web Application

MagiKOCR is a full-stack, real-time Optical Character Recognition (OCR) web application designed to extract text from images and PDFs with high accuracy.  
Built using Flask and WebSockets, it supports batch processing, multi-language OCR, secure authentication, and downloadable results — delivering a production-style user experience.

---

## 🚀 Key Features

### 🔐 Authentication & Security
- User signup and login
- Secure password hashing
- Session-based access control
- Protected OCR and download routes

### 📄 OCR Capabilities
- Image OCR (PNG, JPG, JPEG)
- PDF OCR (multi-page support)
- Batch processing of multiple files
- Multi-language OCR (English, Hindi, Malayalam)

### ⚡ Real-Time Experience
- Live per-file OCR progress updates using WebSockets
- Clear processing and completion status for each file
- Responsive and user-friendly UI

### 📦 Output & Downloads
- OCR results saved per file
- Download extracted text as:
  - Individual TXT files
  - Combined ZIP archive
  - JSON format (API-friendly)

### 🎨 User Experience
- Drag & drop file upload
- Loading indicators and progress feedback
- Clean, modern, and intuitive interface

---

## 🏗️ System Architecture

- **Frontend:** HTML, CSS, JavaScript  
- **Backend:** Flask + Flask-SocketIO  
- **OCR Engine:** Tesseract OCR  
- **Database:** SQLite (user authentication)  
- **Real-Time Communication:** WebSockets  
- **File Processing:** PIL, pdf2image  

The application follows a multi-tier architecture with secure user access, real-time backend processing, and modular storage.

---

## 🛠️ Setup & Run Instructions

```bash
# Clone the repository
git clone https://github.com/Girishkumar-Nandakumar/MagiKOCR.git
cd MagiKOCR

# Install dependencies
pip install -r requirements.txt

# Initialize the database
python init_db.py

# Run the application
python app.py

Open your browser and visit:
👉 http://127.0.0.1:5000

⚙️ Prerequisites

Python 3.8+

Tesseract OCR installed locally

Poppler (required for PDF OCR on Windows)

Ensure Tesseract is added to your system PATH.

📌 Use Cases

Digitizing scanned documents

Extracting text from invoices, forms, or reports

Batch OCR processing workflows

Learning reference for Flask, WebSockets, and OCR integration

🧠 Learning Outcomes

This project demonstrates:

Backend architecture and secure authentication

Real-time systems using WebSockets

Batch file processing and OCR optimization

Clean separation of concerns and scalable design

Practical full-stack development skills

📄 License

This project is licensed under the MIT License.

🙌 Acknowledgements

Tesseract OCR

Flask & Flask-SocketIO communities

Open-source contributors who make learning possible
