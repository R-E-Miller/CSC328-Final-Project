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

## How to Build and Run the Client and Server
To start, get the server running. This can be achieved by doing `make server`. This will create a server on the localhost and will allow connections. The next step is to then run `make client` which will execute the client program and connect to the server. Multiple connections can be made to the server (Maximum of 10). From there the connected clients must choose a unique nickname and then they are able to chat with one another. To leave the server simply hit `Ctrl+C`. To shutdown the server also hit `Ctrl+C`, but it has a 5-second wait time as it informs the connected clients that the server is shutting down.

## File & Folder Manifest
- `shared.py`: The shared library used to send and receive messages that both the client and server use.
- `server.py`: The code to create the server and handles multiple client connections as well as broadcasting messages.
- `client.py`: The code to create the client that is able to connect to the server and handles information from the server to the client.
- `Makefile`: The script to create a server and client easily and is prebound to localhost for both as well as using socket 12345.

## Responsibility Matrix (RTM)

| Team Member | Responsibilities |
|-------------|------------------|
| R-E Miller  | - Team leader.<br> - Handled initial client/server connection code.<br> - Wrote majority of the Client code and assisted in Server code development for bug fixes and adding additional features.<br> - Educated teammates on setting up and managing a GitHub repository.<br> - Researched user interface technologies like Textualize and Curses. |
| Elliot Swan | - Developed all Shared Libraries code.<br> - Addressed bugs in Client and Server code.<br> - Managed JSON related functionalities.<br> - Assisted in transitioning from C to Python.<br> - Researched concurrency handling methods. |
| Matthew Hill| - Authored majority of Server code.<br> - Managed GitHub repository to prevent merge conflicts.<br> - Created significant portion of logistical documentation.<br> - Developed server logging system. |


## Tasks Involved/Time Taken (Per Member)
Our project is structured around specific tasks assigned to each team member. We have divided the project into key areas—Server, Client, and Library code—with each area having its own set of tasks and sub-tasks.
### Server Tasks (Matthew Hill)
- **Creating the Server**: Setting up server infrastructure & ensuring it can handle multiple client connections.  
  _Time taken: 1 hour._
- **Name Verification**: Implementing functionality to verify and manage unique client nicknames.  
  _Time taken: 3 hours._
- **Handling Multiple Connections**: Ensuring the server can efficiently manage simultaneous client connections.  
  _Time taken: 12 hours._
- **Graceful Shutdown**: Developing a mechanism for the server to shut down gracefully, including sending notifications to all connected clients.  
  _Time taken: 1/2 hour._
  
### Client Tasks (R-E Miller)
- **Connecting to Server**: Establishing a reliable connection to the server.  
  _Time taken: 4 hours._
- **Nickname Decision**: Enabling clients to choose and confirm a unique nickname.  
  _Time taken: 2 hours._
- **Message Sending and Receiving**: Facilitating the sending and receiving of messages through the client interface.  
  _Time taken: 3 hours._
- **Disconnecting**: Implementing a smooth and user-friendly disconnection process.  
  _Time taken: 2 hours._
- **Debugging**: Fixing any bugs or issues that came up.  
  _Time taken: 3 hours._
  
### Library Code/Curses Integration (Elliot Swan)
- **Encoding/Decoding JSON Packets**: Developing methods to encode and decode messages in JSON format for efficient communication.  
  _Time taken: 3 hours._
- **Sending/Receiving JSON Packets**: Establishing protocols for message transmission and reception.  
  _Time taken: 2 hours._

## Protocol
### Network Socket Specifications
The program utilizes JSON packets for concise and structured data exchange. A packet consists of:
- A **2-byte length** in big endian, specifying the length of the following JSON packet.
- A **JSON packet** with three fields:
  - `msg`: Incoming message or command.
  - `nick`: Nickname of the sender; `None` upon connection, changes upon approval. Server reserved nickname is `SERVER`.
  - `proto`: Protocol type indicating the action or stage.
#### Reading
- The first two bytes of the packet are read and converted from big endian if necessary.
- The indicated number of bytes is then read to obtain a JSON object.
- The JSON object is decoded for use as a dictionary to access `msg`, `nick`, and `proto` fields.
#### Sending
- The JSON packet is created with `msg`, `nick`, and `proto` fields filled.
- The packet's byte length is determined, converted to big endian, and prefixed to the JSON object before sending.
### Chat Protocol Specifications (Client Side)
1. **Initiate Connection**: Open a socket using command line information and connect to the server.
2. **Receive Greeting**: Upon connection, receive a packet with `msg = 'HELLO'` and `proto = 'connect'`.
3. **Nickname Verification Loop**:
   - Prompt user for a unique nickname to join the chat.
   - Send a packet with `proto = 'verify'` and the chosen nickname in `msg`.
   - If accepted, receive `msg = 'READY'`; if not, receive `msg = 'RETRY'`.
