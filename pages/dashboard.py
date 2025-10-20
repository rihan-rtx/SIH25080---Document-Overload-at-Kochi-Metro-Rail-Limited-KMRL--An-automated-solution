"""
Enhanced role-based dashboard page with improved UI
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from modules.database import DocumentDatabase
from config import USER_ROLES
from datetime import datetime, timedelta

def show_dashboard_page(user_info):
    st.markdown(f"""
    <div class="main-header">
        <h2>📊 {user_info['role']} Dashboard</h2>
        <p>Your personalized document management overview</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write(f"**Welcome back, {user_info['name']}!** 👋")
    
    try:
        db = DocumentDatabase()
        
        # Get user's accessible documents
        user_documents = db.get_documents_by_role(user_info['role'])
        
        # Enhanced dashboard metrics with better styling
        st.subheader("📈 Key Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_docs = len(user_documents)
            st.metric("📚 Total Documents", total_docs, delta=None)
        
        with col2:
            high_priority = len([doc for doc in user_documents if doc.get('priority') == 'High'])
            delta_priority = f"+{high_priority}" if high_priority > 0 else None
            st.metric("🚨 High Priority", high_priority, delta=delta_priority)
        
        with col3:
            recent_docs = len([
                doc for doc in user_documents 
                if datetime.fromisoformat(doc['upload_date']) > datetime.now() - timedelta(days=7)
            ])
            st.metric("📅 This Week", recent_docs, delta=f"+{recent_docs}" if recent_docs > 0 else None)
        
        with col4:
            action_items = sum(len(doc.get('action_items', [])) for doc in user_documents)
            st.metric("📋 Action Items", action_items, delta=f"+{action_items}" if action_items > 0 else None)
        
        # Charts section with enhanced visuals
        if user_documents:
            st.markdown("---")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📊 Document Types")
                type_counts = {}
                for doc in user_documents:
                    doc_type = doc['document_type']
                    type_counts[doc_type] = type_counts.get(doc_type, 0) + 1
                
                if type_counts:
                    # Create a more appealing donut chart
                    fig = px.pie(
                        values=list(type_counts.values()),
                        names=list(type_counts.keys()),
                        title="Document Distribution",
                        hole=0.4,
                        color_discrete_sequence=px.colors.qualitative.Set3
                    )
                    fig.update_traces(textposition='inside', textinfo='percent+label')
                    fig.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(size=12),
                        showlegend=True,
                        legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.05)
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("📈 Upload Timeline")
                # Create enhanced timeline data
                timeline_data = []
                for doc in user_documents:
                    upload_date = datetime.fromisoformat(doc['upload_date']).date()
                    timeline_data.append({
                        'Date': upload_date,
                        'Count': 1,
                        'Type': doc['document_type'],
                        'Priority': doc.get('priority', 'Medium')
                    })
                
                if timeline_data:
                    df = pd.DataFrame(timeline_data)
                    daily_counts = df.groupby(['Date', 'Priority'])['Count'].sum().reset_index()
                    
                    fig = px.bar(
                        daily_counts,
                        x='Date',
                        y='Count',
                        color='Priority',
                        title="Documents by Upload Date & Priority",
                        color_discrete_map={'High': '#ff4444', 'Medium': '#ffaa00', 'Low': '#44ff44'}
                    )
                    fig.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        xaxis_title="Upload Date",
                        yaxis_title="Number of Documents"
                    )
                    st.plotly_chart(fig, use_container_width=True)
        
        # Enhanced priority documents section
        st.markdown("---")
        st.subheader("🚨 High Priority Documents")
        
        high_priority_docs = [doc for doc in user_documents if doc.get('priority') == 'High']
        
        if high_priority_docs:
            for i, doc in enumerate(high_priority_docs[:5]):  # Show top 5
                with st.expander(f"⚠️ **{doc['filename']}** - {doc['document_type']}", expanded=(i==0)):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown(f"**📝 Summary:** {doc['summary']}")
                        
                        if doc.get('action_items'):
                            st.markdown("**📋 Action Items:**")
                            for j, action in enumerate(doc['action_items'], 1):
                                st.markdown(f"{j}. {action}")
                        
                        if doc.get('deadlines'):
                            st.markdown("**⏰ Deadlines:**")
                            for deadline in doc['deadlines']:
                                st.markdown(f"🗓️ {deadline}")
                        
                        if doc.get('risks'):
                            st.markdown("**⚠️ Risks & Warnings:**")
                            for risk in doc['risks']:
                                st.markdown(f"🔺 {risk}")
                    
                    with col2:
                        st.markdown(f"**📅 Uploaded:** {doc['upload_date'][:10]}")
                        st.markdown(f"**👤 By:** {doc['uploaded_by']}")
                        st.markdown(f"**🏷️ Type:** {doc['document_type']}")
                        st.markdown(f"**🔍 Confidence:** {doc.get('classification_confidence', 'N/A')}%")
                        
                        if st.button(f"👁️ View Full Details", key=f"view_{doc['id']}", use_container_width=True):
                            st.session_state.selected_doc = doc['id']
                            st.success(f"✅ Selected: {doc['filename']}")
        else:
            st.info("✅ No high priority documents found. Great job!")
        
        # Enhanced recent documents section
        st.markdown("---")
        st.subheader("📋 Recent Documents")
        
        recent_docs = sorted(user_documents, key=lambda x: x['upload_date'], reverse=True)[:10]
        
        if recent_docs:
            # Create enhanced table view
            table_data = []
            for doc in recent_docs:
                # Add status indicators
                status_icon = "🔴" if doc.get('priority') == 'High' else "🟡" if doc.get('priority') == 'Medium' else "🟢"
                
                table_data.append({
                    'Status': status_icon,
                    'Filename': doc['filename'][:30] + '...' if len(doc['filename']) > 30 else doc['filename'],
                    'Type': doc['document_type'],
                    'Priority': doc['priority'],
                    'Upload Date': doc['upload_date'][:10],
                    'Uploaded By': doc['uploaded_by'],
                    'Summary': doc['summary'][:80] + "..." if len(doc['summary']) > 80 else doc['summary']
                })
            
            df = pd.DataFrame(table_data)
            
            # Add interactive filtering
            col1, col2, col3 = st.columns(3)
            
            with col1:
                type_filter = st.selectbox("Filter by Type:", ["All"] + list(df['Type'].unique()), key="recent_type_filter")
            
            with col2:
                priority_filter = st.selectbox("Filter by Priority:", ["All"] + list(df['Priority'].unique()), key="recent_priority_filter")
            
            with col3:
                uploader_filter = st.selectbox("Filter by Uploader:", ["All"] + list(df['Uploaded By'].unique()), key="recent_uploader_filter")
            
            # Apply filters
            filtered_df = df.copy()
            if type_filter != "All":
                filtered_df = filtered_df[filtered_df['Type'] == type_filter]
            if priority_filter != "All":
                filtered_df = filtered_df[filtered_df['Priority'] == priority_filter]
            if uploader_filter != "All":
                filtered_df = filtered_df[filtered_df['Uploaded By'] == uploader_filter]
            
            st.dataframe(filtered_df, use_container_width=True, height=300)
            
            # Download option
            if st.button("📥 Export Document List", use_container_width=False):
                csv = filtered_df.to_csv(index=False)
                st.download_button(
                    label="💾 Download CSV",
                    data=csv,
                    file_name=f"documents_{user_info['role']}_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
        
        else:
            st.info("📭 No documents found for your role. Upload some documents to get started!")
        
        # Enhanced role-specific insights
        st.markdown("---")
        st.subheader(f"💡 {user_info['role']} Insights")
        
        # Create insights based on role
        insights_container = st.container()
        
        with insights_container:
            if user_info['role'] == 'Engineer':
                safety_docs = [doc for doc in user_documents if 'Safety' in doc['document_type']]
                job_cards = [doc for doc in user_documents if 'Job Card' in doc['document_type']]
                engineering_docs = [doc for doc in user_documents if 'Engineering' in doc['document_type']]
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.info(f"🔧 **Safety Documents**\n{len(safety_docs)} safety-related items to review")
                
                with col2:
                    if job_cards:
                        st.warning(f"📋 **Active Job Cards**\n{len(job_cards)} jobs require attention")
                    else:
                        st.success("✅ **No Pending Jobs**\nAll job cards completed")
                
                with col3:
                    st.info(f"📐 **Engineering Docs**\n{len(engineering_docs)} technical documents")
            
            elif user_info['role'] == 'Finance':
                invoices = [doc for doc in user_documents if 'Invoice' in doc['document_type']]
                govt_docs = [doc for doc in user_documents if 'Government' in doc['document_type']]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.info(f"💰 **Financial Documents**\n{len(invoices)} invoices to process")
                    
                    # Calculate total amount
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
                        st.metric("💳 Total Amount", f"₹{total_amount:,.2f}")
                
                with col2:
                    st.info(f"📋 **Compliance**\n{len(govt_docs)} government circulars")
            
            elif user_info['role'] == 'HR':
                policies = [doc for doc in user_documents if 'HR Policy' in doc['document_type']]
                safety_training = [doc for doc in user_documents if 'Safety' in doc['document_type']]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.info(f"👥 **HR Policies**\n{len(policies)} policies to manage")
                
                with col2:
                    if safety_training:
                        st.warning(f"🎓 **Training Required**\n{len(safety_training)} safety updates need training")
                    else:
                        st.success("✅ **Training Up-to-Date**\nNo pending safety training")
            
            elif user_info['role'] == 'Station Controller':
                operational = [doc for doc in user_documents if 'Operational' in doc['document_type']]
                safety_docs = [doc for doc in user_documents if 'Safety' in doc['document_type']]
                job_cards = [doc for doc in user_documents if 'Job Card' in doc['document_type']]
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.info(f"🚇 **Operations**\n{len(operational)} reports to review")
                
                with col2:
                    st.info(f"🔧 **Maintenance**\n{len(job_cards)} job cards")
                
                with col3:
                    if safety_docs:
                        st.warning(f"⚠️ **Safety Alerts**\n{len(safety_docs)} safety notices")
                    else:
                        st.success("✅ **No Safety Issues**\nAll clear")
            
            elif user_info['role'] == 'Compliance Officer':
                govt_docs = [doc for doc in user_documents if 'Government' in doc['document_type']]
                safety_docs = [doc for doc in user_documents if 'Safety' in doc['document_type']]
                policies = [doc for doc in user_documents if 'Policy' in doc['document_type']]
                
                compliance_items = sum(1 for doc in user_documents if doc.get('priority') == 'High')
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.info(f"📋 **Government Circulars**\n{len(govt_docs)} to review")
                
                with col2:
                    st.info(f"📜 **Policies**\n{len(policies)} policy documents")
                
                with col3:
                    if compliance_items > 0:
                        st.warning(f"⚠️ **Priority Items**\n{compliance_items} high-priority items")
                    else:
                        st.success("✅ **Compliance Good**\nNo urgent items")
        
        # # Quick actions section
        # st.markdown("---")
        # st.subheader("⚡ Quick Actions")
        
        # col1, col2, col3, col4 = st.columns(4)
        
        # with col1:
        #     if st.button("📤 Upload New Document", use_container_width=True):
        #         st.session_state.navigation = "📤 Upload Documents"
        #         st.rerun()
        
        # with col2:
        #     if st.button("🔍 Search Documents", use_container_width=True):
        #         st.session_state.navigation = "🔍 Search Documents"
        #         st.rerun()
        
        # with col3:
        #     if st.button("📋 View Audit Log", use_container_width=True):
        #         st.session_state.navigation = "📋 Audit Log"
        #         st.rerun()
        
        # with col4:
        #     if st.button("📈 View Analytics", use_container_width=True):
        #         st.session_state.navigation = "📈 Analytics"
        #         st.rerun()
    
    except Exception as e:
        st.error(f"Error loading dashboard: {str(e)}")
        st.info("Please try refreshing the page or contact support if the issue persists.")
        
        # Show basic fallback info
        st.subheader("📊 Basic Information")
        st.write(f"**User:** {user_info['name']}")
        st.write(f"**Role:** {user_info['role']}")
        st.write(f"**Access Level:** {', '.join(USER_ROLES.get(user_info['role'], []))}")