# This script is called from the server.py script and communicates with clients who wish to create
# virtual machines. This gets a command line argument which is the port number and a list of ports 
# imported from the server.py script
# This script runs on the server

# create <name> <ramsize in MB> <hard disk size in GB>G --> Create virtual machine with a given name ramsize in MB and a hard disk space in GB
# start --> This command starts the virtual machine
# connect --> This command opens an ssh terminal to the virtual machine
# shutdown --> Graceful shutdown of the VM
# suspend --> Suspends the VM
# fshut --> Powers down the VM forcefully
# close --> shuts down all VMs and exits the session
# listvms --> Lists the VMs
# destroy -> Destroys a VM

# Pending tasks:
# Write command executor scripts

import sys
import socket
import subprocess
import time

print("NEW CONNECTION CREATED")

# The port on which the current script is listening
port = int(sys.argv[1])

# The ip address of the user requesting controlling the interface 
ipaddr = sys.argv[2]


# 3 arrays which list all the vms the current user owns in the format ["vm-name", "ip add of host machine"]
# NOTE: Make these empty in the end
vmNames = []
vmIPs = [] 
hostIPs = []
vmStates = [] #0 - off, 1 - on, 2 - paused

minRAM = 1024
maxRAM = 6*1024
minDisk = 3
maxDisk = 100

# Socket to listen to the port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', port))
s.listen(1)

def findipaddr(vmRAM):
	# for i in allIPs:
	# 	print("IN")
	# 	checkport = 2000
	# 	checksock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# 	checksock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	# 	checksock.connect((i, checkport))
	# 	print("CONNECTED")
	# 	# As soon as a connection is established a true/false message is returned
	# 	isFreeMsg = checksock.recv(1024)
	# 	if (isFreeMsg == 'true'):
	# 		return i
	# 	checksock.close()
	# return False

	# Define it temporarily to be some convenient IP for testing purposes
	return "10.194.2.145"

	# print("Find IP request initiated...")
	# print("Calling the executor script...")
	# # Call the script which searches for IPs
	# x = subprocess.check_output(['bash', 'findavailableuser.sh', str(vmRAM)])
	# print(vmRAM)
	# x = x.split("\n")
	# print("Iterating over the message values...")
	# for msg in x:
	# 	parsed = msg.split(" ")
	# 	if (parsed[0] == "NCONFIG"):
	# 		print("SYS ERR: Machine with IP " + parsed[1] + " does not have disa_server installed. Please check.")
	# 	elif (parsed[0] == "BUSY"):
	# 		print("SYS ERR: Resources busy")
	# 		return None
	# 	elif (parsed[0] == "FOUND"):
	# 		print("Free host found. Exiting findIP subroutine...")
	# 		return parsed[1]


def isInteger(s):
	try:
		return int(s)
	except ValueError:
		return False

def printFile(filename, c):
	print("Opening help file list")
	fileObj = open(filename, "r")
	fileText = fileObj.read()
	c.sendall(fileText)

def runScript(scriptname, c):
	output = subprocess.check_output(['bash', scriptname])
	c.sendall(output)

# This function gives the help instructions to the user. 
def help(c):
	#Print the list of commands
	printFile("CommandDescriptors/listCommands.txt", c)
	while True:
		# Use this if command is sent from a bash ncat script
		# ins = str(c.recv(1024))[:-1]

		# Use this if command is sent from python raw_input() function
		ins = str(c.recv(1024))

		errmsg = "ERROR: Please type a valid number or command."
		#Print the documentation. 
		if (len(ins) == 1):
			cmdno = int(ins)
			if (cmdno == 1):
				runScript("CommandDescriptors/create.sh", c)
			elif (cmdno == 2):
				runScript("CommandDescriptors/start.sh", c)
			elif (cmdno == 3):
				runScript("CommandDescriptors/connect.sh", c)
			elif (cmdno == 4):
				runScript("CommandDescriptors/shutdown.sh", c)
			elif (cmdno == 5):
				runScript("CommandDescriptors/suspend.sh", c)
			elif (cmdno == 6):
				runScript("CommandDescriptors/resume.sh", c)
			elif (cmdno == 7):
				runScript("CommandDescriptors/close.sh", c)
			elif (cmdno == 8):
				runScript("CommandDescriptors/listvms.sh", c)
			elif (cmdno == 9):
				runScript("CommandDescriptors/destroy.sh", c)
			else:
				c.send(errmsg)
		elif (ins == "exit"):
			c.send("Exited help mode. \n")
			return
		else:
			c.send(errmsg)

