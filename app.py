import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

def load_sample_data():
    """Load sample data for the dashboard"""
    np.random.seed(42)
    dates = [datetime.now() - timedelta(days=x) for x in range(30, 0, -1)]
    
    data = {
        'date': dates,
        'sales': np.random.randint(100, 1000, 30),
        'profit': np.random.randint(10, 100, 30),
        'region': np.random.choice(['North', 'South', 'East', 'West'], 30),
        'product': np.random.choice(['Product A', 'Product B', 'Product C'], 30)
    }
    
    return pd.DataFrame(data)

def calculate_metrics(df):
    """Calculate key business metrics"""
    total_sales = df['sales'].sum()
    avg_profit_margin = (df['profit'].sum() / df['sales'].sum()) * 100
    total_transactions = len(df)
    
    return {
        'total_sales': total_sales,
        'avg_profit_margin': avg_profit_margin,
        'total_transactions': total_transactions
    }

def create_sales_chart(df):
    """Create sales trend chart"""
    daily_sales = df.groupby('date')['sales'].sum().reset_index()
    fig = px.line(daily_sales, x='date', y='sales', 
                  title='Daily Sales Trend',
                  labels={'sales': 'Sales ($)', 'date': 'Date'})
    return fig

def create_region_chart(df):
    """Create regional performance chart"""
    region_sales = df.groupby('region')['sales'].sum().reset_index()
    fig = px.bar(region_sales, x='region', y='sales',
                 title='Sales by Region',
                 labels={'sales': 'Sales ($)', 'region': 'Region'})
    return fig

def main():
    """Main Streamlit app"""
    st.set_page_config(
        page_title="Sales Dashboard",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("📊 Sales Analytics Dashboard")
    st.markdown("---")
    
    # Load data: 优先使用用户上传的CSV，否则用示例数据
    st.sidebar.header("📂 数据来源")
    uploaded_file = st.sidebar.file_uploader(
        "上传你的销售数据（CSV 文件）",
        type=["csv"]
    )

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        # 自动转换日期列格式（如果存在）
        for col in df.columns:
            if 'date' in col.lower() or '日期' in col:
                df[col] = pd.to_datetime(df[col], errors='coerce')
    else:
        st.sidebar.info("未上传文件时，显示自动生成的示例数据")
        df = load_sample_data()

    metrics = calculate_metrics(df)
    
    # Sidebar filters
    st.sidebar.header("Filters")
    selected_regions = st.sidebar.multiselect(
        "Select Regions",
        options=df['region'].unique(),
        default=df['region'].unique()
    )
    
    selected_products = st.sidebar.multiselect(
        "Select Products", 
        options=df['product'].unique(),
        default=df['product'].unique()
    )
    
    # Filter data
    filtered_df = df[
        (df['region'].isin(selected_regions)) & 
        (df['product'].isin(selected_products))
    ]
    
    # Metrics row
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Total Sales",
            value=f"${metrics['total_sales']:,}",
            delta="12% vs last month"
        )
    
    with col2:
        st.metric(
            label="Avg Profit Margin",
            value=f"{metrics['avg_profit_margin']:.1f}%",
            delta="2.3% vs last month"
        )
    
    with col3:
        st.metric(
            label="Total Transactions",
            value=f"{metrics['total_transactions']:,}",
            delta="8% vs last month"
        )
    
    # Charts row
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(create_sales_chart(filtered_df), use_container_width=True)
    
    with col2:
        st.plotly_chart(create_region_chart(filtered_df), use_container_width=True)
    
    # Data table
    st.subheader("📋 Raw Data")
    st.dataframe(filtered_df, use_container_width=True)
    
    # Download button
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name=f"sales_data_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

if __name__ == "__main__":
    main() 