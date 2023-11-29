# R-E Miller (IT), Matthew Hill (CS), Elliot Swan (CS)
import socket 
import select
import sys
import json

def check_nick(s, storedname):
    #read nickname from the client
    store = s.recv()
    nick = json.load(store)
    print(nick)

    # check nickname if nickname is taken 
    #reply back with either approved name or already taken
    #


def main():
    nickname = []
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
                    #check_nick(s, nickname )
                    verify_name(connection)
            
    except OSError as e:
        print(e)
    except KeyboardInterrupt:
        socket.close()



def verify_name(connection):
    connection.sendall(b"HELLO")
    nick = connection.read(1024)
    print(nick)
    return(connection, nick)



if __name__ == "__main__":
    main()
