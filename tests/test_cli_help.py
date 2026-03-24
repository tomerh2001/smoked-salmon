import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

COMMANDS: list[tuple[str, ...]] = [
    (),
    ("check",),
    ("check", "integrity"),
    ("check", "log"),
    ("check", "mqa"),
    ("check", "upconv"),
    ("checkconf",),
    ("checkspecs",),
    ("compress",),
    ("descgen",),
    ("downconv",),
    ("health",),
    ("images",),
    ("images", "up"),
    ("meta",),
    ("metas",),
    ("play",),
    ("play", "despacito"),
    ("specs",),
    ("tag",),
    ("transcode",),
    ("up",),
]


def test_cli_help_commands_return_success() -> None:
    env = os.environ.copy()
    existing_pythonpath = env.get("PYTHONPATH")
    env["PYTHONPATH"] = str(SRC) if not existing_pythonpath else os.pathsep.join((str(SRC), existing_pythonpath))
    failures: list[str] = []

    for args in COMMANDS:
        result = subprocess.run(
            [sys.executable, "-m", "salmon.run", *args, "--help"],
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            command = "salmon" if not args else f"salmon {' '.join(args)}"
            failure_output = result.stderr or result.stdout
            failures.append(f"{command}: {failure_output}")

    assert not failures, "\n\n".join(failures)
