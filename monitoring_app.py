"""
Monitoring app entry point for resource usage tracking.
"""
import streamlit as st
from core.monitoring.dashboard import MonitoringDashboard
from core.monitoring.resource_monitor import ResourceMonitor
from core.monitoring.cost_allocator import CostAllocation

def main():
    """Main entry point for the monitoring dashboard."""
    st.set_page_config(
        page_title="ProductivityAgent Monitoring",
        page_icon="📊",
        layout="wide"
    )
    
    # Initialize monitoring components
    resource_monitor = ResourceMonitor()
    cost_allocator = CostAllocation()
    
    # Create and render dashboard
    dashboard = MonitoringDashboard(resource_monitor, cost_allocator)
    dashboard.render()

if __name__ == "__main__":
    main() 