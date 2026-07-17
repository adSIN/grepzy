from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Header, Footer, Input, RichLog
from queue import Empty
from log_reader import log_queue

class LogViewer(App):

    def __init__(self, mode="live", search_results=None):
        super().__init__()

        self.mode = mode
        self.search_results = search_results or []

    CSS = """
    Screen {
        layout: vertical;
    }

    #logs {
        height: 1fr;
    }

    #filter {
        dock: bottom;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()

        with Vertical():
            yield RichLog(id="logs")
            yield Input(
                placeholder="Type to filter logs...",
                id="filter"
            )

        yield Footer()

    def on_mount(self):
        self.history = []

        self.log_widget = self.query_one("#logs", RichLog)

        self.last = 0

        self.filter_text = ""

        if self.mode == "live":
            self.set_interval(0.2, self.refresh_logs)
        else:
            self.load_search_results()

    def refresh_logs(self):

         while True:

            try:
                entry = log_queue.get_nowait()

            except Empty:
                break

            self.history.append(entry)

            if self.filter_text in entry["text"].casefold():
                self.log_widget.write(
                    f"{entry['server']} | {entry['text']}"
                )


    def on_input_changed(self, event: Input.Changed) -> None:

        self.filter_text = event.value.casefold()

        self.redraw_logs()


    def redraw_logs(self):

        self.log_widget.clear()

        for entry in self.history:

            if self.filter_text in entry["text"].casefold():

                self.log_widget.write(
                    f"{entry['server']} | {entry['text']}"
                )

    def load_search_results(self):

        for entry in self.search_results:

            self.history.append(entry)

            self.log_widget.write(
                f"{entry['server']} | "
                f"{entry['file']}:{entry['line']} | "
                f"{entry['text']}"
            )

if __name__ == "__main__":
    LogViewer().run()
