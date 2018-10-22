#This script assigns ports to incoming requests for communication. Ports are assigned from 6001 
# through 6050 allowing a maximum of 50 connections

import socket
import subprocess

# The processes array stores the subprocess objects
processes = [None]*50

# Stores the ports which are assigned to each connection
ports = [None]*50

# Stores the ips from which we get requests
reqips = [None]*50

# Main port is the port to which all computers requesting virtual machines connect
mainport = 6000

# Frees ports which no longer need to be used
def free():
	for i in range(50):
		if processes[i] != None:
			if processes[i].poll() != None:
				processes[i] = None
				reqips[i] = None

# The getport finds a free port and assigns it a process
def getport(ipaddr):
	for i in range(50):
		if processes[i] == None:
			useport = mainport+i+1
			processes[i] = subprocess.Popen(['python', 'comm.py', str(useport), str(ipaddr)])
			reqips[i] = ipaddr
			ports[i] = useport
			return useport

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print "Socket successfully created"

# This command initiates the listening on mainport
s.bind(('', mainport))
s.listen(20)
print "Socket is listening"

while True:
	# .accept() halts the script until a connection is made
	c, addr = s.accept() 
	print "Got connection from ", 
	# The free command frees any ports that have completed their scripts
	free()
	if addr[0] in reqips:
		i = reqips.index(addr[0])		
		c.send("You have already requested a port. Multiple ports are not allowed. Connect to port " + str(ports[i]));
	else:
		# Assign the port
		c.send(str(getport(addr[0])))
	c.close()
 	

