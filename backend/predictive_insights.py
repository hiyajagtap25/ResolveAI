"""
Predictive insights and analytics engine
Generates business intelligence metrics from complaint data
"""
from sqlalchemy.orm import Session
from database import Complaint, Product, FaultCategory
from datetime import datetime, timedelta
from sqlalchemy import func, and_, desc
import statistics

class InsightsEngine:
    """Generate predictive insights from complaint data"""
    
    @staticmethod
    def get_complaint_trend(db: Session, days: int = 30) -> dict:
        """
        Get complaint trend over the last N days
        Returns daily complaint counts for visualization
        """
        cutoff_date = datetime.utcnow().date() - timedelta(days=days)
        
        complaints = db.query(
            Complaint.created_date,
            func.count(Complaint.complaint_id).label("count")
        ).filter(
            Complaint.created_date >= cutoff_date
        ).group_by(
            Complaint.created_date
        ).order_by(
            Complaint.created_date
        ).all()
        
        return {
            "period_days": days,
            "data": [
                {"date": str(c[0]), "complaints": c[1]}
                for c in complaints
            ]
        }
    
    @staticmethod
    def get_fault_distribution(db: Session) -> dict:
        """Get distribution of fault types"""
        faults = db.query(
            Complaint.predicted_fault_type,
            func.count(Complaint.complaint_id).label("count")
        ).group_by(
            Complaint.predicted_fault_type
        ).order_by(
            desc(func.count(Complaint.complaint_id))
        ).all()
        
        total = sum(f[1] for f in faults)
        
        return {
            "total_faults": total,
            "distribution": [
                {
                    "fault_type": f[0],
                    "count": f[1],
                    "percentage": round((f[1] / total * 100), 2) if total > 0 else 0
                }
                for f in faults
            ]
        }
    
    @staticmethod
    def get_product_health_scores(db: Session) -> dict:
        """
        Calculate health scores for each product based on complaint metrics
        Score: 0-100 (higher is better)
        """
        products = db.query(Product).all()
        scores = []
        
        for product in products:
            complaints = db.query(Complaint).filter(
                Complaint.product_id == product.product_id
            ).all()
            
            if not complaints:
                score = 100
            else:
                # Calculate based on: severity, resolution time, resolution rate
                critical_count = sum(1 for c in complaints if c.severity == "critical")
                high_count = sum(1 for c in complaints if c.severity == "high")
                resolved_count = sum(1 for c in complaints if c.status == "resolved")
                resolution_rate = (resolved_count / len(complaints) * 100) if complaints else 0
                
                avg_resolution_time = statistics.mean(
                    [c.resolution_time for c in complaints if c.resolution_time]
                ) if any(c.resolution_time for c in complaints) else 0
                
                # Score calculation (0-100)
                severity_penalty = (critical_count * 15) + (high_count * 5)
                time_penalty = min(avg_resolution_time / 3, 20)  # max 20 point penalty
                resolution_bonus = (resolution_rate / 100) * 30  # max 30 point bonus
                
                score = max(0, 100 - severity_penalty - time_penalty + resolution_bonus)
            
            scores.append({
                "product_id": product.product_id,
                "product_name": product.product_name,
                "category": product.category,
                "health_score": round(score, 2),
                "complaint_count": len(complaints)
            })
        
        return {
            "scores": sorted(scores, key=lambda x: x["health_score"], reverse=True)
        }
    
    @staticmethod
    def get_resolution_metrics(db: Session) -> dict:
        """Get complaint resolution statistics"""
        resolved = db.query(Complaint).filter(
            Complaint.status == "resolved"
        ).all()
        
        resolution_times = [c.resolution_time for c in resolved if c.resolution_time]
        
        if not resolution_times:
            return {
                "total_resolved": 0,
                "avg_resolution_days": 0,
                "median_resolution_days": 0,
                "min_resolution_days": 0,
                "max_resolution_days": 0
            }
        
        return {
            "total_resolved": len(resolved),
            "avg_resolution_days": round(statistics.mean(resolution_times), 2),
            "median_resolution_days": round(statistics.median(resolution_times), 2),
            "min_resolution_days": min(resolution_times),
            "max_resolution_days": max(resolution_times)
        }
    
    @staticmethod
    def get_severity_distribution(db: Session) -> dict:
        """Get distribution of complaint severity levels"""
        severities = db.query(
            Complaint.severity,
            func.count(Complaint.complaint_id).label("count")
        ).group_by(
            Complaint.severity
        ).order_by(
            desc(func.count(Complaint.complaint_id))
        ).all()
        
        total = sum(s[1] for s in severities)
        
        return {
            "total": total,
            "by_severity": [
                {
                    "severity": s[0],
                    "count": s[1],
                    "percentage": round((s[1] / total * 100), 2) if total > 0 else 0
                }
                for s in severities
            ]
        }
    
    @staticmethod
    def get_department_workload(db: Session) -> dict:
        """Get complaint distribution by department"""
        departments = db.query(
            Complaint.department,
            func.count(Complaint.complaint_id).label("count"),
            func.avg(Complaint.resolution_time).label("avg_time")
        ).group_by(
            Complaint.department
        ).order_by(
            desc(func.count(Complaint.complaint_id))
        ).all()
        
        return {
            "by_department": [
                {
                    "department": d[0],
                    "complaint_count": d[1],
                    "avg_resolution_time": round(d[2], 2) if d[2] else None
                }
                for d in departments
            ]
        }
    
    @staticmethod
    def get_critical_alerts(db: Session) -> dict:
        """
        Identify critical issues requiring immediate attention
        Returns products and fault types with concerning trends
        """
        # Products with high critical complaints
        critical_products = db.query(
            Product.product_name,
            func.count(Complaint.complaint_id).label("critical_count")
        ).join(
            Complaint, Product.product_id == Complaint.product_id
        ).filter(
            Complaint.severity == "critical"
        ).group_by(
            Product.product_name
        ).order_by(
            desc(func.count(Complaint.complaint_id))
        ).limit(5).all()
        
        # Fault types with high unresolved rate
        unresolved = db.query(
            Complaint.predicted_fault_type,
            func.count(Complaint.complaint_id).label("unresolved_count")
        ).filter(
            Complaint.status != "resolved"
        ).group_by(
            Complaint.predicted_fault_type
        ).order_by(
            desc(func.count(Complaint.complaint_id))
        ).limit(5).all()
        
        return {
            "critical_products": [
                {"product": p[0], "critical_count": p[1]}
                for p in critical_products
            ],
            "unresolved_fault_types": [
                {"fault_type": u[0], "unresolved_count": u[1]}
                for u in unresolved
            ]
        }


# Global insights instance
insights_engine = InsightsEngine()


def get_dashboard_summary(db: Session) -> dict:
    """Get comprehensive dashboard summary"""
    return {
        "fault_distribution": insights_engine.get_fault_distribution(db),
        "product_health": insights_engine.get_product_health_scores(db),
        "resolution_metrics": insights_engine.get_resolution_metrics(db),
        "severity_distribution": insights_engine.get_severity_distribution(db),
        "department_workload": insights_engine.get_department_workload(db),
        "critical_alerts": insights_engine.get_critical_alerts(db),
        "timestamp": datetime.utcnow().isoformat()
    }
