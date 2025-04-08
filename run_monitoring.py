"""
Script to run the monitoring dashboard.
"""
import subprocess
import sys
import os

def main():
    """Run the monitoring dashboard."""
    try:
        # Ensure all dependencies are installed
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        
        # Run the monitoring app
        subprocess.check_call([sys.executable, "-m", "streamlit", "run", "monitoring_app.py"])
    except subprocess.CalledProcessError as e:
        print(f"Error running monitoring dashboard: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 