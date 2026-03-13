import os

def file_state(path: str) -> dict:
    """Return a minimal state snapshot of a file."""
    try:
        st = os.stat(path)
    except FileNotFoundError:
        return {"exists": False, "size": None, "mtime": None}

    return {
        "exists": True,
        "size": st.st_size,     # bytes
        "mtime": st.st_mtime,   # last modification time (float timestamp)
    }
def collect_dir_stats(root: str) -> dict:
    """
    Walk a directory tree and collect simple aggregate stats.

    Returns a dict with:
      - total_files: number of regular files
      - total_dirs: number of directories (including root)
      - total_size: sum of file sizes in bytes
      - newest_mtime: latest modification time among files (or None)
      - oldest_mtime: earliest modification time among files (or None)
    """
    total_files = 0
    total_dirs = 0
    total_size = 0
    newest_mtime = None
    oldest_mtime = None

    for dirpath, dirnames, filenames in os.walk(root):
        total_dirs += 1

        for name in filenames:
            path = os.path.join(dirpath, name)
            state = file_state(path)
            if not state["exists"]:
                continue

            total_files += 1
            size = state["size"]
            mtime = state["mtime"]

            if size is not None:
                total_size += size

            if mtime is not None:
                if newest_mtime is None or mtime > newest_mtime:
                    newest_mtime = mtime
                if oldest_mtime is None or mtime < oldest_mtime:
                    oldest_mtime = mtime

    return {
        "total_files": total_files,
        "total_dirs": total_dirs,
        "total_size": total_size,
        "newest_mtime": newest_mtime,
        "oldest_mtime": oldest_mtime,
    }
