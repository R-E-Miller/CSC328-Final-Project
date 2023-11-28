# R-E Miller (IT), Matthew Hill (CS), Elliot Swan (CS)
import socket 
import select
import sys

def main():
    try:
        print("working")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("", 12345))
        sock.listen()
        while True:
            connection, info = sock.accept()
            print("Got connection", info)
            
    except OSError as e:
        print(e)
    except KeyboardInterrupt:
        sock.close()






if __name__ == "__main__":
    main()
