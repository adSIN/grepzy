import getpass
import paramiko
import shlex
from log_reader import read_logs,logs
import threading
from viewer import LogViewer

host = ""
username = "root"
password = getpass.getpass("Enter the password: ")

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, username=username, password=password)

command = "tail -F /logs/mfpMessages.logs"
stdin,stdout,stderr = ssh.exec_command(command)

thread = threading.Thread(
    target = read_logs,
    args = (stdout,),
    daemon = True
)

thread.start()

LogViewer().run()

ssh.close()
