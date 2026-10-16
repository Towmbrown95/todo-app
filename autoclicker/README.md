# Autoclicker
A small hotkey-controlled autoclicker. It clicks wherever the mouse is.

## Setup
```
python3 -m venv .venv
.venv/bin/pip install -r autoclicker/requirements.txt
```

## Run
```
.venv/bin/python autoclicker/autoclicker.py
```
- **F6** starts / pauses clicking
- **F7** quits

Options:
```
-i, --interval SECONDS   time between clicks (default 0.1)
-b, --button BUTTON      left, right or middle (default left)
-n, --clicks N           pause after N clicks (default 0 = no limit)
--toggle-key KEY         e.g. f8 or x (default f6)
--quit-key KEY           default f7
```
Example: right-click 50 times, twice a second:
```
.venv/bin/python autoclicker/autoclicker.py -b right -i 0.5 -n 50
```

## Platform notes
- **macOS:** grant your terminal Accessibility and Input Monitoring
  permission (System Settings → Privacy & Security), or clicks and hotkeys
  will be ignored.
- **Linux:** needs an X11 session; Wayland generally blocks synthetic input.
- **Windows:** works out of the box.
