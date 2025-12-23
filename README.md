# Resolve - AI-Powered Complaint Intelligence Platform

A production-ready internal analytics application for consumer electronics companies. Uses AI to classify product complaints and provides real-time business intelligence.

## 📋 Overview

**Resolve** is an end-to-end complaint management and analytics platform designed for consumer electronics companies (earbuds, headphones, speakers, smartwatches). It combines:

- **AI-powered complaint classification** (fault type & severity prediction)
- **SQL-driven analytics** with predictive insights
- **Real-time dashboard** for data-driven decision making
- **Clean, explainable architecture** focused on analytics

## 🏗️ Architecture

```
ResolveAI/
├── backend/                 # FastAPI + SQLAlchemy + scikit-learn
│   ├── main.py             # FastAPI application & endpoints
│   ├── database.py         # SQLAlchemy models & database setup
│   ├── init_db.py          # Database initialization with sample data
│   ├── ai_classifier.py    # AI complaint classification engine
│   ├── predictive_insights.py # Analytics & business intelligence
│   └── requirements.txt     # Python dependencies
│
└── frontend/               # React + Vite + Recharts
    ├── src/
    │   ├── App.jsx
    │   ├── main.jsx
    │   └── components/
    │       ├── Dashboard.jsx
    │       ├── Navigation.jsx
    │       ├── StatCard.jsx
    │       ├── FaultDistribution.jsx
    │       ├── ProductHealth.jsx
    │       ├── ResolutionMetrics.jsx
    │       ├── TrendChart.jsx
    │       └── AlertsPanel.jsx
    ├── index.html
    ├── vite.config.js
    └── package.json
```

## 🗄️ Database Schema

### Products Table
```sql
products(
  product_id INTEGER PRIMARY KEY,
  product_name TEXT,
  category TEXT  -- earbuds, headphones, speakers, smartwatches
)
```

### Fault Categories Table
```sql
fault_categories(
  fault_id INTEGER PRIMARY KEY,
  fault_name TEXT UNIQUE,
  description TEXT
)
```

### Complaints Table
```sql
complaints(
  complaint_id INTEGER PRIMARY KEY,
  product_id INTEGER FOREIGN KEY,
  department TEXT,
  complaint_text TEXT,
  created_date DATE,
  resolved_date DATE,
  status TEXT,  -- open, in_progress, resolved, escalated
  predicted_fault_type TEXT,
  resolution_time INTEGER,
  severity TEXT,  -- low, medium, high, critical
  customer_satisfaction INTEGER  -- 1-5 rating
)
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- SQLite3

### Backend Setup

1. **Install Python dependencies:**
```bash
cd backend
pip install -r requirements.txt
```

2. **Initialize database:**
```bash
python init_db.py
```

3. **Start FastAPI server:**
```bash
python main.py
```

Server runs on `http://localhost:8000`

**API Documentation:** Visit `http://localhost:8000/docs` (Swagger UI)

### Frontend Setup

1. **Install dependencies:**
```bash
cd frontend
npm install
```

2. **Start development server:**
```bash
npm run dev
```

Frontend runs on `http://localhost:3000`

## 📊 API Endpoints

### Health Check
- `GET /` - Service status
- `GET /health` - Database health check

### Products
- `GET /api/products` - All products
- `GET /api/products/{product_id}` - Specific product

### Complaints
- `POST /api/complaints` - Create new complaint (with AI classification)
- `GET /api/complaints` - List complaints (with filters)
- `GET /api/complaints/{complaint_id}` - Complaint details
- `PUT /api/complaints/{complaint_id}` - Update complaint status

### Analytics
- `GET /api/analytics/dashboard` - Complete dashboard data
- `GET /api/analytics/trends` - Complaint trends over time
- `GET /api/analytics/faults` - Fault distribution
- `GET /api/analytics/product-health` - Product health scores
- `GET /api/analytics/resolution` - Resolution metrics
- `GET /api/analytics/severity` - Severity distribution
- `GET /api/analytics/departments` - Department workload
- `GET /api/analytics/alerts` - Critical alerts

### Statistics
- `GET /api/stats/summary` - High-level statistics

## 🤖 AI Complaint Classification

The classifier uses **TF-IDF + Naive Bayes** to predict:

1. **Fault Type** - The technical issue category (Battery, Audio Quality, Connectivity, etc.)
2. **Severity** - Impact level (Low, Medium, High, Critical)

### How it Works

```python
# Text -> Vectorization -> Classification
complaint_text = "Battery dies after 2 hours of use"
classification = classify_complaint(complaint_text)
# Returns: {
#   "fault_type": "Battery Issue",
#   "severity": "high",
#   "fault_confidence": 0.95,
#   "severity_confidence": 0.87
# }
```

### Prediction Confidence

Each prediction includes confidence scores (0-1) indicating model certainty.

## 📈 Key Analytics Features

### 1. **Fault Distribution**
Pie chart showing breakdown of complaint types by frequency and percentage.

### 2. **Product Health Scores**
0-100 score per product based on:
- Critical severity count (penalty)
- High severity count (penalty)
- Resolution rate (bonus)
- Average resolution time (penalty)

### 3. **Resolution Metrics**
- Total resolved complaints
- Average, median, min, max resolution time in days

### 4. **Complaint Trends**
30-day line chart showing daily complaint volume.

