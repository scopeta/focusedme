"""The --long-break help text must describe the long break, not the focus session."""

import os
import subprocess
import sys

REPO = os.path.join(os.path.dirname(__file__), "..")


def get_help():
    env = dict(os.environ)
    env["PYTHONPATH"] = os.pathsep.join(
        [REPO, env.get("PYTHONPATH", "")]
    ).rstrip(os.pathsep)
    return subprocess.run(
        [sys.executable, "-m", "focusedme", "--help"],
        capture_output=True,
        text=True,
        cwd=REPO,
        env=env,
    )


def test_long_break_help_mentions_long_break():
    proc = get_help()
    assert proc.returncode == 0
    assert "long break" in proc.stdout.lower()


def test_focus_session_mentioned_once():
    proc = get_help()
    assert proc.returncode == 0
    assert proc.stdout.lower().count("focus session") == 1
