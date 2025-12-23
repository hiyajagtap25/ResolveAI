"""
AI Complaint Classifier using scikit-learn
Simulates AI-powered complaint categorization and severity prediction
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import pickle
import os
from typing import Tuple

class ComplaintClassifier:
    """
    AI classifier for complaint categorization and severity prediction
    Uses TF-IDF + Naive Bayes for text classification
    """
    
    def __init__(self):
        self.fault_pipeline = None
        self.severity_pipeline = None
        self.is_trained = False
        
    def train(self, complaint_texts: list, fault_labels: list, severity_labels: list):
        """
        Train the classifier on complaint texts
        
        Args:
            complaint_texts: List of complaint text strings
            fault_labels: List of fault categories (labels)
            severity_labels: List of severity levels (low, medium, high, critical)
        """
        # Fault type classifier
        self.fault_pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=500, stop_words='english')),
            ('nb', MultinomialNB(alpha=1.0))
        ])
        self.fault_pipeline.fit(complaint_texts, fault_labels)
        
        # Severity classifier
        self.severity_pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=500, stop_words='english')),
            ('nb', MultinomialNB(alpha=1.0))
        ])
        self.severity_pipeline.fit(complaint_texts, severity_labels)
        
        self.is_trained = True
    
    def predict_fault_type(self, complaint_text: str) -> str:
        """Predict the fault category for a complaint"""
        if not self.is_trained:
            return self._rule_based_fault_prediction(complaint_text)
        return self.fault_pipeline.predict([complaint_text])[0]
    
    def predict_severity(self, complaint_text: str) -> str:
        """Predict the severity level of a complaint"""
        if not self.is_trained:
            return self._rule_based_severity_prediction(complaint_text)
        return self.severity_pipeline.predict([complaint_text])[0]
    
    def get_confidence(self, complaint_text: str) -> Tuple[float, float]:
        """Get confidence scores for predictions"""
        if not self.is_trained:
            return (0.75, 0.70)
        
        fault_proba = self.fault_pipeline.predict_proba([complaint_text]).max()
        severity_proba = self.severity_pipeline.predict_proba([complaint_text]).max()
        
        return (fault_proba, severity_proba)
    
    def _rule_based_fault_prediction(self, text: str) -> str:
        """
        Simple rule-based fault prediction when model is not trained
        Used for initial predictions before training data is available
        """
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['battery', 'charge', 'drain', 'power']):
            return "Battery Issue"
        elif any(word in text_lower for word in ['sound', 'audio', 'distort', 'crackle']):
            return "Audio Quality"
        elif any(word in text_lower for word in ['bluetooth', 'connect', 'pair', 'disconn']):
            return "Connectivity"
        elif any(word in text_lower for word in ['water', 'damage', 'crack', 'broken']):
            return "Physical Damage"
        elif any(word in text_lower for word in ['crash', 'freeze', 'bug', 'app']):
            return "Software Bug"
        elif any(word in text_lower for word in ['firmware', 'update', 'upgrade']):
            return "Firmware Update"
        elif any(word in text_lower for word in ['warranty', 'return', 'refund']):
            return "Warranty/Return"
        else:
            return "Performance"
    
    def _rule_based_severity_prediction(self, text: str) -> str:
        """
        Simple rule-based severity prediction
        Used for initial predictions before training data is available
        """
        text_lower = text.lower()
        
        critical_keywords = ['won\'t', 'doesn\'t work', 'completely broken', 'not working', 'dead']
        high_keywords = ['completely', 'severe', 'major', 'extreme']
        medium_keywords = ['issue', 'problem', 'bad', 'poor']
        
        if any(word in text_lower for word in critical_keywords):
            return "critical"
        elif any(word in text_lower for word in high_keywords):
            return "high"
        elif any(word in text_lower for word in medium_keywords):
            return "medium"
        else:
            return "low"
    
    def save_model(self, filepath: str):
        """Save trained model to disk"""
        if self.is_trained:
            with open(filepath, 'wb') as f:
                pickle.dump({
                    'fault_pipeline': self.fault_pipeline,
                    'severity_pipeline': self.severity_pipeline
                }, f)
    
    def load_model(self, filepath: str):
        """Load trained model from disk"""
        if os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                data = pickle.load(f)
                self.fault_pipeline = data['fault_pipeline']
                self.severity_pipeline = data['severity_pipeline']
                self.is_trained = True


# Global classifier instance
classifier = ComplaintClassifier()


def classify_complaint(complaint_text: str) -> dict:
    """
    Classify a complaint and return fault type, severity, and confidence
    
    Returns:
        {
            "fault_type": str,
            "severity": str,
            "fault_confidence": float,
            "severity_confidence": float
        }
    """
    fault_type = classifier.predict_fault_type(complaint_text)
    severity = classifier.predict_severity(complaint_text)
    fault_conf, severity_conf = classifier.get_confidence(complaint_text)
    
    return {
        "fault_type": fault_type,
        "severity": severity,
        "fault_confidence": round(fault_conf, 3),
        "severity_confidence": round(severity_conf, 3)
    }
