import getpass

from viewer import LogViewer
from ssh_client import start_server
from session_manager import (
    choose_session,
    get_session,
    create_session,
)

while True:

    print("\n===== GREPZY =====")
    print("1. Start Session")
    print("2. Create Session")
    print("3. Exit")

    choice = input("Choice: ")

    if choice == "1":
        break

    elif choice == "2":
        create_session()

    elif choice == "3":
        exit()


session_name = choose_session()

session = get_session(session_name)

passwords = {}

if len(session) > 0:
    for server in session["servers"]:

        pwd = getpass.getpass(
            f"{server['name']} Password: "
        )

        passwords[server["name"]] = pwd

    connections = []

    search_results = []

    for server in session["servers"]:

        results, errors = search_logs(
            host=server["host"],
            username=server["username"],
            password=passwords[server["name"]],
            search_text=query,
            directory="/logs"
        )

        for result in results:

            result["server"] = server["name"]

            search_results.append(result)

    connections.append(ssh)

LogViewer().run()

for ssh in connections:
    ssh.close()
