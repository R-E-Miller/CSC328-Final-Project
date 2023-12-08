#!/usr/bin/env python3
import socket
import select
import sys
import shared as sh
import threading

#JUST TO GET THIS TO WORK I AM ADDING A PLACEHOLDER FOR PROTO
proto = ''
running = True

def reader_thread(sock):
    global running
    while running:
        myConnection = select.select([sock], [], [], 0)
        if myConnection:
            nick, message, proto = sh.read_message(sock)
            if message == "Connection closed":
                break
            print(f"{nick} said {message}")

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
            serverName, hello_message, proto = sh.read_message(sock)
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
                    proto = 'verify' 
                    sh.send_message(sock, nickname, None, proto)
                    serverName, response, proto = sh.read_message(sock)
                    if response == "READY":
                        print(response)
                        break
                    elif response == "RETRY":
                        print(response)
                    else:
                        print("Error: Unexpected response from server!")
                        continue
            read_Thread = threading.Thread(target=reader_thread, args=[sock])
            read_Thread.start()
            while True:
                myMessage = input()
                sh.send_message(sock, myMessage, nickname, "broadcast")

        except KeyboardInterrupt:
            running = False
            proto = "goodbye"
            sh.send_message(sock, "BYE", nickname, proto)
            read_Thread.join()
            sock.close()
            print("Disconnected from server.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            sock.close()

if __name__ == "__main__":
    main()
