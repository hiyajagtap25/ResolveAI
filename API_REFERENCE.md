# Complete API Reference - Resolve Platform

## 🔌 Base URL
```
http://localhost:8000
```

## 📡 Endpoints Summary

| Category | Endpoint | Method | Purpose |
|----------|----------|--------|---------|
| **Health** | `/` | GET | Service status |
| **Health** | `/health` | GET | Database health check |
| **Products** | `/api/products` | GET | List all products |
| **Products** | `/api/products/{id}` | GET | Get specific product |
| **Faults** | `/api/fault-categories` | GET | List fault types |
| **Complaints** | `/api/complaints` | POST | Create new complaint |
| **Complaints** | `/api/complaints` | GET | List complaints |
| **Complaints** | `/api/complaints/{id}` | GET | Get complaint details |
| **Complaints** | `/api/complaints/{id}` | PUT | Update complaint |
| **Analytics** | `/api/analytics/dashboard` | GET | Complete dashboard |
| **Analytics** | `/api/analytics/trends` | GET | Complaint trends |
| **Analytics** | `/api/analytics/faults` | GET | Fault distribution |
| **Analytics** | `/api/analytics/product-health` | GET | Product scores |
| **Analytics** | `/api/analytics/resolution` | GET | Resolution metrics |
| **Analytics** | `/api/analytics/severity` | GET | Severity stats |
| **Analytics** | `/api/analytics/departments` | GET | Department workload |
| **Analytics** | `/api/analytics/alerts` | GET | Critical alerts |
| **Statistics** | `/api/stats/summary` | GET | High-level stats |

---

## 📝 Health Endpoints

### 1. Service Health Check
```
GET /
```

**Response:**
```json
{
  "status": "operational",
  "service": "Resolve - Complaint Intelligence Platform",
  "version": "1.0.0"
}
```

### 2. Database Health Check
```
GET /health
```

**Response (Healthy):**
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

## 🏢 Product Endpoints

### 1. List All Products
```
GET /api/products
```

**Response:**
```json
[
  {
    "product_id": 1,
    "product_name": "EarBud Pro X",
    "category": "earbuds"
  },
  {
    "product_id": 2,
    "product_name": "Headphone Max",
    "category": "headphones"
  }
]
```

### 2. Get Specific Product
```
GET /api/products/{product_id}
```

**Example:**
```
GET /api/products/1
```

**Response:**
```json
{
  "product_id": 1,
  "product_name": "EarBud Pro X",
  "category": "earbuds"
}
```

---

## 🔧 Fault Category Endpoints

### 1. List All Fault Categories
```
GET /api/fault-categories
```

**Response:**
```json
[
  {
    "fault_id": 1,
    "fault_name": "Battery Issue",
    "description": "Battery drains quickly or won't charge"
  },
  {
    "fault_id": 2,
    "fault_name": "Audio Quality",
    "description": "Poor sound output, distortion, or imbalance"
  }
]
```

---

## 📢 Complaint Endpoints

### 1. Create New Complaint (with AI Classification)
```
POST /api/complaints
```

**Request Body:**
```json
{
  "product_id": 1,
  "department": "support",
  "complaint_text": "Battery dies after 2 hours of use. Not acceptable for the price.",
  "severity": "high"
}
```

**Response:**
```json
{
  "complaint_id": 151,
  "product_id": 1,
  "department": "support",
  "complaint_text": "Battery dies after 2 hours of use. Not acceptable for the price.",
  "created_date": "2024-01-15",
  "resolved_date": null,
  "status": "open",
  "predicted_fault_type": "Battery Issue",
  "resolution_time": null,
  "severity": "high",
  "customer_satisfaction": null,
  "fault_confidence": 0.95,
  "severity_confidence": 0.87
}
```

### 2. List Complaints (with Filters)
```
GET /api/complaints
```

**Query Parameters:**
- `product_id` (integer) - Filter by product
- `status` (string) - Filter by status: open, in_progress, resolved, escalated
- `severity` (string) - Filter by severity: low, medium, high, critical
- `limit` (integer) - Max results (1-100, default: 50)
- `skip` (integer) - Pagination offset (default: 0)

**Examples:**
```
GET /api/complaints
GET /api/complaints?status=open
GET /api/complaints?severity=critical&limit=20
GET /api/complaints?product_id=1&status=resolved&skip=10
```

**Response:**
```json
[
  {
    "complaint_id": 1,
    "product_id": 1,
    "department": "support",
    "complaint_text": "Battery drains completely in 2 hours.",
    "created_date": "2024-01-10",
    "resolved_date": "2024-01-12",
    "status": "resolved",
    "predicted_fault_type": "Battery Issue",
    "resolution_time": 2,
    "severity": "high",
    "customer_satisfaction": 4
  }
]
```

