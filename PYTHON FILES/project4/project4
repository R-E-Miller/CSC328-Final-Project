#!/usr/bin/env python3
# ^ If I do not place it right at the top I get the error - import: unable to open X server `' @ error/import.c/ImportImageCommand/344.

# R-E P. Miller
# CS: Information Technology
# CSC 328_010
# Fall 2023
# Assignment #4
# p4.py
# Created 9/28/23
# Due @ 11pm 10/5/23

import os
import random
import sys

###############################################################################
# Function name: create_pipes                                                 #
# Description: Initializes two pipes for inter-process communication.         #
#              Creates two pipes:                                             #
#                                Parent writes to child, child reads          #
#                                from parent.                                 #
#                                Child writes to parent, parent reads         #
#                                from child.                                  #
# Parameters: None                                                            #
# Return Value: c_read, p_write, p_read, c_write - pipe descriptors (output)  #
###############################################################################

def create_pipes():

    try:

        c_read, p_write = os.pipe()  # Child reads, parent writes
        p_read, c_write = os.pipe()  # Parent reads, child writes
        return c_read, p_write, p_read, c_write

    except OSError as e:

        print("Error creating pipe:", e.strerror)
        sys.exit(-1)

##########################################################################
# Function name: fork_child                                              #
# Description: Attempts to create a child process using the fork system  #
#              call.                                                     #
# Parameters: None                                                       #
# Return Value: child_pid - process ID of the child process (output)     #
##########################################################################

def fork_child():

    try:

        child_pid = os.fork()
        return child_pid

    except OSError as e:

        print("Error forking:", e.strerror)
        sys.exit(-1)

##########################################################################
# Function name: parent_process                                          #
# Description: Contains the logic for the parent process. Sends numbers  #
#              and receives responses from the child process.            #
# Parameters: int p_read - pipe read descriptor - input                  #
#             int p_write - pipe write descriptor - input                #
#             int child_pid - process ID of the child process - input    #
# Return Value: None                                                     #
##########################################################################

def parent_process(p_read, p_write, child_pid):

    os.close(c_read)
    os.close(c_write)
    pin = os.fdopen(p_read, 'r')
    pout = os.fdopen(p_write, 'w')

    # Set random seed using parent PID (I think this is what you are looking for?)
    random.seed(os.getpid())
    random_num = random.randint(1, 99) # Between 1 and 100, but not including 0 or 100.

    # Send random number to child
    print("Parent sending to pipe:", random_num)
    pout.write(str(random_num) + "\n")
    pout.flush()

    # Send product to child
    product = random_num * child_pid
    print("Parent sending to pipe:", product)
    pout.write(str(product) + "\n")
    pout.flush()

    # Read response
    response = pin.readline()
    print("Parent received from pipe:", response, end='')

    # Check child's response
    if response == "Approved\n":

        print("Parent: Thanks for playing!")

    elif response == "Denied\n":

        print("Parent: Wrong. Please try again!")

    print("Parent sending to pipe: BYE")
    pout.write("BYE\n")
    pout.flush()

    # Wait for child
    os.wait()

##########################################################################
# Function name: child_process                                           #
# Description: Contains the logic for the child process. Receives        #
#              numbers and sends responses to the parent process.        #
# Parameters: int c_read - pipe read descriptor - input                  #
#             int c_write - pipe write descriptor - input                #
# Return Value: None                                                     #
##########################################################################

def child_process(c_read, c_write):

    os.close(p_write)
    os.close(p_read)
    pin = os.fdopen(c_read, 'r')
    pout = os.fdopen(c_write, 'w')

    # Read random number from the parent
    received_num = pin.readline().encode().decode()
    print("Child received from pipe:", received_num, end='')

    # Read product from the parent
    received_product = pin.readline().encode().decode()
    print("Child received from pipe:", received_product, end='')

    # Check if product is correct. If it is, send response to the parent. Else deny.
    expected_product = str(os.getpid() * int(received_num))
    if received_product == expected_product + "\n":

        print("Child sending to pipe: Approved")
        pout.write("Approved\n")

    else:

        print("Child sending to pipe: Denied")
        pout.write("Denied\n")

    pout.flush()

    # Wait for the parent to say "BYE" then exit
    the_end = pin.readline().encode().decode()
    print("Child received from pipe:", the_end, end='')
    os._exit(0)

if __name__ == "__main__":

    c_read, p_write, p_read, c_write = create_pipes()

    # Fork & Create Child
    child_pid = fork_child()
    if child_pid > 0:

        parent_process(p_read, p_write, child_pid)

    else:

        child_process(c_read, c_write)
