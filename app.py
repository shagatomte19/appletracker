import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import plotly.express as px
import plotly.graph_objects as go

# Import our modules
from database import DatabaseManager
from models import JobApplication
from utils import (
    create_status_chart, 
    create_timeline_chart, 
    create_company_chart,
    filter_dataframe,
    export_to_csv,
    calculate_metrics
)
from config import (
    PAGE_TITLE, 
    PAGE_ICON, 
    LAYOUT, 
    STATUS_OPTIONS,
    STATUS_COLORS
)

# Page configuration
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=LAYOUT,
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
.main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 10px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
}

.metric-card {
    background: white;
    padding: 1rem;
    border-radius: 8px;
    border-left: 4px solid #667eea;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.status-badge {
    padding: 0.25rem 0.5rem;
    border-radius: 20px;
    color: white;
    font-size: 0.8rem;
    text-align: center;
    display: inline-block;
}

.stSelectbox > div > div > select {
    background-color: #f8fafc;
}
</style>
""", unsafe_allow_html=True)

def init_session_state():
    """Initialize session state variables."""
    if 'db_manager' not in st.session_state:
        st.session_state.db_manager = DatabaseManager()
    
    if 'show_add_form' not in st.session_state:
        st.session_state.show_add_form = False
    
    if 'edit_application' not in st.session_state:
        st.session_state.edit_application = None

def main():
    """Main application function."""
    init_session_state()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎯 Shagato's Applications</h1>
        <p>bhai overthinking koris na, kichu ekta manage hobe</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("🛠️ Controls")
        
        # Add new application button
        if st.button("➕ Add New Application", type="primary", use_container_width=True):
            st.session_state.show_add_form = True
        
        st.markdown("---")
        
        # Filters
        st.subheader("🔍 Filters")
        
        search_term = st.text_input("Search", placeholder="Search by title, company, or location...")
        
        status_filter = st.multiselect(
            "Filter by Status",
            options=STATUS_OPTIONS,
            default=[]
        )
        
        date_range = st.date_input(
            "Date Range",
            value=(date.today() - timedelta(days=90), date.today()),
            key="date_filter"
        )
        
        st.markdown("---")
        
        # Export functionality
        st.subheader("📁 Export Data")
        if st.button("Export to CSV", use_container_width=True):
            df = st.session_state.db_manager.get_applications_df()
            csv = export_to_csv(df)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"job_applications_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    # Load data
    applications = st.session_state.db_manager.get_all_applications()
    df = st.session_state.db_manager.get_applications_df()
    
    # Apply filters
    if not df.empty:
        df = filter_dataframe(df, search_term, status_filter, date_range)
    
    # Dashboard metrics
    col1, col2, col3, col4 = st.columns(4)
    
    metrics = calculate_metrics(df)
    status_counts = st.session_state.db_manager.get_status_counts()
    
    with col1:
        st.metric("Total Applications", metrics['total_applications'])
    
    with col2:
        st.metric("Response Rate", f"{metrics['response_rate']:.1f}%")
    
    with col3:
        st.metric("Interview Rate", f"{metrics['interview_rate']:.1f}%")
    
    with col4:
        st.metric("Offer Rate", f"{metrics['offer_rate']:.1f}%")
    
    # Charts
    if not df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            status_chart = create_status_chart(status_counts)
            if status_chart:
                st.plotly_chart(status_chart, use_container_width=True)
        
        with col2:
            timeline_chart = create_timeline_chart(df)
            if timeline_chart:
                st.plotly_chart(timeline_chart, use_container_width=True)
        
        # Company applications chart
        company_chart = create_company_chart(df)
        if company_chart:
            st.plotly_chart(company_chart, use_container_width=True)
    
    # Add/Edit Application Form
    if st.session_state.show_add_form or st.session_state.edit_application:
        show_application_form()
    
    # Applications table
    st.subheader("📋 Your Applications")
    
    if not df.empty:
        # Display applications
        display_applications_table(df)
    else:
        st.info("No applications found. Add your first application to get started!")
    # Stylish Footer
    st.markdown("---")
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px 20px;
        border-radius: 15px;
        text-align: center;
        margin-top: 50px;
        color: white;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    ">
        <div style="
            font-size: 2.5em;
            margin-bottom: 15px;
            animation: pulse 2s infinite;
        ">🙏</div>
        <div style="
            font-size: 1.4em;
            font-weight: 600;
            margin-bottom: 10px;
            text-shadow: 0 2px 4px rgba(0,0,0,0.2);
        ">Dowa chai bhai</div>
        <div style="
            font-size: 1em;
            opacity: 0.9;
            font-style: italic;
        ">Keep Hunting 🌟</div>
        <div style="
            margin-top: 20px;
            font-size: 0.9em;
            opacity: 0.8;
            border-top: 1px solid rgba(255,255,255,0.2);
            padding-top: 15px;
        ">
            Built with ❤️ using Streamlit | © 2025 ShagatoApple
        </div>
    </div>
    
    <style>
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
    
    .stMarkdown div[data-testid="stMarkdownContainer"] p {
        margin-bottom: 0;
    }
    </style>
    """, unsafe_allow_html=True)

