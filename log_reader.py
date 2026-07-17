from datetime import datetime
from queue import Queue

log_queue = Queue()

def read_logs(stdout, server_name, is_error=False):
    for line in iter(stdout.readline, ""):
        text = line.rstrip()

        if is_error:
            text = f"[tail error] {text}"

        log_queue.put({
            "server": server_name,
            "text": text,
            "time": datetime.now(),
        })
