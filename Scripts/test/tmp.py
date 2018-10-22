import sys
import socket
import subprocess

allIPs = ['192.168.43.134']

def findipaddr():
	for i in allIPs:
		print("IN")
		checkport = 2000
		checksock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		checksock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		checksock.connect((i, checkport))
		print("CONNECTED")
		# As soon as a connection is established a true/false message is returned
		isFreeMsg = checksock.recv(1024)
		if (isFreeMsg == 'true'):
			
			return i
		checksock.close()
	return False

findipaddr()