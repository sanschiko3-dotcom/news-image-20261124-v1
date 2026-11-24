"""News-image entry: copy the rendered front page to /output/entry.png.

The image (entry.png, drawn at build time by render.py with Pillow) is
shipped in this repository; this program only copies it, so the grader
run needs no network and no third-party packages -- standard library
only. Output path is /output/entry.png, or $MAKEFUN_OUTPUT_DIR when set
(for local runs), matching the kit starter convention.
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "entry.png"


def main() -> None:
    # entry.png ships in this repo; fail loudly if it is missing rather
    # than writing a partial output.
    if not SRC.is_file():
        raise FileNotFoundError(f"missing shipped image: {SRC}")
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SRC, out_dir / "entry.png")


if __name__ == "__main__":
    main()
