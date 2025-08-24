import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import streamlit as st
from config import STATUS_COLORS

def create_status_chart(status_counts: dict):
    """Create a donut chart for application status distribution."""
    if not status_counts:
        return None
    
    labels = list(status_counts.keys())
    values = list(status_counts.values())
    colors = [STATUS_COLORS.get(status, '#6b7280') for status in labels]
    
    fig = go.Figure(data=[go.Pie(
        labels=labels, 
        values=values,
        hole=.3,
        marker_colors=colors,
        textinfo='label+percent',
        textposition='inside'
    )])
    
    fig.update_layout(
        title="Application Status Distribution",
        showlegend=True,
        height=400,
        margin=dict(t=50, b=50, l=50, r=50)
    )
    
    return fig

def create_timeline_chart(df: pd.DataFrame):
    """Create a timeline chart showing applications over time."""
    if df.empty:
        return None
    
    # Convert application_date to datetime
    df['application_date'] = pd.to_datetime(df['application_date'])
    
    # Group by date and count applications
    timeline_data = df.groupby('application_date').size().reset_index(name='count')
    timeline_data = timeline_data.sort_values('application_date')
    
    # Create cumulative sum
    timeline_data['cumulative'] = timeline_data['count'].cumsum()
    
    fig = go.Figure()
    
    # Add daily applications
    fig.add_trace(go.Scatter(
        x=timeline_data['application_date'],
        y=timeline_data['count'],
        mode='markers+lines',
        name='Daily Applications',
        line=dict(color='#3b82f6', width=2),
        marker=dict(size=8)
    ))
    
    # Add cumulative applications
    fig.add_trace(go.Scatter(
        x=timeline_data['application_date'],
        y=timeline_data['cumulative'],
        mode='lines',
        name='Cumulative Applications',
        line=dict(color='#10b981', width=3),
        yaxis='y2'
    ))
    
    fig.update_layout(
        title="Applications Timeline",
        xaxis_title="Date",
        yaxis=dict(title="Daily Applications", side='left'),
        yaxis2=dict(title="Cumulative Applications", side='right', overlaying='y'),
        height=400,
        showlegend=True
    )
    
    return fig

def create_company_chart(df: pd.DataFrame):
    """Create a bar chart showing applications by company."""
    if df.empty:
        return None
    
    company_counts = df['company_name'].value_counts().head(10)
    
    fig = px.bar(
        x=company_counts.values,
        y=company_counts.index,
        orientation='h',
        title="Top Companies Applied To",
        labels={'x': 'Number of Applications', 'y': 'Company'},
        color=company_counts.values,
        color_continuous_scale='viridis'
    )
    
    fig.update_layout(height=400, showlegend=False)
    return fig

def filter_dataframe(df: pd.DataFrame, search_term: str, status_filter: list, date_range: tuple) -> pd.DataFrame:
    """Filter dataframe based on search criteria."""
    if df.empty:
        return df
    
    filtered_df = df.copy()
    
    # Text search
    if search_term:
        filtered_df = filtered_df[
            filtered_df['job_title'].str.contains(search_term, case=False) |
            filtered_df['company_name'].str.contains(search_term, case=False) |
            filtered_df['location'].str.contains(search_term, case=False)
        ]
    
    # Status filter
    if status_filter:
        filtered_df = filtered_df[filtered_df['status'].isin(status_filter)]
    
    # Date range filter
    if date_range and len(date_range) == 2:
        start_date, end_date = date_range
        filtered_df['application_date'] = pd.to_datetime(filtered_df['application_date'])
        filtered_df = filtered_df[
            (filtered_df['application_date'] >= pd.to_datetime(start_date)) &
            (filtered_df['application_date'] <= pd.to_datetime(end_date))
        ]
    
    return filtered_df

def export_to_csv(df: pd.DataFrame) -> str:
    """Export dataframe to CSV format."""
    return df.to_csv(index=False)

def calculate_metrics(df: pd.DataFrame) -> dict:
    """Calculate key metrics from the applications data."""
    if df.empty:
        return {
            'total_applications': 0,
            'response_rate': 0,
            'interview_rate': 0,
            'offer_rate': 0
        }
    
    total = len(df)
    responded = len(df[~df['status'].isin(['Applied', 'Follow-up'])])
    interviewed = len(df[df['status'].str.contains('Interview', case=False)])
    offered = len(df[df['status'].isin(['Offered', 'Accepted'])])
    
    return {
        'total_applications': total,
        'response_rate': (responded / total * 100) if total > 0 else 0,
        'interview_rate': (interviewed / total * 100) if total > 0 else 0,
        'offer_rate': (offered / total * 100) if total > 0 else 0
    }