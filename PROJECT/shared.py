#!/usr/bin/env python3

#################################################################################
# Author: R-E Miller, Elliot Swan, Matthew Hill                                 #
# Major: IT, CS, CS (respectively)                                              #
# Creation Date: November 23, 2023                                              #
# Due Date: December 14, 2023 @ 10AM                                            #
# Course: CSC328 Network & Secure Programming                                   #
# Professor Name: Dr. Dylan Schwesinger                                         #
# Assignment: Final Project                                                     #
# Filename: shared.py                                                           #
# Purpose: This script provides the shared functionalities between the client   #
#          and the server for a network chat application. It includes           #
#          functions for sending and reading messages in a JSON formatted       #
#          protocol, ensuring communication consistency across the network.     #
#################################################################################

import socket
import json

def send_message(connection, msg, nick, proto):
    if nick == None:
        nick = "None"
    myData = {'msg': msg, 'nick': nick, 'proto':proto}
    myMsg = json.dumps(myData) 
    myMsg = myMsg.encode()
    length= len(myMsg).to_bytes(2, 'big')
    myMsg = length+myMsg
    connection.sendall(myMsg)

def read_message(connection):
    #TODO Allow for longer messages.
    length = true_read(connection, 2)
    if not length:  # Check if length is an empty byte string
        return (None, "Connection closed", None)
    length = int.from_bytes(length, 'big')
    receivedMsg = true_read(connection, length)
    if not receivedMsg:  # Check if receivedMsg is an empty byte string
        return (None, "Connection closed", None)
    receivedMsg = receivedMsg.decode()
    receivedMsg = json.loads(receivedMsg)
    msg = receivedMsg['msg']
    nick = receivedMsg['nick']
    proto = receivedMsg['proto']
    return (nick, msg, proto)


def true_read(connection, numToRead):
    bytesRead = b''
    while len(bytesRead) < numToRead:
        msg = connection.recv(numToRead - len(bytesRead))
        bytesRead += msg 
        if len(bytesRead) == 0:
            break
    return bytesRead


