# Architecture & Advanced Configuration

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENT TIER (React)                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │  Dashboard   │  │ Navigation   │  │ Analytics Charts │  │
│  │  (Main View) │  │  (Sidebar)   │  │  (Recharts)      │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP/REST (Axios)
                           │ JSON
┌──────────────────────────┴──────────────────────────────────┐
│                API TIER (FastAPI)                           │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ /api/complaints      /api/analytics    /api/products   │ │
│  │ /api/stats           /api/health       /api/fault-...  │ │
│  └────────────────────────────────────────────────────────┘ │
└──────────────────────────┬──────────────────────────────────┘
                           │ SQLAlchemy ORM
                           │ SQL Queries
┌──────────────────────────┴──────────────────────────────────┐
│             SERVICE TIER (Business Logic)                   │
│  ┌────────────────────┐  ┌────────────────────────────────┐ │
│  │  AI Classifier     │  │  Predictive Insights Engine    │ │
│  │  - TF-IDF          │  │  - Fault Distribution          │ │
│  │  - Naive Bayes     │  │  - Product Health Scoring      │ │
│  │  - Rule-based      │  │  - Resolution Analytics        │ │
│  │  - Confidence      │  │  - Critical Alerts             │ │
│  │    Scoring         │  │  - Trend Analysis              │ │
│  └────────────────────┘  └────────────────────────────────┘ │
└──────────────────────────┬──────────────────────────────────┘
                           │ SQLAlchemy Models
                           │ Database Queries
┌──────────────────────────┴──────────────────────────────────┐
│         DATA TIER (SQLite / Production: PostgreSQL)         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │  Products    │  │ Complaints   │  │ Fault Categories │ │
│  │              │  │              │  │                  │ │
│  │ - product_id │  │ - complaint_ │  │ - fault_id       │ │
│  │ - name       │  │   id         │  │ - fault_name     │ │
│  │ - category   │  │ - product_id │  │ - description    │ │
│  │              │  │ - text       │  │                  │ │
│  │              │  │ - status     │  │                  │ │
│  │              │  │ - severity   │  │                  │ │
│  │              │  │ - fault_type │  │                  │ │
│  │              │  │ - resolve... │  │                  │ │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## 🔄 Data Flow

### Complaint Creation Flow
```
User Input (Web Form)
        ↓
POST /api/complaints
        ↓
FastAPI validates (Pydantic)
        ↓
AI Classifier analyzes text
        ├─ TF-IDF vectorization
        ├─ Naive Bayes prediction
        └─ Confidence scoring
        ↓
Store in Database
├─ Complaint record
├─ Predicted fault type
├─ Severity level
└─ Confidence scores
        ↓
Return to client with predictions
        ↓
Dashboard displays in real-time
```

### Analytics Query Flow
```
Dashboard loads
        ↓
Parallel API calls:
├─ GET /api/analytics/dashboard
├─ GET /api/analytics/trends
├─ GET /api/stats/summary
└─ GET /api/analytics/product-health
        ↓
SQL Queries execute
├─ Fault distribution query
├─ Trend aggregation
├─ Product health calculation
└─ Resolution metrics
        ↓
Data transformation (Python)
├─ Aggregations
├─ Calculations
└─ Formatting
        ↓
JSON response to frontend
        ↓
React renders visualizations
```

## 🗄️ Database Query Examples

### Fault Distribution
```sql
SELECT predicted_fault_type, COUNT(*) as count
FROM complaints
GROUP BY predicted_fault_type
ORDER BY count DESC;
```

### Product Health Score Calculation
```sql
SELECT 
    p.product_name,
    COUNT(c.complaint_id) as total_complaints,
    SUM(CASE WHEN c.severity = 'critical' THEN 1 ELSE 0 END) as critical_count,
    SUM(CASE WHEN c.status = 'resolved' THEN 1 ELSE 0 END) as resolved_count,
    AVG(c.resolution_time) as avg_resolution_time
FROM products p
LEFT JOIN complaints c ON p.product_id = c.product_id
GROUP BY p.product_id;
```

### 30-Day Trend
```sql
SELECT created_date, COUNT(*) as complaint_count
FROM complaints
WHERE created_date >= date('now', '-30 days')
GROUP BY created_date
ORDER BY created_date;
```

### Unresolved Faults
```sql
SELECT predicted_fault_type, COUNT(*) as unresolved_count
FROM complaints
WHERE status != 'resolved'
GROUP BY predicted_fault_type
ORDER BY unresolved_count DESC
LIMIT 5;
```

## 🤖 AI Model Details

### Vectorization (TF-IDF)
```
"Battery drains quickly" 
    ↓
Tokenization: ["battery", "drains", "quickly"]
    ↓
TF-IDF Vector: [0.5, 0.3, 0.2, ...500 dimensions]
```

### Classification
```
Vector + Trained Model
    ↓
Naive Bayes probability calculation
    ↓
Output: Most likely class
```

### Supported Fault Types
1. Battery Issue
2. Audio Quality
3. Connectivity
4. Physical Damage
5. Software Bug
6. Firmware Update
7. Warranty/Return
8. Performance

### Severity Levels
- **Low**: Minor inconvenience
- **Medium**: Noticeable problem
- **High**: Major functionality affected
- **Critical**: Complete failure

