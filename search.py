import getpass
import paramiko

from session_manager import choose_session, get_session


def search_logs(host, username, password, search_text, directory):

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect(
        hostname=host,
        username=username,
        password=password
    )

    command = f'grep -R -H -n "{search_text}" {directory}'

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


def start_search():

    session_name = choose_session()

    if not session_name:
        return None

    session = get_session(session_name)

    if not session:
        print("Session not found.")
        return None

    passwords = {}

    for server in session["servers"]:
        passwords[server["name"]] = getpass.getpass(
            f"{server['name']} Password: "
        )

    query = input("\nSearch text: ")

    results = []

    for server in session["servers"]:

        server_results, errors = search_logs(
            host=server["host"],
            username=server["username"],
            password=passwords[server["name"]],
            search_text=query,
            directory="/logs"
        )

        if errors:
            print(errors)

        for entry in server_results:
            entry["server"] = server["name"]
            results.append(entry)

    return results