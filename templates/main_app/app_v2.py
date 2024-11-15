# With Redis logging
# See templates/html_templates/logging_page.html for html page created by Claude

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
    if cpu_percent > 80:
        Message = "WARNING! High CPU Utilization detected. Please scale up CPU." 
    elif mem_percent > 80:
        Message = "WARNING! High Memory Utilization detected. Pleace scale up memory."
    else:
        Message = "WARNING! High CPU & Memory Utilization detected. Please scale up."
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
    
    
"""
To use this updated version:

1. First, install Redis and the Python Redis client:

```bash
# Install Redis server
sudo apt-get install redis-server  # For Ubuntu/Debian
# or
brew install redis  # For macOS

# Install Python Redis client
pip install redis
```

2. Start the Redis server:
```bash
redis-server
```

3. The application now provides:
   - Original monitoring at the root URL "/"
   - Metrics history at "/metrics"
   - Background thread logging metrics to Redis every 5 seconds
   - Storage of the last 100 measurements

4. You can also directly query Redis using the redis-cli:
```bash
redis-cli
> LRANGE system_metrics 0 -1  # Get all metrics
```

Key features of this implementation:
1. Uses a background thread to continuously log metrics
2. Stores metrics as JSON strings in a Redis list
3. Maintains a fixed-size history (100 entries) to prevent unlimited growth
4. Provides a web interface to view the metrics history
5. Includes warning indicators for high utilization
6. Error handling for Redis operations

You can customize this further by:
1. Adjusting the logging interval (currently 5 seconds)
2. Modifying the number of historical entries kept (currently 100)
3. Adding more metrics to track
4. Enhancing the metrics visualization (e.g., adding graphs)
5. Adding data export capabilities

Would you like me to explain any part in more detail or help you customize any of these features?
"""