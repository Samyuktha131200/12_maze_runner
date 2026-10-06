import bisect
import json
import math
import os

MAX_ENTRIES = 5
# Stored next to main.py so it is found no matter where the game is launched from.
LEADERBOARD_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "leaderboard.json"
)


def _is_valid_time(t):
    return (isinstance(t, (int, float)) and not isinstance(t, bool)
            and math.isfinite(t) and t > 0)


def load_leaderboard(path=LEADERBOARD_PATH):
    """Return the saved times, fastest first (max 5).
    A missing, unreadable or corrupted file just gives an empty leaderboard."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError):
        return []
    if not isinstance(data, list):
        return []
    return sorted(float(t) for t in data if _is_valid_time(t))[:MAX_ENTRIES]


def save_leaderboard(times, path=LEADERBOARD_PATH):
    """Write the times to disk. Returns False (instead of crashing) if it fails."""
    tmp = path + ".tmp"
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(times, f, indent=2)
        os.replace(tmp, path)
        return True
    except OSError:
        return False


def add_time(times, new_time):
    """Insert new_time into the sorted leaderboard and keep only the top 5.
    Returns (new_times, rank) where rank is the 0-based position of the new
    time, or None if it did not make the top 5. On a tie, the older time ranks first."""
    if not _is_valid_time(new_time):
        return list(times), None
    new_time = round(float(new_time), 2)
    rank = bisect.bisect_right(times, new_time)
    if rank >= MAX_ENTRIES:
        return list(times), None
    updated = list(times)
    updated.insert(rank, new_time)
    return updated[:MAX_ENTRIES], rank
