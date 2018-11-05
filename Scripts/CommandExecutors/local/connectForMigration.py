# This script runs on the user and connects to the central server
# Takes input as the ipaddress of central server which will be fixed

import socket
import sys
import subprocess 
import time


serverip = sys.argv[1]

# The port which the server is listening on
serverport = 6000


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

connectport = msg.split(" ")[-1]

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
sock.send("migrate "+sys.argv[2]+" "+sys.argv[3]);
sock.close()


