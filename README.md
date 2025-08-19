# Restaurant Tips Prediction Service

A production-ready machine learning microservice for predicting restaurant tips built with FastAPI, scikit-learn, and Docker.

## 🎯 Overview

This project demonstrates a complete machine learning pipeline from data exploration to production deployment. The service predicts restaurant total bills using the classic Seaborn tips dataset and showcases MLOps best practices with microservice architecture.

### Key Features

- **FastAPI** web service with async endpoints
- **scikit-learn** regression model for tip prediction  
- **Docker** containerization for easy deployment
- **Microservice architecture** with separate database service
- **Comprehensive testing** with pytest
- **Production logging** and error handling
- **Heroku deployment** ready

## 🏗️ Architecture

The application follows a two-service microservice design:

1. **Database Service** (separate repo): Data storage and retrieval
2. **Prediction Service** (this repo): ML predictions and new data logging

```
┌─────────────────┐    HTTP    ┌─────────────────┐
│  Prediction     │◄──────────►│  Database       │
│  Service        │   Calls    │  Service        │
│  (FastAPI)      │            │  (FastAPI)      │
└─────────────────┘            └─────────────────┘
         │                              │
         ▼                              ▼
┌─────────────────┐            ┌─────────────────┐
│  ML Model       │            │  Tips Dataset   │
│  (joblib)       │            │  (SQLite)       │
└─────────────────┘            └─────────────────┘
```

## 📊 Dataset & ML Model

**Dataset**: Seaborn Tips Dataset (244 restaurant transactions)
- Features: total_bill, tip, sex, smoker, day, time, party_size
- Task: Regression to predict total_bill from other features
- Preprocessing: Log transforms, one-hot encoding, standardization

**Model**: Linear Regression (optimized for simplicity and interpretability)
- Tested: Linear models, XGBoost (no improvement over linear)
- Key predictors: tip amount and party size
- Deployment: Serialized with joblib

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Docker (optional)

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/CJRockball/pred_service.git
   cd pred_service
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the service**
   ```bash
   uvicorn api.router:app --reload --port 8000
   ```

4. **Test the endpoints**
   - Health check: http://127.0.0.1:8000/predict/
   - API docs: http://127.0.0.1:8000/docs

### Docker Deployment

1. **Build the image**
   ```bash
   docker build -t pred-service .
   ```

2. **Run the container**
   ```bash
   docker run -dp 8000:8000 pred-service
   ```

## 📚 API Endpoints

| Endpoint | Method | Description |
|----------|---------|-------------|
| `/predict/` | GET | Health check and endpoint documentation |
| `/predict/get_test_data` | GET | Retrieve all test dataset |
| `/predict/get_random_test_row` | GET | Get random test sample |
| `/predict/get_test_prediction` | GET | Make prediction with actual vs predicted comparison |

### Example Response

```json
{
  "y_pred": 23.45,
  "y_true": 24.59
}
```

## 🧪 Testing

Run the test suite:

```bash
pytest tests/
```

Tests include:
- Unit tests for core functions
- API endpoint testing
- Model prediction validation

## 📁 Project Structure

```
pred_service/
├── api/                    # FastAPI application
│   ├── main.py            # Core endpoints
│   ├── router.py          # App configuration
│   ├── util.py            # ML prediction logic
│   ├── data_util.py       # Database communication
│   └── custom_trans.py    # Data transformations
├── data/                   # Model artifacts
│   ├── model.joblib       # Trained model
│   └── new_tips.db        # SQLite database
├── notebooks/             # Data science workflow
│   ├── eda_model.ipynb    # EDA and modeling
│   ├── tipsdata.py        # Data loading utilities
│   └── tipspipe.py        # ML pipeline
├── tests/                 # Unit tests
├── logs/                  # Application logs
├── Dockerfile             # Container configuration
└── requirements.txt       # Python dependencies
```

## 🛠️ Technologies Used

**Core Stack**:
- **FastAPI 0.79.0** - Modern async web framework
- **scikit-learn 1.1.1** - Machine learning library  
- **pandas 1.4.3** - Data manipulation
- **uvicorn 0.18.2** - ASGI server

**Deployment**:
- **Docker** - Containerization
- **Heroku** - Cloud platform
- **httpx** - Async HTTP client

**Development**:
- **pytest 7.1.2** - Testing framework
- **jupyter** - Notebook development

## 🔧 Configuration

### Environment Variables

- `PORT` - Service port (default: 8000)
- Database URLs configured in `data_util.py`

### Database Service Setup

This service requires a companion database service. Update the URLs in `api/data_util.py`:

```python
# Development
data_json = await client.get('http://127.0.0.1:8001/tips/test_data')

# Docker
data_json = await client.get('http://host.docker.internal:8001/tips/test_data')

# Production  
data_json = await client.get('http://db-data-service.herokuapp.com/tips/test_data')
```

## 📈 Future Enhancements

**MLOps Improvements**:
- [ ] Model monitoring and drift detection
- [ ] Automated retraining pipeline  
- [ ] A/B testing framework
- [ ] Feature store integration

**Production Readiness**:
- [ ] Authentication and rate limiting
- [ ] Comprehensive monitoring (Prometheus/Grafana)
- [ ] CI/CD pipeline with GitHub Actions
- [ ] Migration to PostgreSQL

**Performance**:
- [ ] Redis caching layer
- [ ] Model ensemble methods
- [ ] Batch prediction endpoints

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)  
5. Open a Pull Request

## 📞 Contact

For questions or suggestions, please open an issue on GitHub.

---

**Built with ❤️ for the MLOps community**