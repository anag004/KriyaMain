 #!/bin/bash

# This script return the ip address of the vm whose name is given as argument
# First argument is the vmName second is the ip address

vmName="$1"
dump=$( virsh dumpxml $vmName | grep "mac addr" )
mac=$(echo $dump | cut -f 2 -d "'")
ip=$(arp -n | grep $mac | cut -f 1 -d " ")
# echo abcd
echo $ip