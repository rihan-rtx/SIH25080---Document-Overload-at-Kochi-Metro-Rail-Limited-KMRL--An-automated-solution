"""
KochiMetro DocuTrack - Main Application
A comprehensive document management system for KMRL with OCR, classification, and role-based access
"""
import streamlit as st
import sys
import os
from pathlib import Path
import torch
from modules.ocr_processor import OCRProcessor



# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

try:
    from modules.auth_manager import AuthManager
    from modules.database import DocumentDatabase
    from pages.upload import show_upload_page
    from pages.dashboard import show_dashboard_page
    import pandas as pd
    import plotly.express as px
except ImportError as e:
    st.error(f"Import error: {e}")
    st.stop()

# Configure Streamlit page
st.set_page_config(
    page_title="KochiMetro DocuTrack",
    page_icon="🚇",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS for better styling with metro theme
st.markdown("""
<style>
    /* Main theme colors - Metro blue and orange */
    :root {
        --primary-blue: #1e3c72;
        --secondary-blue: #2a5298;
        --metro-orange: #ff6b35;
        --light-gray: #f8f9fa;
        --dark-gray: #343a40;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom header styling */
    .main-header {
        background: linear-gradient(135deg, var(--primary-blue) 0%, var(--secondary-blue) 50%, var(--metro-orange) 100%);
        padding: 2rem 1rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(30, 60, 114, 0.3);
        text-align: center;
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.2rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    
    /* Metric cards styling */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border-left: 5px solid var(--metro-orange);
        margin-bottom: 1rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, var(--light-gray) 0%, #e9ecef 100%);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, var(--primary-blue), var(--secondary-blue));
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, var(--secondary-blue), var(--metro-orange));
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    
    /* File uploader styling */
    .uploadedFile {
        border: 2px dashed var(--secondary-blue);
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        background: var(--light-gray);
    }
    
    /* Success/Error message styling */
    .stAlert {
        border-radius: 8px;
        border-left: 4px solid var(--metro-orange);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: var(--light-gray);
        border-radius: 8px;
        border-left: 4px solid var(--secondary-blue);
    }
    
    /* Table styling */
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Navigation styling */
    .nav-item {
        padding: 0.5rem 1rem;
        margin: 0.2rem 0;
        border-radius: 8px;
        background: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Login form styling */
    .login-container {
        max-width: 800px;
        margin: 2rem auto;
        padding: 2rem;
        background: white;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    /* Stats cards */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def show_search_page(user_info):
    """Enhanced search functionality page"""
    st.markdown("""
    <div class="main-header">
        <h2>🔍 Document Search</h2>
        <p>Find documents quickly with advanced search capabilities</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write(f"**Welcome, {user_info['name']}** ({user_info['role']})")
    
    db = DocumentDatabase()
    
    # Enhanced search interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_query = st.text_input(
            "🔍 Search documents...", 
            placeholder="Enter keywords, document type, or content",
            help="Search across document titles, content, and metadata"
        )
    
    with col2:
        st.write("")  # Spacing
        search_button = st.button("🔍 Search", type="primary", use_container_width=True)
    
    # # Quick filters
    # st.subheader("📋 Quick Actions")
    # col1, col2, col3, col4 = st.columns(4)
    
    # with col1:
    #     if st.button("📄 Show All Documents", use_container_width=True):
    #         st.session_state.show_all_docs = True
    
    # with col2:
    #     if st.button("⚠️ High Priority Only", use_container_width=True):
    #         st.session_state.filter_priority = "High"
    
    # with col3:
    #     if st.button("📅 Recent Uploads", use_container_width=True):
    #         st.session_state.filter_recent = True
    
    # with col4:
    #     if st.button("🔄 Clear Filters", use_container_width=True):
    #         for key in ['show_all_docs', 'filter_priority', 'filter_recent']:
    #             if key in st.session_state:
    #                 del st.session_state[key]
    
    # Process search or filters
    documents = []
    
    if search_button and search_query:
        with st.spinner("🔍 Searching documents..."):
            documents = db.search_documents(search_query, user_info['role'])
            st.success(f"✅ Found {len(documents)} matching documents")
    
    elif st.session_state.get('show_all_docs'):
        documents = db.get_documents_by_role(user_info['role'])
        st.info(f"📋 Showing all {len(documents)} accessible documents")
    
    elif st.session_state.get('filter_priority'):
        all_docs = db.get_documents_by_role(user_info['role'])
        documents = [doc for doc in all_docs if doc.get('priority') == st.session_state.filter_priority]
        st.warning(f"⚠️ Found {len(documents)} high priority documents")
    
    elif st.session_state.get('filter_recent'):
        from datetime import datetime, timedelta
        all_docs = db.get_documents_by_role(user_info['role'])
        week_ago = datetime.now() - timedelta(days=7)
        documents = [
            doc for doc in all_docs 
            if datetime.fromisoformat(doc['upload_date']) > week_ago
        ]
        st.info(f"📅 Found {len(documents)} recent documents")
    
    # Display results
    if documents:
        # Create enhanced results display
        for i, doc in enumerate(documents):
            priority_color = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
            priority_icon = priority_color.get(doc.get('priority', 'Medium'), "🟡")
            
            with st.expander(f"{priority_icon} **{doc['filename']}** - {doc['document_type']}" + 
                           (f" (Score: {doc.get('search_score', 'N/A')})" if 'search_score' in doc else "")):
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**📝 Summary:** {doc['summary']}")
                    
                    if doc.get('action_items'):
                        st.markdown("**📋 Action Items:**")
                        for action in doc['action_items']:
                            st.markdown(f"• {action}")
                    
                    if doc.get('deadlines'):
                        st.markdown("**⏰ Deadlines:**")
                        for deadline in doc['deadlines']:
                            st.markdown(f"• {deadline}")
                    
                    if doc.get('risks'):
                        st.markdown("**⚠️ Risks/Warnings:**")
                        for risk in doc['risks']:
                            st.markdown(f"• {risk}")
                
                with col2:
                    st.markdown(f"**📂 Type:** {doc['document_type']}")
                    st.markdown(f"**📊 Priority:** {priority_icon} {doc['priority']}")
                    st.markdown(f"**📅 Uploaded:** {doc['upload_date'][:10]}")
                    st.markdown(f"**👤 By:** {doc['uploaded_by']}")
                    
                    if st.button(f"👁️ View Details", key=f"view_{doc['id']}"):
                        st.session_state.selected_doc = doc['id']
                        st.success(f"Selected document: {doc['filename']}")
    
    elif any(key in st.session_state for key in ['show_all_docs', 'filter_priority', 'filter_recent']) or (search_button and search_query):
        st.info("📭 No documents found matching your criteria.")

def show_audit_page(user_info):
    """Enhanced audit log page"""
    st.markdown("""
    <div class="main-header">
        <h2>📋 Audit Trail</h2>
        <p>Complete activity logging for compliance and security</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write(f"**Welcome, {user_info['name']}** ({user_info['role']})")
    
    db = DocumentDatabase()
    audit_log = db.get_audit_log()
    
    if audit_log:
        # Statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📊 Total Activities", len(audit_log))
        
        with col2:
            upload_count = len([entry for entry in audit_log if entry['action'] == 'UPLOAD'])
            st.metric("📤 Uploads", upload_count)
        
        with col3:
            view_count = len([entry for entry in audit_log if entry['action'] == 'VIEW'])
            st.metric("👁️ Views", view_count)
        
        with col4:
            search_count = len([entry for entry in audit_log if entry['action'] == 'SEARCH'])
            st.metric("🔍 Searches", search_count)
        
        st.markdown("---")
        
        # Enhanced audit table
        st.subheader("📋 Recent Activities")
        
        # Create audit table with better formatting
        audit_data = []
        for entry in reversed(audit_log[-50:]):  # Show last 50 entries
            audit_data.append({
                '🕐 Timestamp': entry['timestamp'][:19].replace('T', ' '),
                '🎯 Action': entry['action'],
                '👤 User': entry['user_name'],
                '🏷️ Role': entry['user_role'],
                '📄 Document ID': entry.get('document_id', 'N/A')[:20] + '...' if len(entry.get('document_id', '')) > 20 else entry.get('document_id', 'N/A'),
                '📝 Details': entry.get('details', 'N/A')[:50] + '...' if len(entry.get('details', '')) > 50 else entry.get('details', 'N/A')
            })
        
        if audit_data:
            df = pd.DataFrame(audit_data)
            st.dataframe(df, use_container_width=True, height=400)
        
        # Activity timeline chart
        if len(audit_log) > 1:
            st.subheader("📈 Activity Timeline")
            
            # Process data for timeline
            timeline_data = {}
            for entry in audit_log:
                date = entry['timestamp'][:10]
                timeline_data[date] = timeline_data.get(date, 0) + 1
            
            if timeline_data:
                timeline_df = pd.DataFrame(list(timeline_data.items()), columns=['Date', 'Activities'])
                timeline_df['Date'] = pd.to_datetime(timeline_df['Date'])
                
                fig = px.line(timeline_df, x='Date', y='Activities', 
                             title="Daily Activity Count",
                             markers=True)
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                )
                st.plotly_chart(fig, use_container_width=True)
    
    else:
        st.info("📭 No audit log entries found.")

def show_analytics_page(user_info):
    """Enhanced analytics and statistics page"""
    st.markdown("""
    <div class="main-header">
        <h2>📊 Analytics Dashboard</h2>
        <p>Comprehensive insights and document statistics</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write(f"**Welcome, {user_info['name']}** ({user_info['role']})")
    
    db = DocumentDatabase()
    stats = db.get_statistics()
    
    # Enhanced metrics display
    st.subheader("📈 System Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📚 Total Documents", stats['total_documents'], delta=None)
    
    with col2:
        st.metric("📂 Document Types", len(stats['documents_by_type']), delta=None)
    
    with col3:
        st.metric("📅 Recent Uploads", stats['recent_uploads'], delta=None)
    
    with col4:
        high_priority = stats['documents_by_priority'].get('High', 0)
        st.metric("⚠️ High Priority", high_priority, delta=None)
    
    if stats['total_documents'] > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Document Types Distribution")
            type_data = stats['documents_by_type']
            if type_data:
                fig = px.bar(
                    x=list(type_data.keys()),
                    y=list(type_data.values()),
                    title="Documents by Type",
                    color=list(type_data.values()),
                    color_continuous_scale="Blues"
                )
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("⚠️ Priority Breakdown")
            priority_data = stats['documents_by_priority']
            if priority_data:
                colors = {'High': '#ff4444', 'Medium': '#ffaa00', 'Low': '#44ff44'}
                fig = px.pie(
                    values=list(priority_data.values()),
                    names=list(priority_data.keys()),
                    title="Priority Distribution",
                    color=list(priority_data.keys()),
                    color_discrete_map=colors
                )
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                )
                st.plotly_chart(fig, use_container_width=True)
    
    # Role-specific analytics
    user_documents = db.get_documents_by_role(user_info['role'])
    
    st.markdown("---")
    st.subheader(f"🎯 Your Role Analytics ({user_info['role']})")
    
    if user_documents:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📄 Your Documents", len(user_documents))
        
        with col2:
            your_high_priority = len([doc for doc in user_documents if doc.get('priority') == 'High'])
            st.metric("⚠️ Your High Priority", your_high_priority)
        
        with col3:
            your_action_items = sum(len(doc.get('action_items', [])) for doc in user_documents)
            st.metric("📋 Your Action Items", your_action_items)
        
        # Role-specific insights with enhanced styling
        st.subheader("💡 Personalized Insights")
        
        insights_container = st.container()
        
        with insights_container:
            if user_info['role'] == 'Engineer':
                safety_docs = [doc for doc in user_documents if 'Safety' in doc['document_type']]
                job_cards = [doc for doc in user_documents if 'Job Card' in doc['document_type']]
                
                col1, col2 = st.columns(2)
                with col1:
                    st.info(f"🔧 **Engineering Focus**: You have {len(safety_docs)} safety-related documents to review.")
                with col2:
                    if job_cards:
                        st.warning(f"📋 **Active Jobs**: {len(job_cards)} job cards require your attention.")
            
            elif user_info['role'] == 'Finance':
                invoices = [doc for doc in user_documents if 'Invoice' in doc['document_type']]
                
                col1, col2 = st.columns(2)
                with col1:
                    st.info(f"💰 **Financial Overview**: You have {len(invoices)} invoices to process.")
                
                with col2:
                    # Calculate total invoice amount
                    total_amount = 0
                    for doc in invoices:
                        key_info = doc.get('key_information', {})
                        if 'amount' in key_info:
                            try:
                                amount = float(key_info['amount'].replace(',', ''))
                                total_amount += amount
                            except:
                                pass
                    
                    if total_amount > 0:
                        st.metric("💳 Total Invoice Amount", f"₹{total_amount:,.2f}")
            
            elif user_info['role'] == 'HR':
                policies = [doc for doc in user_documents if 'HR Policy' in doc['document_type']]
                safety_training = [doc for doc in user_documents if 'Safety' in doc['document_type']]
                
                col1, col2 = st.columns(2)
                with col1:
                    st.info(f"👥 **HR Management**: You have {len(policies)} HR policies to manage.")
                with col2:
                    if safety_training:
                        st.warning(f"🎓 **Training Updates**: {len(safety_training)} safety documents may require training updates.")
            
            elif user_info['role'] == 'Station Controller':
                operational = [doc for doc in user_documents if 'Operational' in doc['document_type']]
                st.info(f"🚇 **Operations**: You have {len(operational)} operational reports to review.")
            
            elif user_info['role'] == 'Compliance Officer':
                govt_docs = [doc for doc in user_documents if 'Government' in doc['document_type']]
                compliance_items = sum(1 for doc in user_documents if doc.get('priority') == 'High')
                
                col1, col2 = st.columns(2)
                with col1:
                    st.info(f"📋 **Compliance**: You have {len(govt_docs)} government circulars to review.")
                with col2:
                    if compliance_items > 0:
                        st.warning(f"⚠️ **Priority Items**: {compliance_items} high-priority compliance items need attention.")
    
    else:
        st.info("📭 No documents found for your role.")

def main():
    """Enhanced main application function"""
    
    try:
        # Initialize authentication
        auth_manager = AuthManager()
        
        # Check authentication
        if not auth_manager.is_authenticated():
            # Enhanced login page
            st.markdown("""
            <div class="main-header">
                <h1>🚇 KochiMetro DocuTrack</h1>
                <p>Intelligent Document Management System for KMRL</p>
            </div>
            """, unsafe_allow_html=True)
            
            auth_manager.login_form()
            return
        
        # Get current user
        user_info = auth_manager.get_current_user()
        
        # Enhanced sidebar navigation
        with st.sidebar:
            st.markdown(f"""
            <div class="main-header">
                <h2>🚇 DocuTrack</h2>
                <p><strong>{user_info['name']}</strong><br>
                <em>{user_info['role']}</em></p>
            </div>
            """, unsafe_allow_html=True)
            
            # Navigation menu with icons
            page_options = [
                "📊 Dashboard", 
                "📤 Upload Documents", 
                "🔍 Search Documents", 
                "📋 Audit Log", 
                "📈 Analytics"
            ]
            
            page = st.selectbox(
                "🧭 Navigate to:",
                page_options,
                key="navigation"
            )
            
            st.markdown("---")
            
            # Enhanced quick stats
            try:
                db = DocumentDatabase()
                user_docs = db.get_documents_by_role(user_info['role'])
                
                st.markdown("### 📊 Quick Stats")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("📄 Documents", len(user_docs))
                with col2:
                    high_priority = len([doc for doc in user_docs if doc.get('priority') == 'High'])
                    st.metric("⚠️ Priority", high_priority)
                
                # Recent activity indicator
                from datetime import datetime, timedelta
                recent_docs = [
                    doc for doc in user_docs 
                    if datetime.fromisoformat(doc['upload_date']) > datetime.now() - timedelta(days=1)
                ]
                
                if recent_docs:
                    st.success(f"🆕 {len(recent_docs)} new document(s) today!")
                
            except Exception as e:
                st.error(f"Error loading stats: {str(e)}")
            
            st.markdown("---")
            
            # Enhanced logout button
            if st.button("🚪 Logout", type="secondary", use_container_width=True):
                auth_manager.logout()
        
        # Main content area with error handling
        try:
            if page == "📊 Dashboard":
                show_dashboard_page(user_info)
            elif page == "📤 Upload Documents":
                show_upload_page(user_info)
            elif page == "🔍 Search Documents":
                show_search_page(user_info)
            elif page == "📋 Audit Log":
                show_audit_page(user_info)
            elif page == "📈 Analytics":
                show_analytics_page(user_info)
        
        except Exception as e:
            st.error(f"Error loading page: {str(e)}")
            st.info("Please try refreshing the page or contact support.")
    
    except Exception as e:
        st.error(f"Application error: {str(e)}")
        st.info("Please refresh the page to restart the application.")

if __name__ == "__main__":
    main()
