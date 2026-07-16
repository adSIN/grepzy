# Connect to one server, execute a search, return the results.

import paramiko


def search_logs(host, username, password, search_text, directory):

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect(
        hostname=host,
        username=username,
        password=password
    )

    command = (
        f'grep -R -H -n "{search_text}" {directory}'
    )

    stdin, stdout, stderr = ssh.exec_command(command)

    results = []

    for line in stdout:
        raw = line.rstrip()

        parts = raw.split(":", 2)

        if len(parts) == 3:
            results.append({
                "file": parts[0],
                "line": parts[1],
                "text": parts[2]
            })

    errors = stderr.read().decode()

    ssh.close()

    return results, errors