# Checks to see if the vmName entered is alphanumeric and unique
# If yes, returns True. If not, returns False and prints error message
def checkVmName(vmName, c):
	# First check if all characters are alphanumeric
	if (vmName.isalnum() == False):
		c.send("The VM name should consist of alphanumeric characters only. No spaces or symbols allowed.\n")
		return False

	# Check if the vmName already does not occur in the vm list
	if (vmName in vmNames):
		c.send("You already own a VM called " + vmName + ". Choose a different name.\n")
		return False

	# If we pass both tests return True
	return True

#Checks the number of arguments in a given command
def checkArgNumber(cmdwords, nArgs, c):
	if (nArgs == len(cmdwords)-1):
		return True
	else:
		c.send(cmdwords[0] + " takes " + str(nArgs) + " argument(s). However, you only entered " + str(len(cmdwords)-1) + ".\n")
		return False

#Checks to see if the RAM entry is an integer and within acceptable range
# Prints error message if not
def checkRAM(vmRAM, c):
	vmRAMValue = isInteger(vmRAM)
	# Checks if the RAM value is an integer
	if (vmRAMValue == False):
		c.send("Please enter an integral value for the RAM size.\n")
		return False
	
	#Checks if the RAM value is larger than 1GB
	if (vmRAMValue < minRAM):
		c.send("You have allocated too little RAM. RAM should be atleast " + str(minRAM) + "MB.\n")
		return False

	#Checks if the RAM value is smalle than 6GB
	if (vmRAMValue > maxRAM):
		c.send("You have allocated too much RAM. RAM should be less than " + str(maxRAM) + "MB.\n")
		return False

	return True

def checkVmDisk(vmDisk, c):
	vmDiskValue = isInteger(vmDisk)
	# Checks if disk value is an integer
	if (vmDiskValue == False):
		c.send("Please enter an integral value for the disk size.\n")
		return False

	#Checks if the disk value is larger than minDisk
	if (vmDiskValue < minDisk):
		c.send("You have allocated too little disk space. Allocate atleast " + str(minDisk) + "GB.\n")
		return False

	# Checks if disk value is smaller than maxDisk
	if (vmDiskValue > maxDisk):
		c.send("You have allocated too much disk space. Allocate not more than " + str(maxDisk) + "GB.\n")
		return False

	return True

<<<<<<< HEAD

# # Checks the remote state of a virtual machine with the given name, returns the remote state
# def checkState(queryName):
# 	print("Checking state of " + queryName + "_" + ipaddr)

# 	# Get the index of the virtual machine in the database
# 	vmId = vmNames.index(queryName)

# 	print("Fetching remote data from " + hostIPs[vmId] + "...")
# 	remoteInfo = subprocess.check_output(['bash', 'CommandExecutors/getRemoveInfo.sh', hostIPs[vmId]]).split("\n")
# 	for i in range(4, len(remoteInfo), 2):



# # Updates the states of the virtual machine by calling virsh list -all
# def checkStates(vmName):
# 	print("Updating states from the host...")
# 	print("Fetching remote VM information...")
# 	for hostip in hostIPs:
# 		# The hostip is needed to connect to it
# 		# The ipaddr is needed to fetch virtual machines only belonging to one user
# 		remoteInfo = subprocess.check_output(['bash', 'CommandExecutors/getRemoveInfo.sh', hostip])
# 		remoteInfo.split("\n")
# 		for i in range(4, len(remoteInfo), 2):
# 			s  = remoteInfo[i]
# 			remoteHostIp = s[len(s) - len(ipaddr):len(s)]
# 			remoteVmName = s-remoteHostIp
# 			if (remoteHostIp == ipaddr):
# 				# Found the ip address
# 				# Check the state
# 				if (remoteInfo[i+1] == "running"):
# 					if (vmStates == )


