from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Header, Footer, Input, RichLog
from queue import Empty
from log_reader import log_queue

class LogViewer(App):

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

        self.set_interval(0.2, self.refresh_logs)

    def refresh_logs(self):

         while True:

            try:
                entry = log_queue.get_nowait()

            except Empty:
                break

            self.history.append(entry)

            if self.filter_text in entry["text"].lower():
                self.log_widget.write(
                    f"{entry['server']} | {entry['text']}"
                )


    def on_input_changed(self, event):

        self.filter_text = event.value.lower()

        self.redraw_logs()


    def redraw_logs(self):

        self.log_widget.clear()

        for entry in self.history:

            if self.filter_text in entry["text"].lower():

                self.log_widget.write(
                    f"{entry['server']} | {entry['text']}"
                )


if __name__ == "__main__":
    LogViewer().run()