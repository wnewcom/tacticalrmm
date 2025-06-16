"""Simple installer for the tickets module."""

import subprocess
import sys


def main() -> None:
    """Run migrations for the tickets app and collectstatic."""
    cmds = [
        [
            sys.executable,
            "api/tacticalrmm/manage.py",
            "makemigrations",
            "tickets",
        ],
        [
            sys.executable,
            "api/tacticalrmm/manage.py",
            "makemigrations",
            "core",
        ],
        [sys.executable, "api/tacticalrmm/manage.py", "migrate"],
        [
            sys.executable,
            "api/tacticalrmm/manage.py",
            "collectstatic",
            "--noinput",
        ],
    ]
    for cmd in cmds:
        subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()