4. **Chat Session**:
   - Interact with the chat room by sending messages (prompted from the user) with `proto = 'broadcast'`.
   - Receive messages with `proto = 'broadcast'` or `proto = 'shutdown'` for server announcements.
5. **Client Exit**: Send `msg = 'BYE'` and `proto = 'goodbye'` to signal intention to disconnect.
### Server Protocol Specifications
1. **Setup**: Bind to command line specified port and start listening.
2. **Connection Handling**:
   - On new connection, accept, send greeting, and monitor for activity.
   - Use `select` library to manage asynchronous I/O.
3. **Protocol Handling**:
   - `verify`: Check nickname uniqueness; respond with `READY` or `RETRY`.
   - `broadcast`: Relay message to all connected clients.
   - `goodbye`: Announce client disconnection and remove from active list.
   - Handle unexpected disconnections and clean up resources.
4. **Server Shutdown**:
   - Broadcast `Server Shutting down in 5 seconds` with `proto = 'shutdown'`.
### Current Status
- Both server and client operate in terminal interface.
- Supports asynchronous client connections, unique nicknames, and broadcasting chat messages.
- Graceful and non-graceful client shutdowns are managed.
- Known issues:
  - Client input can be disrupted by incoming messages, which could be improved with a TUI implementation.
  - Server shutdown allows for client preparation.

## Assumptions
- **Network Environment:** Assumes a stable network connection for uninterrupted client-server communication.
- **Unique Nicknames:** Assumes each client will choose a unique nickname for identification.
- **Graceful Shutdown:** Assumes the server can be terminated gracefully with a keyboard interrupt, signaling shutdown to all clients.
- **JSON-based Communication:** Assumes all messages are in JSON format for structured data exchange.
- **Command-Line Arguments:** Assumes user familiarity with running Python scripts and command-line arguments.
- **Single Chat Room:** Assumes a single chat room for all client communication without private messaging.
- **Port Number Range:** Assumes server port number within the range of 10000 to 65535.
- **Error Handling:** Assumes basic error handling for network errors and client disconnections are in place.
- **Message Display Integrity:** Assumes clients wait to receive a message before sending to prevent overlap.
- **Makefile Usage:** Assumes user familiarity with Makefiles and running `make clean` before compiling.
- **Open Network Port:** Assumes the specified server port is open and not blocked by network security measures.
- **GitHub Repository:** The GitHub repository (found at https://github.com/R-E-Miller/CSC328-Final-Project) is assumed to be public so that the professor can view it as we make progress.
- **Client Disconnection:** It is assumed that the client ALWAYS disconnects using "CTRL-C", and does not just "X" out of the window.

## Discussion on Development Process
The project went pretty well. There was a struggle after the server was first started, particularly with handling multiple clients. We initially wanted to use threads but switched to select to avoid race conditions. Once we figured out how to use select, the rest of the server implementation went well. The client-side was straightforward as we used threads to handle reading. The protocol for different cases, whether broadcasting to everyone, selecting a unique username, or leaving, made the project function well overall. Elliot's shared library was integral as it allowed us to easily read and write messages by calling his functions that created and decoded JSON packets. The main challenge was learning how to work with JSON packets, but we overcame this quickly.

## Current Status
The server and client both operate in a terminal interface.
### Server Features
- Allows asynchronous client connections.
- Supports unique nickname selection for clients.
- Facilitates client-to-client communication through message broadcasting.
- Manages both graceful and non-graceful client shutdowns.
### Client Features
- Connects seamlessly to the server.
- Allows clients to create and use unique nicknames.
- Enables clients to chat with others through server broadcasting.
#### Known Issues
- **Input Disruption**: While typing messages, incoming messages from other clients can disrupt the display. This results in messages appearing in the middle of the user's input, which can look messy. A Text User Interface (TUI) could resolve this issue, but it was not implemented due to time constraints.
- **Shutdown Handling**: The client is capable of handling notifications about server shutdown, ensuring a smooth user experience during server closure.
