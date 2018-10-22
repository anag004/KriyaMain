# This script runs on the user and connects to the central server
# Takes input as the ipaddress of central server which will be fixed

import socket
import sys
import subprocess 
import time

# Colors
CRED = '\033[91m'
CEND = '\033[0m'

serverip = sys.argv[1]

# The port which the server is listening on
serverport = 6000

sock = None

try:
	# Socket to ping the server
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.connect((serverip, serverport))
except socket.error as err:
	if (err[0] == 61):
		print("Error - server " + str(serverip) + " is inactive.")
	else:
		print(err)

msg = sock.recv(1024)
sock.close()

# Get the value of port
connectport = msg.split(" ")[-1]

# # TESTING FILES
# connectport = 6001
# serverip = "127.0.0.1"

print("Port " + str(connectport) + " assigned by the server. Connecting...")

sleeptime = 0.125
success = False

sock = None

while((not success) and sleeptime <= 4):
	try:
		print("Trying to connect...")
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		sock.connect((serverip, int(connectport)))
		success = True
	except socket.error as err:
		print("Connection attempt failed. Trying again...")
		if (err[0] == 61):
			time.sleep(sleeptime)
			sleeptime *= 2
		else:
			print(err)
			# exit()
			# TEMPORARY LINES
			time.sleep(sleeptime)
			sleeptime *= 2

if (not success):
	print("Error - operation timed out. Server not responding.")
	exit()

print("Connection successful on port " + str(connectport))
print("---------------------------------------------------")
print(sock.recv(2**15))

# Parses the ip to remove ending escape characters
def parseIP(ip):
	resultIP = ""
	for char in ip:
		if char == '.' or char.isdigit():
			resultIP += char
		else:
			break
	return resultIP

while(True):
	command = raw_input(CRED + "KRIYA >> " + CEND)
	sock.send(command)
	recvData = sock.recv(2**15)
	if (recvData == "KRIYA shutdown..."):
		exit()
	elif (recvData.split(" ")[0] == "CONNECT"):
		splitted = recvData.split(" ")
		subprocess.call(['bash', 'CommandExecutors/connect.sh', splitted[1], splitted[2], splitted[3], parseIP(splitted[4])])
	else:
		print(recvData)


