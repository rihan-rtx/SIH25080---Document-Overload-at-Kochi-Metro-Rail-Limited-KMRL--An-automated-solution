"""
Simple file-based database for storing document metadata and summaries
"""
import json
import os
from datetime import datetime
from pathlib import Path
import pandas as pd
import streamlit as st
from config import DATA_DIR

class DocumentDatabase:
    def __init__(self):
        self.db_file = DATA_DIR / "documents.json"
        self.audit_file = DATA_DIR / "audit_log.json"
        self.ensure_db_exists()
    
    def ensure_db_exists(self):
        """Create database files if they don't exist"""
        if not self.db_file.exists():
            self.save_data([])
        
        if not self.audit_file.exists():
            self.save_audit_log([])
    
    def load_data(self):
        """Load documents from JSON file"""
        try:
            with open(self.db_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Error loading database: {str(e)}")
            return []
    
    def save_data(self, data):
        """Save documents to JSON file"""
        try:
            with open(self.db_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            st.error(f"Error saving to database: {str(e)}")
    
    def load_audit_log(self):
        """Load audit log from JSON file"""
        try:
            with open(self.audit_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            return []
    
    def save_audit_log(self, data):
        """Save audit log to JSON file"""
        try:
            with open(self.audit_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            st.error(f"Error saving audit log: {str(e)}")
    
    def add_document(self, document_data, user_info):
        """Add a new document to the database"""
        documents = self.load_data()
        
        # Generate unique ID
        doc_id = f"DOC_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(documents)}"
        
        document_record = {
            "id": doc_id,
            "filename": document_data["filename"],
            "file_type": document_data["file_type"],
            "upload_date": datetime.now().isoformat(),
            "uploaded_by": user_info["name"],
            "uploader_role": user_info["role"],
            "document_type": document_data["document_type"],
            "classification_confidence": document_data.get("classification_confidence", 0),
            "summary": document_data["summary"],
            "action_items": document_data.get("action_items", []),
            "deadlines": document_data.get("deadlines", []),
            "risks": document_data.get("risks", []),
            "priority": document_data.get("priority", "Medium"),
            "language": document_data.get("language", "unknown"),
            "text_stats": document_data.get("text_stats", {}),
            "key_information": document_data.get("key_information", {}),
            "file_path": document_data.get("file_path", ""),
            "tags": document_data.get("tags", []),
            "status": "Active"
        }
        
        documents.append(document_record)
        self.save_data(documents)
        
        # Log the upload
        self.log_activity("UPLOAD", doc_id, user_info, f"Uploaded document: {document_data['filename']}")
        
        return doc_id
    
    def get_documents_by_role(self, user_role):
        """Get documents accessible to a specific role"""
        from config import USER_ROLES
        
        documents = self.load_data()
        accessible_types = USER_ROLES.get(user_role, [])
        
        filtered_docs = [
            doc for doc in documents 
            if doc["document_type"] in accessible_types and doc["status"] == "Active"
        ]
        
        return filtered_docs
    
    def search_documents(self, query, user_role=None):
        """Search documents by content, filename, or metadata"""
        documents = self.load_data()
        
        if user_role:
            documents = self.get_documents_by_role(user_role)
        
        query_lower = query.lower()
        results = []
        
        for doc in documents:
            score = 0
            
            # Search in filename
            if query_lower in doc["filename"].lower():
                score += 10
            
            # Search in summary
            if query_lower in doc["summary"].lower():
                score += 8
            
            # Search in document type
            if query_lower in doc["document_type"].lower():
                score += 6
            
            # Search in action items
            for action in doc.get("action_items", []):
                if query_lower in action.lower():
                    score += 5
            
            # Search in risks
            for risk in doc.get("risks", []):
                if query_lower in risk.lower():
                    score += 5
            
            # Search in key information
            for key, value in doc.get("key_information", {}).items():
                if query_lower in str(value).lower():
                    score += 4
            
            if score > 0:
                doc["search_score"] = score
                results.append(doc)
        
        # Sort by relevance score
        results.sort(key=lambda x: x["search_score"], reverse=True)
        
        return results
    
    def get_document_by_id(self, doc_id):
        """Get a specific document by ID"""
        documents = self.load_data()
        for doc in documents:
            if doc["id"] == doc_id:
                return doc
        return None
    
    def log_activity(self, action, doc_id, user_info, details=""):
        """Log user activity for audit purposes"""
        audit_log = self.load_audit_log()
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "document_id": doc_id,
            "user_name": user_info["name"],
            "user_role": user_info["role"],
            "details": details,
            "ip_address": "localhost"  # In real app, get actual IP
        }
        
        audit_log.append(log_entry)
        self.save_audit_log(audit_log)
    
    def get_audit_log(self, limit=100):
        """Get recent audit log entries"""
        audit_log = self.load_audit_log()
        return audit_log[-limit:] if len(audit_log) > limit else audit_log
    
    def get_statistics(self):
        """Get database statistics"""
        documents = self.load_data()
        
        if not documents:
            return {
                "total_documents": 0,
                "documents_by_type": {},
                "documents_by_priority": {},
                "recent_uploads": 0
            }
        
        # Count by document type
        type_counts = {}
        priority_counts = {}
        
        for doc in documents:
            doc_type = doc["document_type"]
            priority = doc.get("priority", "Medium")
            
            type_counts[doc_type] = type_counts.get(doc_type, 0) + 1
            priority_counts[priority] = priority_counts.get(priority, 0) + 1
        
        # Count recent uploads (last 7 days)
        from datetime import datetime, timedelta
        week_ago = datetime.now() - timedelta(days=7)
        recent_count = 0
        
        for doc in documents:
            upload_date = datetime.fromisoformat(doc["upload_date"])
            if upload_date > week_ago:
                recent_count += 1
        
        return {
            "total_documents": len(documents),
            "documents_by_type": type_counts,
            "documents_by_priority": priority_counts,
            "recent_uploads": recent_count
        }