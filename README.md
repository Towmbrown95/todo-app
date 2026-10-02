# To-Do App
A simple to-do list written in Python, with a command-line version and a web version.

Tasks are saved to `tasks.json`, and both versions share it.

## Setup
```
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Run the web app
```
.venv/bin/python web.py
```
Then open http://localhost:5001.

## Run the command-line app
```
python3 app.py
```
