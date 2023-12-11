# R-E Miller (IT), Matthew Hill (CS), Elliot Swan (CS)
import socket 
import select
import sys
import json
import shared as sh
import time
from datetime import datetime

def broadcast(nick, message, proto, connectionList):
    print(f"{nick} said {message}")
    for connection in connectionList:
        sh.send_message(connection, message, nick, proto)

def log_mess(nick, message, proto, file_log):
    print(f"{nick}: {message}: {datetime.now()}", file = file_log, flush = True )


def send_hello(s):
    world = "HELLO"
    name = "SERVER"
    proto = ''
    sh.send_message(s,world, name, proto)

def main():
    nickname = ['SERVER']
    myNick = "SERVER"
    port = int(sys.argv[2])
    host = sys.argv[1]
    if not (10000 <= port <= 65535):
        print("Port number not available")
        sys.exit(-1)
    try:
        file_log = open("server_log.txt", 'a')
        print("file opened", file = file_log, flush = True)
        print(f"trial {datetime.now()}", file = file_log, flush = True )
        print("working")
        with socket.socket() as s:
            #s.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((host, port))
            s.listen(10)
            print("\n Server listening")
            myConnectionsSetup = [s]
            connectionList = []
            connectioninfo = {}

            while True:
                myConnections, _,_ = select.select(myConnectionsSetup, [], [], 0)
                if myConnections == []:
                    pass
                    #Feel free to comment this out I feel it gives a pretty good understanding of what is actually happening
                    #print("Never blocked")
                    #time.sleep(1)
                else:
                    for readySock in myConnections:
                        #This only will go off if we need to accept a connection and say hello
                        if readySock == s:
                            connection, addr = s.accept()
                            print(f"Got connection from {addr}")
                            connectioninfo[connection] = addr
                            connectionList.append(connection)
                            myConnectionsSetup.append(connection)
                            print(len(connectionList))
                            send_hello(connection)
                        #Otherwise someone else sent something and it can be processed or broadcast. 
                        if readySock != s:
                            print("READING FROM CLIENT")
                            nick, message, proto = sh.read_message(readySock)
                            match proto:
                                case "verify":
                                    if message not in nickname:
                                        sh.send_message(readySock, "READY", myNick, 'verify')
                                        nickname.append(message)
                                        print(f"{datetime.now()}: {connectioninfo[connection][0]}: {message} ", file = file_log, flush = True)
                                    else: 
                                        sh.send_message(readySock, "RETRY", myNick, 'verify')
                                case "broadcast":
                                    print("Broadcasting")
                                    broadcast(nick, message, proto, connectionList)
                                    log_mess(nick, message, proto, file_log)
                                case "goodbye":
                                    print(f"{nick} is disconnecting")
                                    myConnectionsSetup.remove(readySock)
                                    connectionList.remove(readySock)
                                    nickname.remove(nick)
                                    readySock.close()
                                case None:
                                    myConnectionsSetup.remove(readySock)
                                    connectionList.remove(readySock)
                                    #NOTE: we need to make a dictionary in case something like this ever happens, map connections to the name
                                    #nickname.remove(nick)
                                    readySock.close()


            
    except OSError as e:
        print(e)
    except KeyboardInterrupt:
        ser_end = "Server Shutting down in 5 seconds"
        proto = "broadcast"
        broadcast(myNick, ser_end, proto, connectionList)
        time.sleep(5)
        s.close()

if __name__ == "__main__":
    main()