### 3. Get Complaint Details
```
GET /api/complaints/{complaint_id}
```

**Example:**
```
GET /api/complaints/1
```

**Response:**
```json
{
  "complaint_id": 1,
  "product_id": 1,
  "department": "support",
  "complaint_text": "Battery drains completely in 2 hours.",
  "created_date": "2024-01-10",
  "resolved_date": "2024-01-12",
  "status": "resolved",
  "predicted_fault_type": "Battery Issue",
  "resolution_time": 2,
  "severity": "high",
  "customer_satisfaction": 4,
  "fault_confidence": 0.95,
  "severity_confidence": 0.87
}
```

### 4. Update Complaint Status
```
PUT /api/complaints/{complaint_id}
```

**Request Body (all optional):**
```json
{
  "status": "resolved",
  "resolved_date": "2024-01-12",
  "customer_satisfaction": 5
}
```

**Response:**
```json
{
  "complaint_id": 1,
  "product_id": 1,
  "department": "support",
  "complaint_text": "Battery drains completely in 2 hours.",
  "created_date": "2024-01-10",
  "resolved_date": "2024-01-12",
  "status": "resolved",
  "predicted_fault_type": "Battery Issue",
  "resolution_time": 2,
  "severity": "high",
  "customer_satisfaction": 5
}
```

---

## 📊 Analytics Endpoints

### 1. Complete Dashboard Summary
```
GET /api/analytics/dashboard
```

**Response:**
```json
{
  "fault_distribution": {
    "total_faults": 150,
    "distribution": [
      {
        "fault_type": "Battery Issue",
        "count": 45,
        "percentage": 30.0
      }
    ]
  },
  "product_health": {
    "scores": [
      {
        "product_id": 1,
        "product_name": "EarBud Pro X",
        "category": "earbuds",
        "health_score": 82.5,
        "complaint_count": 18
      }
    ]
  },
  "resolution_metrics": {
    "total_resolved": 105,
    "avg_resolution_days": 5.2,
    "median_resolution_days": 4.0,
    "min_resolution_days": 1,
    "max_resolution_days": 30
  },
  "severity_distribution": {
    "total": 150,
    "by_severity": [
      {
        "severity": "medium",
        "count": 45,
        "percentage": 30.0
      }
    ]
  },
  "department_workload": {
    "by_department": [
      {
        "department": "support",
        "complaint_count": 50,
        "avg_resolution_time": 5.8
      }
    ]
  },
  "critical_alerts": {
    "critical_products": [
      {
        "product": "EarBud Pro X",
        "critical_count": 8
      }
    ],
    "unresolved_fault_types": [
      {
        "fault_type": "Battery Issue",
        "unresolved_count": 12
      }
    ]
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### 2. Complaint Trends
```
GET /api/analytics/trends
```

**Query Parameters:**
- `days` (integer) - Time period in days (1-365, default: 30)

**Example:**
```
GET /api/analytics/trends?days=30
GET /api/analytics/trends?days=7
```

**Response:**
```json
{
  "period_days": 30,
  "data": [
    {
      "date": "2023-12-16",
      "complaints": 3
    },
    {
      "date": "2023-12-17",
      "complaints": 5
    }
  ]
}
```

### 3. Fault Type Distribution
```
GET /api/analytics/faults
```

**Response:**
```json
{
  "total_faults": 150,
  "distribution": [
    {
      "fault_type": "Battery Issue",
      "count": 45,
      "percentage": 30.0
    },
    {
      "fault_type": "Audio Quality",
      "count": 38,
      "percentage": 25.33
    },
    {
      "fault_type": "Connectivity",
      "count": 32,
      "percentage": 21.33
    }
  ]
}
```

### 4. Product Health Scores
```
GET /api/analytics/product-health
```

**Response:**
```json
{
  "scores": [
    {
      "product_id": 7,
      "product_name": "Watch Ultra",
      "category": "smartwatches",
      "health_score": 92.5,
      "complaint_count": 8
    },
    {
      "product_id": 1,
      "product_name": "EarBud Pro X",
      "category": "earbuds",
      "health_score": 82.5,
      "complaint_count": 18
    }
  ]
}
```

**Health Score Formula:**
```
score = 100 
        - (critical_count × 15) 
        - (high_count × 5) 
        - min(avg_resolution_days / 3, 20)
        + (resolution_rate / 100 × 30)
