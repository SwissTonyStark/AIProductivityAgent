"""
Monitoring dashboard for tracking resource usage and costs.
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pandas as pd
from typing import Dict, List, Any
from core.monitoring.resource_monitor import ResourceMonitor
from core.monitoring.cost_allocator import CostAllocation

class MonitoringDashboard:
    """Streamlit-based monitoring dashboard for resource usage."""
    
    def __init__(self, resource_monitor: ResourceMonitor, cost_allocator: CostAllocation):
        self.resource_monitor = resource_monitor
        self.cost_allocator = cost_allocator
        
    def render(self):
        """Render the monitoring dashboard."""
        st.title("Resource Usage & Cost Monitoring")
        
        # Sidebar for time range selection
        st.sidebar.header("Time Range")
        time_range = st.sidebar.selectbox(
            "Select Time Range",
            ["Last 24 Hours", "Last 7 Days", "Last 30 Days", "Custom"]
        )
        
        if time_range == "Custom":
            start_date = st.sidebar.date_input("Start Date")
            end_date = st.sidebar.date_input("End Date")
        else:
            end_date = datetime.now()
            if time_range == "Last 24 Hours":
                start_date = end_date - timedelta(days=1)
            elif time_range == "Last 7 Days":
                start_date = end_date - timedelta(days=7)
            else:
                start_date = end_date - timedelta(days=30)
        
        # API Usage Overview
        st.header("API Usage Overview")
        self._render_api_usage_chart()
        
        # Cost Breakdown
        st.header("Cost Breakdown")
        self._render_cost_breakdown()
        
        # Resource Utilization
        st.header("Resource Utilization")
        self._render_resource_utilization()
        
        # Alerts and Thresholds
        st.header("Alerts & Thresholds")
        self._render_alerts()
    
    def _render_api_usage_chart(self):
        """Render API usage chart."""
        api_data = self.resource_monitor.get_api_usage()
        if not api_data:
            st.info("No API usage data available yet.")
            return
            
        df = pd.DataFrame(api_data)
        
        fig = px.bar(
            df,
            x="api_name",
            y="total_tokens",
            title="API Token Usage",
            labels={"api_name": "API", "total_tokens": "Total Tokens"}
        )
        st.plotly_chart(fig)
    
    def _render_cost_breakdown(self):
        """Render cost breakdown charts."""
        col1, col2 = st.columns(2)
        
        with col1:
            feature_costs = self.cost_allocator.get_feature_costs()
            if not feature_costs:
                st.info("No feature cost data available yet.")
            else:
                fig = px.pie(
                    values=list(feature_costs.values()),
                    names=list(feature_costs.keys()),
                    title="Cost by Feature"
                )
                st.plotly_chart(fig)
        
        with col2:
            customer_costs = self.cost_allocator.get_customer_costs()
            if not customer_costs:
                st.info("No customer cost data available yet.")
            else:
                fig = px.bar(
                    x=list(customer_costs.keys()),
                    y=list(customer_costs.values()),
                    title="Cost by Customer"
                )
                st.plotly_chart(fig)
    
    def _render_resource_utilization(self):
        """Render resource utilization metrics."""
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Total API Calls",
                self.resource_monitor.get_total_api_calls()
            )
        
        with col2:
            st.metric(
                "Total Tokens Used",
                self.resource_monitor.get_total_tokens()
            )
        
        with col3:
            st.metric(
                "Total Cost",
                f"${self.resource_monitor.get_total_cost():.2f}"
            )
    
    def _render_alerts(self):
        """Render alerts and threshold information."""
        alerts = self.resource_monitor.get_alerts()
        
        if not alerts:
            st.info("No alerts at this time.")
            return
            
        for alert in alerts:
            if alert["severity"] == "high":
                st.error(alert["message"])
            elif alert["severity"] == "medium":
                st.warning(alert["message"])
            else:
                st.info(alert["message"])
        
        # Threshold settings
        st.subheader("Threshold Settings")
        new_daily_threshold = st.number_input(
            "Daily Cost Threshold ($)",
            value=self.resource_monitor.cost_thresholds["daily"]
        )
        if st.button("Update Thresholds"):
            self.resource_monitor.update_thresholds(
                daily=new_daily_threshold
            )
            st.success("Thresholds updated successfully!") 