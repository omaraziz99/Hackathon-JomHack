# backend/app/risk_analyzer.py
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from typing import List, Dict, Union
from datetime import datetime

class RiskAnalyzer:
    def __init__(self):
        self.feature_names = [
            'transaction_amount',
            'multiple_attempts',
            'evidence_score',
            'response_time',
            'weekend_transaction'
        ]
        
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self._train_initial_model()

    def _train_initial_model(self):
        # Mock training data
        X = np.random.rand(1000, len(self.feature_names))
        y = np.random.normal(50, 15, 1000)
        y = np.clip(y, 0, 100)
        self.model.fit(X, y)

    def calculate_risk_score(self, dispute_data: Dict) -> Dict:
        base_score = 50
        
        # Calculate basic risk factors
        amount_factor = min(dispute_data.get('amount', 0) / 1000, 1) * 20
        base_score += amount_factor

        # Pattern analysis
        if dispute_data.get('patterns'):
            pattern_score = self._analyze_patterns(dispute_data['patterns'])
            base_score += pattern_score

        # Evidence evaluation
        evidence_score = 0
        if 'evidence_list' in dispute_data:
            evidence_score = self._evaluate_evidence(dispute_data['evidence_list'])
            base_score -= evidence_score * 0.2

        final_score = max(0, min(100, base_score))
        
        return {
            'risk_score': round(final_score, 2),
            'evidence_score': round(evidence_score, 2),
            'status': self._determine_status(final_score),
            'contributing_factors': self._get_contributing_factors(dispute_data)
        }

    def _analyze_patterns(self, patterns: List[str]) -> float:
        pattern_scores = {
            'multiple attempts': 15,
            'unusual location': 10,
            'new device': 8,
            'failed verification': 12
        }
        
        total_score = 0
        for pattern in patterns:
            for key, score in pattern_scores.items():
                if key in pattern.lower():
                    total_score += score
        
        return min(total_score, 30)

    def _evaluate_evidence(self, evidence_list: List) -> float:
        if not evidence_list:
            return 0
            
        scores = []
        for evidence in evidence_list:
            if evidence.get('type') == 'bank_statement':
                scores.append(5 if evidence.get('verified') else 2)
            elif evidence.get('type') == 'video_recording':
                scores.append(4 if evidence.get('quality') == 'high' else 2)
                
        return np.mean(scores) if scores else 0

    def _determine_status(self, risk_score: float) -> str:
        if risk_score >= 75:
            return "High Risk"
        elif risk_score >= 50:
            return "Medium Risk"
        return "Low Risk"

    def _get_contributing_factors(self, data: Dict) -> List[str]:
        factors = []
        if data.get('amount', 0) > 500:
            factors.append("High transaction amount")
        if 'multiple attempts' in str(data.get('patterns', [])):
            factors.append("Multiple transaction attempts")
        if data.get('evidence_list', []):
            factors.append(f"Evidence score: {self._evaluate_evidence(data['evidence_list']):.1f}")
        return factors
    
    