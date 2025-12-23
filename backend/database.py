"""
Database configuration and session management
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from datetime import datetime

# SQLite database URL
DATABASE_URL = "sqlite:///./resolve_analytics.db"

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


# ==================== Database Models ====================

class Product(Base):
    __tablename__ = "products"
    
    product_id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)  # earbuds, headphones, speakers, smartwatches


class FaultCategory(Base):
    __tablename__ = "fault_categories"
    
    fault_id = Column(Integer, primary_key=True, index=True)
    fault_name = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=True)


class Complaint(Base):
    __tablename__ = "complaints"
    
    complaint_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False)
    department = Column(String(100), nullable=False)  # support, quality, sales, etc.
    complaint_text = Column(Text, nullable=False)
    created_date = Column(Date, nullable=False, default=datetime.utcnow)
    resolved_date = Column(Date, nullable=True)
    status = Column(String(50), default="open")  # open, in_progress, resolved, escalated
    predicted_fault_type = Column(String(255), nullable=True)
    resolution_time = Column(Integer, nullable=True)  # in days
    severity = Column(String(50), default="medium")  # low, medium, high, critical
    customer_satisfaction = Column(Integer, nullable=True)  # 1-5 rating


def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
