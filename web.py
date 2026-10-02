from flask import Flask, redirect, render_template, request, url_for

from storage import load_tasks, save_tasks

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", tasks=load_tasks())


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
