import psutil
from flask import Flask, render_template
import redis
import json
from datetime import datetime
import threading
import time

app = Flask(__name__)

# Redis configuration
redis_client = redis.Redis(host='localhost', port=6379, db=0)
METRICS_KEY = 'system_metrics'
MAX_METRICS_HISTORY = 100  # Keep last 100 measurements

def log_metrics():
    """Background task to log metrics to Redis"""
    while True:
        try:
            cpu_percent = psutil.cpu_percent()
            mem_percent = psutil.virtual_memory().percent
            
            # Create metrics entry
            metric = {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'cpu_percent': cpu_percent,
                'mem_percent': mem_percent
            }
            
            # Add to Redis list
            redis_client.lpush(METRICS_KEY, json.dumps(metric))
            
            # Trim list to keep only recent entries
            redis_client.ltrim(METRICS_KEY, 0, MAX_METRICS_HISTORY - 1)
            
            time.sleep(5)  # Log every 5 seconds
        except Exception as e:
            print(f"Error logging metrics: {e}")
            time.sleep(5)

@app.route("/")
def index():
    cpu_percent = psutil.cpu_percent()
    mem_percent = psutil.virtual_memory().percent
    Message = None
    if cpu_percent > 80 or mem_percent > 80:
        Message = "WARNING! High CPU or Memory Utilization detected. Please scale up."
    return render_template("space-themed.html", 
                         cpu_percent=cpu_percent, 
                         mem_percent=mem_percent, 
                         message=Message)

@app.route("/metrics")
def metrics():
    """Endpoint to display metrics history"""
    try:
        # Get all metrics from Redis
        metrics_data = []
        metrics_raw = redis_client.lrange(METRICS_KEY, 0, -1)
        
        for metric in metrics_raw:
            metrics_data.append(json.loads(metric))
        
        # Sort by timestamp
        metrics_data.sort(key=lambda x: x['timestamp'])
        
        return render_template("metrics.html", metrics=metrics_data)
    except Exception as e:
        return f"Error retrieving metrics: {str(e)}", 500

# Start metrics logging in background
metrics_thread = threading.Thread(target=log_metrics, daemon=True)
metrics_thread.start()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')