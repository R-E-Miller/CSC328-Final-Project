#!/usr/bin/env python3
# R-E Miller (IT), Matthew Hill (CS), Elliot Swan (CS)
# R-E Miller (IT), Matthew Hill (CS), Elliot Swan (CS)
# Author: Matthew Hill, Elliot Swan, R-E Miller
# Major: Computer Science and IT
# Creation Date: November 23, 2023
# Due Date: December 14, 2023
# Course: csc328
# Professor Name: Dr. Schwesinger
# Assignment: Final
# Filename: server.py
# Purpose: The purpose of this file is to create a chat server using sockets.
# Multiple clients(up to 10) are able to connect to the server and chat with one another.
# All messages are sent to all cleints, and messages are sent when clients leave and the server
# gracefully shuts down.
import socket 
import select
import sys
#import json
import shared as sh
import time
from datetime import datetime

# Function Name: broadcast
# Description: Send a message from one client or the server to all cleints
# Parameters: string nick - the name of the person sending the message - input
#             string message - the message that the client is sending to other clients - input
#             string proto - what step the client is at(either verify, broadcast, goodbye) - input
#             array connectionList - all of the connected clients - input
def broadcast(nick, message, proto, connectionList):
    print(f"{nick} : {message}")
    for connection in connectionList:
        sh.send_message(connection, message, nick, proto)

# Function Name: log_mess
# Description: logs when clients connect and the messages they send.
# Parameters: string nick - the name of the person sending the message - input
#             string message - the message that the client is sending to other clients - input
#             string proto - what step the client is at(either verify, broadcast, goodbye) - input
#             FILE Object file_log - the file where the messages are being stored to - input/output
def log_mess(nick, message, proto, file_log):
    print(f"{nick}: {message}: {datetime.now()}", file = file_log, flush = True )

# Function Name: send_hello
# Description: Send a message to the client to confirm connection
# Parameters: File Descriptor s - the socket file descriptor - input
def send_hello(s):
    world = "HELLO"
    name = "SERVER"
    proto = 'connect'
    sh.send_message(s,world, name, proto)

# Function Name: proto_handle
# Description: This function handles the different cases that proto can take on.
# Parameters: string nick - the name of the person sending the message - input
#             string message - the message that the client is sending to other clients - input
#             string proto - what step the client is at(either verify, broadcast, goodbye) - input
#             array connectionList - all of the connected clients - input
#             File descriptor readysock - all of the sockets ready for reading - input
#             array strings nickname - the names of all of the taken names ("SERVER" is in by default) - input
#             FILE Object file_log - the file where message are stored - input/output
#             dictionary connectioninfo - the dictionary storing each users IP address - input
#             key connection - the key to the dictionary connection info to obtain the IP address of the specific user - input
#             string myNick - the nickname of the server "SERVER" which is taken by default - input
#             array File descriptors myConnectionsSetup - all of the sockets that the clients are connected to - input
def proto_handle(nick, message, proto, connectionList, readySock, nickname, file_log, connectioninfo, connection, myNick, myConnectionsSetup):
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
            disc = f"{nick} disconnected"
            broadcast(myNick, disc, proto, connectionList)
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
                            proto_handle(nick, message, proto, connectionList, readySock, nickname, file_log, connectioninfo, connection, myNick, myConnectionsSetup)
                            #match proto:
                            #    case "verify":
                            #        if message not in nickname:
                            #            sh.send_message(readySock, "READY", myNick, 'verify')
                            #            nickname.append(message)
                            #            print(f"{datetime.now()}: {connectioninfo[connection][0]}: {message} ", file = file_log, flush = True)
                            #        else: 
                            #            sh.send_message(readySock, "RETRY", myNick, 'verify')
                            #    case "broadcast":
                            #        print("Broadcasting")
                            #        broadcast(nick, message, proto, connectionList)
                            #        log_mess(nick, message, proto, file_log)
                            #    case "goodbye":
                            #        print(f"{nick} is disconnecting")
                            #        myConnectionsSetup.remove(readySock)
                            #        connectionList.remove(readySock)
                            #        nickname.remove(nick)
                            #        readySock.close()
                            #    case None:
                            #        myConnectionsSetup.remove(readySock)
                            #        connectionList.remove(readySock)
                            #        #NOTE: we need to make a dictionary in case something like this ever happens, map connections to the name
                                    #nickname.remove(nick)
                            #        readySock.close()
            
    except OSError as e:
        print(e)
    except KeyboardInterrupt:
        ser_end = "Server Shutting down in 5 seconds"
        proto = "shutdown"
        broadcast(myNick, ser_end, proto, connectionList)
        time.sleep(5)
        for connection in connectionList:
            connection.close()
        s.close()

if __name__ == "__main__":
    main()
