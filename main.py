from viewer import LogViewer
from search import start_search
from live import start_live
from session_manager import choose_session, get_session, session_menu
from utils import clear
def print_footer():
    print("\n" + "─" * 60)
    print("         Grepzy v1.0 | One Search. Every Server.")
    print("         https://github.com/adSIN/grepzy")
    print("         Made with <3 by adSIN")
    print("─" * 60)

while True:
    clear()

    print("""
==========================================
              GREPZY
      One Search. Every Server.
==========================================
""")
    print("1. Live Monitor")
    print("2. Search Logs")
    print("3. Sessions")
    print("4. Exit")
    print_footer()

    choice = input("Choice: ")

    if choice == "1":
        start_live()

    elif choice == "2":

        results = start_search()

        if results:
            LogViewer(
                mode="search",
                search_results=results
            ).run()

    elif choice == "3":
        session_menu()

    elif choice == "4":
        confirm = input(
        "\nExit Grepzy? (y/N): "
        )

        if confirm.lower() == "y":
            print("\nGoodbye!\n")
            break

