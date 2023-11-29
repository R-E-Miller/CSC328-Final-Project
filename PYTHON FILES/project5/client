#!/usr/bin/env python3

# R-E P. Miller
# CS: Information Technology
# CSC 328_010
# Fall 2023
# Assignment #5 - Sockets (Client)
# p5.py
# Created 10/26/23 - yeah, I started a bit late if you can't tell
# Due @ 11pm 10/31/23

import socket
import sys
import array
import os
import signal
from selectors import DefaultSelector, EVENT_READ
from http.server import HTTPServer, SimpleHTTPRequestHandler
from struct import unpack

###############################################################################
# Function name: read_bytes                                                   #
# Description: Reads a specified number of bytes from a given socket. This    #
#              function will continue to read from the socket until the exact #
#              number of requested bytes is received or an error occurs.      #
# Parameters:  sock - the socket from which to read - Input                   #
#              n - the number of bytes to read - Input                        #
# Return Value: data - a bytearray containing the read bytes - Output         #
###############################################################################

def read_bytes(sock, n):

    data = bytearray() # Read exactly n bytes from the socket.

    while len(data) < n:
        try:
            packet = sock.recv(n - len(data)) # Receives data from the socket up to the buffer size specified - https://realpython.com/python-sockets/

        except OSError as err:
            print(f"Socket error: {err}")
            return None

        if not packet:
            return None

        data.extend(packet)

    return data

###############################################################################
# Function name: read_packet                                                  #
# Description:  Reads and decodes a single 'word' packet from a given socket. #
#               This function first reads the length of the word (2 bytes)    #
#               & then reads the word itself based on the indicated length.   #
# Parameters:   sock - the socket from which to read the packet - Input       #
# Return Value: word - a decoded string from the received packet; or None     #
#               if an error occurs or no data is received - Output            #
###############################################################################

def read_packet(sock):

    length_bytes = read_bytes(sock, 2) # Read and return a single word packet from the socket

    if length_bytes is None:
        return None  # No more data or error occurred

    length = unpack('!h', length_bytes)[0]  # Big endian, signed short (16 bits - used for interpreting two bytes of data) - https://docs.python.org/3/library/struct.html

    if length == 0:  # Zero length indicates end of data
        return ''

    word = read_bytes(sock, length)

    if word is None:
        return None  # Incomplete word data or error occurred

    return word.decode('ascii')

if __name__ == "__main__":

    if len(sys.argv) != 3:  # Step 1: Accept command line arguments
        print("Invalid number of arguments! \nUsage: ./client <host> <port>")
        sys.exit(1)

    # 0 is reserved for ./client
    host = sys.argv[1]
    port = int(sys.argv[2])

    if port < 10000 or port > 65535:
        print("Invalid Port Number! \nUsage: Port Number 10000-65535")
        sys.exit(1)

    print("\nString(s) from Word Packets:\n")

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:    # Step 2: Create a socket - https://docs.python.org/3/library/socket.html

            s.connect((host, port))     # Step 3: Connect to the server - https://docs.python.org/3/howto/sockets.html

            while True:     # Step 4: Read word packets until the server closes the connection
                word = read_packet(s)

                if word is None:
                    print("\nIncomplete packet received. \nExiting socket file descriptor!\n")
                    break

                if word == '':  # End of data
                    break

                print(word)

    except Exception as e:  # Step 5: Close the socket (automatically done by exiting the 'with' block)
        print(f"An error occurred: {e}")
        sys.exit(1)
