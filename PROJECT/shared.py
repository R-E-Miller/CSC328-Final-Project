#!/usr/bin/env python3
import socket
import json

def send_message(connection, msg, nick, proto):
    if nick == None:
        nick = "None"
    myData = {'msg': msg, 'nick': nick, 'proto':proto}
    myMsg = json.dumps(myData) 
    myMsg = myMsg.encode()
    #myMsg = myMsg.decode()
    #myMsg = json.loads(myMsg)
    #print(myMsg['msg'])
    length= len(myMsg).to_bytes(2, 'big')
    myMsg = length+myMsg
    print(f'Sending {myMsg}')
    connection.sendall(myMsg)

def read_message(connection):
    #TODO: THIS HAS TO CHANGE TO ALLOW LARGER MESSAGES 
    length = true_read(connection, 2)
    length = int.from_bytes(length, 'big')
     
    receivedMsg = true_read(connection, length)
    receivedMsg = receivedMsg.decode()
    receivedMsg = json.loads(receivedMsg)
    print(f'received: {receivedMsg}')
    msg = receivedMsg['msg']
    nick = receivedMsg['nick']
    proto = receivedMsg['proto']

    #msg = receivedMsg['msg']
    #nick = receivedMsg['nick']
    return (nick, msg, proto)

def true_read(connection, numToRead):
    bytesRead = b''
    while len(bytesRead) < numToRead:
        msg = connection.recv(numToRead - len(bytesRead))
        bytesRead += msg 
        if len(bytesRead) == 0:
            break
    return bytesRead


