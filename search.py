import getpass
import paramiko
import shlex
from session_manager import choose_session, get_session
from concurrent.futures import ThreadPoolExecutor, as_completed

def search_logs(host, username, password, search_text, directory):

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect(
        hostname=host,
        username=username,
        password=password
    )

    pattern = shlex.quote(search_text)
    search_dir = shlex.quote(directory)
    command = f"grep -R -H -n {pattern} {search_dir}"

    stdin, stdout, stderr = ssh.exec_command(command)
    print(f"[{host}] Running: {command}")

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
    print(f"[{host}] Found {len(results)} matches")
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

    future_to_server = {}

    with ThreadPoolExecutor(max_workers=len(session["servers"])) as executor:

        for server in session["servers"]:

            future = executor.submit(
                search_logs,
                host=server["host"],
                username=server["username"],
                password=passwords[server["name"]],
                search_text=query,
                directory="/logs"
            )

            future_to_server[future] = server

        for future in as_completed(future_to_server):

            server = future_to_server[future]

            try:
                server_results, errors = future.result()

                if errors:
                    print(f"{server['name']}: {errors}")

                for entry in server_results:
                    entry["server"] = server["name"]
                    results.append(entry)

            except Exception as e:
                print(f"{server['name']} failed: {e}")

    return results