### 5. **Critical Alerts**
- Products with high critical complaints
- Fault types with high unresolved rates

### 6. **Department Workload**
Distribution of complaints across departments with average resolution time.

## 💾 Data Model Highlights

### Complaint Flow
```
New Complaint
    ↓
AI Classification (fault type + severity)
    ↓
Database Storage (with predictions)
    ↓
Analytics Processing
    ↓
Dashboard Visualization
```

### Severity Levels
- **Critical**: Product doesn't work at all
- **High**: Major functionality issues
- **Medium**: Notable problems but workarounds available
- **Low**: Minor inconveniences

### Status Lifecycle
- **Open**: New complaint, not yet assigned
- **In Progress**: Being investigated/resolved
- **Resolved**: Issue fixed and closed
- **Escalated**: Needs management attention

## 🎨 Frontend Components

### Dashboard
Main analytics view with all key metrics and visualizations.

### Navigation
Sidebar with branding and navigation menu.

### StatCard
High-level KPI display (totals, rates, counts).

### FaultDistribution
Pie chart of fault types with legend.

### ProductHealth
Health scores bar chart for all products.

### ResolutionMetrics
Key metrics: avg time, median time, min/max.

### TrendChart
30-day complaint trend line chart.

### AlertsPanel
Critical issues requiring attention.

## 🔌 API Request Examples

### Create a Complaint with AI Classification
```bash
curl -X POST "http://localhost:8000/api/complaints" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "department": "support",
    "complaint_text": "Battery drains completely in 2 hours. Not usable.",
    "severity": "high"
  }'
```

### Get Dashboard Data
```bash
curl "http://localhost:8000/api/analytics/dashboard"
```

### Get Trend Data
```bash
curl "http://localhost:8000/api/analytics/trends?days=30"
```

### List Complaints with Filters
```bash
curl "http://localhost:8000/api/complaints?status=open&severity=critical&limit=20"
```

## 📦 Dependencies

### Backend
- **FastAPI** - Modern web framework
- **SQLAlchemy** - ORM for database
- **scikit-learn** - ML for complaint classification
- **Pandas** - Data manipulation
- **Pydantic** - Data validation

### Frontend
- **React** - UI library
- **Vite** - Fast build tool
- **Recharts** - Data visualization
- **Axios** - HTTP client

## 🗂️ File Structure

### Backend Files

**[main.py](backend/main.py)** - FastAPI application
- 25+ REST endpoints
- CORS configuration
- Pydantic schemas
- Request/response handling

**[database.py](backend/database.py)** - Data models
- SQLAlchemy ORM models
- Product, FaultCategory, Complaint tables
- Database session management

**[init_db.py](backend/init_db.py)** - Database initialization
- Creates schema
- Populates sample data (150 complaints, 8 products)

**[ai_classifier.py](backend/ai_classifier.py)** - ML classifier
- TF-IDF vectorization
- Naive Bayes classification
- Confidence scoring
- Rule-based fallback

**[predictive_insights.py](backend/predictive_insights.py)** - Analytics engine
- Complaint trends
- Fault distribution
- Product health scores
- Resolution statistics
- Critical alerts

### Frontend Files

**App.jsx** - Main application component
**Dashboard.jsx** - Dashboard layout & data fetching
**Navigation.jsx** - Sidebar navigation
**StatCard.jsx** - KPI display component
**FaultDistribution.jsx** - Pie chart component
**ProductHealth.jsx** - Health scores component
**ResolutionMetrics.jsx** - Metrics display component
**TrendChart.jsx** - Line chart component
**AlertsPanel.jsx** - Critical alerts component

## 🔐 Security Considerations

For production deployment, add:

1. **Authentication** - JWT tokens, OAuth2
2. **Authorization** - Role-based access control
3. **Rate limiting** - Prevent abuse
4. **Input validation** - SQL injection prevention (already in SQLAlchemy)
5. **HTTPS** - Encrypt data in transit
6. **CORS** - Restrict to trusted origins
7. **Environment variables** - Secure sensitive config

## 🚀 Production Deployment

### Backend (FastAPI)
```bash
# Using Gunicorn + Uvicorn
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

### Frontend (React)
```bash
# Build optimized bundle
npm run build

# Serves static files from dist/
# Deploy to S3, Vercel, Netlify, or similar
```

### Database
- Use PostgreSQL or MySQL for production (vs SQLite)
- Enable backups
- Set up replication

## 📊 Sample Data

The database initializes with:
- **8 products** across 4 categories
- **8 fault categories** with descriptions
- **150 sample complaints** with realistic data
- **Various statuses and severities**

This allows immediate testing without manual data entry.

## 🔄 Data Refresh

Dashboard auto-refreshes every 30 seconds. Click "Refresh" button for manual update.

Complaints are classified in real-time on creation.

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check port 8000 is available
# Clear database and reinitialize
rm resolve_analytics.db
python init_db.py
python main.py
```

### Frontend can't connect to API
- Ensure backend is running on port 8000
- Check CORS is enabled (should be by default)
- Verify API endpoint in browser devtools

### No data in dashboard
- Initialize database: `python init_db.py`
- Check database file exists: `ls backend/resolve_analytics.db`

## 📝 License

This is an internal analytics platform. All data is proprietary.

## 🤝 Support

For issues or improvements, contact the analytics team.
