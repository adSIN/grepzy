import json
import os

SESSION_FILE = "sessions.json"

def load_sessions():

    if not os.path.exists(SESSION_FILE):
        return {}

    try:
        with open(SESSION_FILE, "r") as f:
            return json.load(f)

    except (json.JSONDecodeError, FileNotFoundError):
        return {} 

def save_sessions(data):

    with open(SESSION_FILE, "w") as f:
        json.dump(data, f, indent=4)

def create_session():

    sessions = load_sessions()

    session_name = input("Server name: ")

    server_count = int(input("How many servers? "))

    servers = []

    for i in range(server_count):

        print(f"\nServer {i+1}")

        name = input("Server Name : ")
        host = input("IP Address   : ")
        username = input("Username     : ")
        logfile = input("Log File     : ")

        servers.append({
            "name": name,
            "host": host,
            "username": username,
            "log": logfile
        })

    sessions[session_name] = {
        "servers": servers
    }

    save_sessions(sessions)

    print("\nSession saved successfully.")

def list_sessions():

    sessions = load_sessions()

    if not sessions:
        print("No saved sessions.")
        return []

    names = list(sessions.keys())

    print()

    for i, name in enumerate(names, 1):
        print(f"{i}. {name}")

    return names

def choose_session():

    names = list_sessions()

    if not names:
        return None
    
    choice = int(input("\nChoose session: "))

    return names[choice - 1]

def get_session(session_name):

    sessions = load_sessions()

    return sessions.get(session_name)