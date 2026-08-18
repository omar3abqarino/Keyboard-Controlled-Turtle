# Source - https://stackoverflow.com/a/69750097
# Posted by ilon
# Retrieved 2026-08-18, License - CC BY-SA 4.0

from sshkeyboard import listen_keyboard

def press(key):
    print(f"'{key}' pressed")

def release(key):
    print(f"'{key}' released")

listen_keyboard(
    on_press=press,
    on_release=release,
)
