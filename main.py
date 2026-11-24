#!/usr/bin/env python3
"""news-image-20261123 — entrypoint.

Copies the pre-rendered front page (entry.png, drawn by draw.py in
this repository) to /output/entry.png. Standard library only: no
network, no randomness, no image libraries. Deterministic: two runs
write byte-identical files.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    # Copy only: the grader runs this program with no network, and
    # it must write byte-identical output on every run.
    src = os.path.join(HERE, "entry.png")
    # The grader sandbox sets MAKEFUN_OUTPUT_DIR; fall back to /output.
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    os.umask(0o022)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    os.chmod(dst, 0o644)
    return 0


if __name__ == "__main__":
    sys.exit(main())
