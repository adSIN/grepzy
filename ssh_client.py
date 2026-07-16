import paramiko
import threading
from log_reader import read_logs


def start_server(server_name, host, username, password, logfile):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect(host, username=username, password=password)

    stdin, stdout, stderr = ssh.exec_command(
        f"tail -F {logfile}"
    )

    thread = threading.Thread(
        target=read_logs,
        args=(stdout, server_name),
        daemon=True
    )

    thread.start()

    return ssh