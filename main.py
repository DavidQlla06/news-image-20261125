#!/usr/bin/env python3
"""news-image-20261125 entrypoint.

Builds the day's front page with generate.py and drops the finished
PNG at /output/entry.png. Everything the picture shows comes from
stories.json, so the program needs no network and no clock, and
running it twice writes the same bytes twice.
"""
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
OUT_DIR = Path("/output")


def build():
    subprocess.run([sys.executable, str(ROOT / "generate.py")], check=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ROOT / "entry.png", OUT_DIR / "entry.png")


if __name__ == "__main__":
    build()
    print("wrote /output/entry.png")
