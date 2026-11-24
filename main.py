#!/usr/bin/env python3
"""One Line of Earned Pride — make.fun bounty u-mang-one-line-of-earned-pride-a0138557.

Writes one line of quiet, earned pride to $MAKEFUN_OUTPUT_DIR/entry.txt
(falling back to /output when the variable is unset), then validates the
written file and reads it back to confirm it matches.

The line: a grandmother who spent her life signing with an X finally writes
her whole name at the bottom of her first letter — and underlines it twice.
No trophy, no podium, no speech; the pride is in the gesture.

Stdlib only, no network, no arguments. Deterministic: the same bytes every run.
"""

import os
import sys

LINE = (
    "After a lifetime of signing with an X, my grandmother wrote her whole "
    "name at the bottom of her first letter, slowly, and underlined it twice."
)


def validate(text):
    """Check the line against the bounty gate: one line, 1-240 chars."""
    if not isinstance(text, str):
        raise ValueError("entry is not text")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be exactly one line")
    if not (1 <= len(text) <= 240):
        raise ValueError("entry must be 1 to 240 characters, got %d" % len(text))
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    return True


def main():
    try:
        validate(LINE)
        out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
        os.makedirs(out_dir, exist_ok=True)
        path = os.path.join(out_dir, "entry.txt")
        data = LINE.encode("utf-8")
        with open(path, "wb") as f:
            f.write(data)
        with open(path, "rb") as f:
            written = f.read()
        if written != data:
            print("Error: read-back mismatch, entry.txt does not match the line",
                  file=sys.stderr)
            return 1
        decoded = written.decode("utf-8")
        validate(decoded)
    except (ValueError, OSError) as exc:
        print("Error: %s" % exc, file=sys.stderr)
        return 1
    print("Wrote %s (%d characters, %d bytes)" % (path, len(decoded), len(written)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
