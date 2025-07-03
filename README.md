# 📊 Streamlit Sales Dashboard

A modern, interactive sales analytics dashboard built with Streamlit, featuring real-time data visualization and comprehensive testing.

## 🚀 Features

- **Interactive Dashboard**: Real-time sales analytics with filtering capabilities
- **Data Visualizations**: Charts and graphs using Plotly for enhanced interactivity
- **Responsive Design**: Clean, modern UI that works across devices
- **Comprehensive Testing**: Full test suite with pytest
- **CI/CD Ready**: Jenkins pipeline for automated testing and deployment
- **Containerized**: Docker support for easy deployment

## 📋 Prerequisites

- Python 3.9+
- Docker (optional, for containerization)
- Jenkins (for CI/CD)

## 🛠️ Local Development

### 1. Clone the Repository
```bash
git clone https://github.com/snowflakedb/streamlit-sales-dashboard.git
cd streamlit-sales-dashboard
```

### 2. Set Up Python Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
pip install -r test_requirements.txt  # For development/testing
```

### 4. Run the Application
```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## 🧪 Testing

### Run All Tests
```bash
pytest tests/ -v
```

### Run Tests with Coverage
```bash
pytest tests/ --cov=app --cov-report=html
```

### Code Quality Checks
```bash
# Linting
flake8 app.py tests/

# Formatting
black app.py tests/

# Type checking
mypy app.py --ignore-missing-imports
```

## 🐳 Docker Usage

### Build Image
```bash
docker build -t streamlit-sales-dashboard .
```

### Run Container
```bash
docker run -p 8501:8501 streamlit-sales-dashboard
```

## 🔧 Configuration

The app uses Streamlit's configuration system. Customize settings in `.streamlit/config.toml`:

- **Theme**: Colors and styling
- **Server**: Port and host settings
- **Browser**: Usage statistics and CORS

## 📊 Dashboard Overview

### Key Metrics
- **Total Sales**: Aggregate sales performance
- **Profit Margin**: Average profit margin percentage
- **Transactions**: Total number of transactions

### Visualizations
- **Sales Trend**: Time-series chart showing daily sales
- **Regional Performance**: Bar chart comparing sales by region
- **Data Table**: Interactive table with raw data

### Filters
- **Region Selection**: Filter data by geographic regions
- **Product Selection**: Filter by product categories

## 🏗️ Architecture

```
streamlit-sales-dashboard/
├── app.py                 # Main Streamlit application
├── tests/
│   └── test_app.py       # Comprehensive test suite
├── .streamlit/
│   └── config.toml       # Streamlit configuration
├── requirements.txt       # Python dependencies
├── test_requirements.txt  # Testing dependencies
├── Dockerfile            # Container configuration
├── Jenkinsfile           # CI/CD pipeline
└── README.md             # This file
```

## 🚀 CI/CD Pipeline

The Jenkins pipeline includes:

1. **Code Quality**: Linting, formatting, type checking
2. **Testing**: Unit tests with coverage reporting
3. **Security**: Dependency vulnerability scanning
4. **Build**: Docker image creation
5. **Deploy**: Automated deployment to development

### Pipeline Stages
- ✅ Checkout code
- ✅ Setup Python environment
- ✅ Code quality checks (parallel)
- ✅ Run comprehensive tests
- ✅ Security scanning
- ✅ Build Docker image
- ✅ Test container
- ✅ Push to registry (main branch)
- ✅ Deploy to development (main branch)

## 📈 Monitoring

The application includes:
- **Health Checks**: Docker health check endpoint
- **Performance Tests**: Load time validation
- **Data Validation**: Input/output verification

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest tests/`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

**Port already in use:**
```bash
# Kill process using port 8501
lsof -ti:8501 | xargs kill -9
```

**Module not found:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate
pip install -r requirements.txt
```

**Docker build fails:**
```bash
# Clean Docker cache
docker system prune -a
```

## 📞 Support

For questions or issues, please:
1. Check the troubleshooting section
2. Review existing issues in the repository
3. Create a new issue with detailed description

---

**Built with ❤️ using Streamlit, tested with 🧪 pytest, and deployed with 🚀 Jenkins** 