## 🔐 Security Architecture

### Input Validation
```python
# Pydantic validates all API inputs
class ComplaintCreate(BaseModel):
    product_id: int
    department: str
    complaint_text: str
    severity: Optional[str] = "medium"

# Database uses parameterized queries (SQLAlchemy)
```

### Authentication (for production)
```python
# Add JWT middleware
from fastapi.security import HTTPBearer, HTTPAuthCredentials

security = HTTPBearer()

@app.get("/api/complaints")
async def get_complaints(credentials: HTTPAuthCredentials = Depends(security)):
    # Verify token
    # Return data
```

### CORS Configuration
```python
# Already configured to allow all origins
# In production: restrict to specific domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.example.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT"],
    allow_headers=["*"],
)
```

## 📈 Performance Considerations

### Database Optimization
- Add indexes on frequently queried columns:
  ```sql
  CREATE INDEX idx_complaint_status ON complaints(status);
  CREATE INDEX idx_complaint_severity ON complaints(severity);
  CREATE INDEX idx_complaint_product ON complaints(product_id);
  CREATE INDEX idx_complaint_date ON complaints(created_date);
  ```

### Caching Strategy
- Cache dashboard data for 5-10 minutes
- Cache product list (rarely changes)
- Real-time: complaint creation, status updates

### API Rate Limiting
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.get("/api/complaints")
@limiter.limit("100/minute")
async def get_complaints(request: Request):
    # ...
```

## 🚀 Production Deployment

### Backend Deployment

#### Option 1: Docker
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY backend/ .

CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "main:app"]
```

#### Option 2: Traditional Server
```bash
# Install Gunicorn
pip install gunicorn

# Run with multiple workers
gunicorn -w 4 -b 0.0.0.0:8000 -k uvicorn.workers.UvicornWorker main:app
```

#### Option 3: Cloud PaaS
- **Heroku**: `git push heroku main`
- **Railway**: Connect GitHub repo
- **Render**: Deploy from git

### Frontend Deployment

#### Build for Production
```bash
npm run build
# Creates optimized dist/ folder
```

#### Deploy Static Files
- **Vercel**: `vercel deploy`
- **Netlify**: `netlify deploy --prod`
- **S3 + CloudFront**: Upload dist/ to S3
- **Nginx**: Serve from `/var/www/resolve/`

### Database Deployment

#### SQLite (Development Only)
- Good for testing
- Not suitable for production

#### PostgreSQL (Production)
```bash
# Create database
createdb resolve_analytics

# Update connection string
DATABASE_URL = "postgresql://user:password@localhost/resolve_analytics"

# Run migrations
alembic upgrade head
```

#### MySQL
```python
DATABASE_URL = "mysql+pymysql://user:password@localhost/resolve_analytics"
```

## 🔍 Monitoring & Logging

### Backend Logging
```python
import logging

logger = logging.getLogger(__name__)

@app.post("/api/complaints")
async def create_complaint(complaint: ComplaintCreate):
    logger.info(f"Creating complaint for product {complaint.product_id}")
    try:
        # Process complaint
        logger.info(f"Complaint created: {complaint_id}")
    except Exception as e:
        logger.error(f"Error creating complaint: {str(e)}")
        raise
```

### Frontend Error Tracking
```javascript
// Add Sentry or similar
import * as Sentry from "@sentry/react";

Sentry.init({
  dsn: "your-sentry-dsn",
  environment: "production"
});
```

### Health Checks
```bash
# Monitor with
curl http://localhost:8000/health

# Response:
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## 📊 Analytics Tables

### Fault Statistics
```python
# Raw data
complaints.groupby('predicted_fault_type').size()

# Output
Battery Issue        45
Audio Quality        38
Connectivity         32
Physical Damage      20
Software Bug         15
```

### Product Performance
```python
# Health score formula
score = 100 - (critical_count * 15) - (high_count * 5) - (avg_time / 3) + (resolution_rate * 30)
```

### Time Series Analysis
```python
# Daily complaint counts
complaints.groupby('created_date').size()
```

## 🔧 Configuration Files

### Backend Configuration (production)
```python
# config.py
import os

class Config:
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///resolve.db")
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me")
    DEBUG = os.getenv("DEBUG", False)
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
```

### Frontend Configuration (production)
```javascript
// config.js
const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";
const REFRESH_INTERVAL = 30000; // 30 seconds
```

## 🧪 Testing

### Backend Unit Tests
```python
# tests/test_classifier.py
from ai_classifier import classify_complaint

def test_battery_classification():
    result = classify_complaint("Battery dies after 2 hours")
    assert result["fault_type"] == "Battery Issue"
    assert result["fault_confidence"] > 0.7
```

### API Integration Tests
```python
# tests/test_api.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_complaint():
    response = client.post("/api/complaints", json={
        "product_id": 1,
        "department": "support",
        "complaint_text": "Test complaint",
        "severity": "high"
    })
    assert response.status_code == 200
```

## 📚 References

- **FastAPI**: https://fastapi.tiangolo.com
- **SQLAlchemy**: https://docs.sqlalchemy.org
- **scikit-learn**: https://scikit-learn.org
- **React**: https://react.dev
- **Vite**: https://vitejs.dev
- **Recharts**: https://recharts.org
