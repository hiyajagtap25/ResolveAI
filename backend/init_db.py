"""
Database initialization with sample data
"""
from database import Base, engine, SessionLocal, Product, FaultCategory, Complaint
from datetime import datetime, timedelta
import random

def init_database():
    """Create all tables and populate with sample data"""
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created")
    
    db = SessionLocal()
    
    # Check if data already exists
    if db.query(Product).count() > 0:
        print("✓ Database already populated")
        db.close()
        return
    
    # ==================== Products ====================
    products = [
        Product(product_name="EarBud Pro X", category="earbuds"),
        Product(product_name="EarBud Lite", category="earbuds"),
        Product(product_name="Headphone Max", category="headphones"),
        Product(product_name="Headphone Studio", category="headphones"),
        Product(product_name="Speaker Boom", category="speakers"),
        Product(product_name="Speaker Mini", category="speakers"),
        Product(product_name="Watch Ultra", category="smartwatches"),
        Product(product_name="Watch Fit", category="smartwatches"),
    ]
    db.add_all(products)
    db.flush()
    print(f"✓ Added {len(products)} products")
    
    # ==================== Fault Categories ====================
    fault_categories = [
        FaultCategory(fault_name="Battery Issue", description="Battery drains quickly or won't charge"),
        FaultCategory(fault_name="Audio Quality", description="Poor sound output, distortion, or imbalance"),
        FaultCategory(fault_name="Connectivity", description="Bluetooth pairing or connection issues"),
        FaultCategory(fault_name="Physical Damage", description="Cracked casing, water damage, or breakage"),
        FaultCategory(fault_name="Software Bug", description="App crashes, freezing, or unresponsive"),
        FaultCategory(fault_name="Firmware Update", description="Issues after firmware update"),
        FaultCategory(fault_name="Warranty/Return", description="Warranty claims and return requests"),
        FaultCategory(fault_name="Performance", description="Reduced performance or speed"),
    ]
    db.add_all(fault_categories)
    db.flush()
    print(f"✓ Added {len(fault_categories)} fault categories")
    
    # ==================== Complaints (Sample Data) ====================
    complaint_texts = [
        "Battery dies after 2 hours of use. Not acceptable for the price.",
        "Left earbud stopped working completely. No sound at all.",
        "Bluetooth keeps disconnecting every few minutes.",
        "Audio is extremely distorted and crackles at high volume.",
        "Device won't charge even when plugged in for hours.",
        "App crashes whenever I try to adjust settings.",
        "Water damage after accidental splash, speaker doesn't work.",
        "After the latest firmware update, the device won't turn on.",
        "One speaker is significantly quieter than the other.",
        "Device randomly restarts without warning.",
    ]
    
    departments = ["support", "quality", "sales", "returns", "technical"]
    statuses = ["open", "in_progress", "resolved", "escalated"]
    severities = ["low", "medium", "high", "critical"]
    
    complaints = []
    for i in range(150):
        complaint = Complaint(
            product_id=random.randint(1, 8),
            department=random.choice(departments),
            complaint_text=random.choice(complaint_texts),
            created_date=datetime.utcnow().date() - timedelta(days=random.randint(0, 90)),
            resolved_date=datetime.utcnow().date() - timedelta(days=random.randint(0, 60)) if random.random() > 0.3 else None,
            status=random.choice(statuses),
            predicted_fault_type=random.choice([f.fault_name for f in fault_categories]),
            resolution_time=random.randint(1, 30) if random.random() > 0.3 else None,
            severity=random.choice(severities),
            customer_satisfaction=random.choice([1, 2, 3, 4, 5, None])
        )
        complaints.append(complaint)
    
    db.add_all(complaints)
    db.commit()
    print(f"✓ Added {len(complaints)} sample complaints")
    db.close()
    print("\n✓ Database initialized successfully!")


if __name__ == "__main__":
    init_database()
