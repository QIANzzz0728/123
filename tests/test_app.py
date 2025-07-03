import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Add the parent directory to the path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import (
    load_sample_data, 
    calculate_metrics, 
    create_sales_chart, 
    create_region_chart
)

class TestDataLoading:
    """Test data loading functionality"""
    
    def test_load_sample_data_returns_dataframe(self):
        """Test that load_sample_data returns a pandas DataFrame"""
        df = load_sample_data()
        assert isinstance(df, pd.DataFrame)
    
    def test_load_sample_data_has_expected_columns(self):
        """Test that the DataFrame has all expected columns"""
        df = load_sample_data()
        expected_columns = ['date', 'sales', 'profit', 'region', 'product']
        assert all(col in df.columns for col in expected_columns)
    
    def test_load_sample_data_has_correct_shape(self):
        """Test that the DataFrame has the expected number of rows"""
        df = load_sample_data()
        assert len(df) == 30  # 30 days of data
        assert len(df.columns) == 5  # 5 columns
    
    def test_data_types_are_correct(self):
        """Test that data types are as expected"""
        df = load_sample_data()
        assert df['sales'].dtype in [np.int32, np.int64]
        assert df['profit'].dtype in [np.int32, np.int64]
        assert df['region'].dtype == 'object'
        assert df['product'].dtype == 'object'
    
    def test_sales_values_are_positive(self):
        """Test that sales values are positive"""
        df = load_sample_data()
        assert all(df['sales'] > 0)
    
    def test_profit_values_are_positive(self):
        """Test that profit values are positive"""
        df = load_sample_data()
        assert all(df['profit'] > 0)
    
    def test_dates_are_in_correct_range(self):
        """Test that dates are within the last 30 days"""
        df = load_sample_data()
        today = datetime.now()
        thirty_days_ago = today - timedelta(days=30)
        
        assert all(df['date'] >= thirty_days_ago.date())
        assert all(df['date'] <= today.date())

class TestMetricsCalculation:
    """Test metrics calculation functionality"""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample data for testing"""
        data = {
            'date': [datetime.now().date()] * 5,
            'sales': [100, 200, 300, 400, 500],
            'profit': [10, 20, 30, 40, 50],
            'region': ['North'] * 5,
            'product': ['Product A'] * 5
        }
        return pd.DataFrame(data)
    
    def test_calculate_metrics_returns_dict(self, sample_data):
        """Test that calculate_metrics returns a dictionary"""
        metrics = calculate_metrics(sample_data)
        assert isinstance(metrics, dict)
    
    def test_calculate_metrics_has_expected_keys(self, sample_data):
        """Test that metrics dict has all expected keys"""
        metrics = calculate_metrics(sample_data)
        expected_keys = ['total_sales', 'avg_profit_margin', 'total_transactions']
        assert all(key in metrics for key in expected_keys)
    
    def test_total_sales_calculation(self, sample_data):
        """Test total sales calculation"""
        metrics = calculate_metrics(sample_data)
        expected_total = sum([100, 200, 300, 400, 500])
        assert metrics['total_sales'] == expected_total
    
    def test_profit_margin_calculation(self, sample_data):
        """Test profit margin calculation"""
        metrics = calculate_metrics(sample_data)
        expected_margin = (sum([10, 20, 30, 40, 50]) / sum([100, 200, 300, 400, 500])) * 100
        assert abs(metrics['avg_profit_margin'] - expected_margin) < 0.01
    
    def test_total_transactions_calculation(self, sample_data):
        """Test total transactions calculation"""
        metrics = calculate_metrics(sample_data)
        assert metrics['total_transactions'] == 5
    
    def test_empty_dataframe_handling(self):
        """Test handling of empty DataFrame"""
        empty_df = pd.DataFrame(columns=['date', 'sales', 'profit', 'region', 'product'])
        metrics = calculate_metrics(empty_df)
        assert metrics['total_sales'] == 0
        assert metrics['total_transactions'] == 0

class TestChartCreation:
    """Test chart creation functionality"""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample data for testing"""
        dates = [datetime.now().date() - timedelta(days=x) for x in range(5, 0, -1)]
        data = {
            'date': dates,
            'sales': [100, 200, 300, 400, 500],
            'profit': [10, 20, 30, 40, 50],
            'region': ['North', 'South', 'East', 'West', 'North'],
            'product': ['Product A'] * 5
        }
        return pd.DataFrame(data)
    
    def test_create_sales_chart_returns_figure(self, sample_data):
        """Test that create_sales_chart returns a plotly figure"""
        fig = create_sales_chart(sample_data)
        assert hasattr(fig, 'data')
        assert hasattr(fig, 'layout')
    
    def test_create_region_chart_returns_figure(self, sample_data):
        """Test that create_region_chart returns a plotly figure"""
        fig = create_region_chart(sample_data)
        assert hasattr(fig, 'data')
        assert hasattr(fig, 'layout')
    
    def test_sales_chart_has_correct_data(self, sample_data):
        """Test that sales chart contains the expected data"""
        fig = create_sales_chart(sample_data)
        # Check that we have data traces
        assert len(fig.data) > 0
        # Check that the trace has data points
        assert len(fig.data[0].x) > 0
        assert len(fig.data[0].y) > 0
    
    def test_region_chart_has_correct_data(self, sample_data):
        """Test that region chart contains the expected data"""
        fig = create_region_chart(sample_data)
        # Check that we have data traces
        assert len(fig.data) > 0
        # Check that the trace has data points
        assert len(fig.data[0].x) > 0
        assert len(fig.data[0].y) > 0

class TestDataValidation:
    """Test data validation and edge cases"""
    
    def test_data_consistency(self):
        """Test that the same seed produces consistent data"""
        df1 = load_sample_data()
        df2 = load_sample_data()
        pd.testing.assert_frame_equal(df1, df2)
    
    def test_region_values_are_valid(self):
        """Test that region values are from expected set"""
        df = load_sample_data()
        valid_regions = ['North', 'South', 'East', 'West']
        assert all(region in valid_regions for region in df['region'].unique())
    
    def test_product_values_are_valid(self):
        """Test that product values are from expected set"""
        df = load_sample_data()
        valid_products = ['Product A', 'Product B', 'Product C']
        assert all(product in valid_products for product in df['product'].unique())
    
    def test_no_missing_values(self):
        """Test that there are no missing values in the dataset"""
        df = load_sample_data()
        assert not df.isnull().any().any()

class TestPerformance:
    """Test performance characteristics"""
    
    def test_data_loading_performance(self):
        """Test that data loading completes within reasonable time"""
        import time
        start_time = time.time()
        load_sample_data()
        end_time = time.time()
        
        # Should complete within 1 second
        assert (end_time - start_time) < 1.0
    
    def test_metrics_calculation_performance(self):
        """Test that metrics calculation is fast"""
        import time
        df = load_sample_data()
        
        start_time = time.time()
        calculate_metrics(df)
        end_time = time.time()
        
        # Should complete within 0.1 seconds
        assert (end_time - start_time) < 0.1

if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__]) 