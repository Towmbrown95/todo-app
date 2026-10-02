from storage import load_tasks, save_tasks

tasks = load_tasks()

def show_tasks():
    if not tasks:
        print("No tasks yet!")
    for i, task in enumerate(tasks, start=1):
        mark = "x" if task["done"] else " "
        print(f"{i}. [{mark}] {task['text']}")

def pick_task(prompt):
    show_tasks()
    num = input(prompt)
    if num.isdigit() and 1 <= int(num) <= len(tasks):
        return int(num) - 1
    print("Invalid number.")
    return None

while True:
    print("\n1) Add task  2) View tasks  3) Remove task  4) Mark done/undone  5) Quit")
    choice = input("Choose: ")

    if choice == "1":
        text = input("Task: ").strip()
        if text:
            tasks.append({"text": text, "done": False})
            save_tasks(tasks)
        else:
            print("Task can't be empty.")
    elif choice == "2":
        show_tasks()
    elif choice == "3":
        i = pick_task("Number to remove: ")
        if i is not None:
            print(f"Removed: {tasks.pop(i)['text']}")
            save_tasks(tasks)
    elif choice == "4":
        i = pick_task("Number to toggle: ")
        if i is not None:
            tasks[i]["done"] = not tasks[i]["done"]
            state = "done" if tasks[i]["done"] else "not done"
            print(f"Marked {state}: {tasks[i]['text']}")
            save_tasks(tasks)
    elif choice == "5":
        print("Bye!")
        break
    else:
        print("Please choose 1-5.")
