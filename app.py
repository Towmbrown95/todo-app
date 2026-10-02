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


def save_tasks():
    TASKS_FILE.write_text(json.dumps(tasks, indent=2))


tasks = load_tasks()

def show_tasks():
    if not tasks:
        print("No tasks yet!")
    for i, task in enumerate(tasks, start=1):
        print(f"{i}. {task}")

while True:
    print("\n1) Add task  2) View tasks  3) Remove task  4) Quit")
    choice = input("Choose: ")

    if choice == "1":
        task = input("Task: ").strip()
        if task:
            tasks.append(task)
            save_tasks()
        else:
            print("Task can't be empty.")
    elif choice == "2":
        show_tasks()
    elif choice == "3":
        show_tasks()
        num = input("Number to remove: ")
        if num.isdigit() and 1 <= int(num) <= len(tasks):
            print(f"Removed: {tasks.pop(int(num) - 1)}")
            save_tasks()
        else:
            print("Invalid number.")
    elif choice == "4":
        print("Bye!")
        break
    else:
        print("Please choose 1-4.")
