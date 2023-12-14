#!/usr/bin/env python3
###############################################################################################
# R-E Miller (IT), Matthew Hill (CS), Elliot Swan (CS)
# R-E Miller (IT), Matthew Hill (CS), Elliot Swan (CS)
# Author: Matthew Hill, Elliot Swan, R-E Miller
# Major: Computer Science and IT
# Creation Date: November 23, 2023
# Due Date: December 14, 2023
# Course: CSC328
# Professor Name: Dr. Schwesinger
# Assignment: Final
# Filename: server.py
# Purpose: The purpose of this file is to create a chat server using sockets.
# Multiple clients(up to 10) are able to connect to the server and chat with one another.
# All messages are sent to all clients, and messages are sent when clients leave and the server
# gracefully shuts down.
###############################################################################################
import socket 
import select
import sys
#import json
import shared as sh
import time
from datetime import datetime

###############################################################################################
# Function Name: broadcast
# Description: Send a message from one client or the server to all clients
# Parameters: string nick - the name of the person sending the message - input
#             string message - the message that the client is sending to other clients - input
#             string proto - what step the client is at(either verify, broadcast, goodbye) - input
#             array connectionList - all of the connected clients - input
###############################################################################################
def broadcast(nick, message, proto, connectionList):
    print(f"{nick} : {message}")
    for connection in connectionList:
        sh.send_message(connection, message, nick, proto)

###############################################################################################
# Function Name: log_mess
# Description: logs when clients connect and the messages they send.
# Parameters: string nick - the name of the person sending the message - input
#             string message - the message that the client is sending to other clients - input
#             string proto - what step the client is at(either verify, broadcast, goodbye) - input
#             FILE Object file_log - the file where the messages are being stored to - input/output
###############################################################################################
def log_mess(nick, message, proto, file_log):
    print(f"{nick}: {message}: {datetime.now()}", file = file_log, flush = True )

###############################################################################################
# Function Name: send_hello
# Description: Send a message to the client to confirm connection
# Parameters: File Descriptor s - the socket file descriptor - input
###############################################################################################
def send_hello(s):
    world = "HELLO"
    name = "SERVER"
    proto = 'connect'
    sh.send_message(s,world, name, proto)

###############################################################################################
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
###############################################################################################
def proto_handle(nick, message, proto, connectionList, readySock, nickname, file_log, connectioninfo, connection, myNick, myConnectionsSetup):
    match proto:
        case "verify":
            if message not in nickname:
                sh.send_message(readySock, "READY", myNick, 'ready')
                nickname.append(message)
                print(f"{datetime.now()}: {connectioninfo[connection][0]}: {message} ", file = file_log, flush = True)
            else: 
                sh.send_message(readySock, "RETRY", myNick, 'retry')
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

###############################################################################################
# Function Name: main
# Description:  The main function creates the server using sockets. It creates a socket to 
#                listen and allows for up to 10 clients to connect to the server. Then
#                select is used to handle all of the different clients connecting to the server.
#                Once connected the client chooses a unique nickname and are able to then send messages
#                to the other connected clients. The server stores when they connected and their
#                IP address as well as all of the messages sent in the server with time logs.
#                The server gracefully closes and also lets other clients know when someone leaves.
# Parameters: none
# Much of the basics of setting of a socket was described from the python library for sockets
# This was also presented in class
###############################################################################################
def main():
    nickname = ['SERVER']
    myNick = "SERVER"
    port = int(sys.argv[1])
    host = ''
    if not (10000 <= port <= 65535):
        print("Port number not available")
        sys.exit(-1)
    try:
        file_log = open("server_log.txt", 'a')
        print("file opened", file = file_log, flush = True)
        print(f"trial {datetime.now()}", file = file_log, flush = True )
        with socket.socket() as s:
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
                else:
                    for readySock in myConnections:
                        #This only will go off if we need to accept a connection and say hello
                        if readySock == s:
                            connection, addr = s.accept()
                            print(f"Got connection from {addr}")
                            connectioninfo[connection] = addr
                            connectionList.append(connection)
                            myConnectionsSetup.append(connection)
                            #print(len(connectionList))
                            send_hello(connection)
                        if readySock != s:
                            #print("READING FROM CLIENT")
                            nick, message, proto = sh.read_message(readySock)
                            proto_handle(nick, message, proto, connectionList, readySock, nickname, file_log, connectioninfo, connection, myNick, myConnectionsSetup)

            
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
