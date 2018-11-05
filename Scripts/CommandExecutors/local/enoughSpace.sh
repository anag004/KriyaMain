#!/bin/bash
echo hello >~disa_server/output.log
echo $! > ~disa_server/s.txt
vmName=$1
vmRAM=$2

serverIP="192.168.43.27"
sudo echo $1 $2 > hellozero.txt
while :
do
	var=$(who | grep "(:0)"| wc -l)
	if [ $var -gt 0 ]; then
		python /home/disa_server/DISA/Scripts/CommandExecutors/local/connectForMigration.py "$serverIP" "$vmName" "$vmRAM";
		echo "Migration Started for $vmName";
		break;
	fi
done