=======
# Updates the states of the virtual machine by calling virsh list -all
# def updateStates():
	
>>>>>>> 93a66cee5700195b2dd74e04323a1e456fa2ffc0

def create(cmdwords, c):
	print("Create request initiated...")
	if (checkArgNumber(cmdwords, 3, c) == True):
		#If the correct no. of args proceed
		vmName = cmdwords[1]
		vmRAM = cmdwords[2]
		vmDisk = cmdwords[3]
		# This code block checks if the name of the VM is correct
		if (checkVmName(vmName, c) == False):
			return

		#This code block checks if the amount of RAM allocated to the VM is correct
		if (checkRAM(vmRAM, c)) == False:
			return

		#This code checks the hard disk space
		if(checkVmDisk(vmDisk, c) == False):
			return

		# Run a script to create the virtual machine
		freeHostIP = findipaddr(vmRAM) #Finds the ip address of a free host
		if (freeHostIP == None):
			c.send("No free host available. Please try again later.")
			return
		
		# The create script takes three arguments, name of the VM, the ip addres of host, and the ipaddress of user
		try:
			subprocess.check_output(['bash', 'create_remote.sh', vmName, vmRAM, str(vmDisk) + "G", freeHostIP, ipaddr])
			vmIPs.append(None) # Append a null object which can be changed later
			print("Updating the server database...")
			# The VM created will be named vmName_ipaddr
			vmNames.append(vmName)
			hostIPs.append(freeHostIP)
			vmStates.append(0)
			# Wait for confirmation 

			c.send("Virtual machine " + vmName + " created. To start it run start " + vmName + ". A default user with username ubuntu and password asdf has been created on the machine.\n")
		except subprocess.CalledProcessError as e:
			print(e.output)
	else:
		return 

def ipNotFound(ipstring):
	if (ipstring == "" or ipstring == " " or ipstring == "\n" or ipstring == "\r" or ipstring == None or len(ipstring) <= 3):
		return True
	else:
		return False
	
def start(cmdwords, c):
	#Check the cmdwords has one arguments
	print("Start request initiated...")
	if (checkArgNumber(cmdwords, 1, c) == True):
		vmName = cmdwords[1]

		# Check if the vmName exists in the vmName array
		if (vmName not in vmNames):
			c.send("The virtual machine named " + vmName + " does not exist.\n")
			print("USR ERROR: User tried to start an incorrect VM")
			return
		
		# Else find the Id of the virtual machine
		vmId = vmNames.index(vmName)

	#Check the state of the virtual machine
	if (vmStates[vmId] == 1):
		c.send(vmName + " is already running.\n")
		return
	if (vmStates[vmId] == 2):
		c.send(vmName + " is paused. Use the command resume " + vmName + " if you wish to start it again.\n")
		return

	#If above conditions are met start the virtual machine 
	#Syntax of start.sh takes in vmName hostIP IPuser
	try:
		# Call the start script and store the VMs IP address
		print("Calling the executor script...")
		subprocess.call(['bash', 'CommandExecutors/start.sh', vmName, hostIPs[vmId], ipaddr])
		print("Searching for the IP address...")
		sleeptime = 0.1

		while ((ipNotFound(vmIPs[vmId])) and sleeptime <= 4):
			# Keep trying until you get the IP address
			print("Calling the return ip subroutine...")
			vmIPs[vmId] = subprocess.check_output(['bash', 'returnip.sh', vmName, hostIPs[vmId], ipaddr])
			time.sleep(sleeptime)
			sleeptime *= 2
			print("HALTING")

		if (ipNotFound(vmIPs[vmId])):
			c.send("Virtual machine started.\nERROR: The virtual machine test has started but not been assigned an IP yet. This usually means that the host is too slow to respond.")
			print("SYS ERROR: Host too slow to start VM")
			return 
		else:
			vmStates[vmId] = 1
			print("Start request successful")
			c.send(vmName + " is running. Virtual machine has ip address " + vmIPs[vmId])
			print("Exiting start subroutine...")
			return
	except:
		print("SYS ERROR: Could not start VM")
		c.send("Error - test was not able to start.")



