#!/usr/bin/env python3
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


