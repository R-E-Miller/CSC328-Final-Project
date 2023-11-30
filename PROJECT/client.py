#!/usr/bin/env python3
import socket
import select
import sys
import shared as sh

def main():
    if len(sys.argv) != 3:
        print("Usage: python client.py <host> <port>")
        sys.exit()

    host, port = sys.argv[1], int(sys.argv[2])

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((host, port))
            print("Connected to the server.")

            # Wait for HELLO message from the server
            print("going to try to read from server")
            serverName, hello_message = sh.read_message(sock)
            if "HELLO" in hello_message:
                print(hello_message)
            else:
                print("Did not receive HELLO..")
                return

            # Handle nickname setup loop
            while True:
                nickname = input("Enter your nickname: ").strip()
                if nickname:
                    #send_message(sock, f"NICK:{nickname}")
                    sh.send_message(sock, nickname, None)
                    serverName, response = sh.read_message(sock)
                    if response == "READY":
                        print(response)
                        break
                    elif response == "RETRY":
                        print(response)
                    else:
                        print("Error: Unexpected response from server!")
                        continue

        except KeyboardInterrupt:
            sh.send_message(sock, "BYE", nickname)
            print("BYE")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            sock.close()

if __name__ == "__main__":
    main()
