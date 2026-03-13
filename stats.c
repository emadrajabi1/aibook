import os
import stat
from typing import Optional, Dict, Any

def file_state(path: str) -> Dict[str, Any]:
    """
    Return a snapshot of the 'state' of a filesystem path.
    """
    if not os.path.exists(path):
        return {
            "exists": False,
            "is_file": False,
            "is_dir": False,
            "size": None,
            "mode": None,
            "mtime": None,
            "ctime": None,
            "path": path,
        }

    st = os.stat(path, follow_symlinks=True)

    return {
        "exists": True,
        "is_file": os.path.isfile(path),
        "is_dir": os.path.isdir(path),
        "size": st.st_size,           # bytes
        "mode": stat.S_IMODE(st.st_mode),  # Unix permission bits
        "mtime": st.st_mtime,         # last modification time (timestamp)
        "ctime": st.st_ctime,         # metadata change / creation (platform-dependent)
        "path": path,
    }

# Example usage:
if __name__ == "__main__":
    state = file_state("some/file.txt")
    print(state)

    