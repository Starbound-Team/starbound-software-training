Daedalus-2199: ship's log
=========================

The ship's log is where you read the missions and check your answers. Part b
of a mission unlocks once part a is solved. It needs Python 3.11 or newer.
From this folder:

  Linux / macOS                      Windows
  python3 -m venv .venv              py -m venv .venv
  source .venv/bin/activate          .venv\Scripts\activate
  pip install -r requirements.txt    pip install -r requirements.txt
  python shiplog.py                  python shiplog.py

Use a terminal with a dark background and Unicode support (on Windows, the
Windows Terminal app rather than the old cmd window).

Arrow keys select, enter opens, esc goes back, q quits. Your progress is saved
in progress.json; delete it to start over.

Your puzzle inputs are in input/. The mission texts are also in
missions_text_plain/ as PDF (and Markdown in md/), in case you'd rather read
them outside the ship's log.
