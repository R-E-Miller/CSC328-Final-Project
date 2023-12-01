# R-E Miller (IT), Matthew Hill (CS), Elliot Swan (CS)
import socket 
import select
import sys
import json
import shared as sh
import time

def check_nick(s, storedname):
    #read nickname from the client
    bannedname = ["SERVER"]
    message = ""
    while message != "READY":
        nic,msg,proto = sh.read_message(s)
        if msg in storedname or msg in bannedname: 
            message = "RETRY"
            sh.send_message(s, message, name,proto)
            continue
        message = "READY"
        sh.send_message(s, message, name,proto)
    # check nickname if nickname is taken 
    #reply back with either approved name or already taken
    #

def send_hello(s):
    world = "HELLO"
    name = "SERVER"
    proto = ''
    sh.send_message(s,world, name, proto)

def main():
    nickname = []
    port = int(sys.argv[2])
    host = sys.argv[1]
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
            myConnectionsSetup = [s]
            myConnections, _, _ = select.select(myConnectionsSetup, [], []) 

            while True:
                myConnections, _,_ = select.select(myConnectionsSetup, [], [], 0)
                if myConnections == []:
                    #Feel free to comment this out I feel it gives a pretty good understanding of what is actually happening
                    print("Never blocked")
                    time.sleep(1)
                else:
                    for readySock in myConnections:
                        #This only will go off if we need to accept a connection and say hello
                        if readySock == s:
                            connection, addr = s.accept()
                            print(f"Got connection from {addr}")
                            myConnectionsSetup.append(connection)
                            send_hello(connection)
                        #Otherwise someone else sent something and it can be processed or broadcast. 
                        if readySock != s:
                            nick, message, proto = sh.read_message(readySock)
                            print(f'{nick} said {message}')


            
    except OSError as e:
        print(e)
    except KeyboardInterrupt:
        s.close()






if __name__ == "__main__":
    main()
