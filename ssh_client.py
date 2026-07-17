import paramiko
import shlex
import threading
from log_reader import read_logs


def start_server(server_name, host, username, password, logfile):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect(host, username=username, password=password)

    # Quote the filename because session values can contain spaces or shell
    # metacharacters.  ``--`` also keeps a filename beginning with ``-`` from
    # being interpreted as a tail option.
    command = f"tail -n 20 -F -- {shlex.quote(logfile)}"
    stdin, stdout, stderr = ssh.exec_command(command)

    thread = threading.Thread(
        target=read_logs,
        args=(stdout, server_name),
        daemon=True
    )

    thread.start()

    # A failed tail used to be silent: its diagnostic was left on stderr and
    # the live view simply remained empty.  Feed those diagnostics into the
    # same queue so the user can see the problem in the viewer.
    error_thread = threading.Thread(
        target=read_logs,
        args=(stderr, server_name, True),
        daemon=True,
    )

    error_thread.start()

    return ssh
