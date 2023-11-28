import socket 
import select
import sys

def main():
    try:
        print("working")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("localhost", 12345))

            
    except OSError as e:
        print(e)
    except KeyboardInterrupt:
        sock.close()






if __name__ == "__main__":
    main()
