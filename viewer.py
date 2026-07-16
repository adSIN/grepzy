from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Header, Footer, Input, RichLog
from log_reader import logs

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

        self.log_widget = self.query_one("#logs", RichLog)

        self.last = 0

        self.filter_text = ""

        self.set_interval(0.2, self.refresh_logs)

    def refresh_logs(self):

        while self.last < len(logs):

            entry = logs[self.last]

            if self.filter_text in entry["text"].lower():


                self.log_widget.write(
                    f"{entry['server']} | {entry['text']}"
                )

            self.last += 1


    def on_input_changed(self, event):

        self.filter_text = event.value.lower()

        self.redraw_logs()


    def redraw_logs(self):

        self.log_widget.clear()
        for entry in logs:
            if self.filter_text in entry["text"].lower():

                self.log_widget.write(
                    f"{entry['server']} | {entry['text']}"
                )


if __name__ == "__main__":
    LogViewer().run()