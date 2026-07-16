import getpass

from ssh_client import start_server
from session_manager import choose_session, get_session
from viewer import LogViewer


def start_live():

    session_name = choose_session()

    if not session_name:
        return

    session = get_session(session_name)

    if not session:
        print("Session not found.")
        return

    passwords = {}

    for server in session["servers"]:

        passwords[server["name"]] = getpass.getpass(
            f"{server['name']} Password: "
        )

    connections = []

    for server in session["servers"]:

        ssh = start_server(
            server_name=server["name"],
            host=server["host"],
            username=server["username"],
            password=passwords[server["name"]],
            logfile=server["log"]
        )

        connections.append(ssh)

    try:
        LogViewer(mode="live").run()

    finally:
        for ssh in connections:
            ssh.close()