def connect(cmdwords, c):
	print("Connect request initiated...")
	if (checkArgNumber(cmdwords, 1, c) == True):
		vmName = cmdwords[1]

		# Check if the vmName exists in the vmName array
		if (vmName not in vmNames):
			c.send("The virtual machine named " + vmName + " does not exist.\n")
			print("ERROR: Incorrect vm name entered by the user")
			return
		
		# Else find the Id of the virtual machine
		vmId = vmNames.index(vmName)
		vmState = vmStates[vmId]

		if (vmState != 1):
			c.send(vmName + " is not running. To connect a VM must be running.\n")
			print("ERROR: User's VM was not running")
			return

		print("Attempting to connect to " + vmName + " with state " + str(vmState) + " and IP address " + vmIPs[vmId])
		print("Telling user script to run connect subroutine")
		c.send("CONNECT " + vmName + " " + hostIPs[vmId] + " " + ipaddr + " " + vmIPs[vmId])
		print("Exiting connect subroutine...")
		return 

# Switches off a VM
def shutdown(cmdwords, c, printOutput):
	print("Shutdown request initiated...")
	if (checkArgNumber(cmdwords, 1, c) == False): 
		return 

	vmName = cmdwords[1]

	# Check if the vmName exists in the vmName array
	if (vmName not in vmNames):
		c.send("The virtual machine named " + vmName + " does not exist.\n")
		print("USR ERROR: User tried to shut down a virtual machine that does not exist.")
		return
	
	# Else find the Id of the virtual machine
	vmId = vmNames.index(vmName)
	vmState = vmStates[vmId]

	if (vmState != 1):
		c.send(vmName + " is not powered on. You can only shutdown a VM that is running. If your VM is suspended resume it first.\n")
		print("USR ERROR: User tried to shutdown a powered-off VM")
		return

	print("Calling the shutdown executor script...")
	subprocess.call(['bash', 'CommandExecutors/shutdown.sh', vmName+"_"+ipaddr, hostIPs[vmId]])
	vmStates[vmId] = 0
	if (printOutput):
		c.send(vmName + " is now off\n")
	print("Shutdown successful.")

def suspend(cmdwords, c):
	print("Suspend request initiated...")
	if (checkArgNumber(cmdwords, 1, c) == False): 
		return 

	vmName = cmdwords[1]

	

	# Check if the vmName exists in the vmName array
	if (vmName not in vmNames):
		c.send("The virtual machine named " + vmName + " does not exist.\n")
		return

	

	# Else find the Id of the virtual machine
	vmId = vmNames.index(vmName)
	print("Located VM " + vmName + " in database with Id " + str(vmId))
	vmState = vmStates[vmId]

	if (vmState != 1):
		c.send(vmName + " is not powered on. You can only suspend a VM that is running.\n")

	subprocess.call(['bash', '/CommandExecutor/suspend.sh', vmName, hostIPs[vmId]], ipaddr)
	vmStates[vmId] = 2 #Set the state to paused
	return

def resume(cmdwords, c, printOutput):
	if (checkArgNumber(cmdwords, 1, c) == False): 
		return 

	vmName = cmdwords[1]

	# Check if the vmName exists in the vmName array
	if (vmName not in vmNames):
			c.send("The virtual machine named " + vmName + " does not exist.\n")
			return
	
	# Else find the Id of the virtual machine
	vmId = vmNames.index(vmName)
	vmState = vmStates[vmId]

	if (vmState != 2):
		c.send(vmName + " is not suspended. You can only resume a VM that is suspended.\n")

	subprocess.call(['bash', '/CommandExecutor/suspend.sh', vmName, hostIPs[vmId]], ipaddr)
	vmStates[vmId] = 1 #Set the state to running

