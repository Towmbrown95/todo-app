import json
from datetime import date
from pathlib import Path

TASKS_FILE = Path(__file__).parent / "tasks.json"
CHORES_FILE = Path(__file__).parent / "chores.json"
CHORE_STATUS_FILE = Path(__file__).parent / "chore_status.json"
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def load_tasks():
    if not TASKS_FILE.exists():
        return []
    try:
        tasks = json.loads(TASKS_FILE.read_text())
    except json.JSONDecodeError:
        print("Warning: tasks.json is corrupted, starting with an empty list.")
        return []
    # Older files stored plain strings; upgrade them to task dicts.
    return [{"text": t, "done": False} if isinstance(t, str) else t for t in tasks]


def save_tasks(tasks):
    TASKS_FILE.write_text(json.dumps(tasks, indent=2))


def load_chores():
    """The weekly chore schedule, as {day: [chore, ...]} in Monday-Sunday order."""
    schedule = json.loads(CHORES_FILE.read_text()) if CHORES_FILE.exists() else {}
    return {day: schedule.get(day, []) for day in DAYS}


def current_week():
    year, week, _ = date.today().isocalendar()
    return f"{year}-W{week:02d}"


def load_chore_status():
    """Which chores are done this week. Resets automatically when a new week starts."""
    try:
        status = json.loads(CHORE_STATUS_FILE.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        status = {}
    if status.get("week") != current_week():
        return {"week": current_week(), "done": []}
    return status


def save_chore_status(status):
    CHORE_STATUS_FILE.write_text(json.dumps(status, indent=2))
