# Grepzy

One search. Every server.

Grepzy is a small CLI/TUI tool for anyone who's tired of SSHing into three
different servers, opening the same log file three times, and running the
same `grep` three times to answer one question. It replaces that with one
command that talks to every server at once.

It has two modes:

- **Live** — tails logs from multiple servers in real time, merged into a
  single scrolling view, tagged by server.
- **Search** — greps across a log directory on every configured server at
  once and shows you every match, with the source server and file next to
  each line.

Sessions (named groups of servers) are saved locally so you're not
re-entering hosts and credentials every time.

## Why this exists

At my day job, checking a production issue across two servers meant: SSH
into server A, `cd` into the log folder, `grep` for the transaction ID,
repeat for server B, then manually compare. Grepzy does all of that in one
pass.

## Requirements

- Python 3.9+
- `paramiko`
- `textual`

```bash
pip install -r requirements.txt
```

## Setup

Define your servers in `sessions.json`:

```json
{
  "servlet": {
    "servers": [
      {
        "name": "server1",
        "host": "12.34.56.78",
        "username": "username",
        "log": "/logs/messages.log"
      }
    ]
  }
}
```

Each top-level key is a session name — a group of servers you'll usually
want to look at together. You'll be prompted for each server's password
when you run a session; nothing is stored on disk.

## Usage

```bash
python main.py
```

```
==========================================
              GREPZY
      One Search. Every Server.
==========================================
1. Live Monitor
2. Search Logs
3. Sessions
4. Exit
```

**Live Monitor** — pick a session, enter each server's password once, and
watch logs stream in from all of them merged into one view.

**Search Logs** — pick a session, type what you're looking for, and it
greps that session's servers in parallel and shows every match with its
source server and file.

**Sessions** — create, list, or delete saved server groups.

## How it works

Live mode opens an SSH connection per server and streams `stdout` into a
shared queue that the viewer polls and renders. Search mode opens a
short-lived SSH connection per server, runs a `grep -R` scoped to that
server's log directory, and aggregates the results before handing them to
the same viewer in a static view. Both modes render through the same
Textual-based `LogViewer`, just fed differently.

## Known limitations

- Doesn't scale past a handful of servers — search mode walks the
  filesystem live on every query instead of indexing anything, so it's
  fine for a small fleet and not a replacement for a real log aggregator
  at higher server counts.
- Password-based auth only, entered per run. Works fine for personal use;
  key-based auth would be the next thing to add for anything more serious.
- No output export yet (e.g. saving search results to a file).

## Ideas for later

- SSH key auth instead of typed passwords
- Export search results to CSV/JSON
- Regex support in search mode, not just plain substring grep
- Config for custom search directories per server instead of one shared path
