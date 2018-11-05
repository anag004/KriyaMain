#!/bin/bash
# Keep this script in the home folder of disa_server.
# This script is run on each machine connected to the server. returns 1 if the machine can run the VM and 0 otherwise.
ramneeded=$1
var=$(who | grep "(:0)"| wc -l)
if [ $var -eq 0 ]; then
	freespace=$(free -m | awk 'FNR == 2 {print $7}')
	if [ $freespace -gt $ramneeded ]; then
	 	echo 1
	else
		echo 0
	fi	
else
	echo 0
fi