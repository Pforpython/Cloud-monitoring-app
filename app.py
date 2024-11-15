import psutil
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")

def index():
    cpu_percent = psutil.cpu_percent()
    mem_percent = psutil.virtual_memory().percent
    if cpu_percent > 80 and mem_percent > 80:
        Message = "WARNING! High CPU & Memory Utilization detected. Please scale up."
    if cpu_percent > 80:
        Message = "WARNING! High CPU Utilization detected. Please scale up CPU." 
    elif mem_percent > 80:
        Message = "WARNING! High Memory Utilization detected. Pleace scale up memory."
    else:
        Message=None        
    # return f"CPU Utilization: {cpu_percent} and Memory Utilization: {mem_percent}"
    return render_template("space-themed.html",cpu_percent=cpu_percent, mem_percent=mem_percent, message=Message)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    
    