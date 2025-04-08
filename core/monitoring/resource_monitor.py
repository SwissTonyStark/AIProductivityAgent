"""
Resource monitoring for tracking API usage and costs.
"""
from datetime import datetime, timedelta
from typing import Dict, List, Any
import json
import os
from pathlib import Path

class ResourceMonitor:
    """Monitors resource usage and costs."""
    
    def __init__(self):
        self.api_calls: Dict[str, Dict[str, Any]] = {}
        self.cost_thresholds = {
            'daily': 10.0,   # $10 per day
            'weekly': 50.0,  # $50 per week
            'monthly': 150.0 # $150 per month
        }
        self._load_usage_data()
    
    def _load_usage_data(self):
        """Load usage data from file if it exists."""
        data_file = Path("usage_data.json")
        if data_file.exists():
            with open(data_file, "r") as f:
                self.api_calls = json.load(f)
    
    def _save_usage_data(self):
        """Save usage data to file."""
        with open("usage_data.json", "w") as f:
            json.dump(self.api_calls, f)
    
    async def track_api_call(self, api_name: str, tokens_used: int, cost: float):
        """Track API usage and cost."""
        today = datetime.now().strftime("%Y-%m-%d")
        
        if api_name not in self.api_calls:
            self.api_calls[api_name] = {
                'daily_usage': {},
                'total_tokens': 0,
                'total_cost': 0.0
            }
        
        # Update daily usage
        if today not in self.api_calls[api_name]['daily_usage']:
            self.api_calls[api_name]['daily_usage'][today] = {
                'calls': 0,
                'tokens': 0,
                'cost': 0.0
            }
        
        self.api_calls[api_name]['daily_usage'][today]['calls'] += 1
        self.api_calls[api_name]['daily_usage'][today]['tokens'] += tokens_used
        self.api_calls[api_name]['daily_usage'][today]['cost'] += cost
        
        # Update totals
        self.api_calls[api_name]['total_tokens'] += tokens_used
        self.api_calls[api_name]['total_cost'] += cost
        
        self._save_usage_data()
        await self._check_thresholds(api_name)
    
    async def _check_thresholds(self, api_name: str):
        """Check if cost thresholds are exceeded."""
        today = datetime.now().strftime("%Y-%m-%d")
        daily_cost = self.api_calls[api_name]['daily_usage'][today]['cost']
        
        if daily_cost > self.cost_thresholds['daily']:
            await self._send_alert(
                f"Daily cost threshold exceeded for {api_name}: ${daily_cost:.2f}",
                "high"
            )
    
    async def _send_alert(self, message: str, severity: str = "medium"):
        """Send an alert (placeholder for actual alert implementation)."""
        print(f"[{severity.upper()}] {message}")
    
    def get_api_usage(self) -> List[Dict[str, Any]]:
        """Get API usage data for visualization."""
        return [
            {
                "api_name": api,
                "total_tokens": data["total_tokens"],
                "total_cost": data["total_cost"],
                "daily_calls": sum(day["calls"] for day in data["daily_usage"].values())
            }
            for api, data in self.api_calls.items()
        ]
    
    def get_total_api_calls(self) -> int:
        """Get total number of API calls."""
        return sum(
            sum(day["calls"] for day in data["daily_usage"].values())
            for data in self.api_calls.values()
        )
    
    def get_total_tokens(self) -> int:
        """Get total number of tokens used."""
        return sum(data["total_tokens"] for data in self.api_calls.values())
    
    def get_total_cost(self) -> float:
        """Get total cost."""
        return sum(data["total_cost"] for data in self.api_calls.values())
    
    def get_alerts(self) -> List[Dict[str, str]]:
        """Get current alerts."""
        alerts = []
        today = datetime.now().strftime("%Y-%m-%d")
        
        for api_name, data in self.api_calls.items():
            if today in data["daily_usage"]:
                daily_cost = data["daily_usage"][today]["cost"]
                if daily_cost > self.cost_thresholds["daily"]:
                    alerts.append({
                        "message": f"Daily cost threshold exceeded for {api_name}: ${daily_cost:.2f}",
                        "severity": "high"
                    })
        
        return alerts
    
    def update_thresholds(self, daily: float = None, weekly: float = None, monthly: float = None):
        """Update cost thresholds."""
        if daily is not None:
            self.cost_thresholds["daily"] = daily
        if weekly is not None:
            self.cost_thresholds["weekly"] = weekly
        if monthly is not None:
            self.cost_thresholds["monthly"] = monthly 