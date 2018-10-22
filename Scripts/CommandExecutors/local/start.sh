#!/bin/bash

# # The script will start the local vm
vmName="$1"
virsh start $vmName

# # This script return the ip address of the vm whose name is given as argument
# dump=$(virsh dumpxml $vmName | grep "mac addr")
# mac=$(echo $dump | cut -f 2 -d "'")
# sleep 4	
# ip=$(arp -n | grep $mac | cut -f 1 -d " ")
# echo $ip
