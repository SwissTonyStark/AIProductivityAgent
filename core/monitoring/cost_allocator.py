"""
Cost allocation tracking for features and customers.
"""
from typing import Dict, List, Any
import json
from pathlib import Path

class CostAllocation:
    """Tracks costs by feature and customer."""
    
    def __init__(self):
        self.feature_costs: Dict[str, float] = {}
        self.customer_costs: Dict[str, float] = {}
        self._load_cost_data()
    
    def _load_cost_data(self):
        """Load cost data from file if it exists."""
        data_file = Path("cost_data.json")
        if data_file.exists():
            with open(data_file, "r") as f:
                data = json.load(f)
                self.feature_costs = data.get("feature_costs", {})
                self.customer_costs = data.get("customer_costs", {})
    
    def _save_cost_data(self):
        """Save cost data to file."""
        with open("cost_data.json", "w") as f:
            json.dump({
                "feature_costs": self.feature_costs,
                "customer_costs": self.customer_costs
            }, f)
    
    def track_usage(self, feature: str, customer_id: str, cost: float):
        """Track usage costs by feature and customer."""
        # Update feature costs
        if feature not in self.feature_costs:
            self.feature_costs[feature] = 0.0
        self.feature_costs[feature] += cost
        
        # Update customer costs
        if customer_id not in self.customer_costs:
            self.customer_costs[customer_id] = 0.0
        self.customer_costs[customer_id] += cost
        
        self._save_cost_data()
    
    def get_feature_costs(self) -> Dict[str, float]:
        """Get costs by feature."""
        return self.feature_costs
    
    def get_customer_costs(self) -> Dict[str, float]:
        """Get costs by customer."""
        return self.customer_costs
    
    def get_feature_cost(self, feature: str) -> float:
        """Get cost for a specific feature."""
        return self.feature_costs.get(feature, 0.0)
    
    def get_customer_cost(self, customer_id: str) -> float:
        """Get cost for a specific customer."""
        return self.customer_costs.get(customer_id, 0.0)
    
    def reset_costs(self):
        """Reset all cost tracking."""
        self.feature_costs = {}
        self.customer_costs = {}
        self._save_cost_data() 