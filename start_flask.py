#!/usr/bin/env python
"""Daemonize the Flask app so it isn't suspended by terminal job control."""
import os, sys

pid = os.fork()
if pid > 0:
    print(f"Flask daemon PID: {pid}")
    sys.exit(0)

os.setsid()

pid2 = os.fork()
if pid2 > 0:
    sys.exit(0)

with open("/dev/null", "r") as f:
    os.dup2(f.fileno(), 0)
with open("/tmp/flask_erica.log", "a") as f:
    os.dup2(f.fileno(), 1)
    os.dup2(f.fileno(), 2)

os.chdir("/Users/aadeechheda/Projects/HackUNCP/erica")
sys.path.insert(0, "/Users/aadeechheda/Projects/HackUNCP/erica")

os.environ.setdefault("FLASK_ENV", "development")

from app.main import app
app.run(host="0.0.0.0", port=8000, use_reloader=False, debug=False)
