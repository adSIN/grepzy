from datetime import datetime
from queue import Queue

log_queue = Queue()

def read_logs(stdout, server_name):
    for line in iter(stdout.readline, ""):
        log_queue.put({
        "server": server_name,
        "text": line.rstrip(),
        "time": datetime.now()
        })
