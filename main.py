# Import necessary modules
from socket import *  # import socket module
import sys  # In order to terminate the program
import errno
import os


# Method to send 404 Not Found error message to the client
# Takes in connectionSocket object
# Returns nothing
def send_404(connectionSocket):
    connectionSocket.send("HTTP/1.1 404 Not Found\r\n".encode())
    connectionSocket.send("Content-Type: text/html; charset=utf-8\r\n".encode())
    connectionSocket.send("\r\n".encode())
    connectionSocket.send(
        "<html><head></head><body><h1>404 Not Found</h1></body></html>".encode()
    )
    connectionSocket.send("\r\n".encode())


# Check for command line args and port number
if len(sys.argv) != 2:
    print("Too few arguments")
    print(f"Usage: python3 {sys.argv[0]} <PortNumber>")
    sys.exit(1)
# Try to cast command line port argument to integer
try:
    serverPort = int(sys.argv[1])
except ValueError:
    print("Port number must be an integer.")
    sys.exit(1)

try:
    # Create a TCP server socket (AF_INET for IPv4 protocols, SOCK_STREAM for TCP)
    serverSocket = socket(AF_INET, SOCK_STREAM)
    # Bind socket to server address and port, '' indicates listening on all interfaces
    serverSocket.bind(("", serverPort))
    # Listen for incoming connections
    serverSocket.listen(1)
# Handle Socket errors
except OSError as e:
    print(f"Socket error: {e.strerror}")
    sys.exit(1)
# Handle other exceptions
except Exception as e:
    print(f"An error occured: {e}")
    sys.exit(1)
try:
    while True:
        # Establish the connection
        print("Ready to serve...")
        # Accept connection from client
        connectionSocket, addr = serverSocket.accept()
        try:
            # Recieve clients request
            message = connectionSocket.recv(1024).decode()
            # find filename
            filename = message.split()[1]
            # Open file
            f = open(filename[1:])
            # Read in data
            outputdata = f.read()
            # Send one HTTP header line into socket
            connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
            connectionSocket.send("Content-Type: text/html; charset=utf-8\r\n".encode())
            connectionSocket.send(
                "\r\n".encode()
            )  # Blank line to indicate end of header
            # Send the content of the requested file to the client
            # connectionSocket.send(outputdata.encode()) <--- can do it this way too. Will use byte by byte boilerplate code instead
            for i in range(0, len(outputdata)):
                connectionSocket.send(outputdata[i].encode())
            connectionSocket.send("\r\n".encode())
            print(f"Connection from: ", addr[0])
            print(f"Client requested: {filename}")
            # Close connection to socket
            connectionSocket.close()
        # File requested by teh client was not found
        except FileNotFoundError:
            print("File does not exist")
            send_404(connectionSocket)
            connectionSocket.close()
        # IO error occurred while serving file
        except IOError:
            print("IOError occurred while serving")
            send_404(connectionSocket)
            connectionSocket.close()
except KeyboardInterrupt:
    # Ctrl+C to terminate server
    print(" Server terminated by user.")
    serverSocket.close()
    sys.exit()  # Terminate the program after sending data
