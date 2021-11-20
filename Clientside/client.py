# ********************************
# Client.py is a basic program that connects to a server
# and executes commands that are inputted by the user 
# Author: Albert Paez
# ********************************

import socket, os, sys, tqdm

# Subprocess module is now ued instead of commands module 
import subprocess

# Separator to be used for filename and filesize
SEPARATOR = " "

# Send 4096 bytes each time
BUFFER_SIZE = 4096

def client_interface(sAddress, sPort):

    # Address of the server
    serverAddress = sAddress

    # Port on which the server listens on
    serverPort = int(sPort)

    # File that is being transmitted
    # filename = sys.argv[4]

    # Open the file being transmitted
    # fileObj = open(filename, "r")

    # Try creating a TCP Socket
    try:
        connSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[+] Socket successfully created!\n")
        print("Connecting to", serverAddress, "...")
    except socket.error:
        print("[-] Failed to create a socket with error %s" %(socket.error))
        exit()

    # Try connecting to the server
    try: 
        connSock.connect((serverAddress, serverPort))
        print("[+] Successfully connected to",serverAddress, serverPort)
    except socket.error as err: 
        print("[-] Error connecting ::  %s" %(err))
        exit()

    while True:

        # Receive the user command
        command = input ("ftp> ")

        # Count the number of words in the command 
        numWords = len(command.split())

        # Run the get command
        if  command.startswith("get") and numWords == 2: 

            # Split the two words 
            inputtedCommand, filename = command.split()

        # Run the put command
        elif command.startswith("put") and numWords == 2:

            # Split the two words 
            inputtedCommand, filename = command.split()

            # Check if file exists and check filesize
            try:
                filesize = os.path.getsize(filename)
                print("This is the filesize:", filesize)
            except OSError as err: 
                print("[-] File Error :: %s" %(err))
                exit()

            # List the file that is to be sent
            connSock.send(f"{inputtedCommand}{SEPARATOR}{filename}{SEPARATOR}{filesize}".encode())

            # Begin sending the file through the socket 
            progressBar = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
            with open(filename, "rb") as f:
                
                while True: 
                    # Read the bytes from the file 
                    bytes_read = f.read(BUFFER_SIZE)

                    if not bytes_read:
                        # File has finished transmitting
                        break
                    bytes_sent = connSock.send(bytes_read)

                    # Update the progress bar
                    # progressBar.update(len(bytes_read))
            print("Sent:", bytes_sent, "bytes")

            # connSock.close()
            # fileObj.close()

        # Run the ls command and get the next input
        elif command == "ls":
            # for line in subprocess.getstatusoutput(command):
            #     print(line)
            connSock.send(command.encode())

        elif command == "quit":
            connSock.close()
            break

        # Checks for invalid input
        else: 
            print("Invalid command :: use 'get <filename>' 'put <filename>' 'ls' 'quit'")

    # connSock.close()
    # fileObj.close()

    # # Number of bytes being sent
    # bytesSent = 0

    # # The file data
    # fileData = None

    # while True:

    #     # Read 65536 bytes of data
    #     filename = fileObj.read(65536)


    #     if fileData: 

    #         # Get the size of the data
    #         dataSizeStr = str(len(fileData))

    #         while len(dataSizeStr) < 10:
    #             dataSizeStr = "0" + dataSizeStr

    #         fileData = dataSizeStr + fileData

    #         bytesSent = 0

    #         while len(fileData) > bytesSent:
    #             bytesSent += connSock.send(fileData[bytesSent:])
    #     else:
    #         break

    # print ("Sent,", bytesSent,"bytes")

    # connSock.close()
    # fileObj.close()

# Checks for proper amount of arguments
if len(sys.argv) != 4:
    print ("USAGE: python " + sys.argv[0] + " cli <server machine> <server port>" )
    exit()

# Checks for client mode
if (sys.argv[1] == "cli"):
    client_interface(sys.argv[2], sys.argv[3])

# Reiterate instructions if neither mode is selected 
else:
    print ("USAGE: python " + sys.argv[0] + " cli <server machine> <server port>" )




    

