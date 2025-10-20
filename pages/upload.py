"""
Document upload page with enhanced error handling
"""
import streamlit as st
import os
from pathlib import Path
from modules.ocr_processor import OCRProcessor
from modules.document_classifier import DocumentClassifier
from modules.summarizer import DocumentSummarizer
from modules.database import DocumentDatabase
from config import UPLOAD_DIR, MAX_FILE_SIZE
from googletrans import Translator


def show_upload_page(user_info):
    translator = Translator()

    st.title("📤 Upload Documents")
    st.write(f"Welcome, {user_info['name']} ({user_info['role']})")

    # Initialize processors with Malayalam support
    ocr_processor = OCRProcessor(languages="eng+mal")
    classifier = DocumentClassifier()
    summarizer = DocumentSummarizer()
    db = DocumentDatabase()

    # File upload section
    st.subheader("Upload New Document")
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=['pdf', 'png', 'jpg', 'jpeg', 'docx', 'txt', 'doc'],
        help=f"Supported formats: PDF, Images (PNG, JPG, JPEG), Word Documents (DOCX, DOC), Text files. "
             f"Maximum file size: {MAX_FILE_SIZE}MB"
    )

    if uploaded_file is not None:
        try:
            # Check file size
            file_size_mb = len(uploaded_file.getvalue()) / (1024 * 1024)
            if file_size_mb > MAX_FILE_SIZE:
                st.error(f"❌ File size ({file_size_mb:.1f}MB) exceeds maximum limit")
                return

            st.success(f"✅ File Selected: {uploaded_file.name} ({file_size_mb:.1f}MB)")
            st.info(f"File type: {uploaded_file.type}")

            if uploaded_file.type in ["image/jpeg", "image/jpg", "image/png"]:
                st.image(uploaded_file, caption=f"Preview: {uploaded_file.name}", width=300)

            if st.button("🚀 Process Document", type="primary", use_container_width=True):
                with st.spinner("🔄 Processing document... Please wait..."):
                    # Ensure upload directory exists
                    os.makedirs(UPLOAD_DIR, exist_ok=True)
                    file_path = Path(UPLOAD_DIR) / uploaded_file.name

                    # Handle name conflicts
                    counter = 1
                    orig = file_path
                    while file_path.exists():
                        file_path = orig.with_name(f"{orig.stem}_{counter}{orig.suffix}")
                        counter += 1

                    # Save file
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    st.success(f"✅ File saved as: {file_path.name}")

                    # OCR extraction
                    uploaded_file.seek(0)
                    extracted_text = ocr_processor.process_document(uploaded_file)
                    st.text_area("Extracted OCR Text (Debug)", extracted_text, height=300)

                    if not extracted_text.strip():
                        st.warning("⚠️ Limited text extracted; using filename for classification.")
                        extracted_text = f"Document: {uploaded_file.name}"

                    st.success(f"✅ Extracted {len(extracted_text)} characters")
                    language = ocr_processor.detect_language(extracted_text)
                    text_stats = ocr_processor.get_text_stats(extracted_text)

                    # Translate if Malayalam detected
                    if language.lower() == 'ml':
                        st.write("🌐 Translating Malayalam to English for summarization...")
                        try:
                            translation = translator.translate(extracted_text, src='ml', dest='en')
                            summary_text = translation.text
                            st.success("✅ Translation completed")
                        except Exception as e:
                            st.warning(f"⚠️ Translation failed: {e}")
                            summary_text = extracted_text
                    else:
                        summary_text = extracted_text

                    # Classification
                    classification = classifier.get_classification_details(summary_text, uploaded_file.name)
                    key_info = classifier.extract_key_information(summary_text, classification["predicted_type"])

                    # Summarization with longer output
                    st.write("📝 Generating summary...")
                    insights = summarizer.get_document_insights(
                        summary_text,
                        classification["predicted_type"],
                        uploaded_file.name
                    )

                    # Save to database
                    document_data = {
                        "filename": file_path.name,
                        "file_type": uploaded_file.type,
                        "document_type": classification["predicted_type"],
                        "classification_confidence": classification["confidence"],
                        "summary": insights["summary"],
                        "action_items": insights["action_items"],
                        "deadlines": insights["deadlines"],
                        "risks": insights["risks"],
                        "priority": insights["priority"],
                        "language": language,
                        "text_stats": text_stats,
                        "key_information": key_info,
                        "file_path": str(file_path)
                    }
                    doc_id = db.add_document(document_data, user_info)
                    st.success("🎉 Document processed successfully!")

                    # Display results (abbreviated)
                    st.subheader("📊 Processing Results")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Document ID:** {doc_id}")
                        st.write(f"**Type:** {classification['predicted_type']}")
                        st.write(f"**Language:** {language.upper()}")
                        st.write(f"**Word Count:** {text_stats['words']}")
                    with col2:
                        st.write("**Summary:**")
                        st.write(insights["summary"])

        except Exception as e:
            st.error(f"❌ Error: {e}")
            st.info("Please try again or contact support.")
