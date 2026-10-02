import json
from pathlib import Path

TASKS_FILE = Path(__file__).parent / "tasks.json"


def load_tasks():
    if not TASKS_FILE.exists():
        return []
    try:
        return json.loads(TASKS_FILE.read_text())
    except json.JSONDecodeError:
        print("Warning: tasks.json is corrupted, starting with an empty list.")
        return []


def save_tasks(tasks):
    TASKS_FILE.write_text(json.dumps(tasks, indent=2))
