#!/usr/bin/env python3

#################################################################################
# Author: R-E Miller, Elliot Swan, Matthew Hill                                 #
# Major: IT, CS, CS (respectively)                                              #
# Creation Date: November 23, 2023                                              #
# Due Date: December 14, 2023 @ 10AM                                            #
# Course: CSC328: Network & Secure Programming                                  #
# Professor Name: Dr. Dylan Schwesinger                                         #
# Assignment: Final Project                                                     #
# Filename: client.py                                                           #
# Purpose: This code functions as the client component in a network chat        # 
#          application. It manages the connection to the chat server, processes # 
#          incoming and outgoing messages, and handles user interactions for    # 
#          nickname selection and verification. The client ensures a clean      # 
#          shutdown process, both during normal operation and when intercepting # 
#          keyboard interrupts for termination.                                 #
#################################################################################

import socket
import select
import sys
import shared as sh
import threading

proto = ''
running = True

###############################################################################
# Function name: reader_thread                                                #
# Description: Continuously reads messages from the server and prints them.   #
#              Stops when the global running flag is set to False or upon     #
#              receiving a "Connection closed" message.                       #
# Parameters:  sock - the socket to read messages from - Input                #
# Return Value: None                                                          #
###############################################################################

def reader_thread(sock):

    global running
    while running:
        myConnection = select.select([sock], [], [], 0)
        if myConnection:
            nick, message, proto = sh.read_message(sock)
            if message == "Connection closed":
                break
            print(f"{nick} said {message}")

###############################################################################
# Function name: main                                                         #
# Description: Main function to run the client. Connects to the server,       #
#              handles the initial HELLO message, nickname setup, and         #
#              message sending. Catches keyboard interrupt to close the       #
#              connection gracefully.                                         #
# Parameters:  None                                                           #
# Return Value: None                                                          #
###############################################################################

def main():

    if len(sys.argv) != 3:
        print("Usage: python client.py <host> <port>")
        sys.exit()

    # Sets host + port to commandline values from user
    host, port = sys.argv[1], int(sys.argv[2])

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((host, port))
            print("Connected to the server.")

            # Wait for HELLO message from the server
            print("Attemping to read from server...")
            serverName, hello_message, proto = sh.read_message(sock)
            if "HELLO" in hello_message:
                print(hello_message)
            else:
                print("Did not receive HELLO...")
                return

            # Handle nickname setup loop
            while True:
                nickname = input("Enter your nickname: ").strip()
                if nickname:
                    proto = 'verify' 
                    sh.send_message(sock, nickname, None, proto)
                    serverName, response, proto = sh.read_message(sock)
                    if response == "READY":
                        print(response)
                        break
                    elif response == "RETRY":
                        print(response)
                    else:
                        print("Error: Unexpected response from server!")
                        continue
                        
            read_Thread = threading.Thread(target=reader_thread, args=[sock])
            read_Thread.start()
            
            while True:
                myMessage = input()
                if myMessage.strip():  # Check if message is not just whitespace
                    sh.send_message(sock, myMessage, nickname, "broadcast")

        except KeyboardInterrupt:
            running = False
            proto = "goodbye"
            sh.send_message(sock, "BYE", nickname, proto)
            read_Thread.join()
            sock.close()
            print("Disconnected from server.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            sock.close()

if __name__ == "__main__":
    main() # Calls the main function.