def show_application_form():
    """Display the add/edit application form."""
    is_editing = st.session_state.edit_application is not None
    title = "✏️ Edit Application" if is_editing else "➕ Add New Application"
    
    with st.expander(title, expanded=True):
        with st.form("application_form", clear_on_submit=not is_editing):
            col1, col2 = st.columns(2)
            
            # Get current values if editing
            current_app = st.session_state.edit_application if is_editing else None
            
            with col1:
                job_title = st.text_input(
                    "Job Title *",
                    value=current_app.job_title if current_app else "",
                    placeholder="e.g., Software Engineer"
                )
                
                company_name = st.text_input(
                    "Company Name *",
                    value=current_app.company_name if current_app else "",
                    placeholder="e.g., Google"
                )
                
                location = st.text_input(
                    "Location *",
                    value=current_app.location if current_app else "",
                    placeholder="e.g., San Francisco, CA"
                )
                
                salary_range = st.text_input(
                    "Salary Range",
                    value=current_app.salary_range if current_app else "",
                    placeholder="e.g., $100k - $150k"
                )
            
            with col2:
                application_date = st.date_input(
                    "Application Date *",
                    value=datetime.strptime(current_app.application_date, '%Y-%m-%d').date() if current_app else date.today()
                )
                
                status = st.selectbox(
                    "Status *",
                    options=STATUS_OPTIONS,
                    index=STATUS_OPTIONS.index(current_app.status) if current_app else 0
                )
                
                job_description = st.text_area(
                    "Job Description",
                    value=current_app.job_description if current_app else "",
                    placeholder="Brief description of the role..."
                )
                
                notes = st.text_area(
                    "Notes",
                    value=current_app.notes if current_app else "",
                    placeholder="Any additional notes..."
                )
            
            # Form buttons
            col1, col2, col3 = st.columns([1, 1, 2])
            
            with col1:
                submitted = st.form_submit_button(
                    "Update Application" if is_editing else "Add Application",
                    type="primary",
                    use_container_width=True
                )
            
            with col2:
                cancelled = st.form_submit_button(
                    "Cancel",
                    use_container_width=True
                )
            
            if submitted:
                if job_title and company_name and location:
                    application = JobApplication(
                        id=current_app.id if current_app else None,
                        job_title=job_title,
                        company_name=company_name,
                        location=location,
                        application_date=application_date.strftime('%Y-%m-%d'),
                        status=status,
                        salary_range=salary_range if salary_range else None,
                        job_description=job_description if job_description else None,
                        notes=notes if notes else None
                    )
                    
                    if is_editing:
                        success = st.session_state.db_manager.update_application(current_app.id, application)
                        if success:
                            st.success("Application updated successfully!")
                            st.session_state.edit_application = None
                        else:
                            st.error("Failed to update application.")
                    else:
                        application_id = st.session_state.db_manager.add_application(application)
                        if application_id:
                            st.success("Application added successfully!")
                            st.session_state.show_add_form = False
                        else:
                            st.error("Failed to add application.")
                    
                    st.rerun()
                else:
                    st.error("Please fill in all required fields marked with *")
            
            if cancelled:
                st.session_state.show_add_form = False
                st.session_state.edit_application = None
                st.rerun()

def display_applications_table(df):
    """Display the applications table with action buttons."""
    # Configure columns for display
    display_columns = [
        'job_title', 'company_name', 'location', 
        'application_date', 'status', 'salary_range'
    ]
    
    # Create a copy for display
    display_df = df[display_columns].copy()
    display_df.columns = [
        'Job Title', 'Company', 'Location', 
        'Date', 'Status', 'Salary Range'
    ]
    
    # Format date
    display_df['Date'] = pd.to_datetime(display_df['Date']).dt.strftime('%Y-%m-%d')
    
    # Display table
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Status": st.column_config.TextColumn(
                "Status",
                width="small",
            ),
            "Date": st.column_config.DateColumn(
                "Date",
                width="small"
            ),
            "Job Title": st.column_config.TextColumn(
                "Job Title",
                width="medium"
            ),
            "Company": st.column_config.TextColumn(
                "Company", 
                width="medium"
            )
        }
    )
    
    # Action buttons
    st.subheader("🔧 Actions")
    
    # Get application IDs for selection
    application_options = {
        f"{row['company_name']} - {row['job_title']}": row['id'] 
        for _, row in df.iterrows()
    }
    
    if application_options:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            selected_app = st.selectbox(
                "Select Application",
                options=list(application_options.keys()),
                key="action_selector"
            )
        
        with col2:
            if st.button("Edit", use_container_width=True):
                app_id = application_options[selected_app]
                applications = st.session_state.db_manager.get_all_applications()
                selected_application = next((app for app in applications if app.id == app_id), None)
                if selected_application:
                    st.session_state.edit_application = selected_application
                    st.rerun()
        
        with col3:
            if st.button("Delete", type="secondary", use_container_width=True):
                app_id = application_options[selected_app]
                if st.session_state.db_manager.delete_application(app_id):
                    st.success("Application deleted successfully!")
                    st.rerun()
                else:
                    st.error("Failed to delete application.")

if __name__ == "__main__":

    main()

