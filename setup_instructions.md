# KochiMetro DocuTrack - Setup Instructions

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Tesseract OCR (for image text extraction)

### 1. Install Tesseract OCR

#### Windows:
1. Download Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install and add to PATH
3. Download Malayalam language pack if needed

#### macOS:
```bash
brew install tesseract
brew install tesseract-lang  # For Malayalam support
```

#### Ubuntu/Debian:
```bash
sudo apt update
sudo apt install tesseract-ocr
sudo apt install tesseract-ocr-mal  # For Malayalam support
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 🔐 Demo Login Credentials

| Role | Username | Password | Access |
|------|----------|----------|---------|
| Engineer | engineer1 | eng123 | Safety notices, job cards, engineering drawings |
| Finance | finance1 | fin123 | Invoices, government circulars |
| HR | hr1 | hr123 | HR policies, safety notices, government circulars |
| Station Controller | station1 | sta123 | Operational reports, safety notices, job cards |
| Compliance Officer | compliance1 | comp123 | Government circulars, safety notices, HR policies |

## 📁 Project Structure

```
KochiMetro_DocuTrack/
├── app.py                      # Main Streamlit application
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── setup_instructions.md       # This file
├── todo.md                     # Development plan
├── modules/                    # Core functionality modules
│   ├── auth_manager.py         # User authentication
│   ├── database.py             # Document database operations
│   ├── document_classifier.py  # Document type classification
│   ├── ocr_processor.py        # OCR and text extraction
│   └── summarizer.py           # Content summarization
├── pages/                      # Streamlit pages
│   ├── dashboard.py            # Role-based dashboards
│   └── upload.py               # Document upload interface
├── data/                       # Database files (auto-created)
│   ├── documents.json          # Document metadata
│   └── audit_log.json          # Activity audit log
├── uploads/                    # Uploaded files (auto-created)
└── sample_data/               # Sample documents (auto-created)
```

## 🎯 Key Features Implemented

### ✅ Core Functionality
- **Document Upload**: Support for PDF, images, DOCX, TXT files
- **OCR Processing**: Text extraction from scanned documents
- **Language Detection**: English and Malayalam support
- **Document Classification**: Keyword-based classification with confidence scores
- **Content Summarization**: AI-powered summarization with action items and deadlines
- **Role-based Access**: Different document types for different user roles

### ✅ User Interface
- **Dashboard**: Role-specific document overview with metrics and charts
- **Search**: Full-text search across documents with filtering
- **Upload Interface**: Drag-and-drop file upload with real-time processing
- **Audit Log**: Complete activity tracking for compliance
- **Analytics**: Statistics and insights for document management

### ✅ Security & Compliance
- **User Authentication**: Role-based login system
- **Audit Trail**: Complete logging of all user activities
- **Access Control**: Documents filtered by user role permissions
- **Data Privacy**: Local file storage with secure access

## 🔧 Configuration Options

### Document Types & Keywords
Edit `config.py` to modify document classification rules:
```python
DOCUMENT_TYPES = {
    "Invoice": ["invoice", "bill", "payment", "amount"],
    "Safety Notice": ["safety", "circular", "drill", "emergency"],
    # Add more types as needed
}
```

### User Roles & Access
Modify user roles and their document access in `config.py`:
```python
USER_ROLES = {
    "Engineer": ["Safety Notice", "Engineering Drawing"],
    "Finance": ["Invoice", "Government Circular"],
    # Customize as needed
}
```

### File Size & Language Settings
Adjust limits and supported languages in `config.py`:
```python
MAX_FILE_SIZE = 50  # MB
OCR_LANGUAGES = "eng+mal"  # Tesseract language codes
```

## 🚀 Deployment Options

### Local Development
```bash
streamlit run app.py
```

### Streamlit Cloud
1. Push code to GitHub repository
2. Connect to Streamlit Cloud
3. Deploy with one click

### Docker Deployment
```dockerfile
FROM python:3.9-slim

# Install Tesseract
RUN apt-get update && apt-get install -y tesseract-ocr tesseract-ocr-mal

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## 🔄 Future Enhancements

### Phase 2 Features
- **Machine Learning Classification**: Replace keyword-based with ML models
- **Advanced OCR**: Better Malayalam text recognition
- **Integration APIs**: Connect with existing KMRL systems
- **Mobile App**: React Native mobile application
- **Advanced Analytics**: Predictive insights and reporting

### Phase 3 Features
- **Workflow Automation**: Auto-routing documents to appropriate personnel
- **Digital Signatures**: Secure document approval workflows
- **Version Control**: Document versioning and change tracking
- **Advanced Search**: Vector-based semantic search
- **Multi-language Support**: Additional Indian languages

## 🆘 Troubleshooting

### Common Issues

1. **Tesseract not found**
   - Ensure Tesseract is installed and in PATH
   - On Windows, add Tesseract installation directory to system PATH

2. **Malayalam text not recognized**
   - Install Malayalam language pack for Tesseract
   - Verify language pack installation: `tesseract --list-langs`

3. **Large file upload fails**
   - Check file size limits in `config.py`
   - Increase Streamlit file upload limit if needed

4. **Model loading errors**
   - Ensure stable internet connection for initial model download
   - Check available disk space for model files

### Performance Optimization

1. **For large documents**:
   - Implement text chunking for very long documents
   - Add progress bars for long-running operations

2. **For many users**:
   - Consider switching to proper database (PostgreSQL/MongoDB)
   - Implement caching for frequently accessed documents

3. **For production deployment**:
   - Use proper authentication system (OAuth, LDAP)
   - Implement proper logging and monitoring
   - Add backup and recovery procedures

## 📞 Support

For technical support or feature requests:
1. Check the troubleshooting section above
2. Review the configuration options
3. Contact the development team with specific error messages

---

**KochiMetro DocuTrack v1.0**  
*Empowering KMRL with intelligent document management*