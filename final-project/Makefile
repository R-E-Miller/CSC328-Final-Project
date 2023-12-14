#################################################################################
# Author: R-E Miller, Elliot Swan, Matthew Hill                                 #
# Major: IT, CS, CS (respectively)                                              #
# Creation Date: November 23, 2023                                              #
# Due Date: December 14, 2023 @ 10AM                                            #
# Course: CSC328: Network & Secure Programming                                  #
# Professor Name: Dr. Dylan Schwesinger                                         #
# Assignment: Final Project                                                     #
# Filename: Makefile                                                            #
# Purpose: Build the application.                                               # 
#################################################################################

all: server client

server:
	cp server.py server
	chmod u+x server

client:
	cp client.py client
	chmod u+x client
	
.PHONY: clean
	
clean:
	rm -rf client
	rm -rf server
