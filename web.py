from datetime import date

from flask import Flask, redirect, render_template, request, url_for

from storage import DAYS, load_chore_status, load_chores, load_tasks, save_chore_status, save_tasks

app = Flask(__name__)


@app.route("/")
def index():
    chores = load_chores()
    status = load_chore_status()
    return render_template(
        "index.html",
        tasks=load_tasks(),
        chores=chores,
        chores_done=set(status["done"]),
        chore_total=sum(len(c) for c in chores.values()),
        today=DAYS[date.today().weekday()],
    )


@app.route("/chores/toggle", methods=["POST"])
def toggle_chore():
    key = f"{request.form['day']}|{request.form['chore']}"
    status = load_chore_status()
    if key in status["done"]:
        status["done"].remove(key)
    else:
        status["done"].append(key)
    save_chore_status(status)
    return redirect(url_for("index"))


@app.route("/add", methods=["POST"])
def add():
    text = request.form.get("task", "").strip()
    if text:
        tasks = load_tasks()
        tasks.append({"text": text, "done": False})
        save_tasks(tasks)
    return redirect(url_for("index"))


@app.route("/toggle/<int:index>", methods=["POST"])
def toggle(index):
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        tasks[index]["done"] = not tasks[index]["done"]
        save_tasks(tasks)
    return redirect(url_for("index"))


@app.route("/remove/<int:index>", methods=["POST"])
def remove(index):
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        tasks.pop(index)
        save_tasks(tasks)
    return redirect(url_for("index"))


if __name__ == "__main__":
    # Port 5000 is taken by AirPlay Receiver on macOS, so use 5001.
    app.run(debug=True, port=5001)
