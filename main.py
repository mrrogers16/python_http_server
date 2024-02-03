from socket import *  # import socket module
import sys  # In order to terminate the program
import errno
import os


def send_404(connectionSocket):
    connectionSocket.send("HTTP/1.1 404 Not Found\r\n".encode())
    connectionSocket.send("Content-Type: text/html; charset=utf-8\r\n".encode())
    connectionSocket.send("\r\n".encode())
    connectionSocket.send(
        "<html><head></head><body><h1>404 Not Found</h1></body></html>".encode()
    )
    connectionSocket.send("\r\n".encode())


try:
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverPort = 8080
    serverSocket.bind(
        ("", serverPort)
    )  # Bind socket to server ip:port empty '' indicates listening on all interfaces
    serverSocket.listen(1)  # Listen for incoming connections
except OSError as e:
    print(f"Socket error: {e.strerror}")
    sys.exit(1)
except Exception as e:
    print(f"An error occured: {e}")
    sys.exit(1)
try:
    while True:
        # Establish the connection
        print("Ready to serve...")
        connectionSocket, addr = serverSocket.accept()
        try:
            message = connectionSocket.recv(1024).decode()
            filename = message.split()[1]  # find filename
            f = open(filename[1:])  # Open file
            outputdata = f.read()  # Read in data
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
            connectionSocket.close()
        except FileNotFoundError:
            print("File does not exist")
            send_404(connectionSocket)
            connectionSocket.close()
        except IOError:
            print("IOError occurred while serving")
            send_404(connectionSocket)
            connectionSocket.close()
except KeyboardInterrupt:
    print("Server terminated by user.")
    serverSocket.close()
    sys.exit()  # Terminate the program after sending data
