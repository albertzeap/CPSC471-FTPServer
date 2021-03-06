import tqdm
import os 
import socket
import subprocess

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
# print("Received the following: ", received)

# Count the number of words
numWords = len(received.split())

if numWords == 3:
	command, filename, filesize = received.split(SEPARATOR)

	if command == "put":
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

			print("Received ::", filename)
			print ("Bytes Received::", bytes_read)


		# clientSock.close()
		# welcomeSock.close()

	if command == "get":
		try:
			filesize = os.path.getsize(filename)
			# print("This is the filesize:", filesize)
		except OSError as err: 
			print("[-] File Error :: %s" %(err))
			exit()

			# Begin sending the file through the socket 
		with open(filename, "rb") as f:
			print("Sending File::", filename)
			while True: 
				# Read the bytes from the file 
				bytes_read = f.read(buffer_size)

				if not bytes_read:
					# File has finished transmitting
					break
				bytes_sent = clientSock.send(bytes_read)

		print("Sent:", bytes_sent, "bytes")


elif numWords == 1:

	command = received

	if command == "ls":

		try:
			for line in subprocess.getstatusoutput(command):
				print(line)
		except subprocess.SubprocessError as err:
			print("[-] Command Error :: %s" %(err))

else:
	print ("Command could not be understood")


clientSock.close()
welcomeSock.close()


