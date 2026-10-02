tasks = []

def show_tasks():
    if not tasks:
        print("No tasks yet!")
    for i, task in enumerate(tasks, start=1):
        print(f"{i}. {task}")

while True:
    print("\n1) Add task  2) View tasks  3) Remove task  4) Quit")
    choice = input("Choose: ")

    if choice == "1":
        tasks.append(input("Task: "))
    elif choice == "2":
        show_tasks()
    elif choice == "3":
        show_tasks()
        num = input("Number to remove: ")
        if num.isdigit() and 1 <= int(num) <= len(tasks):
            print(f"Removed: {tasks.pop(int(num) - 1)}")
    elif choice == "4":
        print("Bye!")
        break