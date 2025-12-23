# Quick Start Guide - Resolve AI Platform

## 🎯 5-Minute Setup

### Terminal 1: Backend Setup
```bash
cd backend

# Install dependencies (first time only)
pip install -r requirements.txt

# Initialize database (first time only)
python init_db.py

# Start server
python main.py
```

Expected output:
```
✓ Database tables created
✓ Added 8 products
✓ Added 8 fault categories
✓ Added 150 sample complaints
✓ Database initialized successfully!

INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Terminal 2: Frontend Setup
```bash
cd frontend

# Install dependencies (first time only)
npm install

# Start dev server
npm run dev
```

Expected output:
```
VITE v5.0.0  ready in XXX ms

➜  Local:   http://localhost:3000/
```

### Terminal 3: Access the Application
1. Open browser: http://localhost:3000
2. View API Docs: http://localhost:8000/docs

## 📊 What You'll See

### Dashboard Displays:
- **Total Complaints**: 150 sample complaints
- **Resolution Rate**: Based on resolved vs open
- **Critical Issues**: By severity level
- **Avg Satisfaction**: Customer ratings (if available)

### Analytics Visualizations:
- 🔧 **Fault Distribution**: Pie chart of complaint types
- 📱 **Product Health**: Scores for all products (0-100)
- ⏱️ **Resolution Metrics**: Average resolution time
- 📈 **Complaint Trend**: 30-day line chart
- 🚨 **Critical Alerts**: High-priority issues

## 🧪 Test Data

Sample data includes:
- 8 products (earbuds, headphones, speakers, smartwatches)
- 150 complaints with realistic scenarios
- Variety of statuses: open, in_progress, resolved, escalated
- Severity levels: low, medium, high, critical

## 🔌 Try the API

### Get Dashboard Summary
```bash
curl http://localhost:8000/api/analytics/dashboard
```

### Create a New Complaint
```bash
curl -X POST http://localhost:8000/api/complaints \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "department": "support",
    "complaint_text": "Battery drains too quickly",
    "severity": "high"
  }'
```

### Get Fault Distribution
```bash
curl http://localhost:8000/api/analytics/faults
```

### Get Product Health Scores
```bash
curl http://localhost:8000/api/analytics/product-health
```

### List All Complaints
```bash
curl http://localhost:8000/api/complaints
```

## 📱 Frontend Features

### Dashboard Tab
- Real-time complaint metrics
- Fault type distribution pie chart
- Product health scores (0-100)
- Resolution time statistics
- 30-day complaint trend
- Critical alerts panel

### Auto-Refresh
Dashboard refreshes every 30 seconds automatically.
Click "Refresh" button for manual update.

## 🤖 AI Classification

Each complaint is automatically classified with:
- **Fault Type**: Battery Issue, Audio Quality, Connectivity, etc.
- **Severity**: Low, Medium, High, Critical
- **Confidence Scores**: How certain the model is

## 📊 Database

**Location**: `backend/resolve_analytics.db`

Contains:
- Products table
- Fault categories table
- Complaints table (150+ records)

## 🔄 Reset Database

To start fresh:
```bash
cd backend
rm resolve_analytics.db
python init_db.py
```

## ⚠️ Common Issues

### Port Already in Use
```bash
# Backend (port 8000)
# Kill process or change port in main.py

# Frontend (port 3000)
# Kill process or run: npm run dev -- --port 3001
```

### Backend Connection Error
- Ensure backend is running on http://localhost:8000
- Check terminal 1 shows "Uvicorn running on http://0.0.0.0:8000"

### No Data in Dashboard
- Check database was created: `ls backend/resolve_analytics.db`
- Reinitialize: `python backend/init_db.py`

## 📚 Key Files

**Backend:**
- `main.py` - FastAPI app with all endpoints
- `database.py` - SQLAlchemy models
- `ai_classifier.py` - ML classification engine
- `predictive_insights.py` - Analytics queries

**Frontend:**
- `App.jsx` - Main component
- `Dashboard.jsx` - Dashboard view
- `components/` - Reusable UI components

## 🚀 Next Steps

1. ✅ Run backend on terminal 1
2. ✅ Run frontend on terminal 2
3. ✅ Open http://localhost:3000 in browser
4. ✅ Explore the dashboard
5. ✅ Check API docs at http://localhost:8000/docs

## 📞 API Documentation

Full Swagger UI: http://localhost:8000/docs

Interactive API testing with example requests.

---

**You're all set! Happy analyzing! 🎉**
