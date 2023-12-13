# Chat Server Application - CSC328 Final Project

## ID Block
- **Authors:** R-E Miller, Elliot Swan, Matthew Hill
- **Majors:** IT, CS, CS (respectively)
- **Creation Date:** November 23, 2023
- **Due Date:** December 14, 2023 @ 10AM
- **Course:** CSC328: Network & Secure Programming
- **Professor Name:** Dr. Dylan Schwesinger
- **Assignment:** Final Project
- **Filename:** Readme.md
- **Purpose:** This file acts as the Readme for our project. The purpose of this assignment was to create a chat server that accepts multiple clients and they are able to converse with one another. They must all have unique nicknames and the server must send their messages to everyone connected. The server also logs and stores all of the information that is received as well as when they logged in and their IP.

## How to Build and Run the Program
To start, get the server running. This can be achieved by doing `make server`. This will create a server on the localhost and will allow connections. The next step is to then run `make client` which will execute the client program and connect to the server. Multiple connections can be made to the server (Maximum of 10). From there the connected clients must choose a unique nickname and then they are able to chat with one another. To leave the server simply hit `Ctrl+C`. To shutdown the server also hit `Ctrl+C`, but it has a 5-second wait time as it informs the connected clients that the server is shutting down.

## Purpose of the Files
- `shared.py`: The shared library used to send and receive messages that both the client and server use.
- `server.py`: The code to create the server and handles multiple client connections as well as broadcasting messages.
- `client.py`: The code to create the client that is able to connect to the server and handles information from the server to the client.
- `Makefile`: The script to create a server and client easily and is prebound to localhost for both as well as using socket 12345.

## Responsibility Matrix

## Tasks Involved

## Protocol

## Assumptions

## Discussion on Development Process
The project went pretty well. There was a struggle after the server was first started, particularly with handling multiple clients. We initially wanted to use threads but switched to select to avoid race conditions. Once we figured out how to use select, the rest of the server implementation went well. The client-side was straightforward as we used threads to handle reading. The protocol for different cases, whether broadcasting to everyone, selecting a unique username, or leaving, made the project function well overall. Elliot's shared library was integral as it allowed us to easily read and write messages by calling his functions that created and decoded JSON packets. The main challenge was learning how to work with JSON packets, but we overcame this quickly.

## Current Status
