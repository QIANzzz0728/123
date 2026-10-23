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
    total_sales = df['sales'].sum() if 'sales' in df.columns else 0
    if 'profit' in df.columns and total_sales != 0:
        avg_profit_margin = (df['profit'].sum() / total_sales) * 100
    else:
        avg_profit_margin = 0
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
        # 智能识别中文/英文列名，统一映射为代码使用的标准列
        column_mapping = {
            '日期': 'date', '时间': 'date', '订单日期': 'date', '下单时间': 'date',
            '销售额': 'sales', '销量': 'sales', '金额': 'sales', '营收': 'sales',
            '利润': 'profit', '利润额': 'profit',
            '地区': 'region', '区域': 'region', '省份': 'region', '城市': 'region', '门店': 'region',
            '产品': 'product', '商品': 'product', '品类': 'product', '商品名称': 'product',
        }
        df = df.rename(columns={c: column_mapping[c] for c in df.columns if c in column_mapping})
        # 自动转换日期列格式（如果存在）
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
        # 提示缺失的关键列
        missing = [c for c in ['date', 'sales', 'region', 'product'] if c not in df.columns]
        if missing:
            st.sidebar.warning(f"你的数据缺少这些列，相关图表可能不显示：{', '.join(missing)}")
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