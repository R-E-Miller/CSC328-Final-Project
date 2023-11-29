#!/usr/bin/env python3
import socket
import json

def send_message(connection, msg, nick):
    myData = {'msg': msg, 'nick': nick}
    myMsg = json.dumps(myData) 
    myMsg = myMsg.encode()
    connection.sendall(myData)

def read_message(connection):
    #TODO: THIS HAS TO CHANGE TO ALLOW LARGER MESSAGES
    receivedMsg = connection.recv(1024)
    receivedMsg = receivedMsg.decode()
    msg = receivedMsg['msg']
    nick = receivedMsg['nick']
    return (nick, msg)