# This script completely removes the VM
def destroy(cmdwords, c, printOutput):
	print("Destroy request initiated...")

	# Check the arguments 
	if (checkArgNumber(cmdwords, 1, c) == False):
		return

	vmName = cmdwords[1]

	# Check if the vmName exists in the vmName array
	if (vmName not in vmNames):
		c.send("The virtual machine named " + vmName + " does not exist.\n")
		print("USR ERR: User tried to destroy non-existent VM")
		return

	# Else find the Id of the virtual machine
	vmId = vmNames.index(vmName)
	vmState = vmStates[vmId]

	if (vmState != 0):
		c.send(vmName + " is not powered off. You can only destroy a VM that is off.\n")
		print("USR ERR: User tried to destroy a running VM")
		return

	print("Call the destroyer executor script...")
	subprocess.call(['bash', 'CommandExecutors/destroy.sh', vmName, hostIPs[vmId], ipaddr])
	# Remove it from the array
	print("Removing VM from the server database...")
	vmNames.pop(vmId)
	vmIPs.pop(vmId)
	hostIPs.pop(vmId)
	vmStates.pop(vmId)
	if (printOutput):
		c.send("VM " + vmName + " removed.")
	print("Deletion successful.")

def close(cmdwords, c):
	if (checkArgNumber(cmdwords, 0, c) == False):
		return

	shuttime = 5 #Time it takes for the VM to shutdown

	#Shutdown then destroy all VMs
	while(len(vmStates) > 0):
		if (vmStates[0] != 0):
			if (vmStates[0] == 2):
				resume(["resume", vmNames[0]], c, False)
			shutdown(["shutdown", vmNames[0]], c, False)
			time.sleep(shuttime)
		destroy(["destroy", vmNames[0]], c, False)
		# subprocess.call(['bash', 'CommandExecutors/close.sh', vmNames[0], hostIPs, ipaddr])

	# Send a closing message to the user to terminate the script
	c.send("KRIYA shutdown...")
	return

def listvms(cmdwords, c):
	outputString = ""

	if (checkArgNumber(cmdwords, 0, c) == False):
		return

	for i in range(len(vmStates)):
		outputString += str(i+1) + ". " + vmNames[i] + " "
		if (vmStates[i] == 0):
			outputString += "off"
		elif (vmStates[i] == 1):
			outputString += "running"
		elif (vmStates[i] == 2):
			outputString += "paused"

	outputString += "\n"
	c.send(outputString)

#This is the main loop that the server runs all the time
while True:
	c, addr = s.accept()
	if (addr[0] == ipaddr):
		# If it is from the IP you want send a greeting
		printFile("greet.txt", c)
		while True:
			# Use this if command is sent from a bash ncat script
			# ins = str(c.recv(1024))[:-1]
			# Use this if command is sent from python raw_input() function
			print("server cycle START. Waiting for data...")
			ins = str(c.recv(1024))
			cmdwords = ins.split()
			if (len(cmdwords) < 1):
				break
			if (cmdwords[0] == "help"):
				help(c)
			elif (cmdwords[0] == "create"):
				create(cmdwords, c)
			elif (cmdwords[0] == "start"):
				start(cmdwords, c)
			elif (cmdwords[0] == "connect"):
				connect(cmdwords, c)
			elif (cmdwords[0] == "shutdown"):
				shutdown(cmdwords, c, True)
			elif (cmdwords[0] == "suspend"):
				suspend(cmdwords, c)
			elif (cmdwords[0] == "resume"):
				resume(cmdwords, c, True)
			elif (cmdwords[0] == "close"):
				close(cmdwords, c)
				c.close()
				exit()
			elif (cmdwords[0] == "listvms"):
				listvms(cmdwords, c)
			elif(cmdwords[0] == "destroy"):
				destroy(cmdwords, c, True)
			elif (cmdwords[0] == "fstart"):
				vmStates[vmNames.index(cmdwords[1])] = 1
			elif (cmdwords[0] == "fcreate"):
				vmNames.append(cmdwords[1])
				vmIPs.append(None)
				hostIPs.append(cmdwords[2])
				vmStates.append(0)
				c.send("Server database updated.")
			else:
				c.send("ERROR: Command " + cmdwords[0] + " does not exist.\n")
		c.close()
	else:
		# Only accept connection if it is from the original IP
		c.send("Connection refused: You are connecting to a port not assigned to you\n")
		c.close()



