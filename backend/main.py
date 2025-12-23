"""
Resolve - AI-Powered Complaint Intelligence Platform
FastAPI Backend
"""
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date

from database import get_db, Complaint, Product, FaultCategory, SessionLocal
from ai_classifier import classify_complaint
from predictive_insights import insights_engine, get_dashboard_summary
from init_db import init_database

# ==================== Initialize Database ====================
init_database()

# ==================== FastAPI App ====================
app = FastAPI(
    title="Resolve - Complaint Intelligence Platform",
    description="AI-powered analytics for consumer electronics complaints",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== Pydantic Models ====================

class ProductSchema(BaseModel):
    product_id: int
    product_name: str
    category: str
    
    class Config:
        from_attributes = True


class FaultCategorySchema(BaseModel):
    fault_id: int
    fault_name: str
    description: Optional[str] = None
    
    class Config:
        from_attributes = True


class ComplaintCreate(BaseModel):
    product_id: int
    department: str
    complaint_text: str
    severity: Optional[str] = "medium"


class ComplaintResponse(BaseModel):
    complaint_id: int
    product_id: int
    department: str
    complaint_text: str
    created_date: date
    resolved_date: Optional[date] = None
    status: str
    predicted_fault_type: Optional[str] = None
    resolution_time: Optional[int] = None
    severity: str
    customer_satisfaction: Optional[int] = None
    
    class Config:
        from_attributes = True


class ComplaintDetailResponse(ComplaintResponse):
    fault_confidence: Optional[float] = None
    severity_confidence: Optional[float] = None


# ==================== Health Check ====================

@app.get("/", tags=["Health"])
def root():
    """Health check endpoint"""
    return {
        "status": "operational",
        "service": "Resolve - Complaint Intelligence Platform",
        "version": "1.0.0"
    }


@app.get("/health", tags=["Health"])
def health_check():
    """Detailed health status"""
    db = SessionLocal()
    try:
        db.query(Complaint).limit(1).all()
        db.close()
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }


# ==================== Products Endpoints ====================

@app.get("/api/products", tags=["Products"], response_model=List[ProductSchema])
def get_products(db: Session = Depends(get_db)):
    """Get all products"""
    return db.query(Product).all()


