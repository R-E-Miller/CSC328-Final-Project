import socket
import select
import sys

def send_message(sock, message):
    """Send a message to the server."""
    try:
        sock.sendall(message.encode())
    except socket.error as e:
        print(f"Error sending message: {e}")

def main():
    if len(sys.argv) != 3:
        print("Usage: python client.py <host> <port>")
        sys.exit()

    host, port = sys.argv[1], int(sys.argv[2])

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((host, port))
            print("Connected to the server.")

            # Handle nickname setup
            while True:
                nickname = input("Enter your nickname: ").strip()
                if nickname:
                    send_message(sock, f"NICK:{nickname}")
                    response = sock.recv(1024).decode()
                    if response == "READY":
                        print("Nickname accepted.")
                        break
                    elif response == "RETRY":
                        print("Nickname already in use, please try a different one.")
                    else:
                        print("Unexpected response from server.")
                        continue

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((host, port))
            print("Connected to the server.")

            while True:
                sockets_list = [sys.stdin, sock]
                read_sockets, _, _ = select.select(sockets_list, [], [])

                for notified_socket in read_sockets:
                    if notified_socket == sock:
                        message = sock.recv(1024)
                        if not message:
                            print("Disconnected from server.")
                            sys.exit()
                        else:
                            print(message.decode())
                    else:
                        message = sys.stdin.readline().strip()
                        if message:
                            send_message(sock, message)

    except KeyboardInterrupt:
        send_message(sock, "BYE")
        print("Disconnected from the server.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    main()
