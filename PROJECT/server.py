# R-E Miller (IT), Matthew Hill (CS), Elliot Swan (CS)
import socket 
import select
import sys

#testing version control
def main():
    port = int(sys.argv[1])
    host = sys.argv[2]
    if not (10000 <= port <= 65535):
        print("Port number not available")
        sys.exit(-1)
    try:
        print("working")
        with socket.socket() as s:
            #s.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((host, port))
            s.listen(10)
            print("\n Server listening")
            while True:
                connection, _ = s.accept()
                with connection:
                    print("Got connection", info)
            
    except OSError as e:
        print(e)
    except KeyboardInterrupt:
        sock.close()






if __name__ == "__main__":
    main()