@app.get("/api/products/{product_id}", tags=["Products"], response_model=ProductSchema)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get specific product"""
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


# ==================== Fault Categories Endpoints ====================

@app.get("/api/fault-categories", tags=["Faults"], response_model=List[FaultCategorySchema])
def get_fault_categories(db: Session = Depends(get_db)):
    """Get all fault categories"""
    return db.query(FaultCategory).all()


# ==================== Complaints Endpoints ====================

@app.post("/api/complaints", tags=["Complaints"], response_model=ComplaintDetailResponse)
def create_complaint(complaint: ComplaintCreate, db: Session = Depends(get_db)):
    """
    Create a new complaint with AI classification
    
    The complaint will be automatically classified for fault type and severity
    """
    # Verify product exists
    product = db.query(Product).filter(Product.product_id == complaint.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # AI Classification
    classification = classify_complaint(complaint.complaint_text)
    
    # Create complaint record
    db_complaint = Complaint(
        product_id=complaint.product_id,
        department=complaint.department,
        complaint_text=complaint.complaint_text,
        created_date=datetime.utcnow().date(),
        status="open",
        predicted_fault_type=classification["fault_type"],
        severity=classification["severity"]
    )
    
    db.add(db_complaint)
    db.commit()
    db.refresh(db_complaint)
    
    return {
        **ComplaintResponse.from_orm(db_complaint).dict(),
        "fault_confidence": classification["fault_confidence"],
        "severity_confidence": classification["severity_confidence"]
    }


@app.get("/api/complaints", tags=["Complaints"], response_model=List[ComplaintResponse])
def get_complaints(
    db: Session = Depends(get_db),
    product_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    severity: Optional[str] = Query(None),
    limit: int = Query(50, le=100),
    skip: int = Query(0)
):
    """
    Get complaints with optional filters
    
    Query parameters:
    - product_id: Filter by product
    - status: Filter by status (open, in_progress, resolved, escalated)
    - severity: Filter by severity (low, medium, high, critical)
    - limit: Maximum number of results (default: 50, max: 100)
    - skip: Number of results to skip (pagination)
    """
    query = db.query(Complaint)
    
    if product_id:
        query = query.filter(Complaint.product_id == product_id)
    if status:
        query = query.filter(Complaint.status == status)
    if severity:
        query = query.filter(Complaint.severity == severity)
    
    return query.offset(skip).limit(limit).all()


@app.get("/api/complaints/{complaint_id}", tags=["Complaints"], response_model=ComplaintDetailResponse)
def get_complaint(complaint_id: int, db: Session = Depends(get_db)):
    """Get a specific complaint with AI confidence scores"""
    complaint = db.query(Complaint).filter(Complaint.complaint_id == complaint_id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    
    # Re-classify to get confidence scores
    classification = classify_complaint(complaint.complaint_text)
    
    return {
        **ComplaintResponse.from_orm(complaint).dict(),
        "fault_confidence": classification["fault_confidence"],
        "severity_confidence": classification["severity_confidence"]
    }


class ComplaintUpdate(BaseModel):
    status: Optional[str] = None
    resolved_date: Optional[date] = None
    customer_satisfaction: Optional[int] = None


@app.put("/api/complaints/{complaint_id}", tags=["Complaints"], response_model=ComplaintResponse)
def update_complaint(
    complaint_id: int,
    update: ComplaintUpdate,
    db: Session = Depends(get_db)
):
    """Update complaint status and resolution"""
    complaint = db.query(Complaint).filter(Complaint.complaint_id == complaint_id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    
    if update.status:
        complaint.status = update.status
    if update.resolved_date:
        complaint.resolved_date = update.resolved_date
        # Calculate resolution time
        if complaint.created_date:
            complaint.resolution_time = (update.resolved_date - complaint.created_date).days
    if update.customer_satisfaction:
        complaint.customer_satisfaction = update.customer_satisfaction
    
    db.commit()
    db.refresh(complaint)
    return complaint


# ==================== Analytics Endpoints ====================

@app.get("/api/analytics/dashboard", tags=["Analytics"])
def get_dashboard(db: Session = Depends(get_db)):
    """
    Get comprehensive dashboard summary with all key metrics
    
    Returns:
    - Fault distribution
    - Product health scores
    - Resolution metrics
    - Severity distribution
    - Department workload
    - Critical alerts
    """
    return get_dashboard_summary(db)


@app.get("/api/analytics/trends", tags=["Analytics"])
def get_trends(
    db: Session = Depends(get_db),
    days: int = Query(30, ge=1, le=365)
):
    """Get complaint trends over the specified period"""
    return insights_engine.get_complaint_trend(db, days)


@app.get("/api/analytics/faults", tags=["Analytics"])
def get_fault_analysis(db: Session = Depends(get_db)):
    """Get fault type distribution and analysis"""
    return insights_engine.get_fault_distribution(db)


@app.get("/api/analytics/product-health", tags=["Analytics"])
def get_product_health(db: Session = Depends(get_db)):
    """Get health scores for all products"""
    return insights_engine.get_product_health_scores(db)


@app.get("/api/analytics/resolution", tags=["Analytics"])
def get_resolution_stats(db: Session = Depends(get_db)):
    """Get complaint resolution statistics"""
    return insights_engine.get_resolution_metrics(db)


@app.get("/api/analytics/severity", tags=["Analytics"])
def get_severity_stats(db: Session = Depends(get_db)):
    """Get severity distribution statistics"""
    return insights_engine.get_severity_distribution(db)


@app.get("/api/analytics/departments", tags=["Analytics"])
def get_department_stats(db: Session = Depends(get_db)):
    """Get complaint distribution and metrics by department"""
    return insights_engine.get_department_workload(db)


@app.get("/api/analytics/alerts", tags=["Analytics"])
def get_critical_alerts(db: Session = Depends(get_db)):
    """Get critical alerts and concerning trends"""
    return insights_engine.get_critical_alerts(db)


# ==================== Stats Endpoints ====================

@app.get("/api/stats/summary", tags=["Statistics"])
def get_summary_stats(db: Session = Depends(get_db)):
    """Get high-level statistics"""
    total_complaints = db.query(Complaint).count()
    resolved_complaints = db.query(Complaint).filter(Complaint.status == "resolved").count()
    critical_complaints = db.query(Complaint).filter(Complaint.severity == "critical").count()
    
    return {
        "total_complaints": total_complaints,
        "resolved_complaints": resolved_complaints,
        "resolution_rate": round((resolved_complaints / total_complaints * 100), 2) if total_complaints > 0 else 0,
        "critical_complaints": critical_complaints,
        "open_complaints": db.query(Complaint).filter(Complaint.status == "open").count(),
        "average_satisfaction": db.query(Complaint).filter(
            Complaint.customer_satisfaction.isnot(None)
        ).all(),
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
