"""A simple hotkey-controlled autoclicker.

Press the toggle key (F6 by default) to start or stop clicking at the
current mouse position. Press the quit key (F7 by default) to exit.
"""
import argparse
import threading
import time

from pynput import keyboard, mouse

BUTTONS = {
    "left": mouse.Button.left,
    "right": mouse.Button.right,
    "middle": mouse.Button.middle,
}


def parse_key(name):
    """Turn a name like 'f6' or 'x' into a pynput key."""
    try:
        return keyboard.Key[name.lower()]
    except KeyError:
        if len(name) == 1:
            return keyboard.KeyCode.from_char(name.lower())
        raise argparse.ArgumentTypeError(f"unknown key: {name}")


class AutoClicker:
    def __init__(self, button, interval, max_clicks, controller=None):
        self.button = button
        self.interval = interval
        self.max_clicks = max_clicks
        self.mouse = controller or mouse.Controller()
        self.clicking = threading.Event()
        self.stopped = threading.Event()
        self.clicks = 0
        self.thread = threading.Thread(target=self._run, daemon=True)

    def start(self):
        self.thread.start()

    def toggle(self):
        if self.clicking.is_set():
            self.clicking.clear()
            print(f"Paused ({self.clicks} clicks so far).")
        else:
            self.clicking.set()
            print("Clicking...")

    def stop(self):
        self.stopped.set()
        self.clicking.set()  # wake the thread so it can exit
        self.thread.join()

    def _run(self):
        while not self.stopped.is_set():
            self.clicking.wait()
            if self.stopped.is_set():
                break
            self.mouse.click(self.button)
            self.clicks += 1
            if self.max_clicks and self.clicks >= self.max_clicks:
                self.clicking.clear()
                print(f"Reached {self.max_clicks} clicks, paused.")
                self.clicks = 0
                continue
            # Sleep in a way that reacts quickly to stop requests.
            self.stopped.wait(self.interval)


def main():
    parser = argparse.ArgumentParser(description="Hotkey-controlled autoclicker.")
    parser.add_argument("-i", "--interval", type=float, default=0.1,
                        help="seconds between clicks (default: 0.1)")
    parser.add_argument("-b", "--button", choices=BUTTONS, default="left",
                        help="mouse button to click (default: left)")
    parser.add_argument("-n", "--clicks", type=int, default=0,
                        help="pause after this many clicks; 0 means no limit")
    parser.add_argument("--toggle-key", type=parse_key, default=keyboard.Key.f6,
                        help="key that starts/stops clicking (default: f6)")
    parser.add_argument("--quit-key", type=parse_key, default=keyboard.Key.f7,
                        help="key that exits the program (default: f7)")
    args = parser.parse_args()

    if args.interval < 0.001:
        parser.error("interval must be at least 0.001 seconds")

    clicker = AutoClicker(BUTTONS[args.button], args.interval, args.clicks)
    clicker.start()

    def on_press(key):
        if key == args.toggle_key:
            clicker.toggle()
        elif key == args.quit_key:
            return False  # stops the listener

    print(f"Autoclicker ready: {args.button} click every {args.interval}s.")
    print("Press the toggle key to start/stop, the quit key to exit.")
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

    clicker.stop()
    print("Bye.")


if __name__ == "__main__":
    main()
