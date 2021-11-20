import tqdm
import os 
import socket

# The port on which to listen
host = '0.0.0.0' #this is the local host addres
listenPort = 1234

# Receive 4066 bytes each time
buffer_size = 4096
SEPARATOR = " "

# Create a welcome socket. 
welcomeSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
welcomeSock.bind((host, listenPort))

# Start listening on the socket
welcomeSock.listen(5)

# ************************************************
# Receives the specified number of bytes
# from the specified socket
# @param sock - the socket from which to receive
# @param numBytes - the number of bytes to receive
# @return - the bytes received
# *************************************************
def recvAll(sock, numBytes):

	# The buffer
	recvBuff = ""
	
	# The temporary buffer
	tmpBuff = ""
	
	# Keep receiving till all is received
	while len(recvBuff) < numBytes:
		
		# Attempt to receive bytes
		tmpBuff =  sock.recv(numBytes)
		
		# The other side has closed the socket
		if not tmpBuff:
			break
		
		# Add the received bytes to the buffer
		recvBuff += tmpBuff
	
	return recvBuff



print("Wating for a connection...")

try:
	clientSock, addr = welcomeSock.accept()
	print("[+] Accepted connection from client: " + str(addr))
	print("\n")
except socket.error:
	print ("[-] Error accepting connection ")

received = clientSock.recv(buffer_size).decode()
print("Received the following: ", received)
filename, filesize = received.split(SEPARATOR)

# remove absolute path if there is
filename = os.path.basename(filename)

# convert to integer
filesize = int(filesize)

# start receiving the file from the socket
# and writing to the file stream
progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "wb") as f:
    while True:
        # read 1024 bytes from the socket (receive)
        bytes_read = clientSock.recv(buffer_size)
        if not bytes_read:    
            # nothing is received
            # file transmitting is done
            break
        # write to the file the bytes we just received
        f.write(bytes_read)
        # update the progress bar
        progress.update(len(bytes_read))

clientSock.close()
welcomeSock.close()


