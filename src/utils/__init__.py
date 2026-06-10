"""
Shared utility functions.
"""

import os
import tempfile
from pathlib import Path
from typing import Union


def _atomic_write(path: Union[str, Path], content_bytes: bytes):
    """Write to temp file then atomically replace — prevents partial writes."""
    path = Path(path)
    parent = path.parent
    parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(dir=str(parent))
    try:
        os.write(fd, content_bytes)
        os.close(fd)
        os.replace(tmp_path, str(path))
    except Exception:
        os.close(fd)
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise
