#!/usr/bin/env python3
"""Entrypoint for the news-image-20261125 submission.

The finished front page already ships in this repo as entry.png, so
all this program does is put a copy of it where the grader looks
for it. It does no image work on purpose: no regeneration, no
extra process, nothing beyond the standard library, and no network.
That keeps the grade run as short and as hard to break as possible.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote " + dst)


if __name__ == "__main__":
    main()