```

### 5. Resolution Metrics
```
GET /api/analytics/resolution
```

**Response:**
```json
{
  "total_resolved": 105,
  "avg_resolution_days": 5.2,
  "median_resolution_days": 4.0,
  "min_resolution_days": 1,
  "max_resolution_days": 30
}
```

### 6. Severity Distribution
```
GET /api/analytics/severity
```

**Response:**
```json
{
  "total": 150,
  "by_severity": [
    {
      "severity": "medium",
      "count": 45,
      "percentage": 30.0
    },
    {
      "severity": "high",
      "count": 38,
      "percentage": 25.33
    },
    {
      "severity": "low",
      "count": 32,
      "percentage": 21.33
    },
    {
      "severity": "critical",
      "count": 35,
      "percentage": 23.33
    }
  ]
}
```

### 7. Department Workload
```
GET /api/analytics/departments
```

**Response:**
```json
{
  "by_department": [
    {
      "department": "support",
      "complaint_count": 50,
      "avg_resolution_time": 5.8
    },
    {
      "department": "quality",
      "complaint_count": 35,
      "avg_resolution_time": 6.2
    },
    {
      "department": "technical",
      "complaint_count": 30,
      "avg_resolution_time": 4.5
    }
  ]
}
```

### 8. Critical Alerts
```
GET /api/analytics/alerts
```

**Response:**
```json
{
  "critical_products": [
    {
      "product": "EarBud Pro X",
      "critical_count": 8
    },
    {
      "product": "Headphone Max",
      "critical_count": 6
    }
  ],
  "unresolved_fault_types": [
    {
      "fault_type": "Battery Issue",
      "unresolved_count": 12
    },
    {
      "fault_type": "Connectivity",
      "unresolved_count": 8
    }
  ]
}
```

---

## 📈 Statistics Endpoints

### 1. Summary Statistics
```
GET /api/stats/summary
```

**Response:**
```json
{
  "total_complaints": 150,
  "resolved_complaints": 105,
  "resolution_rate": 70.0,
  "critical_complaints": 35,
  "open_complaints": 45,
  "average_satisfaction": [
    {
      "complaint_id": 1,
      "customer_satisfaction": 4
    }
  ]
}
```

---

## 🔐 Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | OK | Successful GET/PUT request |
| 201 | Created | Successful POST request |
| 400 | Bad Request | Invalid query parameters |
| 404 | Not Found | Product/complaint doesn't exist |
| 422 | Validation Error | Invalid request body |
| 500 | Server Error | Database error |

---

## 📦 Request/Response Examples

### Example 1: Create Complaint & Get Prediction
```bash
curl -X POST http://localhost:8000/api/complaints \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "department": "support",
    "complaint_text": "Left earbud stopped working. No sound output.",
    "severity": "high"
  }'
```

**AI Prediction Result:**
```json
{
  "fault_type": "Audio Quality",
  "severity": "high",
  "fault_confidence": 0.92,
  "severity_confidence": 0.88
}
```

### Example 2: Get All Critical Complaints
```bash
curl "http://localhost:8000/api/complaints?severity=critical&limit=50"
```

### Example 3: Get Unresolved Open Complaints
```bash
curl "http://localhost:8000/api/complaints?status=open&limit=100"
```

### Example 4: Get Specific Product Complaints
```bash
curl "http://localhost:8000/api/complaints?product_id=1&limit=30"
```

### Example 5: Update Complaint to Resolved
```bash
curl -X PUT http://localhost:8000/api/complaints/1 \
  -H "Content-Type: application/json" \
  -d '{
    "status": "resolved",
    "resolved_date": "2024-01-15",
    "customer_satisfaction": 5
  }'
```

---

## 🚀 Interactive API Documentation

Visit: **http://localhost:8000/docs**

This provides:
- ✅ Interactive Swagger UI
- ✅ Try-it-out functionality
- ✅ Request/response examples
- ✅ Parameter documentation
- ✅ Real-time execution

---

## 💡 Tips

1. **Use limit/skip for pagination:**
   ```
   GET /api/complaints?limit=50&skip=0
   GET /api/complaints?limit=50&skip=50
   ```

2. **Combine multiple filters:**
   ```
   GET /api/complaints?status=open&severity=critical&product_id=1
   ```

3. **Get real-time trends:**
   ```
   GET /api/analytics/trends?days=7
   GET /api/analytics/trends?days=30
   ```

4. **Monitor critical issues:**
   ```
   GET /api/analytics/alerts
   GET /api/stats/summary
   ```

5. **Track product performance:**
   ```
   GET /api/analytics/product-health
   GET /api/complaints?product_id=1
   ```
