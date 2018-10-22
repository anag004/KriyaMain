# This script runs on the user and creates a listening socket on port 2000
# It checks if a physical user is logged onto the system and if yes returns fales
# Otherwise it returns true

import sys
import socket
import subprocess

port = 2000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', port))
s.listen(1)

print("Socket created successfully")

while True:
	c, addr = s.accept()
	print("Received connection from " + addr[0])
	getcheck = subprocess.check_output(['bash', 'free.sh'])
	c.send(getcheck)



