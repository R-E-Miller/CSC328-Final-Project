#!/usr/bin/env python3
<<<<<<< HEAD
# Authors: Elliot Swan(CS), R.E. Miller(IT), Matthew Hill(CS)
# Major: CS and IT
# Creation Date: November 23, 2023
# Due Date: November 14, 2023
# Course: CSC328
# Professor Name: Dr. Schwesinger
# Assignment: final
# Filename: shared.py
# Purpose: Create a shared library that contains useful libraries for sending and receiving 
# JSON packets described in the Network protocol. 
# CITATION: The function true_read was provided to the class under the name really_read by Dr. Schwesinger in project 5's python solution
#
=======

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

>>>>>>> 7f8ca2d47d067996989f6ea2cb0519d567bd7e8a
import socket
import json

def send_message(connection, msg, nick, proto):
    """
    Function Name:      send_message
    Description:        Given a socket connection, message, nickname and protocol, package the message, nickname and protocol within
                        a JSON packet described in the protocol and send it via the socket connection.
    Parameters:         connection - a socket connection used for sending the JSON packet. Import
                        msg - the message that is to be sent within the msg field. Import 
                        nick - the nickname that is to be sent within the nick field. Import
                        proto - the protocol that the message is to follow for processing when it arrives, packed into the proto field. Import
    Return Value:       None
    """
    try:
        if nick == None:
            nick = "None"
        myData = {'msg': msg, 'nick': nick, 'proto':proto}
        myMsg = json.dumps(myData) 
        myMsg = myMsg.encode()
        length= len(myMsg).to_bytes(2, 'big')
        myMsg = length+myMsg
        connection.sendall(myMsg)
    except OSError as e:
        print(e)

def read_message(connection):
    """
    Function Name:      read_message
    Description:        Given a socket connection, read a JSON packet described in the protocol. Handles
                        JSON packet processing, breaking it down into it's components for developer ease. 
                        This function will block if there is nothing to read. 
    Parameters:         connection - The socket connection that will be read from. Import
    Return Value:       A tuple, containing the data from the fields nick, msg and proto in that respective order.
                        In the case that it fails to read a JSON packet described in the protocol, it will return 
                        the tuple (None, "Connection closed", None)
    """
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
    """
    Function Name:      true_read
    Description:        Given a socket connection, ensure that up to numToRead bytes were actually read. 
                        If the  connection fails to read numToRead bytes it will return the number of bytes read instead.
    Parameters:         connection - The socket connection that will be read from - import
                        numToRead - The number of bytes that is specified to be read - import
    bytesRead:          The bytestring that was actually read from the socket. 
    
    CITATION:           This code was provided to the class by Dr. Schwesinger in the example client solution from project 5. 
    """
    bytesRead = b''
    while len(bytesRead) < numToRead:
        msg = connection.recv(numToRead - len(bytesRead))
        bytesRead += msg 
        if len(bytesRead) == 0:
            break
    return bytesRead

