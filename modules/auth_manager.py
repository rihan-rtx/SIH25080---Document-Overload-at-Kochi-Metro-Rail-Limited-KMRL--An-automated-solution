"""
Simple authentication manager for user login and role management
"""
import streamlit as st
from config import SAMPLE_USERS

class AuthManager:
    def __init__(self):
        self.users = SAMPLE_USERS
    
    def authenticate_user(self, username, password):
        """Authenticate user credentials"""
        if username in self.users:
            user_data = self.users[username]
            if user_data["password"] == password:
                return {
                    "username": username,
                    "name": user_data["name"],
                    "role": user_data["role"],
                    "authenticated": True
                }
        return None
    
    def login_form(self):
        """Display login form"""
        st.title("🚇 KochiMetro DocuTrack")
        st.subheader("Login to Access Document Management System")
        
        with st.form("login_form"):
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("### Demo Accounts")
                st.markdown("**Engineer:** `engineer1` / `eng123`")
                st.markdown("**Finance:** `finance1` / `fin123`")
                st.markdown("**HR:** `hr1` / `hr123`")
                st.markdown("**Station Controller:** `station1` / `sta123`")
                st.markdown("**Compliance Officer:** `compliance1` / `comp123`")
            
            with col2:
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submit_button = st.form_submit_button("Login")
        
        if submit_button:
            user_info = self.authenticate_user(username, password)
            if user_info:
                st.session_state.user_info = user_info
                st.success(f"Welcome, {user_info['name']}! ({user_info['role']})")
                st.rerun()
            else:
                st.error("Invalid username or password")
        
        return False
    
    def logout(self):
        """Logout current user"""
        if "user_info" in st.session_state:
            del st.session_state.user_info
        st.rerun()
    
    def is_authenticated(self):
        """Check if user is authenticated"""
        return "user_info" in st.session_state and st.session_state.user_info.get("authenticated", False)
    
    def get_current_user(self):
        """Get current user information"""
        return st.session_state.get("user_info", None)
    
    def require_auth(self):
        """Decorator-like function to require authentication"""
        if not self.is_authenticated():
            return self.login_form()
        return True