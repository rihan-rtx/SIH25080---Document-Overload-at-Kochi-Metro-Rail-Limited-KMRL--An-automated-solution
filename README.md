# MetroVivaram-Document-Management-System-SIH25080-
# SIH25080---Document-Overload-at-Kochi-Metro-Rail-Limited-KMRL--An-automated-solution

https://youtu.be/bZuiEeUCijo?si=8nGXCI8Wq62AnKeN
video demo 

# KochiMetro DocuTrack

## 📌 Overview

KochiMetro DocuTrack is a Streamlit-based application designed to **analyze documents, extract text, authenticate users, perform language detection, apply NLP models, visualize data, and more** using powerful Python libraries.

---

## ✅ Features

* 🔐 User Authentication with `streamlit-authenticator`
* 📄 Text Extraction from **PDFs, Images, and Word Documents**
* 🤖 NLP Features powered by `transformers`, `torch`, and `sentence-transformers`
* 📊 Interactive Visualizations with `plotly`
* 🧠 Text Matching & Fuzzy Search with `fuzzywuzzy`
* 📦 File Upload Support using `python-multipart`
* 🌍 Language Detection using `langdetect`
* 📁 Secure Document Processing & Storage

---

## 🚀 How to Run the Application

### ### 1️⃣ Clone the Repository

```bash
git clone https://github.com/rihan-rtx/SIH25080---Document-Overload-at-Kochi-Metro-Rail-Limited-KMRL--An-automated-solution
cd KochiMetro_DocuTrack
```

### 2️⃣ Create a Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate it:

* **Windows (PowerShell):**

```bash
venv\Scripts\activate
```

* **Mac/Linux:**

```bash
source venv/bin/activate
```

### 3️⃣ Install Dependencies

Make sure you have `pip` updated:

```bash
pip install --upgrade pip
```

Install required libraries:

```bash
pip install -r requirements.txt
```

> If `requirements.txt` is not available, run:

```bash
pip install streamlit streamlit-authenticator pytesseract Pillow PyPDF2 python-docx transformers torch sentence-transformers pandas numpy plotly python-multipart langdetect fuzzywuzzy python-levenshtein
```

### 4️⃣ (Optional) Configure Tesseract OCR

If using image text extraction (`pytesseract`):

* Install Tesseract from: [https://github.com/UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki)
* Add the installation path to your environment variables.

### 5️⃣ Run the Streamlit Application

```bash
streamlit run app.py
```

Your application will open in the browser at:

```
http://localhost:8501
```

---

## 📂 Project Structure

```
KochiMetro_DocuTrack/
│── app.py              # Main application file
│── config.py           # Authentication and settings
│── requirements.txt    # All dependencies
│── modules/            # Feature-specific modules
│── pages/              # Multi-page application support
│── uploads/            # User uploaded files
│── data/               # Sample or processed data
│── venv/               # Virtual environment (ignored in Git)
```

---

## 🧪 Testing the Application

Upload documents (PDF, DOCX, Images) and test:

* Text extraction
* Document similarity search
* NLP model predictions
* Language detection
* User authentication

---

## 🛠 Troubleshooting

| Issue                 | Fix                                         |
| --------------------- | ------------------------------------------- |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` again |
| App not launching     | Ensure virtual environment is activated     |
| Tesseract error       | Install Tesseract and configure PATH        |

---

## 🤝 Contributing

Feel free to submit pull requests or open issues to improve the project.

---

## 📄 License

This project is licensed under the MIT License. You are free to use and modify it.

---

## 📞 Contact

For support or queries, contact: **Rihan Baig**

---

### ⭐ If you like this project, consider giving it a star on GitHub!
