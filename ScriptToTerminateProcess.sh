#!/bin/bash

echo COMMAND LINE $1

while [ 1 -eq 1 ] 
do
	check=$( ps | grep -v "grep" | grep "$1" | wc -l )
	echo $check
	if [ $check -eq 0 ]
	then
		pmset sleepnow
		exit 1
		# sudo shutdown -h now
	fi
	sleep 0.01
done
