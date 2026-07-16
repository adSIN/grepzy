import threading 
from datetime import datetime
import paramiko

logs = []

def read_logs(stdout):
    for line in iter(stdout.readline, ""):

        print("FROM SERVER:", line.rstrip())
        
        logs.append({
        "time": datetime.now(),
        "text": line.rstrip(),
        "server": "SERVER-1"
        })

        if len(logs)> 5000:
            logs.pop(0)