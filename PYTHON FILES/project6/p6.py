#!/usr/bin/env python3

# R-E P. Miller
# CS: Information Technology
# CSC 328_010
# Fall 2023
# Assignment #6 - Sockets (Server)
# p6.py
# Created 10/31/23
# Due @ 11pm 11/07/23

import socket
import sys
import signal
import random

###############################################################################
# Function name: signal_handling                                              #
# Description: This function handles the interruption signal, ensuring        #
#              the server shuts down gracefully by closing the listening      #
#              socket and exiting the program.                                #
# Parameters: num - the signal number - Input                                 #
#             frame - the current stack frame - Input                         #
# Return Value: None - this function exits the program so no return value     #
###############################################################################
def signal_handling(num, frame):

    print("\nInterruption has been signaled. Shutting down...")
    server_socket.close()  # server_socket wasn't declared globally :O
    sys.exit(0)

# https://docs.python.org/3/library/signal.html
signal.signal(signal.SIGINT, signal_handling) # Calls the signal handling stuff (SIGINT is Ctrl+C) (Much better solution than using XARGS to kill all BS processes in the Makefile) lololol

###############################################################################
# Function name: build_packet                                                 #
# Description: Creates a packet with a 2-byte header indicating the           #
#              length of the word, followed by the word itself,               #
#              following big-endian order rules.                              #
# Parameters: word - the string to pack into the packet - Input               #
# Return Value: The constructed packet with the length header and word -      #
#               Output                                                        #
###############################################################################
def build_packet(word):

    wordlen = len(word)
    length = wordlen.to_bytes(2, byteorder='big')
    return length + word.encode()

if __name__ == '__main__':

    words = ['Hello', 'World', 'My', 'Name', 'Is', 'R-E', 'Miller', 'And', 'I', 'Am', 'An',
            'Information', 'Technology', 'Major', 'At', 'Kutztown', 'University', 'Of', 'Pennsylvania',
            'Which', 'Happens', 'To', 'Be', 'A', 'Great', 'College', 'For', 'Computer', 'Science', 'Or', 'IT', 'Students']
    host = 'localhost'
    server_socket = None # I was pretty pissed for a while because I was trying to set the variable in the try loop without initializing it globally first... now it works :D

    if len(sys.argv) != 2:
        print("Usage: <port>")
        sys.exit(1)

    port = int(sys.argv[1])

    if port < 10000 or port > 65535:
        print("Error! The Port must be between 10000 and 65535.")
        sys.exit(1)

    try:

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Have to initialize it globally first
        server_socket.bind((host, port))
        server_socket.listen(1)
        print(f"Connection established on: {host}:{port}")

        while True:
            connection, address = server_socket.accept()

            with connection:
                for i in range(random.randint(1, 10)):
                    word = random.choice(words)
                    packet = build_packet(word)
                    connection.sendall(packet)
                connection.close()

    except OSError as e:

        print(f"OS Error: {e}")
        server_socket.close()
        sys.exit(1)
